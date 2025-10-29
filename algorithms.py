"""
Search algorithms module - BFS, DFS, UCS, A*, Minimax, Alpha-Beta Pruning
Complete implementation with all required algorithms
"""
from collections import deque
import heapq
import math
from config import *


def manhattan_distance(pos1, pos2):
    """Calculate Manhattan distance between two positions"""
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def euclidean_distance(pos1, pos2):
    """Calculate Euclidean distance between two positions"""
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)


def get_neighbors(pos, board):
    """Get valid neighboring positions"""
    row, col = pos
    neighbors = []
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up
    
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if board.is_walkable(new_row, new_col):
            neighbors.append((new_row, new_col))
    
    return neighbors


def reconstruct_path(came_from, start, goal):
    """Reconstruct path from start to goal"""
    path = []
    current = goal
    
    while current != start and current in came_from:
        path.append(current)
        current = came_from[current]
    
    path.reverse()
    return path


class BFS:
    """Breadth-First Search Algorithm"""
    
    @staticmethod
    def search(start, goal, board):
        """
        Find shortest path using BFS
        Returns: path (list of positions), visited_nodes (set)
        """
        queue = deque([start])
        came_from = {start: None}
        visited = {start}
        
        while queue:
            current = queue.popleft()
            
            if current == goal:
                return reconstruct_path(came_from, start, goal), visited
            
            for neighbor in get_neighbors(current, board):
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    queue.append(neighbor)
        
        return [], visited


class DFS:
    """Depth-First Search Algorithm"""
    
    @staticmethod
    def search(start, goal, board, max_depth=100):
        """
        Find path using DFS with depth limit
        Returns: path (list of positions), visited_nodes (set)
        """
        stack = [(start, [start])]
        visited = {start}
        
        while stack:
            current, path = stack.pop()
            
            if current == goal:
                return path[1:], visited
            
            if len(path) > max_depth:
                continue
            
            for neighbor in get_neighbors(current, board):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))
        
        return [], visited


class UCS:
    """Uniform Cost Search (Dijkstra's Algorithm)"""
    
    @staticmethod
    def search(start, goal, board):
        """
        Find lowest cost path using UCS
        Returns: path (list of positions), visited_nodes (set)
        """
        # Priority queue: (cost, position)
        pq = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}
        visited = set()
        
        while pq:
            current_cost, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == goal:
                return reconstruct_path(came_from, start, goal), visited
            
            for neighbor in get_neighbors(current, board):
                new_cost = current_cost + 1  # Uniform cost of 1 per move
                
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost
                    heapq.heappush(pq, (priority, neighbor))
                    came_from[neighbor] = current
        
        return [], visited


class AStar:
    """A* Search Algorithm"""
    
    @staticmethod
    def search(start, goal, board, heuristic=manhattan_distance):
        """
        Find optimal path using A* with heuristic
        Returns: path (list of positions), visited_nodes (set)
        """
        # Priority queue: (f_score, position)
        pq = [(0, start)]
        came_from = {start: None}
        g_score = {start: 0}
        visited = set()
        
        while pq:
            _, current = heapq.heappop(pq)
            
            if current in visited:
                continue
            
            visited.add(current)
            
            if current == goal:
                return reconstruct_path(came_from, start, goal), visited
            
            for neighbor in get_neighbors(current, board):
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(pq, (f_score, neighbor))
                    came_from[neighbor] = current
        
        return [], visited


