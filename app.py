import pygame
import sys
import math
import pygame.gfxdraw

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1500, 900
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
LIGHTBLUE = (0, 191, 255)
DARKYELLOW = (255, 215, 0)
ORANGE = (255, 165, 0)

icon_image = pygame.image.load("images/literallysun2.png")
pygame.display.set_icon(icon_image)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sol Simulation")

distance_font = pygame.font.Font("Abel.ttf", 25)

class Planet:
    #Class representing a planet in the simulation.

    #Attributes:
       # AU (float): Astronomical Unit in meters.
        #G (float): Gravitational constant.
        #SCALE (float): Scale factor for converting AU to pixels.
        #TIMESTEP (int): Time step for the simulation in seconds.
        #name (str): Name of the planet.
        #x (float): X-coordinate of the planet.
        #y (float): Y-coordinate of the planet.
        #radius (int): Radius of the planet.
        #color (tuple): Color of the planet.
        #mass (float): Mass of the planet.
        #orbit (list): List of (x, y) tuples representing the planet's orbit.
        #sun (bool): Whether the planet is the sun.
        #distance_to_sun (float): Distance from the planet to the sun.
        #x_vel (float): X-component of the planet's velocity.
        #y_vel (float): Y-component of the planet's velocity.

    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 10 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day

    def __init__(self, name, x, y, radius, color, mass):
        self.name = name
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
    #Draw the planet on the given window.

    #Args:
    #win (pygame.Surface): The window surface to draw the planet on.

        x = int(self.x * self.SCALE + WIDTH / 2)
        y = int(self.y * self.SCALE + HEIGHT / 2)

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit[-16:]:  # Limit to last 80 points for performance
                x, y = point
                x = int(x * self.SCALE + WIDTH / 2)
                y = int(y * self.SCALE + HEIGHT / 2)
                updated_points.append((x, y))

            pygame.draw.lines(win, self.color, False, updated_points, 2)

        pygame.gfxdraw.aacircle(win, x, y, self.radius, self.color)
        pygame.gfxdraw.filled_circle(win, x, y, self.radius, self.color)

        if not self.sun:
            distance_text = distance_font.render(f"{round(self.distance_to_sun / 150000000000, 2)}AU", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2))

    def attraction(self, other):
        #Calculate the gravitational force exerted on this planet by another planet.

        #Args:
            #other (Planet): The other planet.

        #Returns:
            #tuple: The x and y components of the gravitational force.

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
        #Update the planet's position based on the gravitational forces exerted by other planets.

        #Args:
            #planets (list): List of all planets in the simulation.

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
    #Display the title screen with options to start a new simulation or save files.
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
    #Check if the "New Simulation" button is clicked.
    #Args:
        #pos (tuple): The position of the mouse click.
    #Returns:
        #bool: True if the "New Simulation" button is clicked, False otherwise.
    button_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 50, 400, 100)
    return button_rect.collidepoint(pos)

def check_save_file_click(pos):
    #Check if the "Save Files" button is clicked.
    #Args:
        #pos (tuple): The position of the mouse click.
    #Returns:
        #bool: True if the "Save Files" button is clicked, False otherwise.
    Save_File_button_rect = pygame.Rect(WIDTH // 2 - 172, HEIGHT // 2 + 150, 345, 100)
    return Save_File_button_rect.collidepoint(pos)

def check_save_file_2_click(pos):
    #Check if the "Save File 2" button is clicked.
    #Args:
        #pos (tuple): The position of the mouse click.
    #Returns:
        #bool: True if the "Save File 2" button is clicked, False otherwise.
    save_file2_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 150, 400, 100)
    return save_file2_rect.collidepoint(pos)

def check_save_file_3_click(pos):
    #Check if the "Save File 3" button is clicked.
    #Args:
        #pos (tuple): The position of the mouse click.
    #Returns:
        #bool: True if the "Save File 3" button is clicked, False otherwise.
    save_file3_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 + 300, 400, 100)
    return save_file3_rect.collidepoint(pos)

def check_info_click(pos):
    #Check if the "info" button is clicked.
    #Args:
        #pos (tuple): The position of the mouse click.
    #Returns:
        #bool: True if the "info" button is clicked, False otherwise.
    info_button_rect = pygame.Rect(WIDTH - 100, HEIGHT // 2 - 50 , 100, 100)
    return info_button_rect.collidepoint(pos)

def check_save_file_1_click(pos):
    #Check if the "Save File 1" button is clicked.
    #Args:
        #pos (tuple): The position of the mouse click.
    #Returns:
        #bool: True if the "Save File 1" button is clicked, False otherwise.
    save_file1_rect = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 50, 400, 100)
    return save_file1_rect.collidepoint(pos)

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = WHITE
        self.text = text
        self.font = pygame.font.Font(None, 32)
        self.active = False  # Track if the input box is active (clicked on)
        self.update_text_surface()

    def update_text_surface(self):
        rounded_text = f"{float(self.text):.2e}" if self.text else ""
        self.txt_surface = self.font.render(rounded_text, True, self.color)
        self.txt_surface_rect = self.txt_surface.get_rect()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = WHITE if self.active else GREY

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
            self.update_text_surface()

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect, 2)
        win.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

