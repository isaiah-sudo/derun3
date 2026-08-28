import sys
import math
import time

# Lock Panda3D Engine Clock to 60 FPS with VSync
from panda3d.core import loadPrcFileData, ClockObject
loadPrcFileData('', 'clock-mode limited')
loadPrcFileData('', 'clock-frame-rate 60.0')
loadPrcFileData('', 'sync-video #t')

from ursina import (
    Ursina, window, camera, color, Vec3, Vec4, destroy,
    invoke, application, held_keys
)
from ursina import time as ursina_time

from game.config import (
    WINDOW_TITLE, TARGET_FPS, INITIAL_SPEED, MAX_SPEED,
    SPEED_ACCELERATION, BOOST_SPEED_MULTIPLIER,
    POINTS_PER_METER, COIN_POINTS, COMBO_TIMEOUT,
    BOOST_DURATION, MAGNET_DURATION, SHIELD_DURATION,
    BIOMES, SHIP_SKINS
)
from game.audio_synth import SoundManager
from game.highscores import HighScoreManager
from game.fx import CameraShake, FloatingPopup, ParticleBurst
from game.player import Player
from game.track import TrackManager, destroy_entity_tree
from game.ui import UIManager

# Game States
STATE_MENU = 0
STATE_PLAYING = 1
STATE_PAUSED = 2
STATE_GAMEOVER = 3