class Minimax:
    """Minimax Algorithm for adversarial search"""
    
    @staticmethod
    def evaluate_state(player_pos, ghost_positions, board):
        """
        Evaluate game state from player's perspective
        Higher score = better for player
        """
        score = 0
        
        # Distance to nearest ghost (we want to maximize this)
        if ghost_positions:
            min_ghost_dist = min(manhattan_distance(player_pos, g) for g in ghost_positions)
            score += min_ghost_dist * 10
        
        # Distance to nearest dot (we want to minimize this)
        dots = board.get_all_dots()
        if dots:
            min_dot_dist = min(manhattan_distance(player_pos, (d[0], d[1])) for d in dots)
            score -= min_dot_dist * 5
        
        # Prefer positions with more escape routes
        neighbors = get_neighbors(player_pos, board)
        score += len(neighbors) * 2
        
        return score
    
    @staticmethod
    def minimax(player_pos, ghost_positions, board, depth, is_maximizing):
        """
        Minimax algorithm implementation
        Returns: (best_score, best_move)
        """
        if depth == 0:
            return Minimax.evaluate_state(player_pos, ghost_positions, board), player_pos
        
        if is_maximizing:
            # Player's turn (maximize)
            max_eval = float('-inf')
            best_move = player_pos
            
            for neighbor in get_neighbors(player_pos, board):
                eval_score, _ = Minimax.minimax(neighbor, ghost_positions, board, 
                                                depth - 1, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = neighbor
            
            return max_eval, best_move
        else:
            # Ghosts' turn (minimize)
            min_eval = float('inf')
            best_move = player_pos
            
            # Simulate ghosts moving towards player
            new_ghost_positions = []
            for ghost_pos in ghost_positions:
                ghost_neighbors = get_neighbors(ghost_pos, board)
                if ghost_neighbors:
                    # Ghost moves closer to player
                    closest = min(ghost_neighbors, 
                                key=lambda p: manhattan_distance(p, player_pos))
                    new_ghost_positions.append(closest)
                else:
                    new_ghost_positions.append(ghost_pos)
            
            eval_score, _ = Minimax.minimax(player_pos, new_ghost_positions, board, 
                                           depth - 1, True)
            min_eval = min(min_eval, eval_score)
            
            return min_eval, player_pos
    
    @staticmethod
    def get_best_move(player_pos, ghost_positions, board, depth=MINIMAX_DEPTH):
        """Get best move using minimax"""
        _, best_move = Minimax.minimax(player_pos, ghost_positions, board, depth, True)
        return best_move


class AlphaBeta:
    """Alpha-Beta Pruning optimization of Minimax"""
    
    @staticmethod
    def evaluate_state(player_pos, ghost_positions, board):
        """Same evaluation as Minimax"""
        return Minimax.evaluate_state(player_pos, ghost_positions, board)
    
    @staticmethod
    def alphabeta(player_pos, ghost_positions, board, depth, alpha, beta, is_maximizing):
        """
        Alpha-Beta pruning algorithm
        Returns: (best_score, best_move)
        """
        if depth == 0:
            return AlphaBeta.evaluate_state(player_pos, ghost_positions, board), player_pos
        
        if is_maximizing:
            # Player's turn (maximize)
            max_eval = float('-inf')
            best_move = player_pos
            
            for neighbor in get_neighbors(player_pos, board):
                eval_score, _ = AlphaBeta.alphabeta(neighbor, ghost_positions, board, 
                                                     depth - 1, alpha, beta, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = neighbor
                
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval, best_move
        else:
            # Ghosts' turn (minimize)
            min_eval = float('inf')
            best_move = player_pos
            
            # Simulate ghosts moving towards player
            new_ghost_positions = []
            for ghost_pos in ghost_positions:
                ghost_neighbors = get_neighbors(ghost_pos, board)
                if ghost_neighbors:
                    # Ghost moves closer to player
                    closest = min(ghost_neighbors, 
                                key=lambda p: manhattan_distance(p, player_pos))
                    new_ghost_positions.append(closest)
                else:
                    new_ghost_positions.append(ghost_pos)
            
            eval_score, _ = AlphaBeta.alphabeta(player_pos, new_ghost_positions, board, 
                                               depth - 1, alpha, beta, True)
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            
            return min_eval, player_pos
    
    @staticmethod
    def get_best_move(player_pos, ghost_positions, board, depth=ALPHABETA_DEPTH):
        """Get best move using alpha-beta pruning"""
        _, best_move = AlphaBeta.alphabeta(player_pos, ghost_positions, board, 
                                          depth, float('-inf'), float('inf'), True)
        return best_move


class PathfindingAgent:
    """Agent that uses pathfinding algorithms to navigate"""
    
    def __init__(self, algorithm_mode=MODE_BFS):
        self.algorithm_mode = algorithm_mode
        self.current_path = []
        self.path_index = 0
        self.visited_nodes = set()
        
    def set_algorithm(self, mode):
        """Change the algorithm being used"""
        self.algorithm_mode = mode
        self.current_path = []
        self.path_index = 0
        
    def find_nearest_dot(self, player_pos, board):
        """Find the nearest dot or power pellet"""
        dots = board.get_all_dots()
        if not dots:
            return None
        
        # Convert player position to grid coordinates
        player_grid = (player_pos[1] // TILE_HEIGHT, player_pos[0] // TILE_WIDTH)
        
        # Find nearest dot
        nearest_dot = min(dots, key=lambda d: manhattan_distance(player_grid, d))
        return nearest_dot
    
    def get_next_move(self, player_pos, ghost_positions, board):
        """
        Get next move based on selected algorithm
        Returns: direction (0-3) or None
        """
        # Convert pixel position to grid position
        player_grid = (player_pos[1] // TILE_HEIGHT, player_pos[0] // TILE_WIDTH)
        
        # For minimax and alphabeta, use adversarial search
        if self.algorithm_mode in [MODE_MINIMAX, MODE_ALPHABETA]:
            ghost_grids = [(g[1] // TILE_HEIGHT, g[0] // TILE_WIDTH) for g in ghost_positions]
            
            if self.algorithm_mode == MODE_MINIMAX:
                next_pos = Minimax.get_best_move(player_grid, ghost_grids, board)
            else:
                next_pos = AlphaBeta.get_best_move(player_grid, ghost_grids, board)
            
            # Convert position to direction
            return self._position_to_direction(player_grid, next_pos)
        
        # For other algorithms, find path to nearest dot
        if not self.current_path or self.path_index >= len(self.current_path):
            goal = self.find_nearest_dot((player_pos[0], player_pos[1]), board)
            
            if not goal:
                return None
            
            # Find path using selected algorithm
            if self.algorithm_mode == MODE_BFS:
                self.current_path, self.visited_nodes = BFS.search(player_grid, goal, board)
            elif self.algorithm_mode == MODE_DFS:
                self.current_path, self.visited_nodes = DFS.search(player_grid, goal, board)
            elif self.algorithm_mode == MODE_UCS:
                self.current_path, self.visited_nodes = UCS.search(player_grid, goal, board)
            elif self.algorithm_mode == MODE_ASTAR:
                self.current_path, self.visited_nodes = AStar.search(player_grid, goal, board)
            
            self.path_index = 0
        
        if self.current_path and self.path_index < len(self.current_path):
            next_pos = self.current_path[self.path_index]
            
            # Check if we've reached this position
            if manhattan_distance(player_grid, next_pos) <= 1:
                self.path_index += 1
                if self.path_index < len(self.current_path):
                    next_pos = self.current_path[self.path_index]
                else:
                    return None
            
            # Convert position to direction
            return self._position_to_direction(player_grid, next_pos)
        
        return None
    
    def _position_to_direction(self, current, target):
        """Convert target position to direction"""
        dr = target[0] - current[0]
        dc = target[1] - current[1]
        
        if dc > 0:
            return DIR_RIGHT
        elif dc < 0:
            return DIR_LEFT
        elif dr < 0:
            return DIR_UP
        elif dr > 0:
            return DIR_DOWN
        
        return None
