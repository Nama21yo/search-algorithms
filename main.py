"""
Pac-Man AI Game with Search Algorithms
Main game loop and orchestration
"""
import pygame
import copy
from config import *
from board import Board
from entities import Player, Ghost
from algorithms import PathfindingAgent


class PacManGame:
    """Main game class"""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        pygame.display.set_caption("Pac-Man AI - Search Algorithms")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.small_font = pygame.font.Font('freesansbold.ttf', 16)
        
        # Load images
        self.player_images = self._load_player_images()
        self.ghost_images = self._load_ghost_images()
        
        # Game state
        self.board = Board()
        self.player = None
        self.ghosts = []
        self.agent = PathfindingAgent(MODE_MANUAL)
        
        # Game variables
        self.score = 0
        self.lives = 3
        self.powerup = False
        self.power_counter = 0
        self.eaten_ghosts = [False, False, False, False]
        self.startup_counter = 0
        self.moving = False
        self.game_over = False
        self.game_won = False
        self.counter = 0
        self.flicker = False
        
        # AI mode
        self.ai_mode = MODE_MANUAL
        self.show_path = True
        self.show_visited = False
        
        self._initialize_entities()
    
    def _load_player_images(self):
        """Load player animation images"""
        images = []
        try:
            for i in range(1, 5):
                img = pygame.image.load(f'assets/player_images/{i}.png')
                images.append(pygame.transform.scale(img, (45, 45)))
        except:
            # Create simple circles if images not found
            for i in range(4):
                surface = pygame.Surface((45, 45), pygame.SRCALPHA)
                mouth_angle = i * 15
                pygame.draw.circle(surface, YELLOW, (22, 22), 20)
                return [surface] * 4
        return images
    
    def _load_ghost_images(self):
        """Load ghost images"""
        images = {}
        colors = ['red', 'pink', 'blue', 'orange']
        color_defaults = [RED, PINK, CYAN, ORANGE]
        
        try:
            for color in colors:
                img = pygame.image.load(f'assets/ghost_images/{color}.png')
                images[color] = pygame.transform.scale(img, (45, 45))
            images['powerup'] = pygame.transform.scale(
                pygame.image.load('assets/ghost_images/powerup.png'), (45, 45))
            images['dead'] = pygame.transform.scale(
                pygame.image.load('assets/ghost_images/dead.png'), (45, 45))
        except:
            # Create simple colored circles if images not found
            for i, color in enumerate(colors):
                surface = pygame.Surface((45, 45), pygame.SRCALPHA)
                pygame.draw.circle(surface, color_defaults[i], (22, 22), 20)
                images[color] = surface
            
            surface = pygame.Surface((45, 45), pygame.SRCALPHA)
            pygame.draw.circle(surface, BLUE, (22, 22), 20)
            images['powerup'] = surface
            
            surface = pygame.Surface((45, 45), pygame.SRCALPHA)
            pygame.draw.circle(surface, WHITE, (22, 22), 20)
            images['dead'] = surface
        
        return images
    
    def _initialize_entities(self):
        """Initialize player and ghosts"""
        self.player = Player(PLAYER_START_X, PLAYER_START_Y, self.player_images)
        
        self.ghosts = [
            Ghost(BLINKY_START_X, BLINKY_START_Y, (PLAYER_START_X, PLAYER_START_Y),
                  GHOST_SPEED, self.ghost_images['red'], DIR_RIGHT, 0, "Blinky"),
            Ghost(INKY_START_X, INKY_START_Y, (PLAYER_START_X, PLAYER_START_Y),
                  GHOST_SPEED, self.ghost_images['blue'], DIR_UP, 1, "Inky"),
            Ghost(PINKY_START_X, PINKY_START_Y, (PLAYER_START_X, PLAYER_START_Y),
                  GHOST_SPEED, self.ghost_images['pink'], DIR_UP, 2, "Pinky"),
            Ghost(CLYDE_START_X, CLYDE_START_Y, (PLAYER_START_X, PLAYER_START_Y),
                  GHOST_SPEED, self.ghost_images['orange'], DIR_UP, 3, "Clyde")
        ]
    
    def reset_game(self):
        """Reset game to initial state"""
        self.board.reset()
        self.player.reset(PLAYER_START_X, PLAYER_START_Y)
        for ghost in self.ghosts:
            ghost.reset()
        
        self.score = 0
        self.lives = 3
        self.powerup = False
        self.power_counter = 0
        self.eaten_ghosts = [False, False, False, False]
        self.startup_counter = 0
        self.moving = False
        self.game_over = False
        self.game_won = False
        self.agent.current_path = []
    
    def reset_positions(self):
        """Reset positions after death"""
        self.player.reset(PLAYER_START_X, PLAYER_START_Y)
        for ghost in self.ghosts:
            ghost.reset()
        
        self.powerup = False
        self.power_counter = 0
        self.eaten_ghosts = [False, False, False, False]
        self.startup_counter = 0
        self.agent.current_path = []
    
    def check_collisions(self):
        """Check for dot and power pellet collisions"""
        center_x, center_y = self.player.get_center()
        grid_row = center_y // TILE_HEIGHT
        grid_col = center_x // TILE_WIDTH
        
        if 0 < self.player.x < 870:
            tile = self.board.get_tile(grid_row, grid_col)
            
            if tile == TILE_DOT:
                self.board.set_tile(grid_row, grid_col, TILE_EMPTY)
                self.score += SCORE_DOT
                
            elif tile == TILE_POWER_PELLET:
                self.board.set_tile(grid_row, grid_col, TILE_EMPTY)
                self.score += SCORE_POWER_PELLET
                self.powerup = True
                self.power_counter = 0
                self.eaten_ghosts = [False, False, False, False]
                
                # Slow down ghosts during powerup
                for ghost in self.ghosts:
                    if not ghost.dead:
                        ghost.speed = GHOST_SPEED_SCARED
    
    def check_ghost_collisions(self):
        """Check for player-ghost collisions"""
        player_center = self.player.get_center()
        player_rect = pygame.Rect(player_center[0] - 20, player_center[1] - 20, 40, 40)
        
        for ghost in self.ghosts:
            ghost_center = ghost.get_center()
            ghost_rect = pygame.Rect(ghost_center[0] - 18, ghost_center[1] - 18, 36, 36)
            
            if player_rect.colliderect(ghost_rect):
                if self.powerup and not ghost.dead and not self.eaten_ghosts[ghost.ghost_id]:
                    # Eat ghost
                    ghost.dead = True
                    self.eaten_ghosts[ghost.ghost_id] = True
                    self.score += (2 ** self.eaten_ghosts.count(True)) * SCORE_GHOST_BASE
                    ghost.speed = GHOST_SPEED_DEAD
                    
                elif not self.powerup and not ghost.dead:
                    # Player dies
                    if self.lives > 0:
                        self.lives -= 1
                        self.reset_positions()
                    else:
                        self.game_over = True
                        self.moving = False
                        
                elif self.powerup and self.eaten_ghosts[ghost.ghost_id] and not ghost.dead:
                    # Ghost that was eaten but respawned can still kill
                    if self.lives > 0:
                        self.lives -= 1
                        self.reset_positions()
                    else:
                        self.game_over = True
                        self.moving = False
    
    def update_ghost_targets(self):
        """Update ghost target positions"""
        player_x, player_y = self.player.x, self.player.y
        
        # Determine runaway position if in powerup mode
        if player_x < 450:
            runaway_x = 900
        else:
            runaway_x = 0
        if player_y < 450:
            runaway_y = 900
        else:
            runaway_y = 0
        
        return_target = (380, 400)
        
        for ghost in self.ghosts:
            if self.powerup:
                if not ghost.dead and not self.eaten_ghosts[ghost.ghost_id]:
                    # Run away from player
                    if ghost.ghost_id == 0:  # Blinky
                        ghost.target = (runaway_x, runaway_y)
                    elif ghost.ghost_id == 1:  # Inky
                        ghost.target = (runaway_x, player_y)
                    elif ghost.ghost_id == 2:  # Pinky
                        ghost.target = (player_x, runaway_y)
                    else:  # Clyde
                        ghost.target = (450, 450)
                elif not ghost.dead and self.eaten_ghosts[ghost.ghost_id]:
                    # Return to box
                    if 340 < ghost.x < 560 and 340 < ghost.y < 500:
                        ghost.target = (400, 100)
                    else:
                        ghost.target = (player_x, player_y)
                else:
                    ghost.target = return_target
            else:
                # Chase player
                if not ghost.dead:
                    if 340 < ghost.x < 560 and 340 < ghost.y < 500:
                        ghost.target = (400, 100)
                    else:
                        ghost.target = (player_x, player_y)
                else:
                    ghost.target = return_target
    
    def update_ghosts(self):
        """Update ghost positions and states"""
        for ghost in self.ghosts:
            ghost.check_collisions(self.board)
            
            # Revive ghost if back in box
            if ghost.in_box and ghost.dead:
                ghost.dead = False
                ghost.speed = GHOST_SPEED if not self.powerup else GHOST_SPEED_SCARED
            
            # Move ghost
            if self.moving:
                if not ghost.dead and not ghost.in_box:
                    ghost.move_towards_target()
                else:
                    ghost.move_towards_target()
    
    def draw_ui(self):
        """Draw UI elements"""
        # Score
        score_text = self.font.render(f'Score: {self.score}', True, WHITE)
        self.screen.blit(score_text, (10, 920))
        
        # Lives
        for i in range(self.lives):
            self.screen.blit(pygame.transform.scale(self.player_images[0], (30, 30)), 
                           (650 + i * 40, 915))
        
        # Powerup indicator
        if self.powerup:
            pygame.draw.circle(self.screen, BLUE, (140, 930), 15)
        
        # Algorithm mode
        mode_text = self.small_font.render(
            f'Mode: {ALGORITHM_NAMES[self.ai_mode]}', True, WHITE)
        self.screen.blit(mode_text, (10, 10))
        
        # Instructions
        if self.ai_mode == MODE_MANUAL:
            inst_text = self.small_font.render(
                'Arrow Keys: Move | 1-6: AI Mode | V: Toggle Visited | P: Toggle Path', 
                True, WHITE)
        else:
            inst_text = self.small_font.render(
                'Space: Pause AI | 1-6: Change Mode | V: Toggle Visited | P: Toggle Path', 
                True, WHITE)
        self.screen.blit(inst_text, (10, 35))
        
        # Game over/won messages
        if self.game_over:
            pygame.draw.rect(self.screen, WHITE, [50, 200, 800, 300], 0, 10)
            pygame.draw.rect(self.screen, (50, 50, 50), [70, 220, 760, 260], 0, 10)
            text = self.font.render('Game Over! Press R to Restart', True, RED)
            self.screen.blit(text, (150, 300))
            
        if self.game_won:
            pygame.draw.rect(self.screen, WHITE, [50, 200, 800, 300], 0, 10)
            pygame.draw.rect(self.screen, (50, 50, 50), [70, 220, 760, 260], 0, 10)
            text = self.font.render('Victory! Press R to Restart', True, (0, 255, 0))
            self.screen.blit(text, (180, 300))
    
    def draw_ai_visualization(self):
        """Draw AI pathfinding visualization"""
        if self.ai_mode == MODE_MANUAL:
            return
        
        # Draw visited nodes
        if self.show_visited and hasattr(self.agent, 'visited_nodes'):
            for node in self.agent.visited_nodes:
                x = node[1] * TILE_WIDTH + TILE_WIDTH // 2
                y = node[0] * TILE_HEIGHT + TILE_HEIGHT // 2
                pygame.draw.circle(self.screen, (100, 100, 255, 128), (x, y), 5)
        
        # Draw current path
        if self.show_path and self.agent.current_path:
            for i in range(len(self.agent.current_path) - 1):
                pos1 = self.agent.current_path[i]
                pos2 = self.agent.current_path[i + 1]
                
                x1 = pos1[1] * TILE_WIDTH + TILE_WIDTH // 2
                y1 = pos1[0] * TILE_HEIGHT + TILE_HEIGHT // 2
                x2 = pos2[1] * TILE_WIDTH + TILE_WIDTH // 2
                y2 = pos2[0] * TILE_HEIGHT + TILE_HEIGHT // 2
                
                pygame.draw.line(self.screen, (0, 255, 0), (x1, y1), (x2, y2), 3)
    
    def handle_input(self, event):
        """Handle keyboard input"""
        if event.type == pygame.KEYDOWN:
            # Manual controls
            if self.ai_mode == MODE_MANUAL:
                if event.key == pygame.K_RIGHT:
                    self.player.direction_command = DIR_RIGHT
                elif event.key == pygame.K_LEFT:
                    self.player.direction_command = DIR_LEFT
                elif event.key == pygame.K_UP:
                    self.player.direction_command = DIR_UP
                elif event.key == pygame.K_DOWN:
                    self.player.direction_command = DIR_DOWN
            
            # Algorithm selection
            if event.key == pygame.K_1:
                self.ai_mode = MODE_MANUAL
                self.agent.set_algorithm(MODE_MANUAL)
            elif event.key == pygame.K_2:
                self.ai_mode = MODE_BFS
                self.agent.set_algorithm(MODE_BFS)
            elif event.key == pygame.K_3:
                self.ai_mode = MODE_DFS
                self.agent.set_algorithm(MODE_DFS)
            elif event.key == pygame.K_4:
                self.ai_mode = MODE_UCS
                self.agent.set_algorithm(MODE_UCS)
            elif event.key == pygame.K_5:
                self.ai_mode = MODE_ASTAR
                self.agent.set_algorithm(MODE_ASTAR)
            elif event.key == pygame.K_6:
                self.ai_mode = MODE_MINIMAX
                self.agent.set_algorithm(MODE_MINIMAX)
            elif event.key == pygame.K_7:
                self.ai_mode = MODE_ALPHABETA
                self.agent.set_algorithm(MODE_ALPHABETA)
            
            # Visualization toggles
            elif event.key == pygame.K_v:
                self.show_visited = not self.show_visited
            elif event.key == pygame.K_p:
                self.show_path = not self.show_path
            
            # Restart
            elif event.key == pygame.K_r and (self.game_over or self.game_won):
                self.reset_game()
        
        elif event.type == pygame.KEYUP:
            if self.ai_mode == MODE_MANUAL:
                if event.key == pygame.K_RIGHT and self.player.direction_command == DIR_RIGHT:
                    self.player.direction_command = self.player.direction
                elif event.key == pygame.K_LEFT and self.player.direction_command == DIR_LEFT:
                    self.player.direction_command = self.player.direction
                elif event.key == pygame.K_UP and self.player.direction_command == DIR_UP:
                    self.player.direction_command = self.player.direction
                elif event.key == pygame.K_DOWN and self.player.direction_command == DIR_DOWN:
                    self.player.direction_command = self.player.direction
    
    def update(self):
        """Update game state"""
        # Animation counter
        if self.counter < 19:
            self.counter += 1
            if self.counter > 3:
                self.flicker = False
        else:
            self.counter = 0
            self.flicker = True
        
        self.player.animation_counter = self.counter
        
        # Powerup timer
        if self.powerup and self.power_counter < POWERUP_DURATION:
            self.power_counter += 1
        elif self.powerup and self.power_counter >= POWERUP_DURATION:
            self.power_counter = 0
            self.powerup = False
            self.eaten_ghosts = [False, False, False, False]
            # Reset ghost speeds
            for ghost in self.ghosts:
                if not ghost.dead:
                    ghost.speed = GHOST_SPEED
        
        # Startup delay
        if self.startup_counter < STARTUP_DURATION and not self.game_over and not self.game_won:
            self.moving = False
            self.startup_counter += 1
        else:
            self.moving = True
        
        # Check win condition
        if self.board.is_complete():
            self.game_won = True
            self.moving = False
        
        # Update ghost speeds
        if self.powerup:
            for i, ghost in enumerate(self.ghosts):
                if not ghost.dead:
                    ghost.speed = GHOST_SPEED_SCARED
                if self.eaten_ghosts[i]:
                    ghost.speed = GHOST_SPEED
        else:
            for i, ghost in enumerate(self.ghosts):
                if not ghost.dead:
                    ghost.speed = GHOST_SPEED
        
        for ghost in self.ghosts:
            if ghost.dead:
                ghost.speed = GHOST_SPEED_DEAD
        
        # Update game objects
        if self.moving:
            # Get AI move or use manual control
            if self.ai_mode != MODE_MANUAL:
                ghost_positions = [(g.x, g.y) for g in self.ghosts if not g.dead]
                ai_direction = self.agent.get_next_move(
                    (self.player.x, self.player.y), ghost_positions, self.board)
                
                if ai_direction is not None:
                    self.player.direction_command = ai_direction
            
            # Update player
            turns_allowed = self.player.check_position(self.board)
            
            if self.player.direction_command == DIR_RIGHT and turns_allowed[DIR_RIGHT]:
                self.player.direction = DIR_RIGHT
            elif self.player.direction_command == DIR_LEFT and turns_allowed[DIR_LEFT]:
                self.player.direction = DIR_LEFT
            elif self.player.direction_command == DIR_UP and turns_allowed[DIR_UP]:
                self.player.direction = DIR_UP
            elif self.player.direction_command == DIR_DOWN and turns_allowed[DIR_DOWN]:
                self.player.direction = DIR_DOWN
            
            self.player.move(turns_allowed)
            
            # Update ghosts
            self.update_ghost_targets()
            self.update_ghosts()
            
            # Check collisions
            self.check_collisions()
            self.check_ghost_collisions()
    
    def draw(self):
        """Draw game state"""
        self.screen.fill(BLACK)
        self.board.draw(self.screen, self.flicker)
        
        # Draw AI visualization
        self.draw_ai_visualization()
        
        # Draw entities
        self.player.draw(self.screen)
        
        for i, ghost in enumerate(self.ghosts):
            ghost.draw(self.screen, self.powerup, self.eaten_ghosts[i],
                      self.ghost_images['powerup'], self.ghost_images['dead'])
        
        # Draw UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            self.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_input(event)
            
            self.update()
            self.draw()
        
        pygame.quit()


def main():
    """Entry point"""
    game = PacManGame()
    game.run()


if __name__ == "__main__":
    main()
