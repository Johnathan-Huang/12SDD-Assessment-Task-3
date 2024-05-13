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
import numpy
import pandas
import astroquery

p.r += p.v * dt 
acc = -2.959e-4 * p.r / np.sum(p.r**2)**(3./2) # in units of AU/day^2
p.v += acc * dt