import random
import math
import time
from ursina import Entity, color, Vec3, destroy
from ursina import time as ursina_time

class Collectible(Entity):
    def __init__(self, item_type='shard', position=(0, 0, 0), **kwargs):
        super().__init__(position=position, **kwargs)
        self.item_type = item_type
        self.hover_offset = random.random() * 6.28
        self.base_y = position[1]

        if item_type == 'shard':
            self.model = 'diamond'
            self.color = color.cyan
            self.scale = (0.7, 1.1, 0.7)
            self.core = Entity(parent=self, model='sphere', color=color.white, scale=0.4)
        elif item_type == 'shield':
            self.model = 'sphere'
            self.color = color.azure
            self.scale = 0.85
            self.ring = Entity(parent=self, model='quad', color=color.cyan, scale=1.4, double_sided=True)
            self.ring.rotation_x = 90
        elif item_type == 'magnet':
            self.model = 'cube'
            self.color = color.yellow
            self.scale = 0.8
            self.core = Entity(parent=self, model='sphere', color=color.red, scale=0.5)
        elif item_type == 'boost':
            self.model = 'cube'
            self.color = color.orange
            self.scale = (0.6, 1.2, 0.6)
            self.core = Entity(parent=self, model='sphere', color=color.yellow, scale=0.7)
        elif item_type == 'emp':
            self.model = 'sphere'
            self.color = color.hex('#ff00aa')
            self.scale = 1.1
            self.ring = Entity(parent=self, model='quad', color=color.hex('#00ffee'), scale=1.8, double_sided=True)
            self.ring.rotation_x = 90
            self.core = Entity(parent=self, model='sphere', color=color.white, scale=0.5)
        elif item_type == 'ammo':
            self.model = 'cube'
            self.color = color.hex('#00ffee')
            self.scale = (0.5, 0.9, 0.5)
            self.core = Entity(parent=self, model='cube', color=color.hex('#ff0055'), scale=(0.7, 0.3, 0.7), position=(0, 0, 0))

    def update(self):
        dt = min(ursina_time.dt, 0.05)
        self.rotation_y += 180.0 * dt
        self.y = self.base_y + 0.2 * math.sin(time.time() * 4.0 + self.hover_offset)
