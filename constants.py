# CONSTANTS

from imports import *

# Set sprite size
NATIVE_SPRITE_SIZE = 128
SPRITE_SCALING = 0.25
SPRITE_SIZE = int(NATIVE_SPRITE_SIZE * SPRITE_SCALING)

# Set window size
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
WINDOW_TITLE = "MINUTE MAZES"

# Set movement speed
MOVEMENT_SPEED = 6

# Set camera speed
CAMERA_SPEED = 1

# Set tile types
    # Epmty tile = walkable
    # Crate tile = wall
TILE_EMPTY = 0
TILE_CRATE = 1

# Maze must have an ODD number of rows and columns
    # Walls go on EVEN rows/columns.
    # Openings go on ODD rows/columns
MAZE_HEIGHT = 51
MAZE_WIDTH = 51

# Merge sprites = True
    # If True, we merge sprites into one sprite, with a repeating texture for each cell
    # This reduces our sprite count
MERGE_SPRITES = True