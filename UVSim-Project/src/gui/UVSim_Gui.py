## UVSim GUI

## IMPORTS
import sys
import os
import tkinter as tk
import threading
import time
from tkinter import filedialog, messagebox
from core.UVSim import UVSIM

class UVSIMGUI:
    def __init__(self, root, sim):
        self.root = root
        self.sim = sim
        self.labels = []
        self.mem_start = 0
        root.title("UVSIM")

        ## Create the memory title and the memory layout
        tk.Label(root, text="Memory").pack(pady=(10, 0))
        memory_frame = tk.LabelFrame(root, padx=10, pady=10, borderwidth=2, relief="groove")
        memory_frame.pack(padx=10, pady=10)

        for row in range(2):
            row_labels = []
            for col in range(5):
                addr_label = tk.Label(memory_frame, text="Addr: --", width= 12)
                val_label = tk.Label(memory_frame, text= "Value: ----",width=14)
                addr_label.grid(row = row*2, column= col, padx=4)
                val_label.grid(row=row*2+1, column=col, padx=4)
                row_labels.append((addr_label,val_label))
            self.labels.append(row_labels)


        ## Creates the previous and Next button and their layout
        navigation = tk.Frame(root)
        navigation.pack(fill=tk.X, pady=5)

        prev_button = tk.Button(navigation, text="Prev 10", command=self.prev_memory)
        prev_button.grid(row=0, column=0, sticky='w', padx=10)

        next_button = tk.Button(navigation, text="Next 10", command=self.next_memory)
        next_button.grid(row=0, column=10, sticky='e', padx=10)

        navigation.grid_columnconfigure(0, weight=1)
        navigation.grid_columnconfigure(1, weight=1)

        ## Creates the accumulator and Instruction # labels and amounts
        status_frame = tk.Frame(root)
        status_frame.pack(pady=5)

        self.accumlator_label = tk.Label(status_frame, text= "Accumulator: +0000", width=20, anchor='w')
        self.accumlator_label.pack(side=tk.LEFT, padx=10)
        
        self.instruction_label = tk.Label(status_frame, text= "Instruction #: 00", width=20, anchor='w')
        self.instruction_label.pack(side=tk.LEFT, padx=10)

        ## Creates the Submit Input text box and button
        input_frame = tk.Frame(root)
        input_frame.pack(pady=5)
        self.input_entry = tk.Entry(input_frame, width=10)
        self.input_entry.pack(side=tk.LEFT, padx=(0,5))
        self.input_button = tk.Button(input_frame, text="Submit Input", command=self.submit_input).pack(side=tk.LEFT)


        ## Creates the Run, Step, Pause, and Reset buttons and has their layout
        control_frame = tk.Frame(root)
        control_frame.pack(fill=tk.X)
        tk.Button(control_frame, text="Run", command=self.run).pack(side=tk.LEFT, padx=30)
        tk.Button(control_frame, text="Step", command=self.step).pack(side=tk.LEFT, padx=80)
        tk.Button(control_frame, text="Pause", command=self.pause).pack(side=tk.LEFT, padx=80)
        tk.Button(control_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=30)

        ## Creates the Load Program Button
        tk.Button(root, text="Load Program", command=self.load_program).pack(pady=5)

        ## Creates the Output label and its box
        tk.Label(root, text="Output:").pack()
        self.output_box= tk.Text(root, height=8, width=50, state='disabled')
        self.output_box.pack()

        self.update_display()

    def update_display(self):
        self.update_memory_display()
        self.update_status()
    def update_memory_display(self):
        # Update memory display for addresses from memory_start to memory_start+9
        for i, row_labels in enumerate(self.labels):
            for j, (addr_label, val_label) in enumerate(row_labels):
                mem_index = self.mem_start + i*5 + j
                try:
                    value = self.sim.memory[mem_index]
                    # Make it a signed 4 digit value
                    value_str = f"{value:+05d}"
                except IndexError:
                    value_str = "----"
                
                addr_label.config(text=f"Addr: {mem_index:02d}")
                val_label.config(text=f"Value: {value_str}")
    def update_status(self):
        # Update accumulator label
        acc_value = getattr(self.sim, "accumulator", 0)
        self.accumlator_label.config(text=f"Accumulator: {acc_value:+05d}")

        # Update instruction number label
        instr_num = getattr(self.sim, "instruction_count", 0)
        if (instr_num > 0):
            instr_num -= 1
        self.instruction_label.config(text=f"Instruction #: {instr_num:02d}")

    def load_program(self):
        ##This opens up the file explorer for the user to select a file
        file_path = filedialog.askopenfilename(filetypes=[("Text file", "*.txt")])
        if file_path:
            if self.sim.read_file(file_path):
                self.print_output("File read successfully")
                self.update_display()

            else:
                self.print_output("File couldn't be read")
    
    #Gets the 10 previous Memory locations
    def prev_memory(self):
        self.mem_start = max(0, self.mem_start - 10)
        self.update_display()

    #Gets the 10 next Memory locations
    def next_memory(self):
        self.mem_start = min(len(self.sim.memory) - 10, self.mem_start + 10)
        self.update_display()

    #Prints messages to the Output location
    def print_output(self, message):
        self.output_box.config(state='normal')
        self.output_box.delete('1.0', tk.END) #Makes it so only 1 line of text is in the output at any given time. (We can change if needed)
        self.output_box.insert(tk.END, message + "\n")
        self.output_box.config(state='disabled')

    ########## THESE ARE SOME OF THE FUNCTIONS THAT NEED TO BE MADE #####
      
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
                    self.print_output(f"Output: {self.sim.outputValue}")
                    self.sim.output = False
                    self.sim.outputValue = ""
                self.update_display()
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
                handler = getattr(self.sim, method)
                handler(op)
                self.sim.instruction_count += 1
                self.update_display()
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

    # Resets the simulator to its initial state
    def reset(self):
        self.sim.reset()
        self.update_display()

    # Submits the input from the input entry box to the simulator
    def submit_input(self):
        self.sim.input = self.input_entry.get()
        if (self.sim.instruction_count >= 0):
            self.sim.instruction_count -= 1  # Decrement instruction count to reprocess the read instruction
        self.sim.running = True  # Set running to True to allow execution
        self.run()
        self.update_display()