from globals.Util import Globals
import tkinter as tk

class ExecutionController:
    """
    Controls the execution flow of the simulator, including stepping, running,
    pausing, and handling GUI interactions with memory and input/output.
    """
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
        self.root = self.view.root

    def run(self):
        """Runs the program contiously"""
        self.io.gui = True
        if self.running:
            return  # Already running
        self.running = True
        self.paused = False
        self._execute_step()

    def _execute_step(self):
        """Recursively executes instructions with delay, updates display, and handles output."""
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
        """Pause program execution and stop the simulator."""
        self.paused = True
        self.running = False
        self.cpu.running = False  # Stop the simulator
        self.view.print_output("Program has been paused")

    # Resets the simulator to its initial state
    def reset(self):
        """Reset the simulator and display to the initial state."""
        self.running = False
        self.paused = False
        self.waiting_input = False
        self.cpu.reset()
        self.view.print_output("Program has been reset.")
        self.view.update_display()

    


    def load_from_editor(self):
        self.sim.memory.clear()
        editor = self.view.get_current_editor()
        if editor is None:
            self.view.print_output("No active editor tab.")
            return False
        raw = editor.get("1.0", tk.END).strip().splitlines()
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
    
    def reload_memory_from_editor(self, content_lines):
        self.sim.memory.clear()
        if self.sim.memory.load_program(content_lines):
            self.view.print_output("Memory reloaded from selected tab.")
            self.view.update_display()
        else:
            self.view.print_output("Could not reload memory from tab content.")

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
            