import cx_Freeze
import win32api
import pygame
import time
import datetime
import numpy
import sys
import os
from PIL import ImageGrab
import xlwt
from tkinter import *

os.environ['TCL_LIBRARY'] = "C:\\Users\\Mix_Tera_Windows10\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Users\\Mix_Tera_Windows10\\AppData\\Local\\Programs\\Python\\Python36\\tcl\\tk8.6"

base = None

if sys.platform == 'win32':
    base='Win32GUI'

executables = [cx_Freeze.Executable("bonelabel2.py", base=None)]

cx_Freeze.setup(
    name="Bone scintigraphy installer",
    options = {"build_exe": {"packages":["numpy"]}},
    version = "0.0.1",
    description = "Trying to get this work",
    executables = executables
)