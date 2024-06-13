import pygame
import sys
import math
import pygame.gfxdraw

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 800
BACKGROUND_COLOUR = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
GREENHOVER = (0, 80, 0)
RED = (100, 0, 0)
BLUE = (0, 0, 100)
YELLOW = (255, 255, 0)
GREY = (100, 100, 100)
GREYHOVER = (80, 80, 80)
BROWN = (139, 69, 19)

icon_image = pygame.image.load("images/literallysun2.png")
pygame.display.set_icon(icon_image)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sol Simulation")

distance_font = pygame.font.Font("Abel.ttf", 25)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = int(self.x * self.SCALE + WIDTH / 2)
        y = int(self.y * self.SCALE + HEIGHT / 2)

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit[-50:]:  # Limit to last 50 points for performance
                x, y = point
                x = int(x * self.SCALE + WIDTH / 2)
                y = int(y * self.SCALE + HEIGHT / 2)
                updated_points.append((x, y))

            pygame.draw.aalines(win, self.color, False, updated_points, 1)

        pygame.gfxdraw.aacircle(win, x, y, self.radius, self.color)
        pygame.gfxdraw.filled_circle(win, x, y, self.radius, self.color)

        if not self.sun:
            distance_text = distance_font.render(f"{round(self.distance_to_sun / 1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def display_title_screen():
    title_font = pygame.font.Font("Abel.ttf", 150)
    button_font = pygame.font.Font("Abel.ttf", 50)
    title_text = title_font.render("Sol Simulation", True, WHITE)
    start_button_text = button_font.render("New Simulation", True, WHITE)

    button_width = 400
    button_height = 100
    button_y = HEIGHT // 2 - button_height // 2
    button_x = (WIDTH - button_width) // 2

    screen.fill(BACKGROUND_COLOUR)

    title_x = WIDTH // 2 - title_text.get_width() // 2
    screen.blit(title_text, (title_x, 50))

    start_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    mouse_pos = pygame.mouse.get_pos()
    if start_button_rect.collidepoint(mouse_pos):
        start_button_colour = GREENHOVER
    else:
        start_button_colour = GREEN

    pygame.draw.rect(screen, start_button_colour, start_button_rect, border_radius=10)
    start_button_text_x = start_button_rect.centerx - start_button_text.get_width() // 2
    start_button_text_y = start_button_rect.centery - start_button_text.get_height() // 2
    screen.blit(start_button_text, (start_button_text_x, start_button_text_y))

    Save_File_button_width = 345
    Save_File_button_height = 100
    Save_File_button_x = (WIDTH - Save_File_button_width) // 2
    Save_File_button_y = (HEIGHT - Save_File_button_height) // 2 + 150
    Save_File_button_rect = pygame.Rect(Save_File_button_x, Save_File_button_y, Save_File_button_width, Save_File_button_height)
    if Save_File_button_rect.collidepoint(mouse_pos):
        Save_File_button_colour = GREENHOVER
    else:
        Save_File_button_colour = GREEN
    pygame.draw.rect(screen, Save_File_button_colour, Save_File_button_rect, border_radius=10)
    Save_File_button_text = button_font.render("Save Files", True, WHITE)
    Save_File_button_text_x = Save_File_button_rect.centerx - Save_File_button_text.get_width() // 2
    Save_File_button_text_y = Save_File_button_rect.centery - Save_File_button_text.get_height() // 2
    screen.blit(Save_File_button_text, (Save_File_button_text_x, Save_File_button_text_y))

    pygame.display.flip()

def check_button_click(pos):
    button_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 50, 400, 100)
    return button_rect.collidepoint(pos)

def check_save_file_click(pos):
    Save_File_button_rect = pygame.Rect(WIDTH // 2 - 172, HEIGHT // 2 + 150, 345, 100)
    return Save_File_button_rect.collidepoint(pos)

def check_info_click(pos):
    info_button_rect = pygame.Rect(WIDTH // 2 - 172, HEIGHT // 2 + 300, 345, 100)
    return info_button_rect.collidepoint(pos)

def infoscreen():
    info_font = pygame.font.Font("Abel.ttf", 50)
    info_title = info_font.render("Info", True, WHITE)
    screen.blit(info_title, (WIDTH // 2 - info_title.get_width() // 2, 50))
    # Additional info screen content can be added here
    pygame.display.flip()

def sim_loop():
    global screen, WIDTH, HEIGHT
    pygame.mixer.music.stop()
    pygame.mixer.music.load("sounds/maxkomusic-space-technologies.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, BROWN, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    clock = pygame.time.Clock()
    show_info_screen = False  # Flag to indicate if the info screen should be displayed

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_info_click(event.pos):
                    show_info_screen = not show_info_screen

        if show_info_screen:
            infoscreen()
        else:
            screen.fill(BACKGROUND_COLOUR)
            
            for planet in planets:
                planet.update_position(planets)
                planet.draw(screen)

            # Draw info button
            mouse_pos = pygame.mouse.get_pos()
            info_button_rect = pygame.Rect(WIDTH // 2 - 172, HEIGHT // 2 + 300, 345, 100)
            if info_button_rect.collidepoint(mouse_pos):
                info_button_colour = GREYHOVER
            else:
                info_button_colour = GREY
            pygame.draw.rect(screen, info_button_colour, info_button_rect, border_radius=10)

        pygame.display.flip()
        clock.tick(60)  # Limit frame rate to 60 FPS

def save_screen():
    pass
    
def play_game():
    global screen, WIDTH, HEIGHT
    pygame.mixer.music.load("sounds/alexander-nakarada-space-ambience.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)
    title_screen = True

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            if title_screen and event.type == pygame.MOUSEBUTTONDOWN:
                if check_button_click(event.pos):
                    title_screen = False
                    sim_loop()
                elif check_save_file_click(event.pos):
                    title_screen = False
                    save_screen()

        if title_screen:
            display_title_screen()

# Start the game
play_game()