def infoscreen(planets):
    info_font = pygame.font.Font("Abel.ttf", 50)
    detail_font = pygame.font.Font("Abel.ttf", 25)
    info_title = info_font.render("Info", True, WHITE)
    screen.fill(GREYHOVER)
    screen.blit(info_title, (WIDTH // 4 - info_title.get_width() // 2, 50))  # Title centered

    # Calculate start positions for columns
    start_y_left = 150
    start_y_right = 150

    Astronomical_Unit = f"1 AU = 149.6e6 km"
    Gravitational_Constant = f"Gravitational Constant = {Planet.G:.2e} m^3/kg/s^2"
    Scale = f"Scale = {Planet.SCALE:.2e}"

    au_text = detail_font.render(Astronomical_Unit, True, WHITE)
    gc_text = detail_font.render(Gravitational_Constant, True, WHITE)
    scale_text = detail_font.render(Scale, True, WHITE)

    # Render text in left column
    screen.blit(au_text, (WIDTH // 4 - au_text.get_width() // 2, start_y_left))
    screen.blit(gc_text, (WIDTH // 4 - gc_text.get_width() // 2, start_y_left + 25))
    screen.blit(scale_text, (WIDTH // 4 - scale_text.get_width() // 2, start_y_left + 50))

    input_boxes = []

    # Render planets in left column with input boxes
    for i, planet in enumerate(planets[:5]):  # Render first 5 planets in the left column
        planet_info = f"{planet.name}: Mass={planet.mass:.2e}, Distance to Sun={planet.distance_to_sun / 1.496e11:.2f} AU"
        info_text = detail_font.render(planet_info, True, WHITE)
        screen.blit(info_text, (WIDTH // 4 - info_text.get_width() // 2, start_y_left + 100 + i * 100))

        mass_box = InputBox(WIDTH // 4 - 200, start_y_left + 100 + i * 100 + 45, 140, 32, text=str(planet.mass))
        distance_box = InputBox(WIDTH // 4 + 150, start_y_left + 100 + i * 100 + 45, 140, 32, text=str(round(planet.distance_to_sun / 1.496e11, 2)))

        input_boxes.append((mass_box, distance_box))

        mass_box.draw(screen)
        distance_box.draw(screen)

    # Render planets in right column with input boxes
    start_y_right = 150
    for i, planet in enumerate(planets[5:]):  # Render remaining planets in the right column
        planet_info = f"{planet.name}: Mass={planet.mass:.2e}, Distance to Sun={planet.distance_to_sun / 1.496e11:.2f} AU"
        info_text = detail_font.render(planet_info, True, WHITE)
        screen.blit(info_text, (3 * WIDTH // 4 - info_text.get_width() // 2, start_y_right + i * 100))

        mass_box = InputBox(3 * WIDTH // 4 - 200, start_y_right + i * 100 + 45, 140, 32, text=str(planet.mass))
        distance_box = InputBox(3 * WIDTH // 4 + 150, start_y_right + i * 100 + 45, 140, 32, text=str(round(planet.distance_to_sun / 1.496e11, 2)))

        input_boxes.append((mass_box, distance_box))

        mass_box.draw(screen)
        distance_box.draw(screen)

    mouse_pos = pygame.mouse.get_pos()
    info_button_rect = pygame.Rect(WIDTH - 100, HEIGHT // 2 - 50, 100, 100)
    if info_button_rect.collidepoint(mouse_pos):
        info_button_colour = RED
    else:
        info_button_colour = GREY
    pygame.draw.rect(screen, info_button_colour, info_button_rect, border_radius=10)
    info_button_text = detail_font.render("X", True, WHITE)
    info_button_text_x = info_button_rect.centerx - info_button_text.get_width() // 2
    info_button_text_y = info_button_rect.centery - info_button_text.get_height() // 2
    screen.blit(info_button_text, (info_button_text_x, info_button_text_y))

    pygame.display.flip()

    return input_boxes

def sim_loop():
    global screen, WIDTH, HEIGHT
    pygame.mixer.music.stop()
    pygame.mixer.music.load("sounds/maxkomusic-space-technologies.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)

    sun = Planet("Sun", 0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet("Earth", -1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet("Mars", -1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet("Mercury", 0.387 * Planet.AU, 0, 8, GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet("Venus", 0.723 * Planet.AU, 0, 14, BROWN, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet("Jupiter", 5.203 * Planet.AU, 0, 20, ORANGE, 1.898 * 10**27)
    jupiter.y_vel = -13.07 * 1000

    saturn = Planet("Saturn", 9.582 * Planet.AU, 0, 18, DARKYELLOW, 5.683 * 10**26)
    saturn.y_vel = -9.69 * 1000

    uranus = Planet("Uranus", 19.22 * Planet.AU, 0, 16, LIGHTBLUE, 8.681 * 10**25)
    uranus.y_vel = -6.81 * 1000

    neptune = Planet("Neptune", 30.05 * Planet.AU, 0, 16, BLUE, 1.024 * 10**26)
    neptune.y_vel = -5.43 * 1000

    pluto = Planet("Pluto", 39.48 * Planet.AU, 0, 8, WHITE, 1.309 * 10**22)
    pluto.y_vel = -4.74 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune, pluto]

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
            infoscreen(planets)
        else:
            screen.fill(BACKGROUND_COLOUR)
            
            for planet in planets:
                planet.update_position(planets)
                planet.draw(screen)

            # Draw info button
            mouse_pos = pygame.mouse.get_pos()
            info_button_rect = pygame.Rect(WIDTH - 100, HEIGHT // 2 - 50, 100, 100)
            if info_button_rect.collidepoint(mouse_pos):
                info_button_colour = GREYHOVER
            else:
                info_button_colour = GREY
            pygame.draw.rect(screen, info_button_colour, info_button_rect, border_radius=10)

        pygame.display.flip()
        clock.tick(60)  # Limit frame rate to 60 FPS

def display_save_screen():
    #Display the save file options screen with options to select different save files.
    title_font = pygame.font.Font("Abel.ttf", 150)
    button_font = pygame.font.Font("Abel.ttf", 50)
    title_text = title_font.render("Save Files", True, WHITE)
    save_file1_text = button_font.render("Save File 1", True, WHITE)

    button_width = 400
    button_height = 100
    button_y = HEIGHT // 2 - button_height // 2
    button_x = (WIDTH - button_width) // 2

    screen.fill(BACKGROUND_COLOUR)

    title_x = WIDTH // 2 - title_text.get_width() // 2
    screen.blit(title_text, (title_x, 50))

    save_file1_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    mouse_pos = pygame.mouse.get_pos()
    if save_file1_rect.collidepoint(mouse_pos):
        save_file1_colour = GREYHOVER
    else:
        save_file1_colour = GREY

    pygame.draw.rect(screen, save_file1_colour, save_file1_rect, border_radius=10)
    start_button_text_x = save_file1_rect.centerx - save_file1_text.get_width() // 2
    start_button_text_y = save_file1_rect.centery - save_file1_text.get_height() // 2
    screen.blit(save_file1_text, (start_button_text_x, start_button_text_y))

    save_file2_rect = pygame.Rect(button_x, button_y + 150, button_width, button_height)
    if save_file2_rect.collidepoint(mouse_pos):
        save_file2_colour = GREYHOVER
    else:
        save_file2_colour = GREY

    pygame.draw.rect(screen, save_file2_colour, save_file2_rect, border_radius=10)
    save_file2_text = button_font.render("Save File 2", True, WHITE)
    save_file2_text_x = save_file2_rect.centerx - save_file2_text.get_width() // 2
    save_file2_text_y = save_file2_rect.centery - save_file2_text.get_height() // 2
    screen.blit(save_file2_text, (save_file2_text_x, save_file2_text_y))

    save_file3_rect = pygame.Rect(button_x, button_y + 300, button_width, button_height)
    if save_file3_rect.collidepoint(mouse_pos):
        save_file3_colour = GREYHOVER
    else:
        save_file3_colour = GREY
        
    pygame.draw.rect(screen, save_file3_colour, save_file3_rect, border_radius=10)
    save_file3_text = button_font.render("Save File 3", True, WHITE)
    save_file3_text_x = save_file3_rect.centerx - save_file3_text.get_width() // 2
    save_file3_text_y = save_file3_rect.centery - save_file3_text.get_height() // 2
    screen.blit(save_file3_text, (save_file3_text_x, save_file3_text_y))

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if check_save_file_1_click(event.pos):
                    sim_loop()
                elif check_save_file_2_click(event.pos):
                    sim_loop()
                elif check_save_file_3_click(event.pos):
                    sim_loop()
    
def play_game():
    global screen, WIDTH, HEIGHT
    pygame.mixer.music.load("sounds/alexander-nakarada-space-ambience.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)
    title_screen = True
    save_screen = False

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
                    save_screen = True
                    display_save_screen()

        if title_screen:
            display_title_screen()

# Start the game
play_game()