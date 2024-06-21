# 12SDD Assessment Task 3 - Solar System Simulation

Solar System Simulation Program Repository Link: https://github.com/Johnathan-Huang/12SDD-Assessment-Task-3

Description: The purpose of this software project is to create a solar system simulation program that depicts the normal or customised movement of major solar system objects in a GUI-based format. This project is small-medium scale, as it is a somewhat complex game being developed by 1 developer. This program may suffer from performance issues after significant runtime. There are customisable values, settings, and save files implemented.

Instructions: To install the project and its dependencies, including prerequisites, install the following languages and extensions:

Python, Pygame, Pygame.gfx draw, math, sys

Usage: 

Run app.py and press new simulation to start the simulation. The grey square button on the right side of the screen can be pressed to show the information screen which shows information about the planets and some values. There is a bug that prevents users from accessing the text input boxes to customise values.

Pressing the 'save files' button shows the possible save files that can be accessed. Saving and accessing save files has not been implemented.

In order to change values, the app.py Planet class or sim_loop() must be accessed. These following variables can be changed to customise the simulation:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 10 / AU  # 1AU = 100 pixels
    TIMESTEP = 3600 * 24  # 1 day
    
    sun = Planet("Sun", 0, 0, 30, YELLOW, 1.98892 * 10**30)
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
    clock.tick(60)

System Requirements:

Minimum:
Requires a 64-bit processor and operating system
OS: Windows 10 (x64) - Windows 11 (x64)
Processor: Intel Core i5-2310
Memory: 4 GB RAM
Graphics: Intel® HD 4400 or equivalent or better
Storage: 1 GB free disk space
Network: None

Recommended:
Requires a 64-bit processor and operating system
OS: Windows 10 (x64) - Windows 11 (x64)
Processor: Intel Core i5-7200U and above
Memory: 6 GB RAM
Graphics: Intel® HD Graphics 620 or equivalent or better
Storage: 2 GB free disk space
Network: None


Authors: Johnathan Huang

Stakeholders: Dean Groom

Credits: 

Space Technologies by MaxKoMusic | https://maxkomusic.com/
Music promoted by https://www.free-stock-music.com
Creative Commons / Attribution-ShareAlike 3.0 Unported (CC BY-SA 3.0)
https://creativecommons.org/licenses/by-sa/3.0/deed.en_US

Space Ambience by Alexander Nakarada | https://www.serpentsoundstudios.com
Music promoted by https://www.free-stock-music.com
Creative Commons / Attribution 4.0 International (CC BY 4.0)
https://creativecommons.org/licenses/by/4.0/

Sound effects from Mixkit | https://mixkit.co/free-sound-effects/

Code from Tech with Tim | Planet Simulation In Python - Tutorial. (2022, February 20). YouTube. Retrieved December 4, 2023, from https://www.youtube.com/watch?v=WTLPmUHTPqo


Contact Information: Johnathan.Huang@education.nsw.gov.au