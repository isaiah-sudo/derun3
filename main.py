import sys
import math
import time
import random

# Lock Panda3D Engine Clock to 60 FPS with VSync & Hardware Optimization Flags
from panda3d.core import loadPrcFileData, ClockObject
loadPrcFileData('', 'clock-mode limited')
loadPrcFileData('', 'clock-frame-rate 60.0')
loadPrcFileData('', 'sync-video #t')
loadPrcFileData('', 'gl-finish #f')
loadPrcFileData('', 'auto-flip #t')
loadPrcFileData('', 'yield-timeslice #f')
loadPrcFileData('', 'framebuffer-multisample 0')
loadPrcFileData('', 'support-threads #t')
loadPrcFileData('', 'garbage-collect-states #t')

from ursina import (
    Ursina, window, camera, color, Vec3, Vec4, destroy,
    invoke, application, held_keys
)
from ursina import time as ursina_time

from game.config import (
    WINDOW_TITLE, TARGET_FPS, MAX_DELTA_TIME,
    POINTS_PER_METER, COIN_POINTS, COMBO_TIMEOUT,
    BIOMES, SHIP_SKINS, GAME_MODES, MODE_CLASSIC, MODE_OVERDRIVE,
    LASER_COOLDOWN, LASER_SPEED, RAMP_LAUNCH_FORCE, SPEED_PAD_BOOST_TIME, ACHIEVEMENTS
)
from game.audio_synth import SoundManager
from game.highscores import HighScoreManager
from game.fx import CameraShake, FloatingPopup, ParticleBurst
from game.player import Player
from game.obstacles import LaserProjectile
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
        self.projectiles = []
        self.state = STATE_MENU
        self.current_skin_index = 0
        self.current_mode_index = 0

        # Gameplay metrics
        self.speed = GAME_MODES[0]['initial_speed']
        self.base_speed = GAME_MODES[0]['initial_speed']
        self.distance = 0.0
        self.score = 0.0
        self.coins_collected = 0
        self.run_destructions = 0
        self.ramps_hit = 0
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
        self.clear_projectiles()
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
            on_skin_change=self.on_change_skin,
            on_mode_change=self.on_change_mode
        )

    def on_change_skin(self, skin_idx):
        self.current_skin_index = skin_idx
        if self.player:
            self.player.change_skin(skin_idx)

    def on_change_mode(self, mode_idx):
        self.current_mode_index = mode_idx

    def start_game(self):
        self.ui_mgr.hide_all()
        self.state = STATE_PLAYING

        mode_cfg = GAME_MODES[self.current_mode_index]
        self.speed = mode_cfg['initial_speed']
        self.base_speed = mode_cfg['initial_speed']
        self.distance = 0.0
        self.score = 0.0
        self.coins_collected = 0
        self.run_destructions = 0
        self.ramps_hit = 0
        self.combo_multiplier = 1
        self.combo_timer = 0.0
        self.invulnerable_timer = 1.8

        self.active_biome_index = 0
        self.apply_dark_theme(BIOMES[0])

        self.clear_projectiles()
        self.track_mgr.init_track()
        if self.player:
            destroy_entity_tree(self.player)
        self.player = Player(skin_index=self.current_skin_index)
        self.player.z = 0.0
        self.player.x = 0.0

        camera.position = Vec3(0, 3.2, -7.5)
        self.cam_shaker.base_pos = Vec3(0, 3.2, -7.5)
        self.cam_shaker.update(0)

        self.ui_mgr.init_hud(mode_index=self.current_mode_index)
        self.ui_mgr.show_hud(True)
        self.sounds.start_music()

    def clear_projectiles(self):
        for p in self.projectiles:
            destroy_entity_tree(p)
        self.projectiles.clear()

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

    def fire_laser(self):
        if self.state != STATE_PLAYING or not self.player or self.player.laser_cooldown > 0:
            return
        if self.player.ammo <= 0:
            FloatingPopup('OUT OF AMMO! [FIND PLASMA CELLS]', position=self.player.position + Vec3(0, 1.2, 0), text_color=color.hex('#ff4466'), scale=1.4)
            return

        self.player.consume_ammo()
        self.player.laser_cooldown = LASER_COOLDOWN
        proj_pos = Vec3(self.player.x, self.player.y + 0.1, self.player.z + 1.2)
        proj = LaserProjectile(position=proj_pos, speed=LASER_SPEED)
        self.projectiles.append(proj)
        self.sounds.play('laser', pitch=random.uniform(0.95, 1.1), volume=0.55)

    def check_achievements(self):
        # 1. Speed
        if self.speed * 3.6 >= 100:
            ach = self.hs_mgr.unlock_achievement('speed_100')
            if ach:
                self.ui_mgr.show_achievement_banner(ach)

        # 2. Shards
        if self.coins_collected >= 50:
            ach = self.hs_mgr.unlock_achievement('shards_50')
            if ach:
                self.ui_mgr.show_achievement_banner(ach)

        # 3. Destructions
        if self.run_destructions >= 15:
            ach = self.hs_mgr.unlock_achievement('destructions_15')
            if ach:
                self.ui_mgr.show_achievement_banner(ach)

        # 4. Combo
        if self.combo_multiplier >= 8:
            ach = self.hs_mgr.unlock_achievement('combo_8')
            if ach:
                self.ui_mgr.show_achievement_banner(ach)

        # 5. Ramps
        if self.ramps_hit >= 5:
            ach = self.hs_mgr.unlock_achievement('ramps_5')
            if ach:
                self.ui_mgr.show_achievement_banner(ach)

    def handle_input(self, key):
        if self.state == STATE_MENU:
            if key in ('space', 'enter'):
                self.start_game()
            elif key in ('tab', 'm'):
                self.current_mode_index = (self.current_mode_index + 1) % len(GAME_MODES)
                self.ui_mgr.mode_index = self.current_mode_index
                m = GAME_MODES[self.current_mode_index]
                self.ui_mgr.mode_label.text = '[ MODE: OVERDRIVE ]' if self.current_mode_index == 1 else '[ MODE: CLASSIC ]'
                self.ui_mgr.mode_label.color = color.orange if self.current_mode_index == 1 else color.cyan
                self.ui_mgr.mode_desc.text = m['description']
                self.ui_mgr.hs_label.text = f"HIGH SCORE: {self.hs_mgr.get_high_score(self.current_mode_index):,}   |   RUNS: {self.hs_mgr.runs_played}"
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
                if self.player.jump():
                    self.sounds.play('jump', pitch=1.1, volume=0.5)
            elif key in ('s', 'down arrow'):
                self.player.slide()
            elif key in ('f', 'left mouse down'):
                self.fire_laser()
            elif key in ('e', 'left shift'):
                mode_cfg = GAME_MODES[self.current_mode_index]
                stack = mode_cfg['stacking_powerups']
                self.player.activate_boost(mode_cfg['boost_duration'], stack=stack)
                self.cam_shaker.add_shake(0.4)
                self.sounds.play('boost', pitch=1.2, volume=0.6)
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
        self.sounds.play('explosion', pitch=0.8, volume=0.7)
        self.cam_shaker.add_shake(1.0)
        ParticleBurst(position=self.player.position, burst_color=color.red, count=16)

        is_new_high = self.hs_mgr.record_run(
            self.score, self.distance, self.coins_collected, destructions=self.run_destructions, mode_index=self.current_mode_index
        )
        self.ui_mgr.show_game_over(
            score=self.score,
            distance=self.distance,
            coins=self.coins_collected,
            mode_index=self.current_mode_index,
            is_new_high=is_new_high,
            on_restart=self.start_game,
            on_menu=self.setup_menu
        )

    def trigger_emp(self):
        self.sounds.play('emp', volume=0.7)
        self.cam_shaker.add_shake(0.6)
        FloatingPopup('EMP SHOCKWAVE DISCHARGE!', position=self.player.position + Vec3(0, 1.5, 0), text_color=color.hex('#ff00aa'), scale=2.5)

        cleared_count = 0
        for seg in self.track_mgr.segments:
            for h in seg.hazards:
                if h.enabled and h.visible:
                    h.enabled = False
                    h.visible = False
                    ParticleBurst(position=h.position, burst_color=color.hex('#00ffee'), count=6)
                    cleared_count += 1

        if cleared_count > 0:
            bonus = cleared_count * 200 * self.combo_multiplier
            self.score += bonus
            self.run_destructions += cleared_count
            FloatingPopup(f'+{bonus} EMP CLEARED!', position=self.player.position + Vec3(0, 0.8, 2.0), text_color=color.yellow)

    def check_collisions(self, dt):
        p = self.player
        p_pos = p.position
        mode_cfg = GAME_MODES[self.current_mode_index]

        # 1. Projectiles vs Hazards
        for proj in self.projectiles:
            if not proj.enabled or not proj.visible:
                continue
            for h in self.track_mgr.get_nearby_hazards(proj.z, radius=4.0):
                if not h.enabled or not h.visible:
                    continue
                if abs(proj.z - h.z) < 1.2 and abs(proj.x - h.x) < h.hit_radius_x + 0.4:
                    # Laser hit hazard!
                    h.enabled = False
                    h.visible = False
                    proj.enabled = False
                    proj.visible = False
                    self.sounds.play('explosion', pitch=1.3, volume=0.5)
                    ParticleBurst(position=h.position, burst_color=color.hex('#00ffee'), count=8)
                    pts = 150 * self.combo_multiplier
                    self.score += pts
                    self.run_destructions += 1
                    FloatingPopup(f'+{pts} BLAST!', position=h.position + Vec3(0, 1.0, 0), text_color=color.hex('#00ffee'))
                    break

        # 2. Hazards vs Player
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

        # 3. Interactive Features (Ramps & Speed Pads)
        for feat in self.track_mgr.get_nearby_features(p_pos.z, radius=4.0):
            if not feat.enabled or not feat.visible:
                continue
            dz = abs(feat.z - p_pos.z)
            if dz < 1.4:
                dx = abs(feat.x - p_pos.x)
                if dx < feat.hit_radius_x:
                    if feat.feature_type == 'ramp' and p.is_grounded:
                        p.launch_ramp(RAMP_LAUNCH_FORCE)
                        self.ramps_hit += 1
                        self.cam_shaker.add_shake(0.3)
                        self.sounds.play('jump', pitch=0.9, volume=0.7)
                        FloatingPopup('RAMP LAUNCH!', position=feat.position + Vec3(0, 1.2, 0), text_color=color.yellow, scale=2.0)
                        feat.enabled = False
                    elif feat.feature_type == 'speed_pad':
                        p.activate_boost(SPEED_PAD_BOOST_TIME, stack=mode_cfg['stacking_powerups'])
                        self.cam_shaker.add_shake(0.35)
                        self.sounds.play('boost', pitch=1.4, volume=0.6)
                        FloatingPopup('TURBO BOOST!', position=feat.position + Vec3(0, 0.8, 0), text_color=color.cyan, scale=2.0)
                        feat.enabled = False

        # 4. Collectibles & Magnet
        base_magnet_range = 14.0
        if p.has_magnet:
            magnet_range = base_magnet_range + (p.magnet_stacks * 6.0 if mode_cfg['stacking_powerups'] else 0.0)
            pull_speed = 24.0 + (p.magnet_stacks * 8.0 if mode_cfg['stacking_powerups'] else 0.0)
        else:
            magnet_range = 3.0
            pull_speed = 0.0

        for item in self.track_mgr.get_nearby_items(p_pos.z, radius=magnet_range + 2.0):
            if not item.enabled or not item.visible:
                continue

            dist_x = item.x - p_pos.x
            dist_y = item.y - p_pos.y
            dist_z = item.z - p_pos.z
            dist_sq = dist_x * dist_x + dist_y * dist_y + dist_z * dist_z

            if p.has_magnet and dist_sq < magnet_range * magnet_range:
                dist_len = math.sqrt(dist_sq)
                if dist_len > 0.001:
                    step = pull_speed * dt / dist_len
                    item.x -= dist_x * step
                    item.y -= dist_y * step
                    item.z -= dist_z * step

            if dist_sq < 3.24:  # 1.8^2
                item.enabled = False
                item.visible = False
                self.handle_item_pickup(item)

    def trigger_hit(self, hazard):
        if self.invulnerable_timer > 0:
            return

        if self.player.is_boosting:
            self.cam_shaker.add_shake(0.35)
            self.sounds.play('explosion', pitch=1.4, volume=0.55)
            ParticleBurst(position=hazard.position, burst_color=color.orange, count=8)
            FloatingPopup('+200 SMASH!', position=hazard.position + Vec3(0, 1, 0), text_color=color.orange)
            self.score += 200 * self.combo_multiplier
            self.run_destructions += 1
            hazard.enabled = False
            hazard.visible = False
            return

        if self.player.has_shield:
            charges_left = self.player.consume_shield_charge()
            self.invulnerable_timer = 1.6
            self.cam_shaker.add_shake(0.5)
            self.sounds.play('explosion', pitch=1.1, volume=0.6)
            ParticleBurst(position=self.player.position, burst_color=color.azure, count=8)
            
            if charges_left > 0:
                FloatingPopup(f'SHIELD HIT! [{charges_left} REMAIN]', position=self.player.position + Vec3(0, 1.2, 0), text_color=color.azure)
            else:
                FloatingPopup('SHIELD BROKEN!', position=self.player.position + Vec3(0, 1.2, 0), text_color=color.orange)
                
            hazard.enabled = False
            hazard.visible = False
            
            for nearby_h in self.track_mgr.get_nearby_hazards(self.player.z, radius=8.0):
                nearby_h.enabled = False
                nearby_h.visible = False
            return

        self.game_over()

    def handle_item_pickup(self, item):
        mode_cfg = GAME_MODES[self.current_mode_index]
        is_stack = mode_cfg['stacking_powerups']
        ParticleBurst(position=item.position, burst_color=item.color, count=5)
        self.sounds.play('pickup', pitch=1.0 + (self.combo_multiplier * 0.05), volume=0.5)

        if item.item_type == 'shard':
            self.coins_collected += 1
            self.score += COIN_POINTS * self.combo_multiplier
            self.combo_timer = COMBO_TIMEOUT
            max_c = mode_cfg['max_combo']
            self.combo_multiplier = min(max_c, self.combo_multiplier + 1)
            FloatingPopup(f'+{COIN_POINTS * self.combo_multiplier}', position=item.position, text_color=color.cyan)

        elif item.item_type == 'shield':
            self.player.activate_shield(mode_cfg['shield_duration'], stack=is_stack)
            tag = f'SHIELD x{self.player.shield_charges}!' if is_stack and self.player.shield_charges > 1 else 'SHIELD MATRIX!'
            FloatingPopup(tag, position=item.position, text_color=color.azure, scale=2.0)

        elif item.item_type == 'magnet':
            self.player.activate_magnet(mode_cfg['magnet_duration'], stack=is_stack)
            tag = f'MAGNET x{self.player.magnet_stacks}!' if is_stack and self.player.magnet_stacks > 1 else 'MAGNET FLUX!'
            FloatingPopup(tag, position=item.position, text_color=color.yellow, scale=2.0)

        elif item.item_type == 'boost':
            self.player.activate_boost(mode_cfg['boost_duration'], stack=is_stack)
            self.cam_shaker.add_shake(0.4)
            tag = f'HYPERDRIVE x{self.player.boost_stacks}!' if is_stack and self.player.boost_stacks > 1 else 'HYPERDRIVE ENGAGED!'
            FloatingPopup(tag, position=item.position, text_color=color.orange, scale=2.2)

        elif item.item_type == 'ammo':
            from game.config import AMMO_PICKUP_AMOUNT
            total = self.player.add_ammo(AMMO_PICKUP_AMOUNT)
            FloatingPopup(f'+{AMMO_PICKUP_AMOUNT} PLASMA CELLS [{total} TOTAL]', position=item.position, text_color=color.hex('#00ffee'), scale=2.0)

        elif item.item_type == 'emp':
            self.trigger_emp()

    def update(self):
        dt = min(ursina_time.dt, MAX_DELTA_TIME)
        mode_cfg = GAME_MODES[self.current_mode_index]

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

            # Mode-specific acceleration & max speed
            accel_rate = mode_cfg['speed_acceleration']
            max_spd = mode_cfg['max_speed']
            self.base_speed = min(max_spd, mode_cfg['initial_speed'] + (self.distance / 100.0) * accel_rate)
            
            if self.player.is_boosting:
                if mode_cfg['stacking_powerups']:
                    boost_mult = mode_cfg['boost_multiplier'] + (self.player.boost_stacks - 1) * 0.25
                    self.target_fov = min(96, 82 + (self.player.boost_stacks - 1) * 5)
                else:
                    boost_mult = mode_cfg['boost_multiplier']
                    self.target_fov = 82
                self.speed = self.base_speed * boost_mult
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

            # Update & Clean projectiles
            for proj in list(self.projectiles):
                if not proj.enabled or not proj.visible:
                    destroy_entity_tree(proj)
                    self.projectiles.remove(proj)

            self.check_collisions(dt)
            self.check_achievements()

            # Dynamic Camera follow tracking behind player
            cam_target_y = self.player.y + 2.8 if not self.player.is_sliding else 2.2
            self.cam_shaker.base_pos = Vec3(
                self.player.x * 0.45,
                cam_target_y,
                self.player.z - 7.5
            )
            self.cam_shaker.update(dt)

            if self.track_mgr.current_biome_index != self.active_biome_index:
                self.active_biome_index = self.track_mgr.current_biome_index
                curr_biome = self.track_mgr.get_current_biome()
                self.apply_dark_theme(curr_biome)

            # Update HUD status
            powerup_msg = ''
            if self.player.is_boosting:
                stack_str = f' x{self.player.boost_stacks}' if self.player.boost_stacks > 1 else ''
                powerup_msg += f'[BOOST{stack_str}: {self.player.boost_timer:.1f}s]  '
            if self.player.has_shield:
                stack_str = f' x{self.player.shield_charges}' if self.player.shield_charges > 1 else ''
                powerup_msg += f'[SHIELD{stack_str}: {self.player.shield_timer:.1f}s]  '
            if self.player.has_magnet:
                stack_str = f' x{self.player.magnet_stacks}' if self.player.magnet_stacks > 1 else ''
                powerup_msg += f'[MAGNET{stack_str}: {self.player.magnet_timer:.1f}s]'

            laser_ready = (self.player.laser_cooldown <= 0.0)

            self.ui_mgr.update_hud(
                score=self.score,
                high_score=max(self.score, self.hs_mgr.get_high_score(self.current_mode_index)),
                multiplier=self.combo_multiplier,
                speed=self.speed,
                powerup_msg=powerup_msg,
                ammo=self.player.ammo,
                laser_ready=laser_ready,
                dt=dt
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
