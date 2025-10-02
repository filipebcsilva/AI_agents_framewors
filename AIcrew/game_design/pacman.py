import pygame                                                                                                                                                                            
import random                                                                                                                                                                            
import math                                                                                                                                                                              
# from collections import deque # Not used, removed for cleaner code                                                                                                                     
                                                                                                                                                                                        
# --- Constants ---                                                                                                                                                                      
TILE_SIZE = 20                                                                                                                                                                           
MAZE_WIDTH = 28                                                                                                                                                                          
MAZE_HEIGHT = 31                                                                                                                                                                         
SCREEN_WIDTH = MAZE_WIDTH * TILE_SIZE                                                                                                                                                    
SCREEN_HEIGHT = MAZE_HEIGHT * TILE_SIZE + 50 # +50 for score/lives display                                                                                                               
                                                                                                                                                                                        
# Colors                                                                                                                                                                                 
BLACK = (0, 0, 0)                                                                                                                                                                        
WHITE = (255, 255, 255)                                                                                                                                                                  
BLUE = (0, 0, 255)                                                                                                                                                                       
YELLOW = (255, 255, 0)                                                                                                                                                                   
RED = (255, 0, 0)                                                                                                                                                                        
PINK = (255, 184, 255)                                                                                                                                                                   
CYAN = (0, 255, 255)                                                                                                                                                                     
ORANGE = (255, 184, 82)                                                                                                                                                                  
GHOST_FRIGHTENED_COLOR = (0, 0, 200) # Darker blue                                                                                                                                       
                                                                                                                                                                                        
# Directions (dx, dy)                                                                                                                                                                    
UP = (0, -1)                                                                                                                                                                             
DOWN = (0, 1)                                                                                                                                                                            
LEFT = (-1, 0)                                                                                                                                                                           
RIGHT = (1, 0)                                                                                                                                                                           
DIRECTIONS = [UP, DOWN, LEFT, RIGHT] # Used for ghost pathfinding                                                                                                                        
                                                                                                                                                                                        
# Game States                                                                                                                                                                            
GAME_STATE_MENU = 0                                                                                                                                                                      
GAME_STATE_PLAYING = 1                                                                                                                                                                   
GAME_STATE_GAME_OVER = 2                                                                                                                                                                 
GAME_STATE_LEVEL_COMPLETE = 3                                                                                                                                                            
                                                                                                                                                                                        
# Maze elements (numbers correspond to tile types)                                                                                                                                       
# 0: Empty / Corridor                                                                                                                                                                    
# 1: Wall                                                                                                                                                                                
# 2: Pellet                                                                                                                                                                              
# 3: Power Pellet                                                                                                                                                                        
# 4: Ghost house entry (door)                                                                                                                                                            
# 5: Ghost house inside                                                                                                                                                                  
# 6: Warp tunnel (left)                                                                                                                                                                  
# 7: Warp tunnel (right)                                                                                                                                                                 
                                                                                                                                                                                        
# Initial Maze Layout                                                                                                                                                                    
# This is a common Pac-Man maze template (simplified)                                                                                                                                    
# Rows: 0-30, Cols: 0-27                                                                                                                                                                 
initial_maze_layout = [                                                                                                                                                                  
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], # 0                                                                                                                       
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1], # 1                                                                                                                       
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1], # 2                                                                                                                       
    [1,3,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,3,1], # 3 Power Pellets                                                                                                         
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1], # 4                                                                                                                       
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1], # 5                                                                                                                       
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1], # 6                                                                                                                       
    [1,2,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,2,1], # 7                                                                                                                       
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1], # 8                                                                                                                       
    [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1], # 9                                                                                                                       
    [1,1,1,1,1,1,2,1,1,1,1,1,0,1,1,0,1,1,1,1,1,2,1,1,1,1,1,1], # 10                                                                                                                      
    [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1], # 11                                                                                                                      
    [1,1,1,1,1,1,2,1,1,0,1,1,1,4,4,1,1,1,0,1,1,2,1,1,1,1,1,1], # 12 Ghost House Entry (Door is at (13,12) & (14,12))                                                                     
    [1,1,1,1,1,1,2,1,1,0,1,5,5,5,5,5,5,1,0,1,1,2,1,1,1,1,1,1], # 13 Ghost House Inside                                                                                                   
    [6,0,0,0,0,0,2,0,0,0,1,5,5,5,5,5,5,1,0,0,0,2,0,0,0,0,0,7], # 14 Warp Tunnel row                                                                                                      
    [1,1,1,1,1,1,2,1,1,0,1,5,5,5,5,5,5,1,0,1,1,2,1,1,1,1,1,1], # 15 Ghost House Inside                                                                                                   
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1], # 16                                                                                                                      
    [1,1,1,1,1,1,2,1,1,0,0,0,0,0,0,0,0,0,0,1,1,2,1,1,1,1,1,1], # 17                                                                                                                      
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1], # 18                                                                                                                      
    [1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,1,1,1,0,1,1,2,1,1,1,1,1,1], # 19                                                                                                                      
    [1,2,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2,2,2,2,2,1], # 20                                                                                                                      
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1], # 21                                                                                                                      
    [1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2,1,1,1,1,2,1], # 22                                                                                                                      
    [1,3,2,2,1,1,2,2,2,2,2,2,2,0,0,2,2,2,2,2,2,2,1,1,2,2,3,1], # 23 Pac-Man Start (0,0) is usually here                                                                                  
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1], # 24                                                                                                                      
    [1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1], # 25                                                                                                                      
    [1,2,2,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,1,1,2,2,2,2,2,2,1], # 26                                                                                                                      
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1], # 27                                                                                                                      
    [1,2,1,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,1,1,1,1,2,1], # 28                                                                                                                      
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1], # 29                                                                                                                      
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]  # 30                                                                                                                      
]                                                                                                                                                                                        
                                                                                                                                                                                        
# Pac-Man and Ghost initial positions                                                                                                                                                    
PACMAN_START_POS = (13, 23) # x, y grid coordinates                                                                                                                                      
GHOST_START_POS = {                                                                                                                                                                      
    "Blinky": (13, 14), # Red ghost, usually starts outside ghost house or moves out fast                                                                                                
    "Pinky": (13, 16),                                                                                                                                                                   
    "Inky": (11, 14),                                                                                                                                                                    
    "Clyde": (15, 14),                                                                                                                                                                   
}                                                                                                                                                                                        
# Ghost scatter targets (corners)                                                                                                                                                        
GHOST_SCATTER_TARGETS = {                                                                                                                                                                
    "Blinky": (MAZE_WIDTH - 2, 1), # Top-right                                                                                                                                           
    "Pinky": (1, 1),              # Top-left                                                                                                                                             
    "Inky": (MAZE_WIDTH - 2, MAZE_HEIGHT - 2), # Bottom-right                                                                                                                            
    "Clyde": (1, MAZE_HEIGHT - 2), # Bottom-left                                                                                                                                         
}                                                                                                                                                                                        
GHOST_HOUSE_EXIT = (13, 13) # Tile above the ghost house door                                                                                                                            
                                                                                                                                                                                        
# --- Helper Functions ---                                                                                                                                                               
def add_tuples(t1, t2):                                                                                                                                                                  
    """Adds two tuple vectors."""                                                                                                                                                        
    return (t1[0] + t2[0], t1[1] + t2[1])                                                                                                                                                
                                                                                                                                                                                        
def euclidean_distance(pos1, pos2):                                                                                                                                                      
    """Calculates Euclidean distance between two grid positions."""                                                                                                                      
    return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)                                                                                                                    
                                                                                                                                                                                        
# --- Classes ---                                                                                                                                                                        
                                                                                                                                                                                        
