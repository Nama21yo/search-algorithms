"""
Board module - Contains board layout and rendering logic
"""
import pygame
import math
from config import *

# Original board layout
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
        self.reset()
        
    def reset(self):
        """Reset board to initial state"""
        self.level = [row[:] for row in BOARDS]
        
    def draw(self, screen, flicker, color=BLUE):
        """Draw the board on screen"""
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                x = j * TILE_WIDTH + (0.5 * TILE_WIDTH)
                y = i * TILE_HEIGHT + (0.5 * TILE_HEIGHT)
                
                if self.level[i][j] == TILE_DOT:
                    pygame.draw.circle(screen, WHITE, (x, y), 4)
                    
                elif self.level[i][j] == TILE_POWER_PELLET and not flicker:
                    pygame.draw.circle(screen, WHITE, (x, y), 10)
                    
                elif self.level[i][j] == TILE_VERTICAL:
                    pygame.draw.line(screen, color, (x, i * TILE_HEIGHT),
                                   (x, i * TILE_HEIGHT + TILE_HEIGHT), 3)
                    
                elif self.level[i][j] == TILE_HORIZONTAL:
                    pygame.draw.line(screen, color, (j * TILE_WIDTH, y),
                                   (j * TILE_WIDTH + TILE_WIDTH, y), 3)
                    
                elif self.level[i][j] == TILE_TOP_RIGHT:
                    pygame.draw.arc(screen, color, 
                                  [(j * TILE_WIDTH - (TILE_WIDTH * 0.4)) - 2, y, 
                                   TILE_WIDTH, TILE_HEIGHT],
                                  0, math.pi / 2, 3)
                    
                elif self.level[i][j] == TILE_TOP_LEFT:
                    pygame.draw.arc(screen, color,
                                  [(j * TILE_WIDTH + (TILE_WIDTH * 0.5)), y, 
                                   TILE_WIDTH, TILE_HEIGHT],
                                  math.pi / 2, math.pi, 3)
                    
                elif self.level[i][j] == TILE_BOTTOM_LEFT:
                    pygame.draw.arc(screen, color, 
                                  [(j * TILE_WIDTH + (TILE_WIDTH * 0.5)), 
                                   i * TILE_HEIGHT - (0.4 * TILE_HEIGHT), 
                                   TILE_WIDTH, TILE_HEIGHT],
                                  math.pi, 3 * math.pi / 2, 3)
                    
                elif self.level[i][j] == TILE_BOTTOM_RIGHT:
                    pygame.draw.arc(screen, color,
                                  [(j * TILE_WIDTH - (TILE_WIDTH * 0.4)) - 2, 
                                   i * TILE_HEIGHT - (0.4 * TILE_HEIGHT), 
                                   TILE_WIDTH, TILE_HEIGHT],
                                  3 * math.pi / 2, 2 * math.pi, 3)
                    
                elif self.level[i][j] == TILE_GATE:
                    pygame.draw.line(screen, WHITE, (j * TILE_WIDTH, y),
                                   (j * TILE_WIDTH + TILE_WIDTH, y), 3)
    
    def is_walkable(self, row, col):
        """Check if a position is walkable (not a wall)"""
        if row < 0 or row >= len(self.level) or col < 0 or col >= len(self.level[0]):
            return False
        return self.level[row][col] < 3 or self.level[row][col] == TILE_GATE
    
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
