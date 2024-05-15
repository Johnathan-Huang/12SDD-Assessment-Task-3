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
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())

def clicked():
    print(" Button Clicked ")

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setGeometry(500, 500, 1920, 1080)
        self.setWindowTitle(" Space Simulation ")
        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText(" Placeholder ")
        self.label.move(10,10)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText(" Button 1 ")
        self.b1.move(50,50)
        self.b1.clicked.connect(self.clicked)

    def clicked(self):
        self.label.setText(" Button Clicked ")

window()