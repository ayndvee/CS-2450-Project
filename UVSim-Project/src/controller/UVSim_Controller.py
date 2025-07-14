import time
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import threading
import json
import os

DEFAULT_PRIMARY = "#4C721D"
DEFAULT_OFF = "#FFFFFF"
CONFIG_FILE = CONFIG_FILE = os.path.join(os.path.dirname(__file__), '..', 'config.json')

class UVSIM_Controller:
    def __init__(self, sim, view):
        self.sim = sim
        self.cpu = sim.cpu
        self.memory = sim.memory
        self.io = sim.io
        self.view = view
        self.running = False
        self.paused = False
        self.waiting_input = False
        self.recieved_input = False
        self.view.bind_controller(self)
        self.root = self.view.root  

        self.apply_theme()

    def run(self):
        """Run program continuously on the main thread using Tk.after."""
        self.io.gui = True
        if self.running:
            return  # Already running
        self.running = True
        self.paused = False
        self._execute_step()

    def _execute_step(self):
        if self.running and self.cpu.running and not self.paused:
            self.step()
            if self.io.output:
                self.view.print_output(f"Output: {self.io.outputValue}")
                self.io.output = False
                self.io.outputValue = ""
            self.view.update_display()
            self.root.after(500, self._execute_step)  # Schedule next step in 500ms
        else:
            self.running = False  # Clean up when done

    def step(self):
        """Execute a single instruction and update GUI."""
        self.io.gui = True
        try:
            if not self.cpu.running:
                self.view.print_output("Simulator is not running. Please run the program first.")
                return
            if self.cpu.running:
                code, op = divmod(self.memory.memory[self.cpu.instruction_count], 100)
                method = self.cpu.OPCODES.get(code)
                if method is None:
                    raise RuntimeError(f"Unknown opcode: {code}")
                if code == 10:
                    if not self.waiting_input and not self.recieved_input:
                        self.view.print_output("Waiting for input...")
                        self.waiting_input = True
                        self.cpu.running = False
                        self.view.update_display()
                        
                    self.recieved_input = False
                        
                handler = getattr(self.cpu, method)
                handler(op)
                self.cpu.instruction_count += 1
                self.view.update_display()
        except ZeroDivisionError as e:
            self.view.print_output(f"Error: {e}")
            self.pause()
        except Exception as e:
            self.view.print_output(f"Execution error: {e}")
            self.pause()

    def pause(self):
        """Pause program execution."""
        self.paused = True
        self.running = False
        self.cpu.running = False  # Stop the simulator
        self.view.print_output("Program has been paused")

    # Resets the simulator to its initial state
    def reset(self):
        self.running = False
        self.paused = False
        self.waiting_input = False
        self.cpu.reset()
        self.view.print_output("Program has been reset.")
        self.view.update_display()

    def load_program(self):
        ##This opens up the file explorer for the user to select a file
        file_path = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
        if file_path:
            if self.sim.read_file(file_path):
                self.view.print_output("File read successfully")
                self.view.update_display()

            else:
                self.view.print_output("File couldn't be read")

    #Gets the 10 previous Memory locations
    def prev_memory(self):
        self.view.mem_start = max(0, self.view.mem_start - 10)
        self.view.update_display()

    #Gets the 10 next Memory locations
    def next_memory(self):
        self.view.mem_start = min(len(self.memory.memory) - 10, self.view.mem_start + 10)
        self.view.update_display()

    # Submits the input from the input entry box to the simulator
    def submit_input(self):
        self.io.input = self.view.input_entry.get()
        if (self.cpu.instruction_count >= 0):
            self.cpu.instruction_count -= 1  # Decrement instruction count to reprocess the read instruction
        self.waiting_input = False
        self.cpu.running = True  # Set running to True to allow execution
        self.recieved_input = True
        self.run()
        self.view.update_display()        


    ## THEME RELATED CODE

    def apply_theme(self):
        """
        Applies the theme to the GUI.
        If there is no theme given it will just use the defaults
        """
        theme = self.load_theme()
        if theme:
            primary_color = theme.get("primary_color", DEFAULT_PRIMARY)
            off_color = theme.get("off_color", DEFAULT_OFF)
        else:
            primary_color, off_color = DEFAULT_PRIMARY, DEFAULT_OFF
        
        self.view.set_theme(primary_color, off_color)

    def load_theme(self):
        """
        LOADS the theme from the config file to apply it.
        """
        try:
            with open(CONFIG_FILE, 'r') as file:
                return json.load(file)
        except Exception:
            return None
    def change_theme(self):
        """
        Opens a color picker for user to select new primary and off color theme

        Applies the color immediately to the GUI and saves them to the config file so it is saved
        between closing and opening the GUI.
        
        """
        primary = colorchooser.askcolor(title="Choose Primary Color")[1]
        if not primary: return
        off = colorchooser.askcolor(title= "Choose Off Color")[1]
        if not off: return
        self.view.set_theme(primary, off)
        self.save_theme(primary, off)  
        
    def save_theme(self, primary_color, off_color):
        """
        Saves the given color thme to the config file and applies them to the GUI
        """

        config = {
            "primary_color": primary_color,
            "off_color": off_color
        }
        try:
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=4)
            self.theme = config
            self.view.set_theme(primary_color, off_color)
            self.view.print_output("Theme saved and applied")
        except Exception as e:
            self.view.print_output(f"Failed to save theme: {e}")

    def reset_theme(self):
        """
        Resets the theme to default colors and updates config
        """
        self.save_theme(DEFAULT_PRIMARY, DEFAULT_OFF)

    def save_file(self):
        """
        Saves the current memory state to a file.
        """
        ##This opens up the file explorer for the user to select a file
        file_path = filedialog.asksaveasfile(defaultextension='.txt', filetypes=[("Text File", "*.txt")])
        if file_path:
            if self.sim.save_file(file_path.name):
                self.view.print_output("File saved successfully")
                self.view.update_display()

            else:
                self.view.print_output("File couldn't be saved")