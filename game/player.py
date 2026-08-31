import math
import time
from ursina import Entity, Vec3, color, destroy, held_keys
from ursina import time as ursina_time
from game.config import (
    LANE_POSITIONS, JUMP_FORCE, GRAVITY, SLIDE_DURATION,
    LANE_LERP_SPEED, SHIP_SKINS
)

class Player(Entity):
    def __init__(self, skin_index=0, **kwargs):
        super().__init__(**kwargs)
        self.current_lane_idx = 1  # 0: Left, 1: Center, 2: Right
        self.target_x = LANE_POSITIONS[self.current_lane_idx]
        self.x = self.target_x
        self.y = 0.5
        self.z = 0.0

        self.vy = 0.0
        self.is_grounded = True
        self.is_sliding = False
        self.slide_timer = 0.0

        # Powerups state & Stacking
        self.has_shield = False
        self.shield_timer = 0.0
        self.shield_charges = 0

        self.has_magnet = False
        self.magnet_timer = 0.0
        self.magnet_stacks = 0

        self.is_boosting = False
        self.boost_timer = 0.0
        self.boost_stacks = 0

        # Ammo state & Stacking
        self.ammo = 0

        # Stats
        self.skin_index = skin_index % len(SHIP_SKINS)
        self.skin_data = SHIP_SKINS[self.skin_index]

        self.build_model()

    def build_model(self):
        for child in list(self.children):
            destroy(child)

        pri_col = self.skin_data['primary']
        sec_col = self.skin_data['secondary']
        hull_dark = color.hex('#161420')
        thruster_glow = color.hex('#00e5ff')

        # Central hovercraft fuselage
        self.body = Entity(
            parent=self,
            model='cube',
            color=hull_dark,
            scale=(1.2, 0.45, 2.2),
            position=(0, 0, 0)
        )
        # Cockpit canopy
        self.cockpit = Entity(
            parent=self,
            model='sphere',
            color=sec_col,
            scale=(0.7, 0.4, 1.1),
            position=(0, 0.28, 0.2)
        )
        # Left wing
        self.left_wing = Entity(
            parent=self,
            model='cube',
            color=pri_col,
            scale=(1.1, 0.12, 1.4),
            position=(-1.0, 0.0, -0.2),
            rotation_z=-8
        )
        # Right wing
        self.right_wing = Entity(
            parent=self,
            model='cube',
            color=pri_col,
            scale=(1.1, 0.12, 1.4),
            position=(1.0, 0.0, -0.2),
            rotation_z=8
        )
        # Left & Right Thruster nozzles
        self.thruster_l = Entity(
            parent=self,
            model='cube',
            color=thruster_glow,
            scale=(0.3, 0.3, 0.5),
            position=(-0.45, 0.0, -1.1)
        )
        self.thruster_r = Entity(
            parent=self,
            model='cube',
            color=thruster_glow,
            scale=(0.3, 0.3, 0.5),
            position=(0.45, 0.0, -1.1)
        )
        # Shield Bubble
        self.shield_bubble = Entity(
            parent=self,
            model='sphere',
            color=color.azure,
            alpha=0.35,
            scale=3.2,
            position=(0, 0.2, 0),
            enabled=False
        )
        # Magnet Aura
        self.magnet_aura = Entity(
            parent=self,
            model='quad',
            color=color.yellow,
            scale=3.6,
            rotation_x=90,
            position=(0, -0.2, 0),
            double_sided=True,
            enabled=False
        )

        # Laser Cannons
        self.cannon_l = Entity(
            parent=self,
            model='cube',
            color=color.hex('#ff0055'),
            scale=(0.14, 0.14, 1.0),
            position=(-0.9, -0.05, 0.4)
        )
        self.cannon_r = Entity(
            parent=self,
            model='cube',
            color=color.hex('#ff0055'),
            scale=(0.14, 0.14, 1.0),
            position=(0.9, -0.05, 0.4)
        )

        # Laser Weapon Cooldown
        self.laser_cooldown = 0.0

    def change_skin(self, index):
        self.skin_index = index % len(SHIP_SKINS)
        self.skin_data = SHIP_SKINS[self.skin_index]
        self.build_model()

    def move_left(self):
        if self.current_lane_idx > 0:
            self.current_lane_idx -= 1
            self.target_x = LANE_POSITIONS[self.current_lane_idx]
            return True
        return False

    def move_right(self):
        if self.current_lane_idx < len(LANE_POSITIONS) - 1:
            self.current_lane_idx += 1
            self.target_x = LANE_POSITIONS[self.current_lane_idx]
            return True
        return False

    def jump(self):
        if self.is_grounded:
            self.vy = JUMP_FORCE
            self.is_grounded = False
            self.is_sliding = False
            return True
        return False

    def launch_ramp(self, force=24.0):
        self.vy = force
        self.is_grounded = False
        self.is_sliding = False

    def slide(self):
        if not self.is_sliding:
            self.is_sliding = True
            self.slide_timer = SLIDE_DURATION
            if not self.is_grounded:
                self.vy = -JUMP_FORCE * 1.5
            return True
        return False

    def activate_shield(self, duration=15.0, stack=False):
        self.has_shield = True
        if stack:
            self.shield_charges += 1
            self.shield_timer += duration
        else:
            self.shield_charges = 1
            self.shield_timer = duration
        self.shield_bubble.enabled = True
        self.shield_bubble.scale = 3.2 + min(1.2, self.shield_charges * 0.3)

    def consume_shield_charge(self):
        self.shield_charges = max(0, self.shield_charges - 1)
        if self.shield_charges <= 0:
            self.has_shield = False
            self.shield_timer = 0.0
            self.shield_bubble.enabled = False
        else:
            self.shield_bubble.scale = 3.2 + min(1.2, self.shield_charges * 0.3)
        return self.shield_charges

    def activate_magnet(self, duration=8.0, stack=False):
        self.has_magnet = True
        if stack:
            self.magnet_stacks = min(4, self.magnet_stacks + 1)
            self.magnet_timer += duration
        else:
            self.magnet_stacks = 1
            self.magnet_timer = duration
        self.magnet_aura.enabled = True
        self.magnet_aura.scale = 3.6 + (self.magnet_stacks * 0.8)

    def add_ammo(self, count=5):
        from game.config import MAX_AMMO
        self.ammo = min(MAX_AMMO, self.ammo + count)
        return self.ammo

    def consume_ammo(self):
        if self.ammo > 0:
            self.ammo -= 1
            return True
        return False

    def activate_boost(self, duration=5.0, stack=False):
        self.is_boosting = True
        if stack:
            self.boost_stacks = min(4, self.boost_stacks + 1)
            self.boost_timer += duration
        else:
            self.boost_stacks = 1
            self.boost_timer = duration

    def update_player(self, dt):
        if self.laser_cooldown > 0:
            self.laser_cooldown = max(0.0, self.laser_cooldown - dt)

        dx = self.target_x - self.x
        self.x += dx * LANE_LERP_SPEED * dt

        target_roll = -dx * 8.0
        self.rotation_z += (target_roll - self.rotation_z) * 12.0 * dt

        if not self.is_grounded:
            self.vy -= GRAVITY * dt
            self.y += self.vy * dt
            if self.y <= 0.5:
                self.y = 0.5
                self.vy = 0.0
                self.is_grounded = True
                self.rotation_x = 0
            else:
                self.rotation_x = -self.vy * 1.5
        else:
            self.y = 0.5 + 0.08 * math.sin(time.time() * 6.0)

        if self.is_sliding:
            self.slide_timer -= dt
            self.scale_y = 0.45
            self.rotation_x = 12.0
            if self.slide_timer <= 0.0:
                self.is_sliding = False
                self.scale_y = 1.0
                self.rotation_x = 0.0
        else:
            self.scale_y = 1.0

        if self.has_shield:
            self.shield_timer -= dt
            self.shield_bubble.rotation_y += 90.0 * dt
            if self.shield_timer <= 0:
                self.has_shield = False
                self.shield_charges = 0
                self.shield_bubble.enabled = False

        if self.has_magnet:
            self.magnet_timer -= dt
            self.magnet_aura.rotation_z += 180.0 * dt
            if self.magnet_timer <= 0:
                self.has_magnet = False
                self.magnet_stacks = 0
                self.magnet_aura.enabled = False

        if self.is_boosting:
            self.boost_timer -= dt
            intensity = 1.0 + (self.boost_stacks * 0.3)
            flicker = (1.2 + 0.4 * math.sin(time.time() * 30.0)) * intensity
            self.thruster_l.scale_z = 0.5 * flicker
            self.thruster_r.scale_z = 0.5 * flicker
            if self.boost_timer <= 0:
                self.is_boosting = False
                self.boost_stacks = 0
                self.thruster_l.scale_z = 0.5
                self.thruster_r.scale_z = 0.5
