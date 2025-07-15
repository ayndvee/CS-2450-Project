
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser
import json
from globals.Util import Globals

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
        self.received_input = False
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
            self.root.after(Globals.INTERVAL, self._execute_step)  # Schedule next step in 500ms
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
                    if not self.waiting_input and not self.received_input:
                        self.view.print_output("Waiting for input...")
                        self.waiting_input = True
                        self.cpu.running = False
                        self.view.update_display()
                        
                    self.received_input = False
                        
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
            try:
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                if self.sim.memory.load_program(lines):
                    self.view.print_output("Successfully loaded file")
                    self.view.update_display()
                    editor_content = "".join(lines)
                    if hasattr(self.view, "program_editor"):
                        self.view.program_editor.config(state='normal')
                        self.view.program_editor.delete("1.0", "end")
                        self.view.program_editor.insert("1.0", editor_content)
                        self.view.program_editor.config(state='normal')
                    self.view.update_display()
                        
                else:
                    self.view.print_output("File couldn't be read")
            except Exception as e:
                self.view.print_output(f"Error loading file: {e}")


    def load_from_editor(self):
        raw = self.view.program_editor.get("1.0", tk.END).strip().splitlines()
        if len(raw) > Globals.MEMORYSIZE:
            self.view.print_output("Error: Editor has more than 100 instructions.")
            return False

        for i, line in enumerate(raw):
            line = line.strip()
            if not line or line == Globals.STOP:
                break
            if not line[0] in '+-' or not line[1:].isdigit() or len(line[1:]) != 4:
                self.view.print_output(f"Error on line {i}: Invalid instruction '{line}'")
                return False
            self.memory.memory[i] = int(line)
            self.memory.spareMemory[i] = int(line)
        self.view.print_output("Editor contents loaded into memory.")
        self.view.update_display()
        return True
    
    def cut_text(self, event=None):
        self.copy_text()
        self.program_editor.delete("sel.first", "sel.last")
        return "break"

    def copy_text(self, event=None):
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.program_editor.get("sel.first", "sel.last"))
        except tk.TclError:
            pass
        return "break"

    def paste_text(self, event=None):
        try:
            pasted = self.root.clipboard_get()
            current_text = self.program_editor.get("1.0", tk.END).strip().splitlines()
            if len(current_text) + pasted.count("\n") > 100:
                self.print_output("Paste would exceed 100 lines. Cancelled.")
                return "break"
            self.program_editor.insert(tk.INSERT, pasted)
        except tk.TclError:
            pass
        return "break"

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
        value = self.view.input_entry.get()
        if (value.startswith(('+', '-')) and value[1:].isdigit() and len(value) == 5) or (value[0:].isdigit() and len(value) == 4):
            self.io.input = value
            if (self.cpu.instruction_count >= 0):
                self.cpu.instruction_count -= 1  # Decrement instruction count to reprocess the read instruction
            self.waiting_input = False
            self.cpu.running = True  # Set running to True to allow execution
            self.received_input = True
            self.run()
            self.view.update_display()
        else:
            self.view.print_output("Invalid input format, input should be a signed 4-digit integer")


    ## THEME RELATED CODE

    def apply_theme(self):
        """
        Applies the theme to the GUI.
        If there is no theme given it will just use the defaults
        """
        theme = self.load_theme()
        if theme:
            primary_color = theme.get("primary_color", Globals.DEFAULT_PRIMARY)
            off_color = theme.get("off_color", Globals.DEFAULT_OFF)
        else:
            primary_color, off_color = Globals.DEFAULT_PRIMARY, Globals.DEFAULT_OFF
        
        self.view.set_theme(primary_color, off_color)

    def load_theme(self):
        """
        LOADS the theme from the config file to apply it.
        """
        try:
            with open(Globals.CONFIG_FILE, 'r') as file:
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
            with open(Globals.CONFIG_FILE, 'w') as f:
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
        self.save_theme(Globals.DEFAULT_PRIMARY, Globals.DEFAULT_OFF)

    def save_file(self):
        """
        Saves the current memory state to a file.
        """
        ##This opens up the file explorer for the user to select a file
        try:
            file_path = filedialog.asksaveasfile(defaultextension='.txt', filetypes=[("Text File", "*.txt")])
            if file_path:
                if self.sim.save_file(file_path.name):
                    self.view.print_output("File saved successfully")
                    self.view.update_display()

                else:
                    raise FileNotFoundError
        except Exception as e:
            self.view.print_output(f"Failed to save file: {e}")