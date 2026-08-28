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
        'bg_color': color.rgb(8, 6, 16),
        'bg_clear': Vec4(0.03, 0.02, 0.06, 1.0),
        'track_color': color.rgb(18, 16, 28),
        'grid_color': color.cyan,
        'rail_color': color.magenta,
        'accent_color': color.cyan,
        'sun_color': color.rgb(255, 60, 160),
    },
    {
        'name': 'SOLAR FLARE',
        'bg_color': color.rgb(18, 8, 5),
        'bg_clear': Vec4(0.07, 0.03, 0.02, 1.0),
        'track_color': color.rgb(26, 16, 16),
        'grid_color': color.orange,
        'rail_color': color.yellow,
        'accent_color': color.orange,
        'sun_color': color.rgb(255, 180, 40),
    },
    {
        'name': 'CYBER TOXIC',
        'bg_color': color.rgb(5, 16, 10),
        'bg_clear': Vec4(0.02, 0.06, 0.04, 1.0),
        'track_color': color.rgb(14, 24, 18),
        'grid_color': color.lime,
        'rail_color': color.green,
        'accent_color': color.lime,
        'sun_color': color.rgb(50, 255, 140),
    },
    {
        'name': 'DEEP VOID',
        'bg_color': color.rgb(6, 6, 14),
        'bg_clear': Vec4(0.02, 0.02, 0.05, 1.0),
        'track_color': color.rgb(16, 14, 26),
        'grid_color': color.violet,
        'rail_color': color.azure,
        'accent_color': color.violet,
        'sun_color': color.rgb(190, 60, 255),
    }
]

# Ship Skins
SHIP_SKINS = [
    {'name': 'NEON BLADE', 'primary': color.cyan, 'secondary': color.magenta, 'trail': color.cyan},
    {'name': 'SOLAR PHANTOM', 'primary': color.orange, 'secondary': color.yellow, 'trail': color.orange},
    {'name': 'TOXIC VIPER', 'primary': color.lime, 'secondary': color.azure, 'trail': color.lime},
    {'name': 'DARK MATTER', 'primary': color.violet, 'secondary': color.red, 'trail': color.violet},
]
