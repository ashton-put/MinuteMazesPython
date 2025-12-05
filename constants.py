# CONSTANTS

# Sprite configuration
NATIVE_SPRITE_SIZE = 128
SPRITE_SCALING = 0.25
SPRITE_SIZE = int(NATIVE_SPRITE_SIZE * SPRITE_SCALING)

# Window configuration
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_TITLE = "MINUTE MAZES"

# Player configuration
MOVEMENT_SPEED = 5
DIAGONAL_MOVEMENT_FACTOR = 0.7071  # 1/sqrt(2) for normalized diagonal movement

# Camera configuration
CAMERA_SPEED = 0.2
CAMERA_ZOOM = 2.0

# Audio configuration
MUSIC_VOLUME_MULTIPLIER = 0.3
SOUND_VOLUME_MULTIPLIER = 0.3

# Timing configuration
CONGRATULATIONS_DELAY = 10.0

# Tile types
TILE_EMPTY = 0
TILE_CRATE = 1

# Sprite optimization
MERGE_SPRITES = True

# Pathfinder configuration
PATHFINDER_MAX_USES = 3
PATHFINDER_DURATION = 3.0
PATHFINDER_MAX_TILES = 10

# Story mode configuration
STORY_MODE_MAZE_SEQUENCE = [
    21, 21, 21,  # 3 small mazes
    31, 31, 31, 31,  # 4 medium mazes
    51, 51, 51  # 3 large mazes
]
STORY_MODE_TOTAL_MAZES = 10

# Game settings (mutable - can be changed by user)
MAZE_SIZE_SETTING = 21  # Options: 21 (Small), 31 (Medium), 51 (Large)
MOUSE_COLOR_SETTING = "white"  # Options: "white", "grey", "brown"
VOLUME_SETTING = 0.5  # Range: 0.0 to 1.0

# UI configuration
UI_BUTTON_WIDTH_LARGE = 250
UI_BUTTON_WIDTH_SMALL = 150
UI_BUTTON_WIDTH_TINY = 75
UI_BUTTON_HEIGHT_LARGE = 50
UI_BUTTON_HEIGHT_MEDIUM = 45
UI_BUTTON_HEIGHT_SMALL = 40
UI_SPACING_LARGE = 30
UI_SPACING_MEDIUM = 20
UI_SPACING_SMALL = 15
UI_SPACING_TINY = 10