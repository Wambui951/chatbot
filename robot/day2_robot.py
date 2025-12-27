import pygame
import sys
import random

pygame.init()

# CONFIGURATION SECTION

WINDOWS_HEIGHT = 800
WINDOWS_WIDTH = 800
GRID_SIZE = 10
CELL_SIZE = WINDOWS_WIDTH // GRID_SIZE

# RGB COLOURS

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
SKY_BLUE = (135, 206, 235)
INDIGO = (100, 100, 255)
GOLDEN = (255, 215, 0)


class Robot():
    # Every robot has
    # name
    # color
    # speed
    # position (x,y)
    # battery percentage
    def __init__(self, name, x, y, speed=1, battery=100, color=RED):
        """constructor runs automatically when an object is created from a class
        it initializes the attributes of the object"""
        self.name = name   # robot name
        self.color = color   # robot color
        self.speed = speed  # robot speed
        self.x = x    # robot position x
        self.y = y    # robot position y
        self.max_battery = battery  # robot max battery
        self.battery = battery  # robot current battery
        self.moves = 0  # number of moves made by the robot

        print(f"Robot {self.name} at position ({self.x}, {self.y})")

    def move_up(self):
        """move the robot up by its speed if within grid bounds and has enough battery (decrease y)"""
        if self.battery > 0 and self.y > 0:
            self.y -= self.speed
            self.battery -= 1
            self.moves += 1
            return True
        return False

    def move_down(self):
        """move the robot down by its speed if within the grid bounds and has enough battery (increase y)"""
        if self.battery > 0 and self.y < GRID_SIZE - 1:
            self.y += self.speed
            self.battery -= 1
            self.moves += 1
            return True
        return False

    def move_left(self):
        """move the robot left by its speed if within the bounds and has enough battery (decrease x)"""
        if self.battery > 0 and self.x > 0:
            self.x -= self.speed
            self.battery -= 1
            self.moves += 1
            return True
        return False

    def move_right(self):
        """move the robot to the right if within the grid bounds and has enough battery (increase x)"""
        if self.battery > 0 and self.x < GRID_SIZE - 1:
            self.x += self.speed
            self.battery -= 1
            self.moves += 1
            return True
        return False

    def recharge(self):
        """recharge the robot to the max battery"""
        if self.battery < self.max_battery:
            self.battery = self.max_battery
            print(f"Robot {self.name} recharged to {self.battery}%")
            return True
        return False

    def move_towards_goal(self, goal_x, goal_y):
        """the robot moves towards the goal position(x, y)
        this is a basic pathfinding algorithm that moves the robot in the direction of the goal"""
        if self.battery <= 0:
            return False
        dx = goal_x - self.x
        dy = goal_y - self.y
        if abs(dx) > abs(dy):
            if dx > 0:
                return self.move_right()
            else:
                return self.move_left()
        else:
            if dy > 0:
                return self.move_down()
            else:
                return self.move_up()

    def get_position(self):
        """returns the current position of the robot as a tuple (x,y)"""
        return (self.x, self.y)

    def get_battery(self):
        """returns the current battery percentage of robot """
        return self.battery

    def get_moves(self):
        """returns the number of moves made by the robot"""
        return self.moves

    def draw(self, screen):
        """draw the robot on the screen at its current position"""
        pixel_x = int(self.x * CELL_SIZE + CELL_SIZE // 2)
        pixel_y = int(self.y * CELL_SIZE + CELL_SIZE // 2)
        # Draw the robot as a circle
        pygame.draw.circle(screen, self.color, (pixel_x, pixel_y), CELL_SIZE // 3)
        # draw robot outline
        pygame.draw.circle(screen, BLACK, (pixel_x, pixel_y), CELL_SIZE // 3, 2)
        # draw name above the robot
        font = pygame.font.Font(None, 18)
        text = font.render(self.name, True, BLACK)
        screen.blit(text, (pixel_x - 20, pixel_y - CELL_SIZE // 2 - 10))

    def get_status(self):
        """returns the robot status as a string"""
        return (
            f"ROBOT {self.name}:\n"
            f"Position: ({self.x}, {self.y})\n"
            f"Battery: {self.battery}%\n"
            f"Moves made: {self.moves}\n"
        )

    def get_info(self):
        """returns robot info in one line - FIXED: Added this method"""
        return f"{self.name}: ({self.x},{self.y}) Battery:{int(self.battery)}% Moves:{self.moves}"

    def is_at_goal(self, goal_x, goal_y):
        """checks if the robot is at the goal position (x,y)"""
        return self.x == goal_x and self.y == goal_y


# SPECIAL ROBOT CLASSES (INHERITANCE)

class FastRobot(Robot):
    """a robot that moves faster than others but uses more battery"""
    def __init__(self, name, x, y, speed=2, battery=80, color=SKY_BLUE):
        super().__init__(name, x, y, speed=speed, battery=battery, color=color)
        self.type = "FAST ROBOT"

    def move_up(self):
        if super().move_up():
            # extra battery drain for fast robot
            self.battery = max(0, self.battery - 1)
            return True
        return False

    def move_down(self):
        if super().move_down():
            self.battery = max(0, self.battery - 1)
            return True
        return False

    def move_left(self):
        if super().move_left():
            self.battery = max(0, self.battery - 1)
            return True
        return False

    def move_right(self):
        if super().move_right():
            self.battery = max(0, self.battery - 1)
            return True
        return False


class StrongRobot(Robot):
    """a robot that can push obstacles out of the way but moves slower and uses less battery"""
    def __init__(self, name, x, y, speed=1, battery=120, color=INDIGO):
        super().__init__(name, x, y, speed=speed, battery=battery, color=color)
        self.type = "STRONG ROBOT"

    def push_obstacle(self, obstacle):
        """pushes an obstacle out of the way if adjacent to it"""
        if (abs(self.x - obstacle.x) <= 1 and self.y == obstacle.y) or (abs(self.y - obstacle.y) <= 1 and self.x == obstacle.x):
            # move the obstacle in the direction away from the robot
            if self.x < obstacle.x:
                obstacle.x += 1
            elif self.x > obstacle.x:
                obstacle.x -= 1
            elif self.y < obstacle.y:
                obstacle.y += 1
            elif self.y > obstacle.y:
                obstacle.y -= 1
            self.battery = max(0, self.battery - 2)  # pushing uses extra battery
            return True
        return False


class ScoutRobot(Robot):
    """a robot that can scan the area around it to detect obstacles and goals"""
    def __init__(self, name, x, y, speed=2, battery=100, color=GOLDEN):
        super().__init__(name, x, y, speed=speed, battery=battery, color=color)
        self.type = "SCOUT ROBOT"
        self.scan_range = 2  # scan range in cells

    def scan_area(self, obstacles, goals):
        """scans the area around the robot to detect obstacles and goals within a scan radius"""
        detected_obstacles = []
        detected_goals = []
        for obstacle in obstacles:
            if abs(self.x - obstacle[0]) <= self.scan_range and abs(self.y - obstacle[1]) <= self.scan_range:
                detected_obstacles.append(obstacle)
        for goal in goals:
            if abs(self.x - goal[0]) <= self.scan_range and abs(self.y - goal[1]) <= self.scan_range:
                detected_goals.append(goal)
        self.battery = max(0, self.battery - 1)  # scanning uses battery
        return detected_obstacles, detected_goals


# SET UP PYGAME WINDOW
screen = pygame.display.set_mode((WINDOWS_WIDTH, WINDOWS_HEIGHT))
pygame.display.set_caption("ROBOT SIMULATION")
clock = pygame.time.Clock()
FPS = 60

font = pygame.font.Font(None, 24)
small_font = pygame.font.Font(None, 18)
large_font = pygame.font.Font(None, 36)

# draw goal and obstacle positions
goals = [
    [9, 9],
    [2, 8],
    [8, 2],
]

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

# create multiple robots
robots = [
    Robot("WAMBUI", 0, 0),
    FastRobot("FAITH", 1, 0),
    StrongRobot("OPTIMUS PRIME", 0, 1),
    ScoutRobot("REX", 1, 1),
]

# KEEP TRACK OF ROBOT SELECTED
selected_robot_index = 0
selected_robot = robots[selected_robot_index]


# GAME CONTROL UNITS
def draw_grid():
    """draw the grid lines on the screen"""
    for x in range(0, WINDOWS_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, WINDOWS_HEIGHT), 1)
    for y in range(0, WINDOWS_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WINDOWS_WIDTH, y), 1)


def draw_goals():
    """draw the goal positions on the grid"""
    for goal in goals:
        pixel_x = int(goal[0] * CELL_SIZE + CELL_SIZE // 2)
        pixel_y = int(goal[1] * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.rect(screen, GREEN, (goal[0] * CELL_SIZE, goal[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.circle(screen, BLACK, (pixel_x, pixel_y), CELL_SIZE // 4, 2)


def draw_obstacles():
    """draw obstacles on the grid """
    for obstacle in obstacles:
        pygame.draw.rect(screen, BLACK, (obstacle[0] * CELL_SIZE, obstacle[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_ui():
    """draw user interface"""
    y_offset = 10
    # title 
    title = large_font.render("ROBOT RACE DEMO", True, BLACK)
    screen.blit(title, (10, y_offset))
    y_offset += 40

    # robot selection indicator
    for i, robot in enumerate(robots):
        color = BLACK if i == selected_robot_index else GRAY

        # robot info
        info = font.render(f"[{i+1}] {robot.get_info()}", True, color)
        screen.blit(info, (10, y_offset))

        # battery bar
        bar_x = 10
        bar_y = y_offset + 20
        bar_width = 200
        bar_height = 10

        # background
        pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_width, bar_height))

        # fill
        fill = int((robot.battery / robot.max_battery) * bar_width)
        if fill > 0:
            pygame.draw.rect(screen, robot.color, (bar_x, bar_y, fill, bar_height))

        # BORDER
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_width, bar_height), 1)
        y_offset += 40

    # instructions
    y_offset = WINDOWS_HEIGHT - 100
    instructions = [
        "keys: 1, 2, 3, 4 - Select Robot",
        "Arrows - Move selected",
        "SPACE - auto-move ALL",
        "R - Reset | ESC - Quit"
    ]

    for instruction in instructions:
        text = font.render(instruction, True, BLACK)
        screen.blit(text, (10, y_offset))
        y_offset += 20


def reset_robots():
    """reset all robots to start point"""
    global robots, selected_robot_index, selected_robot
    robots = [
        Robot("WAMBUI", 0, 0,  color = RED),
        FastRobot("FAITH", 1, 0),
        StrongRobot("OPTIMUS PRIME", 0, 1),
        ScoutRobot("REX", 1, 1)
    ]
    selected_robot_index = 0
    selected_robot = robots[selected_robot_index]
    print("\nAll robots reset!")


# MAIN GAME LOOP
game_running = True
auto_mode = False

print("="*60)
print("DAY2: ROBOT CLASSES & OBJECT ORIENTED PROGRAMMING")
print("="*60)
print("\nYou created 4 different robots: ")
for robot in robots:
    print(f" - {robot.name} ({robot.__class__.__name__})")
print("\nControls: ")
print(" 1, 2, 3, 4 - select robot")
print(" Arrow keys - move the selected robot")
print(" Space  - Auto-Move all robots")
print(' R - reset')
print("="*60)

while game_running:
    # handles input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_running = False
            
            if event.key == pygame.K_r:
                reset_robots()
            
            # Select robots
            if event.key == pygame.K_1:
                selected_robot_index = 0
                selected_robot = robots[selected_robot_index]
                print(f"Selected: {selected_robot.name}")
            
            if event.key == pygame.K_2:
                selected_robot_index = 1
                selected_robot = robots[selected_robot_index]
                print(f"Selected: {selected_robot.name}")
            
            if event.key == pygame.K_3:
                selected_robot_index = 2
                selected_robot = robots[selected_robot_index]
                print(f"Selected: {selected_robot.name}")
            
            if event.key == pygame.K_4:
                selected_robot_index = 3
                selected_robot = robots[selected_robot_index]
                print(f"Selected: {selected_robot.name}")
            
            # automode
            if event.key == pygame.K_SPACE:
                auto_mode = not auto_mode
                print(f"Auto-mode: {'ON' if auto_mode else 'OFF'}")
            
            # MANUAL movement
            if not auto_mode:
                if event.key == pygame.K_UP:
                    if selected_robot.move_up():
                        print(selected_robot.get_info())
                
                if event.key == pygame.K_DOWN:
                    if selected_robot.move_down():
                        print(selected_robot.get_info())
                
                if event.key == pygame.K_LEFT:
                    if selected_robot.move_left():
                        print(selected_robot.get_info())
                
                if event.key == pygame.K_RIGHT:
                    if selected_robot.move_right():
                        print(selected_robot.get_info())

    # UPDATE GAME STATE
    # AUTO MODE all robots move toward the goal
    if auto_mode:
        for robot in robots:
            # Move toward first goal in list
            if len(goals) > 0:
                robot.move_towards_goal(goals[0][0], goals[0][1])
    
    # check if any robot reached goal
    for robot in robots:
        if len(goals) > 0:
            if robot.is_at_goal(goals[0][0], goals[0][1]):
                # you can add celebration here
                pass

    # DRAW EVERYTHING
    screen.fill(WHITE)

    draw_grid()
    draw_goals()
    draw_obstacles()
    
    # DRAW all robots
    for robot in robots:
        robot.draw(screen)

    # highlight the selected robot
    pixel_x = int(selected_robot.x * CELL_SIZE + CELL_SIZE // 2)
    pixel_y = int(selected_robot.y * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.circle(screen, (255, 255, 0), (pixel_x, pixel_y), CELL_SIZE // 2, 3)

    draw_ui()

    # auto mode indicator
    if auto_mode:
        auto_text = large_font.render("AUTO MODE", True, GREEN)
        screen.blit(auto_text, (WINDOWS_WIDTH // 2 - 80, 10))

    # UPDATE DISPLAY
    pygame.display.flip()
    clock.tick(FPS)

# ENDING GAME
pygame.quit()
sys.exit()
print("\nGOOD MORNING!! Great work!")