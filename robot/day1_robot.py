"""
DAY 1: MY First Robot Simulator

A simple grid-based robot that you can control with arrow keys.

HOW TO RUN:
1. Save this file as: day1_robot.py
2. Make sure pygame is installed: pip install pygame
3. Click the Run button  in VS Code, or press F5
4. A window will pop up with your robot!

CONTROLS:
- Arrow keys: Move the robot
- ESC or close window: Exit

YOUR GOAL: Move the blue robot to the green goal!
"""

import pygame
import sys

# Initialize Pygame (this must happen first)
pygame.init()
pygame.mixer.init()

# ============================================
# CONFIGURATION - Change these to experiment!
# ============================================

# Window settings
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
GRID_SIZE = 10  # 10x10 grid
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE  # Size of each grid cell

# Colors (RGB format - Red, Green, Blue from 0-255)
WHITE = (255, 255, 255)      # Background
BLACK = (0, 0, 0)            # Grid lines
BLUE = (0, 100, 255)         # Robot
GREEN = (0, 255, 0)          # Goal
RED = (255, 0, 0)            # Obstacles
GRAY = (200, 200, 200)       # Grid
ORANGE = (255, 165, 0)

#GAME SETTINGS
MAX_BATTERY = 100
BATTERY_DRAIN_PER_MOVE = 1
TOTAL_GOALS = 3
moves_count = 0
# Robot starting position (grid coordinates)
robot_x = 0
robot_y = 0

# Goal position
goals = [
    [9, 9],
    [2, 8],
    [8, 2],
]

# Obstacles (list of [x, y] positions)
obstacles = [
    [0, 3],
    [0, 6],
    [0, 7],
    [1, 2],
    [1, 4],
    [1, 5],
    [1, 8],
    [2, 0],
    [2, 4],
    [2, 9],
    [3, 0],
    [3, 1],
    [3, 3],
    [4, 5],
    [4, 7],
    [4, 0],
    [4, 6],
    [5, 0],
    [5, 2],
    [5, 4],
    [5, 7],
    [5, 9],
    [6, 2],
    [6, 3],
    [7, 1],
    [7, 2],
    [7, 4],
    [7, 6],
    [7, 7],
    [7, 9],
    [8, 4],
    [8, 8],
    [9, 1],
    [9, 3],
    [9, 6],
]

# Movement speed (cells per key press)
move_speed = 1
battery= MAX_BATTERY
moves_count = 0
goals_collected = 0
game_won = False
TOTALGOALS = 3
goals_collected = 0

# ============================================
# SETUP THE GAME WINDOW
# ============================================

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Day 1: Robot Simulator - Use Arrow Keys!")

# Clock to control frame rate
clock = pygame.time.Clock()
FPS = 30  # Frames per second

# Font for displaying text
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# ============================================
# HELPER FUNCTIONS
# ============================================

def draw_grid():
    """Draw the grid lines on the screen"""
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOW_HEIGHT), 1)
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOW_WIDTH, y), 1)

