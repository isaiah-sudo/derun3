import random
from ursina import Entity, color, Vec3, destroy
from game.config import (
    SEGMENT_LENGTH, SEGMENTS_AHEAD, LANE_POSITIONS, BIOMES
)
from game.obstacles import LaserHurdle, HighBarrier, DroneHazard, PylonHazard
from game.collectibles import Collectible

def destroy_entity_tree(entity):
    if not entity:
        return
    for child in list(entity.children):
        destroy_entity_tree(child)
    destroy(entity)

class TrackSegment(Entity):
    def __init__(self, z_pos=0.0, biome=None, is_safe=False, **kwargs):
        super().__init__(position=(0, 0, z_pos), **kwargs)
        self.biome = biome or BIOMES[0]
        self.is_safe = is_safe
        self.hazards = []
        self.items = []

        self.build_segment()

    def build_segment(self):
        b = self.biome
        road_width = 11.5

        # 1. Main road floor slab (dark cyber asphalt)
        Entity(
            parent=self,
            model='cube',
            color=b['track_color'],
            scale=(road_width, 0.4, SEGMENT_LENGTH),
            position=(0, -0.2, SEGMENT_LENGTH / 2)
        )

        # 2. Glowing Lane Dividers
        for x_line in [-1.7, 1.7]:
            Entity(
                parent=self,
                model='cube',
                color=b['grid_color'],
                scale=(0.12, 0.42, SEGMENT_LENGTH),
                position=(x_line, -0.19, SEGMENT_LENGTH / 2)
            )

        # 3. Glowing Outer Guard Rails
        Entity(
            parent=self,
            model='cube',
            color=b['rail_color'],
            scale=(0.35, 0.6, SEGMENT_LENGTH),
            position=(-road_width / 2, 0.1, SEGMENT_LENGTH / 2)
        )
        Entity(
            parent=self,
            model='cube',
            color=b['rail_color'],
            scale=(0.35, 0.6, SEGMENT_LENGTH),
            position=(road_width / 2, 0.1, SEGMENT_LENGTH / 2)
        )

        # 4. Occasional Neon Archway
        if random.random() < 0.35:
            arch_z = SEGMENT_LENGTH * 0.5
            Entity(parent=self, model='cube', color=b['accent_color'], scale=(0.4, 5.0, 0.4), position=(-5.5, 2.5, arch_z))
            Entity(parent=self, model='cube', color=b['accent_color'], scale=(0.4, 5.0, 0.4), position=(5.5, 2.5, arch_z))
            Entity(parent=self, model='cube', color=b['rail_color'], scale=(11.4, 0.4, 0.4), position=(0, 5.0, arch_z))

        # 5. Background Floating Cyber Skyscrapers (Dark Obsidian monoliths)
        building_dark = color.hex('#0b0914')
        for _ in range(2):
            side = -1 if random.random() < 0.5 else 1
            dist_x = side * random.uniform(18.0, 42.0)
            dist_z = random.uniform(2.0, SEGMENT_LENGTH - 2.0)
            height = random.uniform(25.0, 60.0)
            width = random.uniform(6.0, 12.0)
            building = Entity(
                parent=self,
                model='cube',
                color=building_dark,
                scale=(width, height, width),
                position=(dist_x, height / 2 - 8, dist_z)
            )
            # Glowing neon accent band on skyscraper
            Entity(
                parent=building,
                model='cube',
                color=b['grid_color'],
                scale=(1.02, 0.05, 1.02),
                position=(0, 0.2, 0)
            )

        # Combine all static pieces into 1 single efficient mesh with vertex colors
        self.combine(auto_destroy=True)

        # 6. Spawn Obstacles & Collectibles
        if not self.is_safe:
            self.spawn_content()

    def spawn_content(self):
        b = self.biome
        available_lanes = [0, 1, 2]
        pattern_type = random.random()

        if pattern_type < 0.40:
            hazard_lane = random.choice(available_lanes)
            hz_pos = Vec3(LANE_POSITIONS[hazard_lane], 0, self.z + SEGMENT_LENGTH * 0.5)
            h_type = random.choice(['hurdle', 'high', 'pylon'])
            if h_type == 'hurdle':
                h = LaserHurdle(position=hz_pos)
            elif h_type == 'high':
                h = HighBarrier(position=hz_pos)
            else:
                h = PylonHazard(position=hz_pos)
            self.hazards.append(h)

            for l_idx in available_lanes:
                if l_idx != hazard_lane:
                    for k in range(3):
                        c_pos = Vec3(LANE_POSITIONS[l_idx], 0.7, self.z + SEGMENT_LENGTH * 0.3 + k * 2.5)
                        self.items.append(Collectible(item_type='shard', position=c_pos))

        elif pattern_type < 0.70:
            clear_lane = random.choice(available_lanes)
            blocked_lanes = [l for l in available_lanes if l != clear_lane]
            
            for l_idx in blocked_lanes:
                hz_pos = Vec3(LANE_POSITIONS[l_idx], 0, self.z + SEGMENT_LENGTH * 0.5)
                h_kind = random.choice(['hurdle', 'high'])
                if h_kind == 'hurdle':
                    h = LaserHurdle(position=hz_pos)
                else:
                    h = HighBarrier(position=hz_pos)
                self.hazards.append(h)

            pickup_roll = random.random()
            item_kind = 'shard'
            if pickup_roll < 0.15:
                item_kind = 'shield'
            elif pickup_roll < 0.28:
                item_kind = 'magnet'
            elif pickup_roll < 0.38:
                item_kind = 'boost'
            c_pos = Vec3(LANE_POSITIONS[clear_lane], 0.7, self.z + SEGMENT_LENGTH * 0.5)
            self.items.append(Collectible(item_type=item_kind, position=c_pos))

        elif pattern_type < 0.88:
            drone_pos = Vec3(0, 0, self.z + SEGMENT_LENGTH * 0.5)
            d = DroneHazard(position=drone_pos, speed=random.uniform(2.6, 3.8))
            self.hazards.append(d)
            for l_idx in available_lanes:
                c_pos = Vec3(LANE_POSITIONS[l_idx], 0.7, self.z + SEGMENT_LENGTH * 0.7)
                self.items.append(Collectible(item_type='shard', position=c_pos))

        else:
            for l_idx in available_lanes:
                for k in range(3):
                    c_pos = Vec3(LANE_POSITIONS[l_idx], 0.7, self.z + SEGMENT_LENGTH * 0.2 + k * 3.0)
                    self.items.append(Collectible(item_type='shard', position=c_pos))

    def cleanup(self):
        for h in self.hazards:
            destroy_entity_tree(h)
        for itm in self.items:
            destroy_entity_tree(itm)
        self.hazards.clear()
        self.items.clear()
        destroy(self)


