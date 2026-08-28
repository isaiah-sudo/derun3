# Game configuration, constants, and palettes
from ursina import color, Vec3, Vec4

WINDOW_TITLE = 'CYBERSURGE 3D // SYNTHWAVE RUNNER'
TARGET_FPS = 60

# Track and Gameplay Constants
LANE_WIDTH = 3.4
NUM_LANES = 3  # -1 (Left), 0 (Center), 1 (Right)
LANE_POSITIONS = [-LANE_WIDTH, 0, LANE_WIDTH]

SEGMENT_LENGTH = 24
SEGMENTS_AHEAD = 14
SEGMENT_TOTAL = SEGMENTS_AHEAD + 3

INITIAL_SPEED = 34.0
MAX_SPEED = 85.0
SPEED_ACCELERATION = 0.55
BOOST_SPEED_MULTIPLIER = 1.6
BOOST_DURATION = 5.0
MAGNET_DURATION = 8.0
SHIELD_DURATION = 15.0

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

# Ship Skins
SHIP_SKINS = [
    {'name': 'NEON BLADE', 'primary': color.cyan, 'secondary': color.magenta, 'trail': color.cyan},
    {'name': 'SOLAR PHANTOM', 'primary': color.orange, 'secondary': color.yellow, 'trail': color.orange},
    {'name': 'TOXIC VIPER', 'primary': color.lime, 'secondary': color.azure, 'trail': color.lime},
    {'name': 'DARK MATTER', 'primary': color.violet, 'secondary': color.red, 'trail': color.violet},
]
