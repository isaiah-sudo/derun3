from ursina import Entity, color, Vec3, time

class LaserHurdle(Entity):
    def __init__(self, position=(0, 0, 0), theme_color=None):
        super().__init__(position=position)
        self.hazard_type = 'low_jump'
        laser_red = color.hex('#ff1946')
        post_coral = color.hex('#ff4664')
        warning_yellow = color.hex('#ffe628')

        # Glowing neon barrier posts
        self.left_post = Entity(parent=self, model='cube', color=post_coral, scale=(0.35, 1.4, 0.35), position=(-1.5, 0.7, 0))
        self.right_post = Entity(parent=self, model='cube', color=post_coral, scale=(0.35, 1.4, 0.35), position=(1.5, 0.7, 0))
        # Glowing crimson laser beam
        self.beam = Entity(parent=self, model='cube', color=laser_red, scale=(3.0, 0.45, 0.25), position=(0, 0.55, 0))
        self.glow = Entity(parent=self, model='cube', color=warning_yellow, scale=(2.9, 0.18, 0.15), position=(0, 0.55, 0))
        self.hit_radius_x = 0.95
        self.clear_height = 0.85

class HighBarrier(Entity):
    def __init__(self, position=(0, 0, 0), theme_color=None):
        super().__init__(position=position)
        self.hazard_type = 'high_slide'
        orange_base = color.hex('#ff780a')
        post_orange = color.hex('#ffa028')
        glow_yellow = color.hex('#fff032')

        # Tall side pillars
        self.left_post = Entity(parent=self, model='cube', color=post_orange, scale=(0.35, 3.5, 0.35), position=(-1.5, 1.75, 0))
        self.right_post = Entity(parent=self, model='cube', color=post_orange, scale=(0.35, 3.5, 0.35), position=(1.5, 1.75, 0))
        # Overhead orange barrier block
        self.block = Entity(parent=self, model='cube', color=orange_base, scale=(3.0, 1.5, 0.4), position=(0, 2.2, 0))
        self.glow = Entity(parent=self, model='cube', color=glow_yellow, scale=(2.9, 0.28, 0.2), position=(0, 1.5, 0))
        self.hit_radius_x = 0.95

class DroneHazard(Entity):
    def __init__(self, position=(0, 0, 0), min_x=-3.2, max_x=3.2, speed=3.2, theme_color=None):
        super().__init__(position=position)
        self.hazard_type = 'drone'
        chassis_magenta = color.hex('#d220e6')
        wing_orange = color.hex('#ff961e')

        self.body = Entity(parent=self, model='sphere', color=chassis_magenta, scale=(1.1, 0.55, 1.1), position=(0, 1.0, 0))
        self.eye = Entity(parent=self, model='sphere', color=color.cyan, scale=(0.45, 0.45, 0.45), position=(0, 1.0, 0.45))
        self.wing1 = Entity(parent=self, model='cube', color=wing_orange, scale=(1.7, 0.12, 0.3), position=(0, 1.05, 0))
        self.min_x = min_x
        self.max_x = max_x
        self.speed = speed
        self.direction = 1
        self.hit_radius_x = 0.8
        self.clear_height = 0.85

    def update(self):
        dt = min(time.dt, 0.05)
        self.x += self.direction * self.speed * dt
        if self.x > self.max_x:
            self.x = self.max_x
            self.direction = -1
        elif self.x < self.min_x:
            self.x = self.min_x
            self.direction = 1
        self.wing1.rotation_y += 360.0 * dt

class PylonHazard(Entity):
    def __init__(self, position=(0, 0, 0), theme_color=None):
        super().__init__(position=position)
        self.hazard_type = 'pylon'
        pillar_blue = color.hex('#1e5ae6')
        core_cyan = color.hex('#00f0ff')

        self.pillar = Entity(parent=self, model='cube', color=pillar_blue, scale=(0.95, 3.5, 0.95), position=(0, 1.75, 0))
        self.core = Entity(parent=self, model='cube', color=core_cyan, scale=(0.6, 3.2, 0.6), position=(0, 1.75, 0))
        self.hit_radius_x = 0.85

class JumpRamp(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position)
        self.feature_type = 'ramp'
        ramp_yellow = color.hex('#ffee00')
        ramp_dark = color.hex('#181824')

        # Slanted ramp wedge
        self.base = Entity(parent=self, model='cube', color=ramp_dark, scale=(2.6, 0.5, 3.2), position=(0, 0.25, 0), rotation_x=-16)
        self.arrow = Entity(parent=self, model='cube', color=ramp_yellow, scale=(1.8, 0.54, 0.4), position=(0, 0.28, 0.4), rotation_x=-16)
        self.arrow2 = Entity(parent=self, model='cube', color=ramp_yellow, scale=(1.2, 0.54, 0.4), position=(0, 0.45, 1.0), rotation_x=-16)
        self.hit_radius_x = 1.3

class SpeedPad(Entity):
    def __init__(self, position=(0, 0, 0)):
        super().__init__(position=position)
        self.feature_type = 'speed_pad'
        pad_cyan = color.hex('#00ffee')

        self.base = Entity(parent=self, model='cube', color=color.hex('#0a1020'), scale=(2.8, 0.08, 4.0), position=(0, 0.04, 0))
        self.chevron1 = Entity(parent=self, model='cube', color=pad_cyan, scale=(1.8, 0.1, 0.5), position=(0, 0.05, -1.0))
        self.chevron2 = Entity(parent=self, model='cube', color=pad_cyan, scale=(1.8, 0.1, 0.5), position=(0, 0.05, 0.0))
        self.chevron3 = Entity(parent=self, model='cube', color=pad_cyan, scale=(1.8, 0.1, 0.5), position=(0, 0.05, 1.0))
        self.hit_radius_x = 1.3

class LaserProjectile(Entity):
    def __init__(self, position=(0, 0, 0), speed=140.0):
        super().__init__(position=position)
        self.speed = speed
        self.laser_color = color.hex('#00ffee')
        self.bolt_l = Entity(parent=self, model='cube', color=self.laser_color, scale=(0.18, 0.18, 1.6), position=(-0.5, 0, 0))
        self.bolt_r = Entity(parent=self, model='cube', color=self.laser_color, scale=(0.18, 0.18, 1.6), position=(0.5, 0, 0))
        self.core = Entity(parent=self, model='sphere', color=color.white, scale=(0.3, 0.3, 0.8), position=(0, 0, 0))
        self.lifetime = 1.2
        self.elapsed = 0.0

    def update(self):
        dt = min(time.dt, 0.05)
        self.z += self.speed * dt
        self.elapsed += dt
        if self.elapsed >= self.lifetime:
            self.enabled = False
            self.visible = False
