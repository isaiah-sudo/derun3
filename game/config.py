# Game configuration, constants, and palettes
from ursina import color, Vec3, Vec4

WINDOW_TITLE = 'CYBERSURGE 3D // SYNTHWAVE RUNNER'
TARGET_FPS = 60

# Track and Gameplay Constants
LANE_WIDTH = 3.4
NUM_LANES = 3  # -1 (Left), 0 (Center), 1 (Right)
LANE_POSITIONS = [-LANE_WIDTH, 0, LANE_WIDTH]

SEGMENT_LENGTH = 24
SEGMENTS_AHEAD = 10
SEGMENT_TOTAL = SEGMENTS_AHEAD + 3
MAX_DELTA_TIME = 0.05

# Game Modes
MODE_CLASSIC = 0
MODE_OVERDRIVE = 1

GAME_MODES = [
    {
        'name': 'CLASSIC',
        'tag': 'CRUISE',
        'initial_speed': 34.0,
        'max_speed': 85.0,
        'speed_acceleration': 0.55,
        'boost_multiplier': 1.6,
        'boost_duration': 5.0,
        'magnet_duration': 8.0,
        'shield_duration': 15.0,
        'max_combo': 8,
        'stacking_powerups': False,
        'description': 'Balanced speed acceleration and standard powerup timers.'
    },
    {
        'name': 'OVERDRIVE',
        'tag': 'HYPER-SURGE',
        'initial_speed': 42.0,
        'max_speed': 175.0,
        'speed_acceleration': 2.40,
        'boost_multiplier': 1.75,
        'boost_duration': 5.5,
        'magnet_duration': 9.0,
        'shield_duration': 16.0,
        'max_combo': 32,
        'stacking_powerups': True,
        'description': 'Ultra-fast speed growth! Powerups stack in count, duration, and power!'
    }
]

# Player Movement
JUMP_FORCE = 15.0
GRAVITY = 36.0
SLIDE_DURATION = 0.55
LANE_LERP_SPEED = 18.0

# Scoring
POINTS_PER_METER = 2
COIN_POINTS = 50
COMBO_TIMEOUT = 3.5

# Visual Themes (Dark Cyberpunk Biomes)
BIOMES = [
    {
        'name': 'NEON METROPOLIS',
        'bg_color': color.hex('#07050e'),
        'bg_clear': Vec4(0.027, 0.02, 0.055, 1.0),
        'track_color': color.hex('#120f1e'),
        'grid_color': color.cyan,
        'rail_color': color.magenta,
        'accent_color': color.cyan,
        'sun_color': color.hex('#ff32a0'),
    },
    {
        'name': 'SOLAR FLARE',
        'bg_color': color.hex('#0e0503'),
        'bg_clear': Vec4(0.055, 0.02, 0.012, 1.0),
        'track_color': color.hex('#1a0f0d'),
        'grid_color': color.orange,
        'rail_color': color.yellow,
        'accent_color': color.orange,
        'sun_color': color.hex('#ffb428'),
    },
    {
        'name': 'CYBER TOXIC',
        'bg_color': color.hex('#030c07'),
        'bg_clear': Vec4(0.012, 0.047, 0.027, 1.0),
        'track_color': color.hex('#0a1610'),
        'grid_color': color.lime,
        'rail_color': color.green,
        'accent_color': color.lime,
        'sun_color': color.hex('#32ff8c'),
    },
    {
        'name': 'DEEP VOID',
        'bg_color': color.hex('#04040a'),
        'bg_clear': Vec4(0.016, 0.016, 0.039, 1.0),
        'track_color': color.hex('#0d0c18'),
        'grid_color': color.violet,
        'rail_color': color.azure,
        'accent_color': color.violet,
        'sun_color': color.hex('#be3cff'),
    }
]

# Ship Skins - 8 Unique Cyber Vessels
SHIP_SKINS = [
    {'name': 'NEON BLADE', 'primary': color.cyan, 'secondary': color.magenta, 'trail': color.cyan},
    {'name': 'SOLAR PHANTOM', 'primary': color.orange, 'secondary': color.yellow, 'trail': color.orange},
    {'name': 'TOXIC VIPER', 'primary': color.lime, 'secondary': color.azure, 'trail': color.lime},
    {'name': 'DARK MATTER', 'primary': color.violet, 'secondary': color.red, 'trail': color.violet},
    {'name': 'HYPERION PHOENIX', 'primary': color.hex('#ff2a2a'), 'secondary': color.hex('#ffd700'), 'trail': color.hex('#ff5500')},
    {'name': 'VOID SPECTRE', 'primary': color.hex('#00ffea'), 'secondary': color.hex('#202028'), 'trail': color.hex('#00ffee')},
    {'name': 'GLITCH RUNNER', 'primary': color.hex('#ff007f'), 'secondary': color.white, 'trail': color.hex('#ff00aa')},
    {'name': 'QUANTUM PULSE', 'primary': color.hex('#00ffa2'), 'secondary': color.hex('#9400d3'), 'trail': color.hex('#7df9ff')},
]

# Laser Combat, Ammo & Ramp Mechanics
LASER_COOLDOWN = 0.28
LASER_SPEED = 140.0
INITIAL_AMMO = 0
AMMO_PICKUP_AMOUNT = 5
MAX_AMMO = 99
RAMP_LAUNCH_FORCE = 24.0
SPEED_PAD_BOOST_TIME = 2.0

# Achievements / Missions
ACHIEVEMENTS = [
    {'id': 'speed_100', 'name': 'SPEED DEMON', 'desc': 'Exceed 100 KM/H in any run', 'target': 100},
    {'id': 'shards_50', 'name': 'SHARD HOARDER', 'desc': 'Collect 50 energy shards in one run', 'target': 50},
    {'id': 'destructions_15', 'name': 'ANNIHILATOR', 'desc': 'Destroy 15 hazards with Laser Cannons', 'target': 15},
    {'id': 'combo_8', 'name': 'COMBO MASTER', 'desc': 'Attain an 8x combo multiplier', 'target': 8},
    {'id': 'ramps_5', 'name': 'AERIAL ACE', 'desc': 'Hit 5 neon jump ramps in one run', 'target': 5},
]
