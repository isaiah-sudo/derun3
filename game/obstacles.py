from ursina import Entity, color, Vec3, time

class LaserHurdle(Entity):
    def __init__(self, position=(0, 0, 0), theme_color=color.magenta):
        super().__init__(position=position)
        self.hazard_type = 'low_jump'
        self.left_post = Entity(parent=self, model='cube', color=color.dark_gray, scale=(0.3, 1.4, 0.3), position=(-1.5, 0.7, 0))
        self.right_post = Entity(parent=self, model='cube', color=color.dark_gray, scale=(0.3, 1.4, 0.3), position=(1.5, 0.7, 0))
        self.beam = Entity(parent=self, model='cube', color=theme_color, scale=(3.0, 0.35, 0.2), position=(0, 0.55, 0))
        self.glow = Entity(parent=self, model='cube', color=color.white, scale=(2.9, 0.15, 0.1), position=(0, 0.55, 0))
        self.hit_radius_x = 0.95
        self.clear_height = 0.85

class HighBarrier(Entity):
    def __init__(self, position=(0, 0, 0), theme_color=color.orange):
        super().__init__(position=position)
        self.hazard_type = 'high_slide'
        self.left_post = Entity(parent=self, model='cube', color=color.dark_gray, scale=(0.3, 3.5, 0.3), position=(-1.5, 1.75, 0))
        self.right_post = Entity(parent=self, model='cube', color=color.dark_gray, scale=(0.3, 3.5, 0.3), position=(1.5, 1.75, 0))
        self.block = Entity(parent=self, model='cube', color=theme_color, scale=(3.0, 1.5, 0.35), position=(0, 2.2, 0))
        self.glow = Entity(parent=self, model='cube', color=color.yellow, scale=(2.9, 0.25, 0.15), position=(0, 1.5, 0))
        self.hit_radius_x = 0.95

class DroneHazard(Entity):
    def __init__(self, position=(0, 0, 0), min_x=-3.2, max_x=3.2, speed=3.2, theme_color=color.red):
        super().__init__(position=position)
        self.hazard_type = 'drone'
        self.body = Entity(parent=self, model='sphere', color=color.rgb(30, 30, 30), scale=(1.0, 0.5, 1.0), position=(0, 1.0, 0))
        self.eye = Entity(parent=self, model='sphere', color=theme_color, scale=(0.4, 0.4, 0.4), position=(0, 1.0, 0.4))
        self.wing1 = Entity(parent=self, model='cube', color=theme_color, scale=(1.6, 0.1, 0.25), position=(0, 1.05, 0))
        self.min_x = min_x
        self.max_x = max_x
        self.speed = speed
        self.direction = 1
        self.hit_radius_x = 0.8
        self.clear_height = 0.85

    def update(self):
        self.x += self.direction * self.speed * time.dt
        if self.x > self.max_x:
            self.x = self.max_x
            self.direction = -1
        elif self.x < self.min_x:
            self.x = self.min_x
            self.direction = 1
        self.wing1.rotation_y += 360.0 * time.dt

class PylonHazard(Entity):
    def __init__(self, position=(0, 0, 0), theme_color=color.magenta):
        super().__init__(position=position)
        self.hazard_type = 'pylon'
        self.pillar = Entity(parent=self, model='cube', color=color.rgb(20, 20, 30), scale=(0.9, 3.5, 0.9), position=(0, 1.75, 0))
        self.core = Entity(parent=self, model='cube', color=theme_color, scale=(0.55, 3.2, 0.55), position=(0, 1.75, 0))
        self.hit_radius_x = 0.85