class TrackManager:
    def __init__(self):
        self.segments = []
        self.current_biome_index = 0
        self.next_z = -SEGMENT_LENGTH

        self.sun = Entity(
            model='sphere',
            scale=30.0,
            position=(0, 15, 200),
            color=BIOMES[0]['sun_color']
        )
        self.init_track()

    def get_current_biome(self):
        return BIOMES[self.current_biome_index]

    def init_track(self):
        self.clear()
        self.next_z = -SEGMENT_LENGTH
        for i in range(SEGMENTS_AHEAD):
            is_safe = (i < 4)
            seg = TrackSegment(z_pos=self.next_z, biome=self.get_current_biome(), is_safe=is_safe)
            self.segments.append(seg)
            self.next_z += SEGMENT_LENGTH

    def update_track(self, player_z):
        target_biome = int(player_z / 600) % len(BIOMES)
        if target_biome != self.current_biome_index:
            self.current_biome_index = target_biome
            self.sun.color = self.get_current_biome()['sun_color']

        self.sun.z = player_z + 200

        while self.segments and self.segments[0].z < player_z - SEGMENT_LENGTH * 1.5:
            old_seg = self.segments.pop(0)
            old_seg.cleanup()

            new_seg = TrackSegment(z_pos=self.next_z, biome=self.get_current_biome(), is_safe=False)
            self.segments.append(new_seg)
            self.next_z += SEGMENT_LENGTH

    def get_nearby_hazards(self, player_z, radius=10.0):
        nearby = []
        for seg in self.segments:
            if abs(seg.z + SEGMENT_LENGTH * 0.5 - player_z) < radius + SEGMENT_LENGTH:
                for h in seg.hazards:
                    if h.enabled and h.visible and abs(h.z - player_z) < radius:
                        nearby.append(h)
        return nearby

    def get_nearby_items(self, player_z, radius=16.0):
        nearby = []
        for seg in self.segments:
            if abs(seg.z + SEGMENT_LENGTH * 0.5 - player_z) < radius + SEGMENT_LENGTH:
                for item in seg.items:
                    if item.enabled and item.visible and abs(item.z - player_z) < radius:
                        nearby.append(item)
        return nearby

    def clear(self):
        for seg in self.segments:
            seg.cleanup()
        self.segments.clear()
