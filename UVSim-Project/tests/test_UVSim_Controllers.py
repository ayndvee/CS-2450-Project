import unittest
import tkinter as tk
from model.UVSim import UVSIM
from controller.ExecutionController import ExecutionController
from view.UVSim_Gui import UVSIMGUI
from globals.Util import Globals

class TestUVSimController(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.sim = UVSIM()
        self.view = UVSIMGUI(self.root, self.sim)
        self.controller = ExecutionController(self.sim, self.view)

    def tearDown(self):
        self.root.destroy()

    def test_pause_stops_execution(self):
        self.controller.running = True
        self.sim.cpu.running = True
        self.controller.pause()
        self.assertFalse(self.controller.running)
        self.assertFalse(self.sim.cpu.running)
        self.assertTrue(self.controller.paused)

    def test_reset_clears_state_and_resets_cpu(self):
        self.controller.running = True
        self.controller.paused = True
        self.controller.waiting_input = True
        self.sim.cpu.accumulator = 999
        self.controller.reset()
        self.assertFalse(self.controller.running)
        self.assertFalse(self.controller.paused)
        self.assertFalse(self.controller.waiting_input)
        self.assertEqual(self.sim.cpu.accumulator, 0)

    def test_load_from_editor_valid_program(self):
        # Add a tab with valid instructions
        tab_id = self.view.tab_manager.add_tab("Test Tab")
        editor = self.view.tab_manager.tabs[tab_id]
        editor.insert("1.0", "+1234\n+5678\n+0000\n")
        result = self.controller.load_from_editor()
        self.assertTrue(result)
        self.assertEqual(self.sim.memory.memory[0], 1234)
        self.assertEqual(self.sim.memory.memory[1], 5678)

    def test_load_from_editor_invalid_instruction(self):
        tab_id = self.view.tab_manager.add_tab("Bad Tab")
        editor = self.view.tab_manager.tabs[tab_id]
        editor.insert("1.0", "+123\n+56a8\n+0000\n")
        result = self.controller.load_from_editor()
        self.assertFalse(result)

    def test_reload_memory_from_editor_loads_memory(self):
        program = ["+1234", "+5678", "+0000"]
        self.controller.reload_memory_from_editor(program)
        self.assertEqual(self.sim.memory.memory[0], 1234)
        self.assertEqual(self.sim.memory.memory[1], 5678)

    def test_submit_input_accepts_valid_and_rejects_invalid(self):
        self.sim.memory.word_length = Globals.MINWORDLEN
        self.view.input_entry.delete(0, tk.END)
        self.view.input_entry.insert(0, "+1234")
        self.controller.submit_input()
        self.assertEqual(self.sim.io.input, "+1234")

        self.view.input_entry.delete(0, tk.END)
        self.view.input_entry.insert(0, "abcd")
        self.controller.submit_input()
        # sim.io.input should remain as "+1234"
        self.assertEqual(self.sim.io.input, "+1234")

    def test_prev_memory_and_next_memory_adjust_mem_start(self):
        self.view.mem_start = 0
        self.controller.next_memory()
        self.assertGreaterEqual(self.view.mem_start, 0)

        self.controller.prev_memory()
        self.assertLessEqual(self.view.mem_start, 10)

    def test_execute_step_stops_when_not_running_or_paused(self):
        self.controller.running = True
        self.sim.cpu.running = False
        self.controller.paused = False
        self.controller._execute_step()
        self.assertFalse(self.controller.running)

    def test_load_from_editor_success(self):
        tab_id = self.view.tab_manager.add_tab("Test Tab")
        editor = self.view.tab_manager.tabs[tab_id]
        editor.insert("1.0", "+1234\n+5678\n")
        printed = []
        self.controller.view.print_output = lambda msg, *_: printed.append(msg)
        result = self.controller.load_from_editor()
        self.assertTrue(result)
        self.assertTrue(any("Editor contents loaded into memory." in msg for msg in printed))