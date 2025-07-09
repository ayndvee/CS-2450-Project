import time
from tkinter import filedialog, messagebox
import threading
import json

DEFAULT_PRIMARY = "#4C721D"
DEFAULT_OFF = "#FFFFFF"

class UVSIM_Controller:
    def __init__(self, sim, view):
        self.sim = sim
        self.view = view
        self.running = False
        self.paused = False
        self.waiting_input = False
        self.view.bind_controller(self)

        self.apply_theme()

    def run(self):
        """Run program continuously in a separate thread."""
        self.sim.gui = True
        if getattr(self, "running", False):
            return  # Already running
        self.running = True
        self.paused = False

        def execute_loop():
            while self.running and self.sim.running:
                if self.paused:
                    break
                self.step()
                if (self.sim.output):
                    self.view.print_output(f"Output: {self.sim.outputValue}")
                    self.sim.output = False
                    self.sim.outputValue = ""
                self.view.update_display()
                time.sleep(0.5)  # Adjust execution speed here
            self.running = False  # Clean up when done

        threading.Thread(target=execute_loop, daemon=True).start()

    def step(self):
        """Execute a single instruction and update GUI."""
        try:
            if self.sim.running:
                code, op = divmod(self.sim.memory[self.sim.instruction_count], 100)
                method = self.sim.OPCODES.get(code)
                if method is None:
                    raise RuntimeError(f"Unknown opcode: {code}")
                if code == 10:
                    if not self.waiting_input:
                        self.view.print_output("Waiting for input...")
                        self.waiting_input = True
                        self.sim.running = False
                        
                
                handler = getattr(self.sim, method)
                handler(op)
                self.sim.instruction_count += 1
                self.view.update_display()
        except ZeroDivisionError as e:
            self.print_output(f"Error: {e}")
            self.pause()
        except Exception as e:
            self.print_output(f"Execution error: {e}")
            self.pause()

    def pause(self):
        """Pause program execution."""
        self.paused = True
        self.running = False
        self.sim.running = False  # Stop the simulator
        self.view.print_output("Program has been paused")

    # Resets the simulator to its initial state
    def reset(self):
        self.running = False
        self.paused = False
        self.waiting_input = False
        self.sim.reset()
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
        self.view.mem_start = min(len(self.sim.memory) - 10, self.view.mem_start + 10)
        self.view.update_display()

    # Submits the input from the input entry box to the simulator
    def submit_input(self):
        self.sim.input = self.view.input_entry.get()
        if (self.sim.instruction_count >= 0):
            self.sim.instruction_count -= 1  # Decrement instruction count to reprocess the read instruction
        
        self.sim.running = True  # Set running to True to allow execution
        self.run()
        self.view.update_display()
        self.waiting_input = False


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
            with open('../config.json', 'r') as file:
                return json.load(file)
        except Exception:
            return None
        
        
    def save_theme(self, primary_color, off_color):
        config = {
            "primary_color": primary_color,
            "off_color": off_color
        }
        try:
            with open('../config.json', 'w') as f:
                json.dump(config, f, indent=4)
            self.theme = config
            self.view.set_theme(primary_color, off_color)
            self.view.print_output("Theme saved and applied")
        except Exception as e:
            self.view.print_output(f"Failed to save theme: {e}")