"""
Entity classes for Player and Ghosts
"""
import pygame
from config import *


class Player:
    """Player (Pac-Man) class"""
    
    def __init__(self, x, y, images):
        self.x = x
        self.y = y
        self.images = images
        self.direction = DIR_RIGHT
        self.direction_command = DIR_RIGHT
        self.speed = PLAYER_SPEED
        self.animation_counter = 0
        
    def reset(self, x=None, y=None):
        """Reset player to starting position"""
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.direction = DIR_RIGHT
        self.direction_command = DIR_RIGHT
        
    def get_center(self):
        """Get center position of player"""
        return (self.x + 23, self.y + 24)
    
    def get_grid_position(self):
        """Get grid position of player"""
        center_x, center_y = self.get_center()
        return (center_y // TILE_HEIGHT, center_x // TILE_WIDTH)
    
    def check_position(self, board):
        """Check which directions player can turn"""
        center_x, center_y = self.get_center()
        turns = [False, False, False, False]  # R, L, U, D
        num3 = 15
        
        if center_x // 30 < 29:
            # Check each direction
            if self.direction == DIR_RIGHT:
                if board.get_tile(center_y // TILE_HEIGHT, 
                                 (center_x - num3) // TILE_WIDTH) < 3:
                    turns[DIR_LEFT] = True
            if self.direction == DIR_LEFT:
                if board.get_tile(center_y // TILE_HEIGHT, 
                                 (center_x + num3) // TILE_WIDTH) < 3:
                    turns[DIR_RIGHT] = True
            if self.direction == DIR_UP:
                if board.get_tile((center_y + num3) // TILE_HEIGHT, 
                                 center_x // TILE_WIDTH) < 3:
                    turns[DIR_DOWN] = True
            if self.direction == DIR_DOWN:
                if board.get_tile((center_y - num3) // TILE_HEIGHT, 
                                 center_x // TILE_WIDTH) < 3:
                    turns[DIR_UP] = True
            
            # Additional turning checks based on alignment
            if self.direction in [DIR_UP, DIR_DOWN]:
                if 12 <= center_x % TILE_WIDTH <= 18:
                    if board.get_tile((center_y + num3) // TILE_HEIGHT, 
                                     center_x // TILE_WIDTH) < 3:
                        turns[DIR_DOWN] = True
                    if board.get_tile((center_y - num3) // TILE_HEIGHT, 
                                     center_x // TILE_WIDTH) < 3:
                        turns[DIR_UP] = True
                if 12 <= center_y % TILE_HEIGHT <= 18:
                    if board.get_tile(center_y // TILE_HEIGHT, 
                                     (center_x - TILE_WIDTH) // TILE_WIDTH) < 3:
                        turns[DIR_LEFT] = True
                    if board.get_tile(center_y // TILE_HEIGHT, 
                                     (center_x + TILE_WIDTH) // TILE_WIDTH) < 3:
                        turns[DIR_RIGHT] = True
            
            if self.direction in [DIR_RIGHT, DIR_LEFT]:
                if 12 <= center_x % TILE_WIDTH <= 18:
                    if board.get_tile((center_y + TILE_HEIGHT) // TILE_HEIGHT, 
                                     center_x // TILE_WIDTH) < 3:
                        turns[DIR_DOWN] = True
                    if board.get_tile((center_y - TILE_HEIGHT) // TILE_HEIGHT, 
                                     center_x // TILE_WIDTH) < 3:
                        turns[DIR_UP] = True
                if 12 <= center_y % TILE_HEIGHT <= 18:
                    if board.get_tile(center_y // TILE_HEIGHT, 
                                     (center_x - num3) // TILE_WIDTH) < 3:
                        turns[DIR_LEFT] = True
                    if board.get_tile(center_y // TILE_HEIGHT, 
                                     (center_x + num3) // TILE_WIDTH) < 3:
                        turns[DIR_RIGHT] = True
        else:
            turns[DIR_RIGHT] = True
            turns[DIR_LEFT] = True
        
        return turns
    
    def move(self, turns_allowed):
        """Move player based on direction and allowed turns"""
        if self.direction == DIR_RIGHT and turns_allowed[DIR_RIGHT]:
            self.x += self.speed
        elif self.direction == DIR_LEFT and turns_allowed[DIR_LEFT]:
            self.x -= self.speed
        if self.direction == DIR_UP and turns_allowed[DIR_UP]:
            self.y -= self.speed
        elif self.direction == DIR_DOWN and turns_allowed[DIR_DOWN]:
            self.y += self.speed
        
        # Handle wrap-around
        if self.x > 900:
            self.x = -47
        elif self.x < -50:
            self.x = 897
    
    def draw(self, screen):
        """Draw player on screen"""
        image_index = (self.animation_counter // 5) % len(self.images)
        
        if self.direction == DIR_RIGHT:
            screen.blit(self.images[image_index], (self.x, self.y))
        elif self.direction == DIR_LEFT:
            screen.blit(pygame.transform.flip(self.images[image_index], True, False), 
                       (self.x, self.y))
        elif self.direction == DIR_UP:
            screen.blit(pygame.transform.rotate(self.images[image_index], 90), 
                       (self.x, self.y))
        elif self.direction == DIR_DOWN:
            screen.blit(pygame.transform.rotate(self.images[image_index], 270), 
                       (self.x, self.y))


class Ghost:
    """Ghost enemy class"""
    
    def __init__(self, x, y, target, speed, img, direction, ghost_id, name):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.target = target
        self.speed = speed
        self.img = img
        self.direction = direction
        self.ghost_id = ghost_id
        self.name = name
        self.dead = False
        self.in_box = False
        self.turns = [False, False, False, False]
        
    def reset(self):
        """Reset ghost to starting position"""
        self.x = self.start_x
        self.y = self.start_y
        self.dead = False
        self.in_box = False
        
    def get_center(self):
        """Get center position"""
        return (self.x + 22, self.y + 22)
    
    def get_grid_position(self):
        """Get grid position"""
        center_x, center_y = self.get_center()
        return (center_y // TILE_HEIGHT, center_x // TILE_WIDTH)
    
    def check_collisions(self, board):
        """Check available turns for ghost"""
        center_x, center_y = self.get_center()
        num3 = 15
        self.turns = [False, False, False, False]
        
        if 0 < center_x // 30 < 29:
            # Check gate passage
            if board.get_tile((center_y - num3) // TILE_HEIGHT, 
                            center_x // TILE_WIDTH) == TILE_GATE:
                self.turns[DIR_UP] = True
            
            # Check basic movements
            if (board.get_tile(center_y // TILE_HEIGHT, 
                             (center_x - num3) // TILE_WIDTH) < 3 or
                (board.get_tile(center_y // TILE_HEIGHT, 
                              (center_x - num3) // TILE_WIDTH) == TILE_GATE and 
                 (self.in_box or self.dead))):
                self.turns[DIR_LEFT] = True
                
            if (board.get_tile(center_y // TILE_HEIGHT, 
                             (center_x + num3) // TILE_WIDTH) < 3 or
                (board.get_tile(center_y // TILE_HEIGHT, 
                              (center_x + num3) // TILE_WIDTH) == TILE_GATE and 
                 (self.in_box or self.dead))):
                self.turns[DIR_RIGHT] = True
                
            if (board.get_tile((center_y + num3) // TILE_HEIGHT, 
                             center_x // TILE_WIDTH) < 3 or
                (board.get_tile((center_y + num3) // TILE_HEIGHT, 
                              center_x // TILE_WIDTH) == TILE_GATE and 
                 (self.in_box or self.dead))):
                self.turns[DIR_DOWN] = True
                
            if (board.get_tile((center_y - num3) // TILE_HEIGHT, 
                             center_x // TILE_WIDTH) < 3 or
                (board.get_tile((center_y - num3) // TILE_HEIGHT, 
                              center_x // TILE_WIDTH) == TILE_GATE and 
                 (self.in_box or self.dead))):
                self.turns[DIR_UP] = True
            
            # Additional alignment checks
            if self.direction in [DIR_UP, DIR_DOWN]:
                if 12 <= center_x % TILE_WIDTH <= 18:
                    if (board.get_tile((center_y + num3) // TILE_HEIGHT, 
                                     center_x // TILE_WIDTH) < 3 or
                        (board.get_tile((center_y + num3) // TILE_HEIGHT, 
                                      center_x // TILE_WIDTH) == TILE_GATE and 
                         (self.in_box or self.dead))):
                        self.turns[DIR_DOWN] = True
                    if (board.get_tile((center_y - num3) // TILE_HEIGHT, 
                                     center_x // TILE_WIDTH) < 3 or
                        (board.get_tile((center_y - num3) // TILE_HEIGHT, 
                                      center_x // TILE_WIDTH) == TILE_GATE and 
                         (self.in_box or self.dead))):
                        self.turns[DIR_UP] = True
                        
            if self.direction in [DIR_RIGHT, DIR_LEFT]:
                if 12 <= center_x % TILE_WIDTH <= 18:
                    if (board.get_tile((center_y + num3) // TILE_HEIGHT, 
                                     center_x // TILE_WIDTH) < 3 or
                        (board.get_tile((center_y + num3) // TILE_HEIGHT, 
                                      center_x // TILE_WIDTH) == TILE_GATE and 
                         (self.in_box or self.dead))):
                        self.turns[DIR_DOWN] = True
                    if (board.get_tile((center_y - num3) // TILE_HEIGHT, 
                                     center_x // TILE_WIDTH) < 3 or
                        (board.get_tile((center_y - num3) // TILE_HEIGHT, 
                                      center_x // TILE_WIDTH) == TILE_GATE and 
                         (self.in_box or self.dead))):
                        self.turns[DIR_UP] = True
                if 12 <= center_y % TILE_HEIGHT <= 18:
                    if (board.get_tile(center_y // TILE_HEIGHT, 
                                     (center_x - num3) // TILE_WIDTH) < 3 or
                        (board.get_tile(center_y // TILE_HEIGHT, 
                                      (center_x - num3) // TILE_WIDTH) == TILE_GATE and 
                         (self.in_box or self.dead))):
                        self.turns[DIR_LEFT] = True
                    if (board.get_tile(center_y // TILE_HEIGHT, 
                                     (center_x + num3) // TILE_WIDTH) < 3 or
                        (board.get_tile(center_y // TILE_HEIGHT, 
                                      (center_x + num3) // TILE_WIDTH) == TILE_GATE and 
                         (self.in_box or self.dead))):
                        self.turns[DIR_RIGHT] = True
        else:
            self.turns[DIR_RIGHT] = True
            self.turns[DIR_LEFT] = True
        
        # Check if in box
        if 350 < self.x < 550 and 370 < self.y < 480:
            self.in_box = True
        else:
            self.in_box = False
        
        return self.turns
    
    def move_towards_target(self):
        """Basic ghost movement towards target"""
        # Aggressive pursuit behavior
        if self.direction == DIR_RIGHT:
            if self.target[0] > self.x and self.turns[DIR_RIGHT]:
                self.x += self.speed
            elif not self.turns[DIR_RIGHT]:
                self._choose_new_direction()
            elif self.turns[DIR_RIGHT]:
                self.x += self.speed
                
        elif self.direction == DIR_LEFT:
            if self.target[0] < self.x and self.turns[DIR_LEFT]:
                self.x -= self.speed
            elif not self.turns[DIR_LEFT]:
                self._choose_new_direction()
            elif self.turns[DIR_LEFT]:
                self.x -= self.speed
                
        elif self.direction == DIR_UP:
            if self.target[1] < self.y and self.turns[DIR_UP]:
                self.y -= self.speed
            elif not self.turns[DIR_UP]:
                self._choose_new_direction()
            elif self.turns[DIR_UP]:
                self.y -= self.speed
                
        elif self.direction == DIR_DOWN:
            if self.target[1] > self.y and self.turns[DIR_DOWN]:
                self.y += self.speed
            elif not self.turns[DIR_DOWN]:
                self._choose_new_direction()
            elif self.turns[DIR_DOWN]:
                self.y += self.speed
        
        # Wrap around
        if self.x < -30:
            self.x = 900
        elif self.x > 900:
            self.x = -30
    
    def _choose_new_direction(self):
        """Choose new direction when blocked"""
        if self.target[1] > self.y and self.turns[DIR_DOWN]:
            self.direction = DIR_DOWN
            self.y += self.speed
        elif self.target[1] < self.y and self.turns[DIR_UP]:
            self.direction = DIR_UP
            self.y -= self.speed
        elif self.target[0] < self.x and self.turns[DIR_LEFT]:
            self.direction = DIR_LEFT
            self.x -= self.speed
        elif self.target[0] > self.x and self.turns[DIR_RIGHT]:
            self.direction = DIR_RIGHT
            self.x += self.speed
        elif self.turns[DIR_DOWN]:
            self.direction = DIR_DOWN
            self.y += self.speed
        elif self.turns[DIR_UP]:
            self.direction = DIR_UP
            self.y -= self.speed
        elif self.turns[DIR_LEFT]:
            self.direction = DIR_LEFT
            self.x -= self.speed
        elif self.turns[DIR_RIGHT]:
            self.direction = DIR_RIGHT
            self.x += self.speed
    
    def draw(self, screen, powerup, eaten, spooked_img, dead_img):
        """Draw ghost on screen"""
        if (not powerup and not self.dead) or (eaten and powerup and not self.dead):
            screen.blit(self.img, (self.x, self.y))
        elif powerup and not self.dead and not eaten:
            screen.blit(spooked_img, (self.x, self.y))
        else:
            screen.blit(dead_img, (self.x, self.y))
        
        center_x, center_y = self.get_center()
        return pygame.Rect(center_x - 18, center_y - 18, 36, 36)