def draw_robot(x, y):
    """Draw the robot as a blue circle"""
    pixel_x = x * CELL_SIZE + CELL_SIZE // 2
    pixel_y = y * CELL_SIZE + CELL_SIZE // 2
    pygame.draw.circle(screen, BLUE, (pixel_x, pixel_y), CELL_SIZE // 3)

def draw_goals():
    """Draw the goal as a green square"""
    pixel_x = goal[0] * CELL_SIZE
    pixel_y = goal[1] * CELL_SIZE
    pygame.draw.rect(screen, GREEN, (pixel_x, pixel_y, CELL_SIZE, CELL_SIZE))

def draw_obstacles():
    """Draw all obstacles as red squares"""
    for obstacle in obstacles:
        pixel_x = obstacle[0] * CELL_SIZE
        pixel_y = obstacle[1] * CELL_SIZE
        pygame.draw.rect(screen, RED, (pixel_x, pixel_y, CELL_SIZE, CELL_SIZE))

def is_obstacle(x, y):
    """Check if position (x, y) has an obstacle"""
    for obstacle in obstacles:
        if obstacle[0] == x and obstacle[1] == y:
            return True
    return False

def is_valid_position(x, y):
    """Check if position is within grid and not an obstacle"""
    if x < 0 or x >= GRID_SIZE or y < 0 or y >= GRID_SIZE:
        return False  # Outside grid
    if is_obstacle(x, y):
        return False  # Hit an obstacle
    return True

def display_text(text, x, y, font_obj, color=BLACK):
    """Display text on screen at position (x, y)"""
    text_surface = font_obj.render(text, True, color)
    screen.blit(text_surface, (x, y))
def play_beep(frequency, duration):
    """paly simple beep sound"""
    sample_rate = 22050
    n_smaples = int(round(duration* sample_rate))
    # craete  asimple sine wave 
    buf = []
    for i in range (n_smaples):
        value = int(127* (1+(i%int(sample_rate / frequency ))/(sample_rate /frequency)))
        buf.append(value)

        sound = pygame.sndarray.make_sound(bytearray(buf))
        sound.play()
        #when collecting goal
        if robot_x == goal[0] and robot_y ==[1]:
            play_beep(800,0.1) #high pitch goal sound
            #when hitting an obstacle 
        else:
            print(f"cannot move there!")
            play_beep(200, 0.1) # low pitch sound for errors

            #when winning 
            if goals_collected >= TOTALGOALS:
                game_won = True
                play_beep(1000, 0.3) #victory sound


def draw_battery_bar():
    bar_x = 10
    bar_y = 100
    bar_width = 200
    bar_height = 20

    #background (empty)
    pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))
    #filled portion(current battery)
    fill_width = int((battery/MAX_BATTERY)*bar_width)
    if battery > 50:
        fill_color = GREEN
    elif battery > 20:
        fill_color = ORANGE
    else:
        fill_color= RED

    pygame.draw.rect(screen, fill_color,  ( bar_x, bar_y, fill_width, bar_height))
        #border 
    pygame.draw.rect(screen, BLACK, (bar_x, bar_y, fill_width, bar_height), 2)
def reset_game():
    """ reset all variables to stating state """
    global robot_x, robot_y, battery, moves_count, goals_collected, game_won, goals
    robot_x = 0
    robot_y = 0
    battery = MAX_BATTERY
    moves_count = 0 
    goals_collected = 0
    game_won = 0 
    goals = 0 
    #rest goal list
    goals = [
    [9, 9],
    [2, 8],
    [8, 2],
]
    print ("\n" + "="*50)
    print("GAME RESET!")
    print("="*50)



# ============================================
# MAIN GAME LOOP
# ============================================
game_running = True
game_won = False

print("=" * 50)
print("ROBOT SIMULATOR STARTED!")
print("=" * 50)
print("Use ARROW KEYS to move the robot")
print(f"Starting position: ({robot_x}, {robot_y})")
print(f"Goal position: ({goals})")
print(f"Obstacles: {len(obstacles)}")
print("=" * 50)

