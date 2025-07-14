import unittest
import tkinter as tk
from model.UVSim import UVSIM
from controller.UVSim_Controller import UVSIM_Controller
from view.UVSim_Gui import UVSIMGUI
from unittest.mock import patch
from io import StringIO

"""
How to run:
PYTHONPATH=./src python -m unittest discover -s tests

"""

class TestUVSIMGUI(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.sim = UVSIM()
        self.gui = UVSIMGUI(self.root, self.sim)
        self.controller = UVSIM_Controller(self.sim, self.gui)

    def tearDown(self):
        self.root.destroy()


## Create test cases here
    def test_set_theme_applies_color(self):
        primary = "#4C721D"
        off = "#FFFFFF"

        self.gui.set_theme(primary, off)
        self.assertEqual(self.gui.root.cget("bg"), primary)

    def test_print_output(self):
        message = "Error UVSIM stopped working..."
        self.gui.print_output(message)
        self.gui.output_box.config(state="normal")
        content = self.gui.output_box.get("1.0" ,tk.END)
        self.gui.output_box.config(state= 'disabled')
        self.assertIn(message, content)