class CyberSurgeGame:
    def __init__(self):
        self.app = Ursina(
            title=WINDOW_TITLE,
            vsync=True,
            borderless=False,
            fullscreen=False,
            development_mode=False
        )
        
        # Enforce 60 FPS cap on the engine clock
        global_clock = ClockObject.getGlobalClock()
        global_clock.setMode(ClockObject.MLimited)
        global_clock.setFrameRate(60.0)

        # Enforce Dark Theme 3D Viewport Clear Background
        self.active_biome_index = 0
        self.apply_dark_theme(BIOMES[0])

        window.fps_counter.enabled = True
        window.vsync = True

        # Camera setup
        camera.fov = 68
        camera.rotation_x = 15
        self.cam_shaker = CameraShake(camera)

        # Core Subsystems
        self.sounds = SoundManager()
        self.hs_mgr = HighScoreManager()
        self.ui_mgr = UIManager(self.hs_mgr)
        self.track_mgr = TrackManager()

        self.player = None
        self.state = STATE_MENU
        self.current_skin_index = 0

        # Gameplay metrics
        self.speed = INITIAL_SPEED
        self.base_speed = INITIAL_SPEED
        self.distance = 0.0
        self.score = 0.0
        self.coins_collected = 0
        self.combo_multiplier = 1
        self.combo_timer = 0.0
        self.invulnerable_timer = 0.0
        self.target_fov = 68

        self.setup_menu()

    def apply_dark_theme(self, biome):
        window.color = biome['bg_color']
        try:
            from direct.showbase.ShowBaseGlobal import base
            clr = biome['bg_clear']
            base.setBackgroundColor(clr.x, clr.y, clr.z, 1.0)
            dr = base.camNode.getDisplayRegion(0)
            dr.setClearColorActive(True)
            dr.setClearColor(Vec4(clr.x, clr.y, clr.z, 1.0))
        except Exception:
            pass

    def setup_menu(self):
        self.state = STATE_MENU
        self.track_mgr.init_track()
        if self.player:
            destroy_entity_tree(self.player)
        self.player = Player(skin_index=self.current_skin_index)
        self.player.z = 0.0
        self.player.x = 0.0

        camera.position = Vec3(0, 3.2, -7.5)
        self.cam_shaker.base_pos = Vec3(0, 3.2, -7.5)
        self.cam_shaker.update(0)

        self.ui_mgr.show_menu(
            on_start=self.start_game,
            on_skin_change=self.on_change_skin
        )

    def on_change_skin(self, skin_idx):
        self.current_skin_index = skin_idx
        if self.player:
            self.player.change_skin(skin_idx)

    def start_game(self):
        self.ui_mgr.hide_all()  # Hide title screen & menus immediately
        self.state = STATE_PLAYING
        self.speed = INITIAL_SPEED
        self.base_speed = INITIAL_SPEED
        self.distance = 0.0
        self.score = 0.0
        self.coins_collected = 0
        self.combo_multiplier = 1
        self.combo_timer = 0.0
        self.invulnerable_timer = 1.8  # Starting grace period

        self.active_biome_index = 0
        self.apply_dark_theme(BIOMES[0])

        self.track_mgr.init_track()
        if self.player:
            destroy_entity_tree(self.player)
        self.player = Player(skin_index=self.current_skin_index)
        self.player.z = 0.0
        self.player.x = 0.0

        camera.position = Vec3(0, 3.2, -7.5)
        self.cam_shaker.base_pos = Vec3(0, 3.2, -7.5)
        self.cam_shaker.update(0)

        self.ui_mgr.init_hud()
        self.ui_mgr.show_hud(True)
        self.sounds.start_music()

    def toggle_pause(self):
        if self.state == STATE_PLAYING:
            self.state = STATE_PAUSED
            self.sounds.stop_music()
            self.ui_mgr.show_pause(
                on_resume=self.resume_game,
                on_restart=self.start_game,
                on_menu=self.setup_menu
            )
        elif self.state == STATE_PAUSED:
            self.resume_game()

    def resume_game(self):
        self.state = STATE_PLAYING
        self.sounds.start_music()
        self.ui_mgr.hide_pause()
        self.ui_mgr.show_hud(True)

    def handle_input(self, key):
        if self.state == STATE_MENU:
            if key in ('space', 'enter'):
                self.start_game()
            elif key in ('left arrow', 'a'):
                self.current_skin_index = (self.current_skin_index - 1) % len(SHIP_SKINS)
                self.ui_mgr.skin_index = self.current_skin_index
                self.ui_mgr.skin_label.text = f"[ SHIP: {SHIP_SKINS[self.current_skin_index]['name']} ]"
                self.on_change_skin(self.current_skin_index)
            elif key in ('right arrow', 'd'):
                self.current_skin_index = (self.current_skin_index + 1) % len(SHIP_SKINS)
                self.ui_mgr.skin_index = self.current_skin_index
                self.ui_mgr.skin_label.text = f"[ SHIP: {SHIP_SKINS[self.current_skin_index]['name']} ]"
                self.on_change_skin(self.current_skin_index)

        elif self.state == STATE_PLAYING:
            if key in ('a', 'left arrow'):
                self.player.move_left()
            elif key in ('d', 'right arrow'):
                self.player.move_right()
            elif key in ('w', 'up arrow', 'space'):
                self.player.jump()
            elif key in ('s', 'down arrow'):
                self.player.slide()
            elif key in ('e', 'left shift'):
                if not self.player.is_boosting:
                    self.player.activate_boost(BOOST_DURATION)
                    self.cam_shaker.add_shake(0.4)
            elif key == 'escape':
                self.toggle_pause()

        elif self.state == STATE_PAUSED:
            if key == 'escape':
                self.resume_game()

        elif self.state == STATE_GAMEOVER:
            if key in ('space', 'r', 'enter'):
                self.start_game()
            elif key in ('m', 'escape'):
                self.setup_menu()

    def game_over(self):
        self.state = STATE_GAMEOVER
        self.sounds.stop_music()
        self.cam_shaker.add_shake(1.0)
        ParticleBurst(position=self.player.position, burst_color=color.red, count=16)

        is_new_high = self.hs_mgr.record_run(self.score, self.distance, self.coins_collected)
        self.ui_mgr.show_game_over(
            score=self.score,
            distance=self.distance,
            coins=self.coins_collected,
            is_new_high=is_new_high,
            on_restart=self.start_game,
            on_menu=self.setup_menu
        )

    def check_collisions(self):
        p = self.player
        p_pos = p.position

        for h in self.track_mgr.get_nearby_hazards(p_pos.z, radius=6.0):
            if not h.enabled or not h.visible:
                continue

            dz = h.z - p_pos.z
            if abs(dz) < 0.75:
                dx = abs(h.x - p_pos.x)
                if dx < h.hit_radius_x:
                    if h.hazard_type == 'low_jump':
                        if p.y < h.clear_height:
                            self.trigger_hit(h)
                    elif h.hazard_type == 'high_slide':
                        if not p.is_sliding:
                            self.trigger_hit(h)
                    elif h.hazard_type == 'drone':
                        if p.y < h.clear_height:
                            self.trigger_hit(h)
                    elif h.hazard_type == 'pylon':
                        self.trigger_hit(h)

        for item in self.track_mgr.get_nearby_items(p_pos.z, radius=14.0):
            if not item.enabled or not item.visible:
                continue

            dist_vec = item.position - p_pos
            dist_sq = dist_vec.length()

            if p.has_magnet and dist_sq < 14.0:
                item.position -= dist_vec.normalized() * 24.0 * ursina_time.dt

            if dist_sq < 1.8:
                item.enabled = False
                item.visible = False
                self.handle_item_pickup(item)

    def trigger_hit(self, hazard):
        if self.invulnerable_timer > 0:
            return

        if self.player.is_boosting:
            self.cam_shaker.add_shake(0.35)
            ParticleBurst(position=hazard.position, burst_color=color.orange, count=12)
            FloatingPopup('+200 SMASH!', position=hazard.position + Vec3(0, 1, 0), text_color=color.orange)
            self.score += 200 * self.combo_multiplier
            hazard.enabled = False
            hazard.visible = False
            return

        if self.player.has_shield:
            self.player.has_shield = False
            self.player.shield_bubble.enabled = False
            self.invulnerable_timer = 1.8
            self.cam_shaker.add_shake(0.5)
            ParticleBurst(position=self.player.position, burst_color=color.azure, count=14)
            FloatingPopup('SHIELD DEFLECT!', position=self.player.position + Vec3(0, 1.2, 0), text_color=color.azure)
            hazard.enabled = False
            hazard.visible = False
            
            for nearby_h in self.track_mgr.get_nearby_hazards(self.player.z, radius=8.0):
                nearby_h.enabled = False
                nearby_h.visible = False
            return

        self.game_over()

    def handle_item_pickup(self, item):
        ParticleBurst(position=item.position, burst_color=item.color, count=6)

        if item.item_type == 'shard':
            self.coins_collected += 1
            self.score += COIN_POINTS * self.combo_multiplier
            self.combo_timer = COMBO_TIMEOUT
            self.combo_multiplier = min(8, self.combo_multiplier + 1)
            FloatingPopup(f'+{COIN_POINTS * self.combo_multiplier}', position=item.position, text_color=color.cyan)

        elif item.item_type == 'shield':
            self.player.activate_shield(SHIELD_DURATION)
            FloatingPopup('SHIELD MATRIX ACTIVE!', position=item.position, text_color=color.azure, scale=2.0)

        elif item.item_type == 'magnet':
            self.player.activate_magnet(MAGNET_DURATION)
            FloatingPopup('MAGNET FLUX ON!', position=item.position, text_color=color.yellow, scale=2.0)

        elif item.item_type == 'boost':
            self.player.activate_boost(BOOST_DURATION)
            self.cam_shaker.add_shake(0.4)
            FloatingPopup('HYPERDRIVE ENGAGED!', position=item.position, text_color=color.orange, scale=2.2)

    def update(self):
        dt = ursina_time.dt

        if self.state == STATE_PLAYING:
            if self.invulnerable_timer > 0:
                self.invulnerable_timer -= dt
                if self.player and hasattr(self.player, 'body'):
                    self.player.body.visible = (int(time.time() * 20.0) % 2 == 0)
            else:
                if self.player and hasattr(self.player, 'body'):
                    self.player.body.visible = True

            if self.combo_timer > 0:
                self.combo_timer -= dt
                if self.combo_timer <= 0:
                    self.combo_multiplier = 1

            self.base_speed = min(MAX_SPEED, INITIAL_SPEED + (self.distance / 100.0) * SPEED_ACCELERATION)
            if self.player.is_boosting:
                self.speed = self.base_speed * BOOST_SPEED_MULTIPLIER
                self.target_fov = 82
            else:
                self.speed = self.base_speed
                self.target_fov = 68

            camera.fov += (self.target_fov - camera.fov) * 5.0 * dt

            # Distance & Score progress
            dist_delta = self.speed * dt
            self.player.z += dist_delta
            self.distance = self.player.z
            self.score += dist_delta * POINTS_PER_METER * self.combo_multiplier

            # Update entities
            self.player.update_player(dt)
            self.track_mgr.update_track(self.player.z)
            self.check_collisions()

            # Dynamic Camera follow tracking behind player
            cam_target_y = self.player.y + 2.8 if not self.player.is_sliding else 2.2
            self.cam_shaker.base_pos = Vec3(
                self.player.x * 0.45,
                cam_target_y,
                self.player.z - 7.5
            )
            self.cam_shaker.update(dt)

            # Apply dark theme only when biome index changes
            if self.track_mgr.current_biome_index != self.active_biome_index:
                self.active_biome_index = self.track_mgr.current_biome_index
                curr_biome = self.track_mgr.get_current_biome()
                self.apply_dark_theme(curr_biome)

            powerup_msg = ''
            if self.player.is_boosting:
                powerup_msg += f'⚡ HYPERDRIVE [{self.player.boost_timer:.1f}s]  '
            if self.player.has_shield:
                powerup_msg += f'🛡️ SHIELD [{self.player.shield_timer:.1f}s]  '
            if self.player.has_magnet:
                powerup_msg += f'🧲 MAGNET [{self.player.magnet_timer:.1f}s]'

            self.ui_mgr.update_hud(
                score=self.score,
                high_score=max(self.score, self.hs_mgr.high_score),
                multiplier=self.combo_multiplier,
                speed=self.speed,
                powerup_msg=powerup_msg
            )

        elif self.state == STATE_MENU:
            if self.player:
                self.player.y = 0.5 + 0.12 * math.sin(time.time() * 3.5)
                self.player.rotation_y += 20.0 * dt
            self.cam_shaker.update(dt)

def run():
    game = CyberSurgeGame()

    def update():
        game.update()

    def input(key):
        game.handle_input(key)

    import __main__
    __main__.update = update
    __main__.input = input

    game.app.run()

if __name__ == '__main__':
    run()
