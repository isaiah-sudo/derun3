from ursina import Entity, Text, Button, color, camera, Vec2, Vec3, destroy
from game.config import SHIP_SKINS, GAME_MODES

def destroy_entity_tree(entity):
    if not entity:
        return
    for child in list(entity.children):
        destroy_entity_tree(child)
    destroy(entity)

class UIManager:
    def __init__(self, highscore_mgr):
        self.hs_mgr = highscore_mgr
        self.hud_root = None
        self.menu_root = None
        self.pause_root = None
        self.gameover_root = None

        self.score_text = None
        self.mode_badge_text = None
        self.high_score_text = None
        self.multiplier_text = None
        self.speed_text = None
        self.powerup_text = None
        self.skin_index = 0
        self.mode_index = 0

    def init_hud(self, mode_index=0):
        if self.hud_root:
            destroy_entity_tree(self.hud_root)
        self.hud_root = Entity(parent=camera.ui)
        self.mode_index = mode_index
        mode_data = GAME_MODES[mode_index]

        # Top Left: Score, Multiplier & Mode Badge
        self.score_text = Text(
            parent=self.hud_root,
            text='SCORE: 0',
            position=(-0.82, 0.44),
            scale=1.5,
            color=color.cyan
        )
        self.multiplier_text = Text(
            parent=self.hud_root,
            text='MULTIPLIER: x1',
            position=(-0.82, 0.39),
            scale=1.1,
            color=color.yellow
        )
        
        mode_col = color.orange if mode_index == 1 else color.cyan
        mode_label = f"MODE: {mode_data['name']} // {mode_data['tag']}"
        self.mode_badge_text = Text(
            parent=self.hud_root,
            text=mode_label,
            position=(-0.82, 0.34),
            scale=1.0,
            color=mode_col
        )

        # Top Right: High Score & Speed
        best_val = self.hs_mgr.get_high_score(mode_index)
        self.high_score_text = Text(
            parent=self.hud_root,
            text=f'BEST: {best_val:,}',
            position=(0.55, 0.44),
            scale=1.2,
            color=color.magenta
        )
        self.speed_text = Text(
            parent=self.hud_root,
            text='SPEED: 120 KM/H',
            position=(0.55, 0.39),
            scale=1.1,
            color=color.lime
        )

        # Bottom Center: Powerup Status Indicator
        self.powerup_text = Text(
            parent=self.hud_root,
            text='',
            origin=(0, 0),
            position=(0, -0.4),
            scale=1.35,
            color=color.orange
        )

    def update_hud(self, score, high_score, multiplier, speed, powerup_msg):
        if not self.hud_root or not self.hud_root.enabled:
            return
        self.score_text.text = f'SCORE: {int(score):,}'
        self.high_score_text.text = f'BEST: {int(high_score):,}'
        if multiplier > 1:
            self.multiplier_text.text = f'COMBO: x{multiplier} !'
            self.multiplier_text.color = color.orange
        else:
            self.multiplier_text.text = 'COMBO: x1'
            self.multiplier_text.color = color.yellow

        display_speed = int(speed * 3.6)
        self.speed_text.text = f'SPEED: {display_speed} KM/H'
        self.powerup_text.text = powerup_msg

    def show_hud(self, show=True):
        if self.hud_root:
            self.hud_root.enabled = show

    def show_menu(self, on_start, on_skin_change, on_mode_change):
        self.hide_all()
        self.menu_root = Entity(parent=camera.ui)

        # Title
        Text(
            parent=self.menu_root,
            text='C Y B E R S U R G E   3 D',
            origin=(0, 0),
            position=(0, 0.34),
            scale=2.2,
            color=color.cyan
        )
        Text(
            parent=self.menu_root,
            text='// SYNTHWAVE ENDLESS RUNNER //',
            origin=(0, 0),
            position=(0, 0.28),
            scale=1.1,
            color=color.magenta
        )

        # Highscore display for selected mode
        self.hs_label = Text(
            parent=self.menu_root,
            text=f'HIGH SCORE: {self.hs_mgr.get_high_score(self.mode_index):,}   |   RUNS: {self.hs_mgr.runs_played}',
            origin=(0, 0),
            position=(0, 0.20),
            scale=1.1,
            color=color.yellow
        )

        # Mode Selector
        def update_mode_ui():
            m = GAME_MODES[self.mode_index]
            mode_tag = '[ MODE: OVERDRIVE ]' if self.mode_index == 1 else '[ MODE: CLASSIC ]'
            mode_color = color.orange if self.mode_index == 1 else color.cyan
            self.mode_label.text = mode_tag
            self.mode_label.color = mode_color
            self.mode_desc.text = m['description']
            self.hs_label.text = f"HIGH SCORE: {self.hs_mgr.get_high_score(self.mode_index):,}   |   RUNS: {self.hs_mgr.runs_played}"

        def toggle_mode():
            self.mode_index = (self.mode_index + 1) % len(GAME_MODES)
            update_mode_ui()
            on_mode_change(self.mode_index)

        self.mode_label = Text(
            parent=self.menu_root,
            text='[ MODE: CLASSIC ]',
            origin=(0, 0),
            position=(0, 0.11),
            scale=1.4,
            color=color.cyan
        )
        self.mode_desc = Text(
            parent=self.menu_root,
            text=GAME_MODES[self.mode_index]['description'],
            origin=(0, 0),
            position=(0, 0.05),
            scale=0.95,
            color=color.light_gray
        )

        Button(
            parent=self.menu_root,
            text='SWITCH MODE',
            scale=(0.26, 0.05),
            position=(0, -0.01),
            color=color.dark_gray,
            highlight_color=color.orange,
            on_click=toggle_mode
        )

        # Skin selector info
        skin_name = SHIP_SKINS[self.skin_index]['name']
        self.skin_label = Text(
            parent=self.menu_root,
            text=f'[ SHIP: {skin_name} ]',
            origin=(0, 0),
            position=(0, -0.09),
            scale=1.2,
            color=color.lime
        )

        def prev_skin():
            self.skin_index = (self.skin_index - 1) % len(SHIP_SKINS)
            self.skin_label.text = f'[ SHIP: {SHIP_SKINS[self.skin_index]["name"]} ]'
            on_skin_change(self.skin_index)

        def next_skin():
            self.skin_index = (self.skin_index + 1) % len(SHIP_SKINS)
            self.skin_label.text = f'[ SHIP: {SHIP_SKINS[self.skin_index]["name"]} ]'
            on_skin_change(self.skin_index)

        Button(
            parent=self.menu_root,
            text='PREV',
            scale=(0.12, 0.05),
            position=(-0.24, -0.09),
            color=color.dark_gray,
            highlight_color=color.azure,
            on_click=prev_skin
        )
        Button(
            parent=self.menu_root,
            text='NEXT',
            scale=(0.12, 0.05),
            position=(0.24, -0.09),
            color=color.dark_gray,
            highlight_color=color.azure,
            on_click=next_skin
        )

        # Controls info
        controls_str = "CONTROLS: [A]/[D] Shift Lanes | [W]/[Space] Jump | [S] Slide | [E] Hyper-Boost"
        Text(
            parent=self.menu_root,
            text=controls_str,
            origin=(0, 0),
            position=(0, -0.19),
            scale=0.95,
            color=color.gray
        )

        # Launch Button
        Button(
            parent=self.menu_root,
            text='[ LAUNCH MISSION ]',
            scale=(0.35, 0.08),
            position=(0, -0.31),
            color=color.azure,
            highlight_color=color.cyan,
            on_click=on_start
        )

    def show_game_over(self, score, distance, coins, mode_index, is_new_high, on_restart, on_menu):
        self.hide_all()
        self.gameover_root = Entity(parent=camera.ui)
        mode_name = GAME_MODES[mode_index]['name']

        Text(
            parent=self.gameover_root,
            text='S U R G E   T E R M I N A T E D',
            origin=(0, 0),
            position=(0, 0.32),
            scale=2.2,
            color=color.red
        )

        if is_new_high:
            Text(
                parent=self.gameover_root,
                text=f'* NEW {mode_name} RECORD! *',
                origin=(0, 0),
                position=(0, 0.23),
                scale=1.4,
                color=color.yellow
            )

        summary_text = (
            f"MODE:          {mode_name}\n"
            f"FINAL SCORE:   {int(score):,}\n\n"
            f"DISTANCE:      {int(distance):,} m\n"
            f"ENERGY SHARDS: {coins}\n"
            f"BEST RECORD:   {self.hs_mgr.get_high_score(mode_index):,}"
        )
        Text(
            parent=self.gameover_root,
            text=summary_text,
            origin=(0, 0),
            position=(0, 0.05),
            scale=1.2,
            color=color.white
        )

        Button(
            parent=self.gameover_root,
            text='[ RETRY - SPACE ]',
            scale=(0.28, 0.07),
            position=(-0.16, -0.23),
            color=color.azure,
            highlight_color=color.cyan,
            on_click=on_restart
        )
        Button(
            parent=self.gameover_root,
            text='[ MAIN MENU ]',
            scale=(0.28, 0.07),
            position=(0.16, -0.23),
            color=color.dark_gray,
            highlight_color=color.magenta,
            on_click=on_menu
        )

    def show_pause(self, on_resume, on_restart, on_menu):
        if self.pause_root:
            destroy_entity_tree(self.pause_root)
        self.pause_root = Entity(parent=camera.ui)

        Text(
            parent=self.pause_root,
            text='P A U S E D',
            origin=(0, 0),
            position=(0, 0.22),
            scale=2.0,
            color=color.yellow
        )

        Button(
            parent=self.pause_root,
            text='[ RESUME ]',
            scale=(0.26, 0.06),
            position=(0, 0.06),
            color=color.azure,
            on_click=on_resume
        )
        Button(
            parent=self.pause_root,
            text='[ RESTART ]',
            scale=(0.26, 0.06),
            position=(0, -0.04),
            color=color.dark_gray,
            on_click=on_restart
        )
        Button(
            parent=self.pause_root,
            text='[ MAIN MENU ]',
            scale=(0.26, 0.06),
            position=(0, -0.14),
            color=color.dark_gray,
            on_click=on_menu
        )

    def hide_pause(self):
        if self.pause_root:
            destroy_entity_tree(self.pause_root)
            self.pause_root = None

    def hide_all(self):
        if self.menu_root:
            destroy_entity_tree(self.menu_root)
            self.menu_root = None
        if self.hud_root:
            self.hud_root.enabled = False
        if self.gameover_root:
            destroy_entity_tree(self.gameover_root)
            self.gameover_root = None
        if self.pause_root:
            destroy_entity_tree(self.pause_root)
            self.pause_root = None
