"""
Board module - Contains board layout and rendering logic
Complete implementation with all board management functions
"""
import pygame
import math
import copy
from config import *

# Original board layout
# 0 = empty black rectangle, 1 = dot, 2 = big dot (power pellet), 3 = vertical line,
# 4 = horizontal line, 5 = top right, 6 = top left, 7 = bot left, 8 = bot right, 9 = gate
BOARDS = [
    [6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
    [3, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
    [3, 3, 2, 3, 0, 0, 3, 1, 3, 0, 0, 0, 3, 1, 3, 3, 1, 3, 0, 0, 0, 3, 1, 3, 0, 0, 3, 2, 3, 3],
    [3, 3, 1, 7, 4, 4, 8, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 7, 4, 4, 8, 1, 3, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 1, 6, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 6, 4, 4, 5, 1, 3, 3],
    [3, 3, 1, 7, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 4, 4, 8, 1, 3, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 7, 4, 4, 4, 4, 5, 1, 3, 7, 4, 4, 5, 0, 3, 3, 0, 6, 4, 4, 8, 3, 1, 6, 4, 4, 4, 4, 8, 3],
    [3, 0, 0, 0, 0, 0, 3, 1, 3, 6, 4, 4, 8, 0, 7, 8, 0, 7, 4, 4, 5, 3, 1, 3, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
    [8, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 4, 9, 9, 4, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 7],
    [4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 0, 3, 0, 0, 0, 0, 0, 0, 3, 0, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4],
    [5, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 7, 4, 4, 4, 4, 4, 4, 8, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 6],
    [3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 3, 1, 3, 3, 0, 6, 4, 4, 4, 4, 4, 4, 5, 0, 3, 3, 1, 3, 0, 0, 0, 0, 0, 3],
    [3, 6, 4, 4, 4, 4, 8, 1, 7, 8, 0, 7, 4, 4, 5, 6, 4, 4, 8, 0, 7, 8, 1, 7, 4, 4, 4, 4, 5, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 1, 6, 4, 4, 5, 1, 6, 4, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 4, 5, 1, 6, 4, 4, 5, 1, 3, 3],
    [3, 3, 1, 7, 4, 5, 3, 1, 7, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 8, 1, 3, 6, 4, 8, 1, 3, 3],
    [3, 3, 2, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 2, 3, 3],
    [3, 7, 4, 5, 1, 3, 3, 1, 6, 5, 1, 6, 4, 4, 4, 4, 4, 4, 5, 1, 6, 5, 1, 3, 3, 1, 6, 4, 8, 3],
    [3, 6, 4, 8, 1, 7, 8, 1, 3, 3, 1, 7, 4, 4, 5, 6, 4, 4, 8, 1, 3, 3, 1, 7, 8, 1, 7, 4, 5, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 3, 3, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 3, 1, 6, 4, 4, 4, 4, 8, 7, 4, 4, 5, 1, 3, 3, 1, 6, 4, 4, 8, 7, 4, 4, 4, 4, 5, 1, 3, 3],
    [3, 3, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 7, 8, 1, 7, 4, 4, 4, 4, 4, 4, 4, 4, 8, 1, 3, 3],
    [3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3],
    [3, 7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 3],
    [7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8]
]


class Board:
    """Manages the game board and rendering"""
    
    def __init__(self):
        self.level = None
        self.original_board = copy.deepcopy(BOARDS)
        self.reset()
        
    def reset(self):
        """Reset board to initial state"""
        self.level = copy.deepcopy(self.original_board)
        
    def draw(self, screen, flicker, color=BLUE):
        """Draw the board on screen with all maze elements"""
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                x = j * TILE_WIDTH + (0.5 * TILE_WIDTH)
                y = i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)
                
                if self.level[i][j] == TILE_DOT:
                    # Draw small dot
                    pygame.draw.circle(screen, WHITE, (int(x), int(y)), 4)
                    
                elif self.level[i][j] == TILE_POWER_PELLET and not flicker:
                    # Draw power pellet (flickers)
                    pygame.draw.circle(screen, WHITE, (int(x), int(y)), 10)
                    
                elif self.level[i][j] == TILE_VERTICAL:
                    # Draw vertical wall
                    pygame.draw.line(screen, color, (int(x), int(i * TILE_HEIGHT)),
                                   (int(x), int(i * TILE_HEIGHT + TILE_HEIGHT)), 3)
                    
                elif self.level[i][j] == TILE_HORIZONTAL:
                    # Draw horizontal wall
                    pygame.draw.line(screen, color, (int(j * TILE_WIDTH), int(y)),
                                   (int(j * TILE_WIDTH + TILE_WIDTH), int(y)), 3)
                    
                elif self.level[i][j] == TILE_TOP_RIGHT:
                    # Draw top-right corner
                    pygame.draw.arc(screen, color, 
                                  [int(j * TILE_WIDTH - (TILE_WIDTH * 0.4) - 2), int(y), 
                                   int(TILE_WIDTH), int(TILE_HEIGHT)],
                                  0, math.pi / 2, 3)
                    
                elif self.level[i][j] == TILE_TOP_LEFT:
                    # Draw top-left corner
                    pygame.draw.arc(screen, color,
                                  [int(j * TILE_WIDTH + (TILE_WIDTH * 0.5)), int(y), 
                                   int(TILE_WIDTH), int(TILE_HEIGHT)],
                                  math.pi / 2, math.pi, 3)
                    
                elif self.level[i][j] == TILE_BOTTOM_LEFT:
                    # Draw bottom-left corner
                    pygame.draw.arc(screen, color, 
                                  [int(j * TILE_WIDTH + (TILE_WIDTH * 0.5)), 
                                   int(i * TILE_HEIGHT - (0.4 * TILE_HEIGHT)), 
                                   int(TILE_WIDTH), int(TILE_HEIGHT)],
                                  math.pi, 3 * math.pi / 2, 3)
                    
                elif self.level[i][j] == TILE_BOTTOM_RIGHT:
                    # Draw bottom-right corner
                    pygame.draw.arc(screen, color,
                                  [int(j * TILE_WIDTH - (TILE_WIDTH * 0.4) - 2), 
                                   int(i * TILE_HEIGHT - (0.4 * TILE_HEIGHT)), 
                                   int(TILE_WIDTH), int(TILE_HEIGHT)],
                                  3 * math.pi / 2, 2 * math.pi, 3)
                    
                elif self.level[i][j] == TILE_GATE:
                    # Draw gate (for ghost house)
                    pygame.draw.line(screen, WHITE, (int(j * TILE_WIDTH), int(y)),
                                   (int(j * TILE_WIDTH + TILE_WIDTH), int(y)), 3)
    
    def is_walkable(self, row, col):
        """Check if a position is walkable (not a wall)"""
        if row < 0 or row >= len(self.level) or col < 0 or col >= len(self.level[0]):
            return False
        tile = self.level[row][col]
        # Walkable if: empty, dot, power pellet, or gate
        return tile < 3 or tile == TILE_GATE
    
    def get_tile(self, row, col):
        """Get tile type at position"""
        if row < 0 or row >= len(self.level) or col < 0 or col >= len(self.level[0]):
            return -1
        return self.level[row][col]
    
    def set_tile(self, row, col, value):
        """Set tile type at position"""
        if 0 <= row < len(self.level) and 0 <= col < len(self.level[0]):
            self.level[row][col] = value
    
    def is_complete(self):
        """Check if all dots and power pellets are collected"""
        for row in self.level:
            if TILE_DOT in row or TILE_POWER_PELLET in row:
                return False
        return True
    
    def get_all_dots(self):
        """Get positions of all dots and power pellets"""
        dots = []
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.level[i][j] in [TILE_DOT, TILE_POWER_PELLET]:
                    dots.append((i, j))
        return dots
    
    def get_random_walkable_position(self):
        """Get a random walkable position for goal setting"""
        import random
        walkable_positions = []
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                if self.is_walkable(i, j) and not (350 < j * TILE_WIDTH < 550 and 370 < i * TILE_HEIGHT < 480):
                    walkable_positions.append((i, j))
        if walkable_positions:
            return random.choice(walkable_positions)
        return (15, 15)  # Default fallback
