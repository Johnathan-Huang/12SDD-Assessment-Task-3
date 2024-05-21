import pygame
import math
import pygame.gfxdraw
import numpy as np
from scipy.interpolate import splprep, splev

pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Planet Simulation")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)

FONT = pygame.font.SysFont("comicsans", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600*24 # 1 day

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.orbit_spline = None
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win, orbit_surface):
        x = int(self.x * self.SCALE + WIDTH / 2)
        y = int(self.y * self.SCALE + HEIGHT / 2)

        if len(self.orbit) > 3:  # Ensure we have more than 3 points for splprep
            if not self.orbit_spline or len(self.orbit) > len(self.orbit_spline[0]):
                # Recompute the spline if new points were added
                points = np.array(self.orbit)
                points[:, 0] = points[:, 0] * self.SCALE + WIDTH / 2
                points[:, 1] = points[:, 1] * self.SCALE + HEIGHT / 2

                tck, u = splprep(points.T, s=0, k=3)
                unew = np.linspace(0, 1, num=min(1000, len(self.orbit) * 10), endpoint=True)  # Adjusted for performance
                self.orbit_spline = splev(unew, tck)

            updated_points = [(int(self.orbit_spline[0][i]), int(self.orbit_spline[1][i])) for i in range(len(self.orbit_spline[0]))]
            pygame.draw.aalines(orbit_surface, self.color, False, updated_points)

        pygame.gfxdraw.aacircle(win, x, y, self.radius, self.color)
        pygame.gfxdraw.filled_circle(win, x, y, self.radius, self.color)
        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x - distance_text.get_width()/2, y - distance_text.get_height()/2))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
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

        # Optimize by only adding unique points
        if len(self.orbit) == 0 or (self.x, self.y) != self.orbit[-1]:
            self.orbit.append((self.x, self.y))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000 

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    planets = [sun, earth, mars, mercury, venus]

    # Create a surface for drawing orbits
    orbit_surface = pygame.Surface((WIDTH, HEIGHT))
    orbit_surface.set_colorkey((0, 0, 0))  # Make the background transparent

    while run:
        clock.tick(30)
        WIN.fill((0, 0, 0))
        orbit_surface.fill((0, 0, 0))  # Clear the orbit surface

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN, orbit_surface)

        WIN.blit(orbit_surface, (0, 0))  # Draw the orbit surface onto the main window
        pygame.display.update()

    pygame.quit()

main()
