import subprocess
import sys
from arduino.arduino_communication import walk_robot
import pygame
import global_variables
import threading

current_process = None
start_flag: bool = False
stop_flag: bool = False
simulate_flag: bool = False


# Functions to run
def run_simulation():
    global current_process
    current_process = subprocess.Popen(['python', 'Simulation/walk.py'])


def run_robot(arduino):
    if arduino is None:
        print("Not connected to robot")
    else:
        global current_process
        global_variables.PAUSE_ROBOT = False  # Reset pause_robot
        # current_process = walk_robot(arduino, False)
        current_thread = threading.Thread(target=walk_robot, args=(arduino, False))
        current_thread.start()

def run_function_3():
    print("banana")


def create_window_gui(arduino):
    pygame.init()

    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
    pygame.display.set_caption("Robot Control Center")

    DARK_BLUE = (0, 65, 89)
    AQUA = (101, 168, 196)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    TEAL = (0, 77, 64)

    button_radius = 65
    button_font = pygame.font.SysFont("None", 30)
    title_font = pygame.font.SysFont("Arial", 40, bold=True)  # Change font for the title

    global start_flag, stop_flag, simulate_flag
    start_flag = False
    stop_flag = False
    simulate_flag = False

    def draw_button(text, x, y, color, radius):
        pygame.draw.circle(screen, color, (x, y), radius)
        text_surface = button_font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)
        return pygame.Rect(x - radius, y - radius, 2 * radius, 2 * radius)

    def draw_exit_button(x, y, color, radius):
        pygame.draw.line(screen, color, (x - radius, y - radius), (x + radius, y + radius), 15)
        pygame.draw.line(screen, color, (x + radius, y - radius), (x - radius, y + radius), 15)
        return pygame.Rect(x - radius, y - radius, 2 * radius, 2 * radius)

    def exit_action():
        pygame.quit()
        sys.exit()

    running = True
    while running:
        screen.fill(AQUA)

        # Draw title
        title_text = title_font.render("Robot Control Center", True, TEAL)  # Change title color to TEAL
        title_rect = title_text.get_rect(center=(screen_width // 2, 50))
        screen.blit(title_text, title_rect)

        start_button = draw_button("Start", screen_width // 4, screen_height // 2, DARK_BLUE, button_radius)
        stop_button = draw_button("Stop", screen_width // 2, screen_height // 2, DARK_BLUE, button_radius)
        simulate_button = draw_button("Simulate", 3 * screen_width // 4, screen_height // 2, DARK_BLUE, button_radius)
        exit_button = draw_exit_button(screen_width - button_radius - 10, button_radius + 10, BLACK,
                                       button_radius // 2 - 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_pos):
                    if current_process:
                        current_process.terminate()  # Terminate the current process if any
                    global_variables.PAUSE_ROBOT = True  # Set pause_robot to True
                    run_robot(arduino)  # Start simulation
                elif stop_button.collidepoint(mouse_pos):
                    if current_process:
                        current_process.terminate()  # Terminate the current process if any
                    global_variables.PAUSE_ROBOT = True  # Set pause_robot to True
                    run_function_3()  # Start function 2
                elif simulate_button.collidepoint(mouse_pos):
                    if current_process:
                        current_process.terminate()  # Terminate the current process if any
                    global_variables.PAUSE_ROBOT = True  # Set pause_robot to True
                    run_simulation()  # Start simulation
                elif exit_button.collidepoint(mouse_pos):
                    exit_action()

        pygame.display.flip()

    pygame.quit()
    sys.exit()
