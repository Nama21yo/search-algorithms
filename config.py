"""
Configuration file for Pac-Man AI Game
Contains all game constants and settings
"""

# Screen dimensions
WIDTH = 900
HEIGHT = 950
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

# Game settings
PLAYER_SPEED = 2
GHOST_SPEED = 2
GHOST_SPEED_SCARED = 1
GHOST_SPEED_DEAD = 4

# Scoring
SCORE_DOT = 10
SCORE_POWER_PELLET = 50
SCORE_GHOST_BASE = 200

# Power-up duration (frames)
POWERUP_DURATION = 600
STARTUP_DURATION = 180

# Grid dimensions
TILE_HEIGHT = (HEIGHT - 50) // 32
TILE_WIDTH = WIDTH // 30

# Initial positions
PLAYER_START_X = 450
PLAYER_START_Y = 663

BLINKY_START_X = 56
BLINKY_START_Y = 58

INKY_START_X = 440
INKY_START_Y = 388

PINKY_START_X = 440
PINKY_START_Y = 438

CLYDE_START_X = 440
CLYDE_START_Y = 438

# Board tile types
TILE_EMPTY = 0
TILE_DOT = 1
TILE_POWER_PELLET = 2
TILE_VERTICAL = 3
TILE_HORIZONTAL = 4
TILE_TOP_RIGHT = 5
TILE_TOP_LEFT = 6
TILE_BOTTOM_LEFT = 7
TILE_BOTTOM_RIGHT = 8
TILE_GATE = 9

# Directions
DIR_RIGHT = 0
DIR_LEFT = 1
DIR_UP = 2
DIR_DOWN = 3

# AI Algorithm modes
MODE_MANUAL = 0
MODE_BFS = 1
MODE_DFS = 2
MODE_UCS = 3
MODE_ASTAR = 4
MODE_MINIMAX = 5

# Algorithm names for display
ALGORITHM_NAMES = {
    MODE_MANUAL: "Manual Control",
    MODE_BFS: "Breadth-First Search",
    MODE_DFS: "Depth-First Search",
    MODE_UCS: "Uniform Cost Search",
    MODE_ASTAR: "A* Search",
    MODE_MINIMAX: "Minimax (Alpha-Beta)"
}

# Minimax settings
MINIMAX_DEPTH = 3
ALPHABETA_DEPTH = 4
