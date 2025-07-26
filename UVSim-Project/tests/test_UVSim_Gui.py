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

    def test_update_status_reflects_cpu_state(self):
        self.sim.cpu.accumulator = 1234
        self.sim.cpu.instruction_count = 5
        self.gui.update_status()

        self.assertIn("+1234", self.gui.accumlator_label.cget("text"))
        self.assertIn("04", self.gui.instruction_label.cget("text")) 

    def test_submit_input_sets_io_input(self):
        self.gui.input_entry.insert(0, "+1234")
        self.controller.submit_input()

        self.assertEqual(self.sim.io.input, "+1234")

    def test_memory_scroll(self):

        self.gui.mem_start = 0
        self.controller.next_memory()
        self.assertEqual(self.gui.mem_start, 10)


        self.controller.prev_memory()
        self.assertEqual(self.gui.mem_start, 0)

    def test_create_tab_adds_new_tab(self):
        initial_tab_count = len(self.gui.tab_manager.tabs)
        self.gui.tab_manager.add_tab("New Tab")
        new_tab_count = len(self.gui.tab_manager.tabs)
        self.assertEqual(new_tab_count, initial_tab_count + 1)

    def test_get_active_text_widget(self):
        tab_id = self.gui.tab_manager.add_tab("ActiveTab")
        widget = self.gui.tab_manager.get_active_text_widget()
        self.assertIs(widget, self.gui.tab_manager.tabs[tab_id])

    def test_close_tab_removes_tab(self):
        tab_id = self.gui.tab_manager.add_tab("Close Me")
        initial_count = len(self.gui.tab_manager.tabs)
        self.gui.tab_manager.close_tab(tab_id)
        new_count = len(self.gui.tab_manager.tabs)
        self.assertEqual(new_count, initial_count - 1)

    def test_get_current_editor_returns_correct_widget(self):
        self.gui.tab_manager.add_tab("Editor Tab")
        text_widget = self.gui.tab_manager.get_active_text_widget()
        self.assertIsInstance(text_widget, tk.Text)