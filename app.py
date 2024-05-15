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

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(500, 500, 1920, 1080)
    win.setWindowTitle(" Space Simulation ")

    label = QtWidgets.QLabel(win)
    label.setText(" Placeholder ")
    label.move(10,10)

    b1 = QtWidgets.QPushButton(win)
    b1.setText(" Button 1 ")
    b1.move(50,50)
    b1.clicked.connect(clicked)

    win.show()
    sys.exit(app.exec_())

def clicked():
    print(" Button Clicked ")

window()