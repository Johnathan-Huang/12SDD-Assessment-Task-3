import pygame
import sys
import os
import turtle
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import scipy
import spacepy
import poliastro
import astropy
import numpy as np
import pandas
from astropy.time import Time
from astroquery.jplhorizons import Horizons
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QGridLayout, QWidget, QPushButton, QFileDialog

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT =  900, 800
BACKGROUND_COLOUR = 0,0,0
BACKGROUND_COLOUR_2 = 50,50,50
WHITE = (255, 255, 255)
GREEN = (0, 100, 0)
RED = (100, 0, 0)
BLUE = (0, 0, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Sol Simulation")

def display_title_screen():
    title_font = pygame.font.Font("Abel.ttf", 150)
    button_font = pygame.font.Font("Abel.ttf", 50)
    title_text = title_font.render("Sol Simulation", True, WHITE)
    start_button_text = button_font.render("New Simulation", True, WHITE)

    # Calculate button positions
    button_width = 400
    button_height = 100
    button_spacing = 20
    button_y = HEIGHT // 2 - button_height // 2
    button_x = (WIDTH - button_width) // 2

    screen.fill(BACKGROUND_COLOUR)

    # Draw the title text
    title_x = WIDTH // 2 - title_text.get_width() // 2
    screen.blit(title_text, (title_x, 50))

    # Draw the start game button
    start_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    pygame.draw.rect(screen, GREEN, start_button_rect, border_radius=10)
    start_button_text_x = start_button_rect.centerx - start_button_text.get_width() // 2
    start_button_text_y = start_button_rect.centery - start_button_text.get_height() // 2
    screen.blit(start_button_text, (start_button_text_x, start_button_text_y))

    # Save File Selection
    Save_File_button_width = 345
    Save_File_button_height = 100
    Save_File_button_x = (WIDTH - Save_File_button_width) // 2
    Save_File_button_y = (HEIGHT - Save_File_button_height) // 2 + 150  # Move the button below the "Start Game" button
    Save_File_button_rect = pygame.Rect(Save_File_button_x, Save_File_button_y, Save_File_button_width, Save_File_button_height)
    pygame.draw.rect(screen, GREEN, Save_File_button_rect, border_radius=10)
    Save_File_button_text = button_font.render("Save Files", True, WHITE)
    Save_File_button_text_x = Save_File_button_rect.centerx - Save_File_button_text.get_width() // 2
    Save_File_button_text_y = Save_File_button_rect.centery - Save_File_button_text.get_height() // 2
    screen.blit(Save_File_button_text, (Save_File_button_text_x, Save_File_button_text_y))

    pygame.display.flip()

def check_button_click(pos):
    button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 100)
    return button_rect.collidepoint(pos)

def sim_loop():
    global screen, WIDTH, HEIGHT
    player_turn_font = pygame.font.Font("Abel.ttf", 40)
    pygame.mixer.music.stop()
    pygame.mixer.music.load("sounds/maxkomusic-space-technologies.mp3")
    pygame.mixer.music.set_volume(0.05)
    pygame.mixer.music.play(-1)
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

def play_game():
    global screen, WIDTH, HEIGHT # Declare global variables
    pygame.mixer.music.load("sounds/alexander-nakarada-space-ambience.mp3")
    pygame.mixer.music.set_volume(0.05)  # Adjust the volume as needed
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

        if title_screen:
            display_title_screen()

# Start the game
play_game()