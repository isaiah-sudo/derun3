import random
from ursina import Entity, Text, color, Vec3, destroy, time

class CameraShake:
    def __init__(self, cam):
        self.cam = cam
        self.trauma = 0.0
        self.base_pos = Vec3(cam.position.x, cam.position.y, cam.position.z)
        self.shake_decay = 3.5

    def add_shake(self, amount=0.5):
        self.trauma = min(1.0, self.trauma + amount)

    def update(self, dt):
        if self.trauma > 0.001:
            self.trauma = max(0.0, self.trauma - self.shake_decay * dt)
            shake_amt = (self.trauma ** 2) * 0.45
            offset_x = (random.random() * 2.0 - 1.0) * shake_amt
            offset_y = (random.random() * 2.0 - 1.0) * shake_amt
            self.cam.x = self.base_pos.x + offset_x
            self.cam.y = self.base_pos.y + offset_y
            self.cam.z = self.base_pos.z
        else:
            self.cam.x = self.base_pos.x
            self.cam.y = self.base_pos.y
            self.cam.z = self.base_pos.z

class FloatingPopup(Entity):
    def __init__(self, text, position, text_color=color.cyan, scale=1.8):
        super().__init__(position=position)
        self.text_entity = Text(
            text=text,
            parent=self,
            origin=(0, 0),
            color=text_color,
            scale=scale,
            billboard=True
        )
        self.lifetime = 1.0
        self.elapsed = 0.0

    def update(self):
        self.y += 3.0 * time.dt
        self.elapsed += time.dt
        alpha = max(0.0, 1.0 - (self.elapsed / self.lifetime))
        self.text_entity.alpha = alpha
        if self.elapsed >= self.lifetime:
            destroy(self)

class ParticleBurst(Entity):
    def __init__(self, position, burst_color=color.cyan, count=14):
        super().__init__(position=position)
        self.particles = []
        for _ in range(count):
            p = Entity(
                parent=self,
                model='cube',
                color=burst_color,
                scale=0.15,
                position=(0, 0.5, 0)
            )
            vel = Vec3(
                (random.random() - 0.5) * 8.0,
                (random.random() * 0.8 + 0.2) * 7.0,
                (random.random() - 0.5) * 8.0
            )
            self.particles.append((p, vel))
        self.lifetime = 0.6
        self.elapsed = 0.0

    def update(self):
        self.elapsed += time.dt
        for p, vel in self.particles:
            p.position += vel * time.dt
            p.scale *= max(0.0, 1.0 - 1.8 * time.dt)
        if self.elapsed >= self.lifetime:
            destroy(self)