while game_running:
    # ========================================
    # 1. HANDLE EVENTS (keyboard, mouse, etc)
    # ========================================
    
    for event in pygame.event.get():
        # Check if user closed the window
        if event.type == pygame.QUIT:
            game_running = False
        
        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False
            if event.key == pygame.K_r:
                    reset_game()
            
            # Only allow movement if game not won
            if not game_won and battery > 0:
                # Arrow key movement
                new_x = robot_x
                new_y = robot_y
                
                if event.key == pygame.K_UP:
                    new_y = robot_y - move_speed
                    print(f"Trying to move UP to ({new_x}, {new_y})")
                
                elif event.key == pygame.K_DOWN:
                    new_y = robot_y + move_speed
                    print(f"Trying to move DOWN to ({new_x}, {new_y})")
                
                elif event.key == pygame.K_LEFT:
                    new_x = robot_x - move_speed
                    print(f"Trying to move LEFT to ({new_x}, {new_y})")
                
                elif event.key == pygame.K_RIGHT:
                    new_x = robot_x + move_speed
                    print(f"Trying to move RIGHT to ({new_x}, {new_y})")
                
                # Check if new position is valid
                if is_valid_position(new_x, new_y):
                    robot_x = new_x
                    robot_y = new_y
                    moves_count += 1 
                    battery -= BATTERY_DRAIN_PER_MOVE
                    print(f"✓ Moved successfully! Now at ({robot_x}, {robot_y})")
                    battery -= BATTERY_DRAIN_PER_MOVE
                    if battery <0:
                         battery = 0
                   
                    print(f" Battery: {battery}%")
                else:
                    print(f"✗ Cannot move there! (obstacle or out of bounds)")
    
    # ========================================
    # 2. UPDATE GAME STATE
    # ========================================
    
    # Check if robot reached any goal
    for goal in goals[:]:
     if robot_x == goal[0] and robot_y == goal[1]:
         goals.remove(goal) 
         goals_collected += 1
     print(f" Goal collected!({goals_collected}/{TOTALGOALS})")
    if goals_collected >= TOTALGOALS:
        game_won= True
        efficiency = int((battery / moves_count) * 100) if moves_count > 0 else 0 
        print(f"\n YOU WON")
        print(f"Moves: {moves_count}")
        print(f"Battery remaining: {battery}%")
        print(F"efficiency score: {efficiency}")
        battery_text = f"Battery: {battery}%"
        #clour changes based on battery level
        if battery > 50:
            battery_color = GREEN
        elif battery > 20 :
            battery_color = (255, 165, 0)  # orange
        else:
            battery_color = RED
            
        display_text(battery_text,10, 70, small_font, battery_color)
        print("\n" + "=" * 50)
        print("🎉 CONGRATULATIONS! ALL GOALS COLLECTED! YOU WON! 🎉")
        print("=" * 50)
        break
    if battery < 0 and not game_won:
        print("\n BATTERY DEPLETED! GMAE OVER!")
        display_text ("OUT OF POWER !", WINDOW_WIDTH // 2 - 100 , WINDOW_HEIGHT // 2, font, RED)

    
    # ========================================
    # 3. DRAW EVERYTHING
    # ========================================
    
    # Clear screen with white background
    screen.fill(WHITE)
    
    # Draw grid
    draw_grid()

    #draw battery bar
    draw_battery_bar()
    
    # Draw game elements
    draw_goals() # Draw goal first (background)
    draw_obstacles()           # Then obstacles
    draw_robot(robot_x, robot_y)  # Robot on top

    moves_text = f"Moves: {moves_count}"
    display_text(moves_text, WINDOW_WIDTH - 150, 10, small_font)

    # Draw position text
    goal_text = f"Goals: ({goals_collected}/{TOTAL_GOALS})"
    display_text(goal_text, 10, 40, small_font)
    
    # Draw instructions
    instructions = "Arrow Keys to Move |R: Restart | ESC to Exit"
    display_text(instructions, 10, WINDOW_HEIGHT - 30, small_font)
    
    # If game won, show victory message
    if game_won:
        display_text("YOU WON!", WINDOW_WIDTH // 2 - 80, WINDOW_HEIGHT // 2, font, GREEN)
        efficiency = int(battery / moves_count)* 100 if moves_count> 0 else 0
        efficiency_text = f"Efficiency: {efficiency}| Mves: {moves_count}"
        display_text(efficiency_text, WINDOW_WIDTH // 2 - 150 , WINDOW_HEIGHT // 2+ 10, small_font, BLACK)
    
    # ========================================
    # 4. UPDATE DISPLAY
    # ========================================
    
    pygame.display.flip()  # Update the full display
    clock.tick(FPS)  # Limit to FPS frames per second

# ============================================
# CLEANUP
# ============================================

pygame.quit()
sys.exit()

print("\nGame closed. Thanks for playing!")