class PacMan:                                                                                                                                                                            
    def __init__(self, x, y, maze_layout):                                                                                                                                               
        self.start_x, self.start_y = x, y                                                                                                                                                
        self.grid_x, self.grid_y = x, y                                                                                                                                                  
        # Pixel coordinates are centered within the tile                                                                                                                                 
        self.pixel_x = x * TILE_SIZE + TILE_SIZE // 2                                                                                                                                    
        self.pixel_y = y * TILE_SIZE + TILE_SIZE // 2                                                                                                                                    
        self.radius = TILE_SIZE // 2 - 2                                                                                                                                                 
        self.color = YELLOW                                                                                                                                                              
        self.direction = LEFT # Initial direction                                                                                                                                        
        self.queued_direction = LEFT # Player input for next direction                                                                                                                   
        self.speed = 2 # Pixels per frame                                                                                                                                                
        self.lives = 3                                                                                                                                                                   
        self.score = 0                                                                                                                                                                   
        self.power_pellet_timer = 0 # Countdown for frightened mode                                                                                                                      
        self.is_moving = True # Pac-Man always attempts to move                                                                                                                          
        self.mouth_open = True # For drawing animation                                                                                                                                   
        self.mouth_timer = 0                                                                                                                                                             
        self.mouth_animation_speed = 5 # Frames per mouth change                                                                                                                         
                                                                                                                                                                                        
        self.reset_pos(maze_layout) # Ensures consistent initial state                                                                                                                   
                                                                                                                                                                                        
    def reset_pos(self, maze_layout):                                                                                                                                                    
        """Resets Pac-Man's position and state for a new life or level."""                                                                                                               
        self.grid_x, self.grid_y = self.start_x, self.start_y                                                                                                                            
        self.pixel_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2                                                                                                                          
        self.pixel_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2                                                                                                                          
        self.direction = LEFT                                                                                                                                                            
        self.queued_direction = LEFT                                                                                                                                                     
        self.power_pellet_timer = 0                                                                                                                                                      
        self.is_moving = True                                                                                                                                                            
        self.mouth_open = True                                                                                                                                                           
        self.mouth_timer = 0                                                                                                                                                             
                                                                                                                                                                                        
                                                                                                                                                                                        
    def can_move_in_direction(self, dx, dy, maze_layout, current_x, current_y):                                                                                                          
        """Checks if Pac-Man can move into the next grid tile."""                                                                                                                        
        next_grid_x, next_grid_y = current_x + dx, current_y + dy                                                                                                                        
                                                                                                                                                                                        
        # Warp tunnels are always passable; their wrapping is handled in `update`                                                                                                        
        if next_grid_x < 0 or next_grid_x >= MAZE_WIDTH:                                                                                                                                 
            return True                                                                                                                                                                  
                                                                                                                                                                                        
        # Check bounds and wall collision                                                                                                                                                
        if 0 <= next_grid_x < MAZE_WIDTH and 0 <= next_grid_y < MAZE_HEIGHT:                                                                                                             
            return maze_layout[next_grid_y][next_grid_x] != 1 # 1 is a wall                                                                                                              
        return False # Out of bounds normally treated as wall if not a warp tunnel                                                                                                       
                                                                                                                                                                                        
                                                                                                                                                                                        
    def update(self, maze_layout, game_manager):                                                                                                                                         
        """Updates Pac-Man's position, handles direction changes, and pellet eating."""                                                                                                  
        current_grid_center_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2                                                                                                                 
        current_grid_center_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2                                                                                                                 
                                                                                                                                                                                        
        # Check if Pac-Man is centered enough on a tile to change direction                                                                                                              
        # This makes turns feel snappy and grid-aligned.                                                                                                                                 
        if abs(self.pixel_x - current_grid_center_x) < self.speed and abs(self.pixel_y - current_grid_center_y) < self.speed:                                                                                                                       
                                                                                                                                                                                        
            # Snap to grid center                                                                                                                                                        
            self.pixel_x = current_grid_center_x                                                                                                                                         
            self.pixel_y = current_grid_center_y                                                                                                                                         
                                                                                                                                                                                        
            # Try to change to queued direction first                                                                                                                                    
            if self.queued_direction != self.direction:                                                                                                                                  
                if self.can_move_in_direction(self.queued_direction[0], self.queued_direction[1], maze_layout, self.grid_x, self.grid_y):                                                
                    self.direction = self.queued_direction                                                                                                                               
                                                                                                                                                                                        
            # If current direction is blocked, Pac-Man stops (cannot pass walls)                                                                                                         
            if not self.can_move_in_direction(self.direction[0], self.direction[1], maze_layout, self.grid_x, self.grid_y):                                                              
                self.is_moving = False                                                                                                                                                   
            else:                                                                                                                                                                        
                self.is_moving = True                                                                                                                                                    
                                                                                                                                                                                        
        if self.is_moving:                                                                                                                                                               
            self.pixel_x += self.direction[0] * self.speed                                                                                                                               
            self.pixel_y += self.direction[1] * self.speed                                                                                                                               
                                                                                                                                                                                        
            # Update grid position based on pixel position                                                                                                                               
            # Use int(round(...)) for better precision when converting float pixel coords to int grid coords.                                                                            
            new_grid_x = int(round((self.pixel_x - TILE_SIZE // 2) / TILE_SIZE))                                                                                                         
            new_grid_y = int(round((self.pixel_y - TILE_SIZE // 2) / TILE_SIZE))                                                                                                         
                                                                                                                                                                                        
            # Warp tunnels                                                                                                                                                               
            if new_grid_x < 0: # Left warp                                                                                                                                               
                new_grid_x = MAZE_WIDTH - 1                                                                                                                                              
                self.pixel_x = new_grid_x * TILE_SIZE + TILE_SIZE // 2                                                                                                                   
            elif new_grid_x >= MAZE_WIDTH: # Right warp                                                                                                                                  
                new_grid_x = 0                                                                                                                                                           
                self.pixel_x = new_grid_x * TILE_SIZE + TILE_SIZE // 2                                                                                                                   
                                                                                                                                                                                        
            # Check if grid position changed                                                                                                                                             
            if new_grid_x != self.grid_x or new_grid_y != self.grid_y:                                                                                                                   
                self.grid_x, self.grid_y = new_grid_x, new_grid_y                                                                                                                        
                self.eat_pellet(maze_layout, game_manager)                                                                                                                               
                                                                                                                                                                                        
        # Update power pellet timer                                                                                                                                                      
        if self.power_pellet_timer > 0:                                                                                                                                                  
            self.power_pellet_timer -= 1                                                                                                                                                 
            if self.power_pellet_timer == 0:                                                                                                                                             
                game_manager.end_frightened_mode()                                                                                                                                       
                                                                                                                                                                                        
        # Mouth animation timer                                                                                                                                                          
        self.mouth_timer += 1                                                                                                                                                            
        if self.mouth_timer >= self.mouth_animation_speed:                                                                                                                               
            self.mouth_open = not self.mouth_open                                                                                                                                        
            self.mouth_timer = 0                                                                                                                                                         
                                                                                                                                                                                        
                                                                                                                                                                                        
    def eat_pellet(self, maze_layout, game_manager):                                                                                                                                     
        """Handles Pac-Man eating pellets or power pellets."""                                                                                                                           
        # Ensure Pac-Man is within maze bounds before checking tile type                                                                                                                 
        if 0 <= self.grid_y < MAZE_HEIGHT and 0 <= self.grid_x < MAZE_WIDTH:                                                                                                             
            current_tile = maze_layout[self.grid_y][self.grid_x]                                                                                                                         
            if current_tile == 2: # Pellet                                                                                                                                               
                self.score += 10                                                                                                                                                         
                game_manager.pellets_left -= 1                                                                                                                                           
                maze_layout[self.grid_y][self.grid_x] = 0 # Mark as eaten (empty corridor)                                                                                               
            elif current_tile == 3: # Power Pellet                                                                                                                                       
                self.score += 50                                                                                                                                                         
                game_manager.pellets_left -= 1                                                                                                                                           
                maze_layout[self.grid_y][self.grid_x] = 0 # Mark as eaten (empty corridor)                                                                                               
                self.power_pellet_timer = game_manager.power_pellet_duration # Start timer for frightened mode                                                                           
                game_manager.start_frightened_mode()                                                                                                                                     
                                                                                                                                                                                        
            if game_manager.pellets_left == 0:                                                                                                                                           
                game_manager.level_complete()                                                                                                                                            
                                                                                                                                                                                        
    def lose_life(self):                                                                                                                                                                 
        """Decrements Pac-Man's lives."""                                                                                                                                                
        self.lives -= 1                                                                                                                                                                  
                                                                                                                                                                                        
    def draw(self, screen):                                                                                                                                                              
        """Draws Pac-Man on the screen."""                                                                                                                                               
        # Ensure all drawing coordinates are integers                                                                                                                                    
        center_x, center_y = int(self.pixel_x), int(self.pixel_y)                                                                                                                        
        draw_rect = (center_x - self.radius, center_y - self.radius, self.radius * 2, self.radius * 2)                                                                                   
                                                                                                                                                                                        
        if self.mouth_open and self.is_moving:                                                                                                                                           
            # Determine mouth angle based on direction                                                                                                                                   
            angle_start = 0                                                                                                                                                              
            angle_end = 360                                                                                                                                                              
            mouth_open_angle = 30 # degrees for mouth opening                                                                                                                            
                                                                                                                                                                                        
            # Pygame arc angles are clockwise from positive x-axis.                                                                                                                      
            # Start angle must be less than end angle for arc drawing.                                                                                                                   
            if self.direction == LEFT:                                                                                                                                                   
                angle_start = 180 + mouth_open_angle                                                                                                                                     
                angle_end = 180 - mouth_open_angle + 360 # Add 360 to ensure end_angle > start_angle for full sweep                                                                      
            elif self.direction == RIGHT:                                                                                                                                                
                angle_start = mouth_open_angle                                                                                                                                           
                angle_end = 360 - mouth_open_angle                                                                                                                                       
            elif self.direction == UP:                                                                                                                                                   
                angle_start = 270 + mouth_open_angle                                                                                                                                     
                angle_end = 270 - mouth_open_angle + 360                                                                                                                                 
            elif self.direction == DOWN:                                                                                                                                                 
                angle_start = 90 + mouth_open_angle                                                                                                                                      
                angle_end = 90 - mouth_open_angle + 360                                                                                                                                  
                                                                                                                                                                                        
            # Draw Pac-Man as an arc                                                                                                                                                     
            pygame.draw.arc(screen, self.color,                                                                                                                                          
                            draw_rect,                                                                                                                                                   
                            math.radians(angle_end), math.radians(angle_start), self.radius)                                                                                             
            pygame.draw.circle(screen, BLACK, (center_x, center_y), self.radius // 3, 0) # Mouth filler (stylized)                                                                       
        else:                                                                                                                                                                            
            # Draw Pac-Man as a closed circle                                                                                                                                            
            pygame.draw.circle(screen, self.color, (center_x, center_y), self.radius)                                                                                                    
                                                                                                                                                                                        
                                                                                                                                                                                        
class Ghost:                                                                                                                                                                             
    def __init__(self, x, y, color, name, pacman, maze_layout, speed_factor=1.0):                                                                                                        
        self.start_x, self.start_y = x, y                                                                                                                                                
        self.grid_x, self.grid_y = x, y                                                                                                                                                  
        self.pixel_x = x * TILE_SIZE + TILE_SIZE // 2                                                                                                                                    
        self.pixel_y = y * TILE_SIZE + TILE_SIZE // 2                                                                                                                                    
        self.color = color                                                                                                                                                               
        self.name = name                                                                                                                                                                 
        self.pacman_ref = pacman # Reference to Pac-Man for targeting                                                                                                                    
        self.radius = TILE_SIZE // 2 - 2                                                                                                                                                 
        self.base_speed = 1.5 * speed_factor # Pixels per frame                                                                                                                          
        self.current_speed = self.base_speed                                                                                                                                             
        self.direction = UP # Initial direction for exiting house                                                                                                                        
        self.state = "CHASE" # CHASE, SCATTER, FRIGHTENED, EATEN                                                                                                                         
        self.frightened_timer = 0                                                                                                                                                        
        self.respawn_timer = 0 # Timer for ghost to respawn after being eaten                                                                                                            
        self.scatter_target = GHOST_SCATTER_TARGETS[name] if name in GHOST_SCATTER_TARGETS else (0,0)                                                                                    
        self.ghost_house_exit_target = GHOST_HOUSE_EXIT                                                                                                                                  
        self.is_in_house = True # Flag if ghost is currently inside the ghost house                                                                                                      
        self._pre_fright_direction = UP # Store direction before frightened for correct reversal                                                                                         
                                                                                                                                                                                        
        self.reset_pos(maze_layout)                                                                                                                                                      
                                                                                                                                                                                        
    def reset_pos(self, maze_layout):                                                                                                                                                    
        """Resets ghost's position and state."""                                                                                                                                         
        self.grid_x, self.grid_y = self.start_x, self.start_y                                                                                                                            
        self.pixel_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2                                                                                                                          
        self.pixel_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2                                                                                                                          
        self.direction = UP # Default direction to attempt exiting house                                                                                                                 
        self.state = "CHASE" # Default state after reset (will be overridden by GameManager phase)                                                                                       
        self.frightened_timer = 0                                                                                                                                                        
        self.respawn_timer = 0                                                                                                                                                           
        self.is_in_house = True                                                                                                                                                          
        self.current_speed = self.base_speed # Reset speed                                                                                                                               
        self._pre_fright_direction = UP # Reset pre-frightened direction                                                                                                                 
                                                                                                                                                                                        
    def set_speed_factor(self, factor):                                                                                                                                                  
        """Adjusts ghost speed based on level difficulty."""                                                                                                                             
        self.base_speed = 1.5 * factor                                                                                                                                                   
        # Adjust current speed instantly if in a special state                                                                                                                           
        if self.state == "FRIGHTENED":                                                                                                                                                   
            self.current_speed = self.base_speed * 0.5 # Frightened ghosts are slower                                                                                                    
        elif self.state == "EATEN":                                                                                                                                                      
            self.current_speed = self.base_speed * 2 # Eaten ghosts are faster                                                                                                           
        else:                                                                                                                                                                            
            self.current_speed = self.base_speed                                                                                                                                         
                                                                                                                                                                                        
                                                                                                                                                                                        
    def get_target_tile(self, pacman_pos, pacman_direction, blinky_pos=None):                                                                                                            
        """Abstract method for ghost-specific targeting logic. To be overridden by subclasses."""                                                                                        
        raise NotImplementedError("Subclasses must implement get_target_tile()")                                                                                                         
                                                                                                                                                                                        
    def can_move_in_direction(self, dx, dy, maze_layout, current_x, current_y, in_house_mode=False):                                                                                     
        """                                                                                                                                                                              
        Checks if the ghost can move into the next grid tile.                                                                                                                            
        `in_house_mode` flag allows ghosts to navigate within or through the ghost house door.                                                                                           
        """                                                                                                                                                                              
        next_grid_x, next_grid_y = current_x + dx, current_y + dy                                                                                                                        
                                                                                                                                                                                        
        # Handle warp tunnels                                                                                                                                                            
        if next_grid_x < 0 or next_grid_x >= MAZE_WIDTH: return True                                                                                                                     
                                                                                                                                                                                        
        if 0 <= next_grid_x < MAZE_WIDTH and 0 <= next_grid_y < MAZE_HEIGHT:                                                                                                             
            tile_type = maze_layout[next_grid_y][next_grid_x]                                                                                                                            
                                                                                                                                                                                        
            if tile_type == 1: # Wall                                                                                                                                                    
                return False                                                                                                                                                             
                                                                                                                                                                                        
            # Special ghost house entry/exit rules                                                                                                                                       
            if tile_type == 4: # Ghost house entry/door                                                                                                                                  
                # Ghosts can exit through the door (move out of the house)                                                                                                               
                # Eaten ghosts can re-enter from outside                                                                                                                                 
                if in_house_mode or self.state == "EATEN":                                                                                                                               
                    return True                                                                                                                                                          
                # Ghosts in CHASE/SCATTER/FRIGHTENED states cannot normally enter the door from outside                                                                                  
                return False                                                                                                                                                             
                                                                                                                                                                                        
            if tile_type == 5: # Ghost house inside (only passable if in_house_mode or EATEN state)                                                                                      
                if not in_house_mode and self.state != "EATEN":                                                                                                                          
                    return False                                                                                                                                                         
                                                                                                                                                                                        
            return True                                                                                                                                                                  
        return False # Out of maze bounds for regular tiles (only warp tunnels are special)                                                                                              
                                                                                                                                                                                        
    def find_next_direction_greedy(self, target_x, target_y, maze_layout, blinky_pos):                                                                                                   
        """                                                                                                                                                                              
        Determines the next direction for the ghost using a greedy pathfinding approach.                                                                                                 
        Chooses the direction that minimizes Euclidean distance to the target.                                                                                                           
        Ghosts cannot reverse direction unless stuck.                                                                                                                                    
        """                                                                                                                                                                              
        current_grid_x, current_grid_y = self.grid_x, self.grid_y                                                                                                                        
                                                                                                                                                                                        
        valid_directions = []                                                                                                                                                            
        for d in DIRECTIONS:                                                                                                                                                             
            # Ghosts cannot reverse direction (180 degree turn)                                                                                                                          
            if d[0] == -self.direction[0] and d[1] == -self.direction[1]:                                                                                                                
                continue                                                                                                                                                                 
            if self.can_move_in_direction(d[0], d[1], maze_layout, current_grid_x, current_grid_y, self.is_in_house or self.state == "EATEN"):                                           
                valid_directions.append(d)                                                                                                                                               
                                                                                                                                                                                        
        # If no valid directions (e.g., in a dead end), allow reversing                                                                                                                  
        if not valid_directions:                                                                                                                                                         
            # Check if reversing is actually possible (not into a wall)                                                                                                                 
            if self.can_move_in_direction(-self.direction[0], -self.direction[1], maze_layout, current_grid_x, current_grid_y, self.is_in_house or self.state == "EATEN"):              
                return (-self.direction[0], -self.direction[1])                                                                                                                         
            return self.direction # If still stuck, keep current direction (shouldn't happen often)                                                                                     
                                                                                                                                                                                        
        # Frightened ghosts flee or move randomly                                                                                                                                        
        if self.state == "FRIGHTENED" and not self.is_in_house:                                                                                                                          
            # Prioritize moving away from Pac-Man                                                                                                                                        
            flee_dirs = []                                                                                                                                                               
            pacman_pos = (self.pacman_ref.grid_x, self.pacman_ref.grid_y)                                                                                                                
            current_dist_to_pacman = euclidean_distance((current_grid_x, current_grid_y), pacman_pos)                                                                                    
                                                                                                                                                                                        
            for d in valid_directions:                                                                                                                                                   
                next_x, next_y = current_grid_x + d[0], current_grid_y + d[1]                                                                                                            
                # If moving in 'd' direction increases distance to Pac-Man, it's a good flee direction                                                                                   
                if euclidean_distance((next_x, next_y), pacman_pos) > current_dist_to_pacman:                                                                                            
                    flee_dirs.append(d)                                                                                                                                                   
                                                                                                                                                                                        
            if flee_dirs:                                                                                                                                                                
                # If multiple valid flee directions, pick one randomly                                                                                                                   
                return random.choice(flee_dirs)                                                                                                                                          
            else:                                                                                                                                                                        
                # If no direction directly increases distance, pick any random valid direction                                                                                           
                return random.choice(valid_directions)                                                                                                                                   
                                                                                                                                                                                        
        # For CHASE/SCATTER/EATEN states, choose the direction that minimizes distance to target                                                                                         
        best_dist = float('inf')                                                                                                                                                         
        best_dir = self.direction # Default to current direction if no better found                                                                                                      
                                                                                                                                                                                        
        for d in valid_directions:                                                                                                                                                       
            next_x, next_y = current_grid_x + d[0], current_grid_y + d[1]                                                                                                                
            dist = euclidean_distance((next_x, next_y), (target_x, target_y))                                                                                                            
            if dist < best_dist:                                                                                                                                                         
                best_dist = dist                                                                                                                                                         
                best_dir = d                                                                                                                                                             
            # Tie-breaking: In original Pac-Man, ties are broken by UP, LEFT, DOWN, RIGHT.                                                                                               
            # For simplicity, we just take the first best_dir found here.                                                                                                                
        return best_dir                                                                                                                                                                  
                                                                                                                                                                                        
    def update(self, maze_layout, blinky_pos=None):                                                                                                                                      
        """Updates ghost's position and state based on its AI."""                                                                                                                        
        # Handle respawn timer (when eaten)                                                                                                                                              
        if self.state == "EATEN":                                                                                                                                                        
            self.respawn_timer -= 1                                                                                                                                                      
            if self.respawn_timer <= 0:                                                                                                                                                  
                self.change_state("CHASE") # Revert to chase (GameManager's phase timer will adjust)                                                                                     
                self.is_in_house = True # Ensure it exits the house again                                                                                                                
                # Teleport to start position inside house (or ghost house exit for Blinky)                                                                                               
                # Blinky's GHOST_START_POS is at the door, so it's already "exiting"                                                                                                     
                self.grid_x, self.grid_y = self.start_x, self.start_y                                                                                                                    
                self.pixel_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2                                                                                                                  
                self.pixel_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2                                                                                                                  
                self.direction = UP # Try to exit ghost house                                                                                                                            
                self.current_speed = self.base_speed                                                                                                                                     
            return # Don't move while respawning or just finished respawning                                                                                                             
                                                                                                                                                                                        
        # Determine target based on state                                                                                                                                                
        target_grid_x, target_grid_y = 0, 0 # Default, will be overwritten                                                                                                               
                                                                                                                                                                                        
        if self.is_in_house:                                                                                                                                                             
            target_grid_x, target_grid_y = self.ghost_house_exit_target                                                                                                                  
            # If at the exit point, consider exiting                                                                                                                                     
            # This check is important to transition from 'in_house' to 'out of house'                                                                                                    
            if self.grid_x == target_grid_x and self.grid_y == target_grid_y and self.direction == UP:                                                                                   
                # Check if the tile directly above the door is not a wall                                                                                                                
                if target_grid_y > 0 and maze_layout[target_grid_y-1][target_grid_x] != 1:                                                                                               
                    self.is_in_house = False # Successfully exited the house                                                                                                             
                    # The ghost's state (CHASE/SCATTER) will be dictated by GameManager's phase timer                                                                                    
                    self.current_speed = self.base_speed # Resume normal speed                                                                                                           
                # Else, keep trying to reach/pass GHOST_HOUSE_EXIT within the house's movement rules                                                                                     
        else: # Ghost is outside the house                                                                                                                                               
            if self.state == "CHASE":                                                                                                                                                    
                target_grid_x, target_grid_y = self.get_target_tile(                                                                                                                     
                    (self.pacman_ref.grid_x, self.pacman_ref.grid_y),                                                                                                                    
                    self.pacman_ref.direction,                                                                                                                                           
                    blinky_pos                                                                                                                                                           
                )                                                                                                                                                                        
            elif self.state == "SCATTER":                                                                                                                                                
                target_grid_x, target_grid_y = self.scatter_target                                                                                                                       
            elif self.state == "FRIGHTENED":                                                                                                                                             
                # Frightened target logic is handled directly in find_next_direction_greedy                                                                                              
                pass                                                                                                                                                                     
                                                                                                                                                                                        
        # Check if ghost is centered on a tile to decide direction                                                                                                                       
        current_grid_center_x = self.grid_x * TILE_SIZE + TILE_SIZE // 2                                                                                                                 
        current_grid_center_y = self.grid_y * TILE_SIZE + TILE_SIZE // 2                                                                                                                 
                                                                                                                                                                                        
        if abs(self.pixel_x - current_grid_center_x) < self.current_speed and abs(self.pixel_y - current_grid_center_y) < self.current_speed:                                                                                                               
                                                                                                                                                                                        
            # Snap to grid center                                                                                                                                                        
            self.pixel_x = current_grid_center_x                                                                                                                                         
            self.pixel_y = current_grid_center_y                                                                                                                                         
                                                                                                                                                                                        
            # Determine new direction (unless frightened, where specific flee logic applies)                                                                                             
            self.direction = self.find_next_direction_greedy(target_grid_x, target_grid_y, maze_layout, blinky_pos)                                                                      
                                                                                                                                                                                        
        # Move ghost                                                                                                                                                                     
        self.pixel_x += self.direction[0] * self.current_speed                                                                                                                           
        self.pixel_y += self.direction[1] * self.current_speed                                                                                                                           
                                                                                                                                                                                        
        # Update grid position and handle warp tunnels                                                                                                                                   
        # Use int(round(...)) for better precision.                                                                                                                                      
        new_grid_x = int(round((self.pixel_x - TILE_SIZE // 2) / TILE_SIZE))                                                                                                             
        new_grid_y = int(round((self.pixel_y - TILE_SIZE // 2) / TILE_SIZE))                                                                                                             
                                                                                                                                                                                        
        # Warp tunnels                                                                                                                                                                   
        if new_grid_x < 0:                                                                                                                                                               
            new_grid_x = MAZE_WIDTH - 1                                                                                                                                                  
            self.pixel_x = new_grid_x * TILE_SIZE + TILE_SIZE // 2                                                                                                                       
        elif new_grid_x >= MAZE_WIDTH:                                                                                                                                                   
            new_grid_x = 0                                                                                                                                                               
            self.pixel_x = new_grid_x * TILE_SIZE + TILE_SIZE // 2                                                                                                                       
                                                                                                                                                                                        
        # Only update grid_x, grid_y if it actually changed                                                                                                                              
        self.grid_x, self.grid_y = new_grid_x, new_grid_y                                                                                                                                
                                                                                                                                                                                        
    def change_state(self, new_state, duration=0):                                                                                                                                       
        """Changes the ghost's state and updates related properties."""                                                                                                                  
        if self.state != new_state: # Only apply changes if state is actually changing                                                                                                   
            if new_state == "FRIGHTENED":                                                                                                                                                
                self._pre_fright_direction = self.direction # Store current direction                                                                                                    
                self.frightened_timer = duration                                                                                                                                         
                self.current_speed = self.base_speed * 0.5 # Slower when frightened                                                                                                      
                self.direction = (-self.direction[0], -self.direction[1]) # Reverse direction immediately                                                                                
            elif new_state == "EATEN":                                                                                                                                                   
                self.respawn_timer = 2 * 60 # 2 seconds of respawn time (at 60 FPS)                                                                                                      
                self.current_speed = self.base_speed * 2 # Faster when eaten, going back to house                                                                                        
                # Ghost should target ghost house center to respawn                                                                                                                      
                # The current update logic will guide it back to its starting position, which is within the house.                                                                       
                # `is_in_house` will be set to True upon respawn completion.                                                                                                             
            else: # CHASE or SCATTER                                                                                                                                                     
                self.current_speed = self.base_speed # Revert to normal speed                                                                                                            
                # If coming out of FRIGHTENED mode, reverse direction again                                                                                                              
                if self.state == "FRIGHTENED":                                                                                                                                           
                    self.direction = (-self.direction[0], -self.direction[1]) # Reverse back to pre-frightened path                                                                      
            self.state = new_state # Update state after all logic is applied                                                                                                             
                                                                                                                                                                                        
    def draw(self, screen):                                                                                                                                                              
        """Draws the ghost on the screen, changing appearance based on state."""                                                                                                         
        # Ensure all drawing coordinates are integers                                                                                                                                    
        center_x, center_y = int(self.pixel_x), int(self.pixel_y)                                                                                                                        
        ghost_color = self.color                                                                                                                                                         
                                                                                                                                                                                        
        if self.state == "FRIGHTENED":                                                                                                                                                   
            # Flash white at the end of frightened mode                                                                                                                                  
            if self.frightened_timer < 60 and (self.frightened_timer // 15) % 2 == 0: # Flash every 15 frames for last second                                                            
                ghost_color = WHITE                                                                                                                                                      
            else:                                                                                                                                                                        
                ghost_color = GHOST_FRIGHTENED_COLOR                                                                                                                                     
        elif self.state == "EATEN":                                                                                                                                                      
            # Only draw eyes for eaten ghost (moving back to house)                                                                                                                      
            eye_radius = self.radius // 3                                                                                                                                                
            pupil_radius = eye_radius // 2                                                                                                                                               
            eye_offset = self.radius // 2                                                                                                                                                
                                                                                                                                                                                        
            # Pupils also indicate direction                                                                                                                                             
            pupil_dx, pupil_dy = 0, 0                                                                                                                                                    
            if self.direction == UP: pupil_dy = -pupil_radius                                                                                                                            
            elif self.direction == DOWN: pupil_dy = pupil_radius                                                                                                                         
            elif self.direction == LEFT: pupil_dx = -pupil_radius                                                                                                                        
            elif self.direction == RIGHT: pupil_dx = pupil_radius                                                                                                                        
                                                                                                                                                                                        
            # Draw only eyes, slightly offset for pupil direction                                                                                                                        
            pygame.draw.circle(screen, WHITE, (center_x - eye_offset, center_y - eye_offset), eye_radius)                                                                                
            pygame.draw.circle(screen, BLACK, (center_x - eye_offset + pupil_dx, center_y - eye_offset + pupil_dy), pupil_radius)                                                        
                                                                                                                                                                                        
            pygame.draw.circle(screen, WHITE, (center_x + eye_offset, center_y - eye_offset), eye_radius)                                                                                
            pygame.draw.circle(screen, BLACK, (center_x + eye_offset + pupil_dx, center_y - eye_offset + pupil_dy), pupil_radius)                                                        
            return                                                                                                                                                                       
                                                                                                                                                                                        
        # Draw body (circle + rectangle for skirt effect)                                                                                                                                
        pygame.draw.circle(screen, ghost_color, (center_x, center_y), self.radius)                                                                                                       
        pygame.draw.rect(screen, ghost_color, (center_x - self.radius, center_y, self.radius * 2, self.radius))                                                                          
                                                                                                                                                                                        
        # Draw eyes (white circles with black pupils)                                                                                                                                    
        eye_radius = self.radius // 3                                                                                                                                                    
        pupil_radius = eye_radius // 2                                                                                                                                                   
        eye_offset = self.radius // 2                                                                                                                                                    
                                                                                                                                                                                        
        # Pupil direction based on ghost movement direction                                                                                                                              
        pupil_dx, pupil_dy = 0, 0                                                                                                                                                        
        if self.direction == UP: pupil_dy = -pupil_radius                                                                                                                                
        elif self.direction == DOWN: pupil_dy = pupil_radius                                                                                                                             
        elif self.direction == LEFT: pupil_dx = -pupil_radius                                                                                                                            
        elif self.direction == RIGHT: pupil_dx = pupil_radius                                                                                                                            
                                                                                                                                                                                        
        pygame.draw.circle(screen, WHITE, (center_x - eye_offset, center_y - eye_offset), eye_radius)                                                                                    
        pygame.draw.circle(screen, BLACK, (center_x - eye_offset + pupil_dx, center_y - eye_offset + pupil_dy), pupil_radius)                                                            
                                                                                                                                                                                        
        pygame.draw.circle(screen, WHITE, (center_x + eye_offset, center_y - eye_offset), eye_radius)                                                                                    
        pygame.draw.circle(screen, BLACK, (center_x + eye_offset + pupil_dx, center_y - eye_offset + pupil_dy), pupil_radius)                                                            
                                                                                                                                                                                        
                                                                                                                                                                                        
class Blinky(Ghost):                                                                                                                                                                     
    def __init__(self, x, y, pacman, maze_layout, speed_factor):                                                                                                                         
        super().__init__(x, y, RED, "Blinky", pacman, maze_layout, speed_factor)                                                                                                         
        self.is_in_house = False # Blinky often starts outside the house immediately                                                                                                     
                                                                                                                                                                                        
    def get_target_tile(self, pacman_pos, pacman_direction, blinky_pos=None):                                                                                                            
        # Blinky (Red Ghost): Aggressively pursues Pac-Man, always targeting his current location.                                                                                       
        return pacman_pos                                                                                                                                                                
                                                                                                                                                                                        
class Pinky(Ghost):                                                                                                                                                                      
    def __init__(self, x, y, pacman, maze_layout, speed_factor):                                                                                                                         
        super().__init__(x, y, PINK, "Pinky", pacman, maze_layout, speed_factor)                                                                                                         
                                                                                                                                                                                        
    def get_target_tile(self, pacman_pos, pacman_direction, blinky_pos=None):                                                                                                            
        # Pinky (Pink Ghost): Attempts to ambush Pac-Man by aiming four tiles ahead of Pac-Man's current direction.                                                                      
        target_x = pacman_pos[0] + pacman_direction[0] * 4                                                                                                                               
        target_y = pacman_pos[1] + pacman_direction[1] * 4                                                                                                                               
                                                                                                                                                                                        
        # Special case: If Pac-Man is moving UP, Pinky's target is 4 tiles up and 4 tiles left                                                                                           
        # This is an original Pac-Man bug/feature.                                                                                                                                       
        if pacman_direction == UP:                                                                                                                                                       
            target_x -= 4                                                                                                                                                                
                                                                                                                                                                                        
        # Clamp target to maze bounds                                                                                                                                                    
        target_x = max(0, min(MAZE_WIDTH - 1, target_x))                                                                                                                                 
        target_y = max(0, min(MAZE_HEIGHT - 1, target_y))                                                                                                                                
        return (target_x, target_y)                                                                                                                                                      
                                                                                                                                                                                        
class Inky(Ghost):                                                                                                                                                                       
    def __init__(self, x, y, pacman, maze_layout, speed_factor):                                                                                                                         
        super().__init__(x, y, CYAN, "Inky", pacman, maze_layout, speed_factor)                                                                                                          
                                                                                                                                                                                        
    def get_target_tile(self, pacman_pos, pacman_direction, blinky_pos):                                                                                                                 
        # Inky (Cyan Ghost): Has a more complex behavior, targeting an area between Pac-Man and Blinky's current location.                                                               
        if blinky_pos is None: # Should not happen if Blinky exists and is passed correctly                                                                                              
            return pacman_pos # Fallback to chasing Pac-Man if Blinky's position is unknown                                                                                              
                                                                                                                                                                                        
        # 1. Get tile 2 in front of Pac-Man                                                                                                                                              
        pacman_ahead_x = pacman_pos[0] + pacman_direction[0] * 2                                                                                                                         
        pacman_ahead_y = pacman_pos[1] + pacman_direction[1] * 2                                                                                                                         
                                                                                                                                                                                        
        # Special case for UP direction (Inky's target bug)                                                                                                                              
        if pacman_direction == UP:                                                                                                                                                       
            pacman_ahead_x -= 2                                                                                                                                                          
                                                                                                                                                                                        
        # 2. Create a vector from Blinky's position to this "2-ahead" tile                                                                                                               
        vec_x = pacman_ahead_x - blinky_pos[0]                                                                                                                                           
        vec_y = pacman_ahead_y - blinky_pos[1]                                                                                                                                           
                                                                                                                                                                                        
        # 3. Double this vector and add it to Blinky's position to get Inky's target                                                                                                     
        target_x = blinky_pos[0] + vec_x * 2                                                                                                                                             
        target_y = blinky_pos[1] + vec_y * 2                                                                                                                                             
                                                                                                                                                                                        
        # Clamp target to maze bounds                                                                                                                                                    
        target_x = max(0, min(MAZE_WIDTH - 1, target_x))                                                                                                                                 
        target_y = max(0, min(MAZE_HEIGHT - 1, target_y))                                                                                                                                
        return (target_x, target_y)                                                                                                                                                      
                                                                                                                                                                                        
class Clyde(Ghost):                                                                                                                                                                      
    def __init__(self, x, y, pacman, maze_layout, speed_factor):                                                                                                                         
        super().__init__(x, y, ORANGE, "Clyde", pacman, maze_layout, speed_factor)                                                                                                       
                                                                                                                                                                                        
    def get_target_tile(self, pacman_pos, pacman_direction, blinky_pos=None):                                                                                                            
        # Clyde (Orange Ghost): Alternates between chasing Pac-Man and wandering randomly                                                                                                
        # when he gets too close to Pac-Man (within 8 tiles).                                                                                                                            
        distance_to_pacman = euclidean_distance((self.grid_x, self.grid_y), pacman_pos)                                                                                                  
                                                                                                                                                                                        
        if distance_to_pacman > 8:                                                                                                                                                       
            return pacman_pos # Chase Pac-Man                                                                                                                                            
        else:                                                                                                                                                                            
            return self.scatter_target # Retreat to scatter corner                                                                                                                       
                                                                                                                                                                                        
class GameManager:                                                                                                                                                                       
    def __init__(self):                                                                                                                                                                  
        pygame.init()                                                                                                                                                                    
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))                                                                                                             
        pygame.display.set_caption("Pac-Man (Python)")                                                                                                                                   
        self.clock = pygame.time.Clock()                                                                                                                                                 
        self.font = pygame.font.Font(None, 24) # Default font, size 24                                                                                                                   
                                                                                                                                                                                        
        self.game_state = GAME_STATE_MENU                                                                                                                                                
        self.reset_game()                                                                                                                                                                
                                                                                                                                                                                        
    def reset_game(self):                                                                                                                                                                
        """Initializes all game elements for a new game."""                                                                                                                              
        self.maze_layout = [row[:] for row in initial_maze_layout] # Deep copy of the maze                                                                                               
        self.pacman = PacMan(PACMAN_START_POS[0], PACMAN_START_POS[1], self.maze_layout)                                                                                                 
                                                                                                                                                                                        
        # Count pellets for level completion                                                                                                                                             
        self.total_pellets = sum(row.count(2) + row.count(3) for row in self.maze_layout)                                                                                                
        self.pellets_left = self.total_pellets                                                                                                                                           
        self.current_level = 1                                                                                                                                                           
        self.ghost_eaten_count = 0 # For scoring multiplier during frightened mode                                                                                                       
        self.power_pellet_duration = 7 * 60 # 7 seconds at 60 FPS                                                                                                                        
        self.ghost_speed_factor = 1.0 # Base speed factor, increases with levels                                                                                                         
                                                                                                                                                                                        
        # Initialize ghosts                                                                                                                                                              
        # Pass the same PacMan instance to all ghosts so they can target it                                                                                                              
        self.blinky = Blinky(GHOST_START_POS["Blinky"][0], GHOST_START_POS["Blinky"][1], self.pacman, self.maze_layout, self.ghost_speed_factor)                                         
        self.pinky = Pinky(GHOST_START_POS["Pinky"][0], GHOST_START_POS["Pinky"][1], self.pacman, self.maze_layout, self.ghost_speed_factor)                                             
        self.inky = Inky(GHOST_START_POS["Inky"][0], GHOST_START_POS["Inky"][1], self.pacman, self.maze_layout, self.ghost_speed_factor)                                                 
        self.clyde = Clyde(GHOST_START_POS["Clyde"][0], GHOST_START_POS["Clyde"][1], self.pacman, self.maze_layout, self.ghost_speed_factor)                                             
        self.ghosts = [self.blinky, self.pinky, self.inky, self.clyde]                                                                                                                   
                                                                                                                                                                                        
        self.frightened_mode_active = False # Flag for global frightened state                                                                                                           
                                                                                                                                                                                        
        # Ghost scatter/chase phase timings (in frames at 60 FPS)                                                                                                                        
        # Typical Pac-Man timings: Scatter, Chase, Scatter, Chase, Scatter, Chase, Scatter, Chase (infinite)                                                                             
        # These are usually level-dependent, but fixed for simplicity here.                                                                                                              
        self.scatter_lengths = [7 * 60, 7 * 60, 5 * 60, 5 * 60] # First four scatter phases                                                                                              
        self.chase_lengths = [20 * 60, 20 * 60, 20 * 60, float('inf')] # First three chase phases, last is infinite                                                                      
        self.current_scatter_chase_phase_idx = 0 # Index for phase arrays                                                                                                                
                                                                                                                                                                                        
        self.respawn_all_entities() # Initialize positions and states based on game start                                                                                                
                                                                                                                                                                                        
        # Set initial ghost states for the beginning of the game (first scatter phase)                                                                                                   
        self.scatter_timer = self.scatter_lengths[0]                                                                                                                                     
        self.chase_timer = 0                                                                                                                                                             
        for ghost in self.ghosts:                                                                                                                                                        
            if ghost.name == "Blinky": ghost.is_in_house = False # Blinky starts outside                                                                                                 
            else: ghost.is_in_house = True # Others start inside and will exit                                                                                                           
            ghost.change_state("SCATTER") # All ghosts start new game in scatter mode                                                                                                    
                                                                                                                                                                                        
                                                                                                                                                                                        
    def respawn_all_entities(self):                                                                                                                                                      
        """Resets Pac-Man and all ghosts to their starting positions/states."""                                                                                                          
        self.pacman.reset_pos(self.maze_layout)                                                                                                                                          
        for ghost in self.ghosts:                                                                                                                                                        
            ghost.reset_pos(self.maze_layout)                                                                                                                                            
            # Blinky starts outside, others inside for initial game state or after life loss                                                                                             
            if ghost.name == "Blinky": ghost.is_in_house = False                                                                                                                         
            else: ghost.is_in_house = True                                                                                                                                               
            ghost.change_state("CHASE") # Ghosts start in chase when Pac-Man loses a life or new game                                                                                    
            ghost.direction = UP # Try to exit ghost house                                                                                                                               
                                                                                                                                                                                        
        self.ghost_eaten_count = 0 # Reset multiplier for ghosts                                                                                                                         
        self.frightened_mode_active = False # Ensure frightened mode is off                                                                                                              
                                                                                                                                                                                        
        # Reset phase timers to start of the current level's phase cycle                                                                                                                 
        # This is important when losing a life to restart the chase/scatter cycle                                                                                                        
        self.current_scatter_chase_phase_idx = 0                                                                                                                                         
        if self.current_scatter_chase_phase_idx < len(self.scatter_lengths):                                                                                                             
            self.scatter_timer = self.scatter_lengths[self.current_scatter_chase_phase_idx]                                                                                             
        else: # Should not happen unless all phases completed (e.g. infinite chase)                                                                                                      
            self.scatter_timer = 0                                                                                                                                                      
        self.chase_timer = 0                                                                                                                                                             
                                                                                                                                                                                        
        # All ghosts (except Blinky) should attempt to exit the house if in CHASE/SCATTER at respawn                                                                                     
        for ghost in self.ghosts:                                                                                                                                                        
            if ghost.name != "Blinky":                                                                                                                                                   
                ghost.is_in_house = True                                                                                                                                                 
            ghost.change_state("CHASE") # Revert to chase mode after respawn (will be governed by phase timer)                                                                           
                                                                                                                                                                                        
                                                                                                                                                                                        
    def start_frightened_mode(self):                                                                                                                                                     
        """Activates frightened mode for all ghosts."""                                                                                                                                  
        self.frightened_mode_active = True                                                                                                                                               
        self.ghost_eaten_count = 0 # Reset multiplier for eating consecutive ghosts                                                                                                      
        for ghost in self.ghosts:                                                                                                                                                        
            if ghost.state != "EATEN": # Eaten ghosts remain in EATEN state                                                                                                              
                ghost.change_state("FRIGHTENED", self.pacman.power_pellet_timer)                                                                                                         
                                                                                                                                                                                        
    def end_frightened_mode(self):                                                                                                                                                       
        """Ends frightened mode for all ghosts."""                                                                                                                                       
        self.frightened_mode_active = False                                                                                                                                              
        for ghost in self.ghosts:                                                                                                                                                        
            if ghost.state != "EATEN":                                                                                                                                                   
                # Ghosts revert to their current phase state (CHASE or SCATTER)                                                                                                          
                if self.scatter_timer > 0: # If currently in a scatter phase                                                                                                             
                    ghost.change_state("SCATTER")                                                                                                                                        
                else: # Otherwise, assume it's a chase phase                                                                                                                             
                    ghost.change_state("CHASE")                                                                                                                                          
                                                                                                                                                                                        
    def level_complete(self):                                                                                                                                                            
        """Handles logic for when a level is cleared."""                                                                                                                                 
        self.current_level += 1                                                                                                                                                          
        self.pacman.score += 5000 # Level clear bonus                                                                                                                                    
        self.game_state = GAME_STATE_LEVEL_COMPLETE                                                                                                                                      
        # Increase difficulty for next level                                                                                                                                             
        self.ghost_speed_factor = min(2.0, self.ghost_speed_factor + 0.05) # Ghosts get slightly faster, cap max speed                                                                   
        # Reduce frightened time, minimum 1 second (60 frames)                                                                                                                           
        self.power_pellet_duration = max(60, self.power_pellet_duration - 30)                                                                                                            
                                                                                                                                                                                        
    def reset_for_next_level(self):                                                                                                                                                      
        """Prepares game elements for the next level."""                                                                                                                                 
        self.maze_layout = [row[:] for row in initial_maze_layout] # Re-populate maze with pellets                                                                                       
        self.total_pellets = sum(row.count(2) + row.count(3) for row in self.maze_layout)                                                                                                
        self.pellets_left = self.total_pellets                                                                                                                                           
                                                                                                                                                                                        
        self.respawn_all_entities() # Reset Pac-Man and ghosts positions and states                                                                                                      
                                                                                                                                                                                        
        for ghost in self.ghosts:                                                                                                                                                        
            ghost.set_speed_factor(self.ghost_speed_factor) # Apply new speed factor                                                                                                     
                                                                                                                                                                                        
        # Reset ghost chase/scatter phase timers for the new level                                                                                                                       
        self.current_scatter_chase_phase_idx = 0                                                                                                                                         
        self.scatter_timer = self.scatter_lengths[0] # Start next level with initial scatter phase                                                                                       
        self.chase_timer = 0                                                                                                                                                             
        for ghost in self.ghosts:                                                                                                                                                        
            if ghost.name == "Blinky": ghost.is_in_house = False                                                                                                                         
            else: ghost.is_in_house = True                                                                                                                                               
            ghost.change_state("SCATTER") # Start new level with scatter phase                                                                                                           
                                                                                                                                                                                        
    def update(self):                                                                                                                                                                    
        """Main update loop for game logic."""                                                                                                                                           
        if self.game_state == GAME_STATE_PLAYING:                                                                                                                                        
            self.pacman.update(self.maze_layout, self)                                                                                                                                   
                                                                                                                                                                                        
            # Update ghost chase/scatter timers if not in frightened mode                                                                                                                
            if not self.frightened_mode_active:                                                                                                                                          
                if self.scatter_timer > 0:                                                                                                                                               
                    self.scatter_timer -= 1                                                                                                                                              
                    if self.scatter_timer == 0:                                                                                                                                          
                        self.current_scatter_chase_phase_idx += 1                                                                                                                        
                        if self.current_scatter_chase_phase_idx < len(self.chase_lengths):                                                                                               
                            # Transition to chase phase                                                                                                                                  
                            self.chase_timer = self.chase_lengths[self.current_scatter_chase_phase_idx - 1] # Index aligns with previous scatter                                         
                        else: # After all defined phases, assume infinite chase                                                                                                          
                            self.chase_timer = float('inf')                                                                                                                              
                        for ghost in self.ghosts:                                                                                                                                        
                            if ghost.state not in ["EATEN", "FRIGHTENED"]:                                                                                                               
                                ghost.change_state("CHASE")                                                                                                                              
                elif self.chase_timer > 0:                                                                                                                                               
                    if self.chase_timer != float('inf'): # Infinite chase timer for final phase                                                                                          
                        self.chase_timer -= 1                                                                                                                                            
                    if self.chase_timer == 0:                                                                                                                                            
                        self.current_scatter_chase_phase_idx += 1                                                                                                                        
                        if self.current_scatter_chase_phase_idx < len(self.scatter_lengths):                                                                                             
                            # Transition to scatter phase                                                                                                                                
                            self.scatter_timer = self.scatter_lengths[self.current_scatter_chase_phase_idx]                                                                              
                        # If no more scatter phases defined, the game will remain in infinite chase mode,                                                                                
                        # so self.chase_timer will already be float('inf') or not set, no need to do anything.                                                                           
                        for ghost in self.ghosts:                                                                                                                                        
                            if ghost.state not in ["EATEN", "FRIGHTENED"]:                                                                                                               
                                ghost.change_state("SCATTER")                                                                                                                            
                                                                                                                                                                                        
            # Update ghosts (pass Blinky's position for Inky's AI)                                                                                                                       
            blinky_pos = (self.blinky.grid_x, self.blinky.grid_y)                                                                                                                        
            for ghost in self.ghosts:                                                                                                                                                    
                ghost.update(self.maze_layout, blinky_pos)                                                                                                                               
                                                                                                                                                                                        
                # Collision detection between Pac-Man and ghosts                                                                                                                         
                # Using euclidean distance for more accurate circular collision                                                                                                          
                distance = euclidean_distance((self.pacman.pixel_x, self.pacman.pixel_y), (ghost.pixel_x, ghost.pixel_y))                                                                
                # Collision occurs if distance is less than sum of radii (or slightly less for tighter collision)                                                                        
                collision_threshold = self.pacman.radius + ghost.radius - 5 # Reduced slightly for better feel                                                                           
                                                                                                                                                                                        
                if distance < collision_threshold:                                                                                                                                       
                    if ghost.state == "FRIGHTENED":                                                                                                                                      
                        # Pac-Man eats ghost                                                                                                                                             
                        ghost_points = 200 * (2 ** self.ghost_eaten_count)                                                                                                               
                        self.pacman.score += ghost_points                                                                                                                                
                        self.ghost_eaten_count += 1                                                                                                                                      
                        ghost.change_state("EATEN")                                                                                                                                      
                    elif ghost.state in ["CHASE", "SCATTER"] and not ghost.is_in_house:                                                                                                  
                        # Ghost eats Pac-Man (only if not in ghost house)                                                                                                                
                        self.pacman.lose_life()                                                                                                                                          
                        if self.pacman.lives <= 0:                                                                                                                                       
                            self.game_state = GAME_STATE_GAME_OVER                                                                                                                       
                        else:                                                                                                                                                            
                            self.respawn_all_entities() # Reset positions for a new life                                                                                                 
                            self.end_frightened_mode() # Ensure frightened mode is off (ghosts won't be blue)                                                                            
                    # If ghost.is_in_house is True, it means Pac-Man is trying to enter the ghost house,                                                                                 
                    # which should not result in a collision or eating.                                                                                                                  
                    # Or if Pac-Man catches an 'EATEN' ghost, nothing happens (it's already eaten/respawning)                                                                            
                                                                                                                                                                                        
    def draw_maze(self):                                                                                                                                                                 
        """Draws the maze layout (walls, pellets, power pellets) on the screen."""                                                                                                       
        for y in range(MAZE_HEIGHT):                                                                                                                                                     
            for x in range(MAZE_WIDTH):                                                                                                                                                  
                tile_type = self.maze_layout[y][x]                                                                                                                                       
                # Ensure rect coordinates are integers                                                                                                                                   
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)                                                                                                   
                                                                                                                                                                                        
                if tile_type == 1: # Wall                                                                                                                                                
                    pygame.draw.rect(self.screen, BLUE, rect)                                                                                                                            
                elif tile_type == 2: # Pellet                                                                                                                                            
                    pygame.draw.circle(self.screen, WHITE, rect.center, TILE_SIZE // 8)                                                                                                  
                elif tile_type == 3: # Power Pellet                                                                                                                                      
                    pygame.draw.circle(self.screen, WHITE, rect.center, TILE_SIZE // 4)                                                                                                  
                elif tile_type == 4: # Ghost house entry (door line)                                                                                                                     
                    # Draw a white line for the door                                                                                                                                     
                    pygame.draw.line(self.screen, WHITE, (rect.left, rect.centery), (rect.right, rect.centery), 2)                                                                       
                # Ghost house internal (5) and empty corridors (0) are drawn as black background by default                                                                              
                                                                                                                                                                                        
    def draw_hud(self):                                                                                                                                                                  
        """Draws the Heads-Up Display (score, lives, level) on the screen."""                                                                                                            
        score_text = self.font.render(f"Score: {self.pacman.score}", True, WHITE)                                                                                                        
        lives_text = self.font.render(f"Lives: {self.pacman.lives}", True, WHITE)                                                                                                        
        level_text = self.font.render(f"Level: {self.current_level}", True, WHITE)                                                                                                       
                                                                                                                                                                                        
        self.screen.blit(score_text, (10, SCREEN_HEIGHT - 40))                                                                                                                           
        self.screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, SCREEN_HEIGHT - 40))                                                                                   
        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT - 40))                                                                              
                                                                                                                                                                                        
    def run(self):                                                                                                                                                                       
        """Main game loop for event handling, updates, and drawing."""                                                                                                                   
        running = True                                                                                                                                                                   
        while running:                                                                                                                                                                   
            for event in pygame.event.get():                                                                                                                                             
                if event.type == pygame.QUIT:                                                                                                                                            
                    running = False                                                                                                                                                      
                elif event.type == pygame.KEYDOWN:                                                                                                                                       
                    if self.game_state == GAME_STATE_MENU:                                                                                                                               
                        if event.key == pygame.K_RETURN:                                                                                                                                 
                            self.game_state = GAME_STATE_PLAYING                                                                                                                         
                        elif event.key == pygame.K_q:                                                                                                                                    
                            running = False                                                                                                                                              
                    elif self.game_state == GAME_STATE_GAME_OVER:                                                                                                                        
                        if event.key == pygame.K_RETURN:                                                                                                                                 
                            self.reset_game()                                                                                                                                            
                            self.game_state = GAME_STATE_PLAYING                                                                                                                         
                        elif event.key == pygame.K_q:                                                                                                                                    
                            running = False                                                                                                                                              
                    elif self.game_state == GAME_STATE_LEVEL_COMPLETE:                                                                                                                   
                        if event.key == pygame.K_RETURN:                                                                                                                                 
                            self.reset_for_next_level()                                                                                                                                  
                            self.game_state = GAME_STATE_PLAYING                                                                                                                         
                        elif event.key == pygame.K_q:                                                                                                                                    
                            running = False                                                                                                                                              
                    elif self.game_state == GAME_STATE_PLAYING:                                                                                                                          
                        # Player controls for Pac-Man                                                                                                                                    
                        if event.key == pygame.K_UP or event.key == pygame.K_w:                                                                                                          
                            self.pacman.queued_direction = UP                                                                                                                            
                        elif event.key == pygame.K_DOWN or event.key == pygame.K_s:                                                                                                      
                            self.pacman.queued_direction = DOWN                                                                                                                          
                        elif event.key == pygame.K_LEFT or event.key == pygame.K_a:                                                                                                      
                            self.pacman.queued_direction = LEFT                                                                                                                          
                        elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:                                                                                                     
                            self.pacman.queued_direction = RIGHT                                                                                                                         
                                                                                                                                                                                        
            self.screen.fill(BLACK) # Clear screen each frame                                                                                                                            
                                                                                                                                                                                        
            if self.game_state == GAME_STATE_MENU:                                                                                                                                       
                # Display menu screen                                                                                                                                                    
                title_text = self.font.render("PAC-MAN (Python Edition)", True, YELLOW)                                                                                                  
                start_text = self.font.render("Press ENTER to Start", True, WHITE)                                                                                                       
                                                                                                                                                                                        
                # Adjust font size for quit text if title is too large                                                                                                                   
                quit_font = pygame.font.Font(None, 24) # Smaller font for options                                                                                                        
                quit_text = quit_font.render("Press Q to Quit", True, WHITE)                                                                                                             
                                                                                                                                                                                        
                self.screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))                                                                 
                self.screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))                                                                      
                self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))                                                                   
            elif self.game_state == GAME_STATE_PLAYING:                                                                                                                                  
                # Update and draw game elements                                                                                                                                          
                self.update()                                                                                                                                                            
                self.draw_maze()                                                                                                                                                         
                self.pacman.draw(self.screen)                                                                                                                                            
                for ghost in self.ghosts:                                                                                                                                                
                    ghost.draw(self.screen)                                                                                                                                              
                self.draw_hud()                                                                                                                                                          
            elif self.game_state == GAME_STATE_GAME_OVER:                                                                                                                                
                # Display game over screen                                                                                                                                               
                game_over_text = self.font.render("GAME OVER", True, RED)                                                                                                                
                final_score_text = self.font.render(f"Final Score: {self.pacman.score}", True, WHITE)                                                                                    
                restart_text = self.font.render("Press ENTER to Play Again", True, WHITE)                                                                                                
                                                                                                                                                                                        
                # Adjust font size for quit text                                                                                                                                         
                quit_font = pygame.font.Font(None, 24) # Smaller font for options                                                                                                        
                quit_text = quit_font.render("Press Q to Quit", True, WHITE)                                                                                                             
                                                                                                                                                                                        
                self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 70))                                                         
                self.screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 20))                                                     
                self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))                                                             
                self.screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))                                                                   
            elif self.game_state == GAME_STATE_LEVEL_COMPLETE:                                                                                                                           
                # Display level complete screen                                                                                                                                          
                level_complete_text = self.font.render(f"LEVEL {self.current_level -1} COMPLETE!", True, YELLOW)                                                                         
                next_level_text = self.font.render("Press ENTER for Next Level", True, WHITE)                                                                                            
                self.screen.blit(level_complete_text, (SCREEN_WIDTH // 2 - level_complete_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))                                               
                self.screen.blit(next_level_text, (SCREEN_WIDTH // 2 - next_level_text.get_width() // 2, SCREEN_HEIGHT // 2))                                                            
                                                                                                                                                                                        
            pygame.display.flip() # Update the full display surface to the screen                                                                                                        
            self.clock.tick(60) # Limit frame rate to 60 FPS                                                                                                                             
                                                                                                                                                                                        
        pygame.quit() # Uninitialize Pygame modules                                                                                                                                      
                                                                                                                                                                                        
if __name__ == "__main__":                                                                                                                                                               
    game = GameManager()                                                                                                                                                                 
    game.run()    