## UVSim GUI

## IMPORTS
import sys
import os
import tkinter as tk
import threading
import time
from tkinter import filedialog, messagebox, ttk
from model.UVSim import UVSIM

class UVSIMGUI:
    def __init__(self, root, sim):
        self.root = root
        self.sim = sim
        self.cpu = sim.cpu
        self.memory = sim.memory
        self.io = sim.io
        self.labels = []
        self.mem_start = 0
        self.controller = None
        root.title("UVSIM")

        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except:
            self.style.theme_use(self.style.theme_use())
        
        ## Create the memory title and the memory layout
        header_frame = ttk.Frame(root)
        header_frame.pack(fill=tk.X, pady=(10, 0), padx=10)
        ttk.Button(header_frame, text= "Reset Theme", command= lambda: self.controller.reset_theme()).pack(side = tk.LEFT)
        ttk.Button(header_frame, text="Change Theme", command=lambda: self.controller.change_theme()).pack(side=tk.RIGHT)
        
        ttk.Label(root, text="Memory").pack(pady=(10, 0))
        memory_frame = ttk.Frame(root, borderwidth=2, relief="groove")
        memory_frame.pack(padx=10, pady=10)

        for row in range(2):
            row_labels = []
            for col in range(5):
                addr_label = ttk.Label(memory_frame, text="Addr: --", width= 12)
                val_label = ttk.Label(memory_frame, text= "Value: ----",width=14)
                addr_label.grid(row = row*2, column= col, padx=4)
                val_label.grid(row=row*2+1, column=col, padx=4)
                row_labels.append((addr_label,val_label))
            self.labels.append(row_labels)


        ## Creates the previous and Next button and their layout
        navigation = ttk.Frame(root)
        navigation.pack(fill=tk.X, pady=5)

        prev_button = ttk.Button(navigation, text="Prev 10", command=lambda: self.controller.prev_memory())
        prev_button.grid(row=0, column=0, sticky='w', padx=10)

        next_button = ttk.Button(navigation, text="Next 10", command=lambda: self.controller.next_memory())
        next_button.grid(row=0, column=10, sticky='e', padx=10)

        navigation.grid_columnconfigure(0, weight=1)
        navigation.grid_columnconfigure(1, weight=1)

        ## Creates the accumulator and Instruction # labels and amounts
        status_frame = ttk.Frame(root)
        status_frame.pack(pady=5)

        self.accumlator_label = ttk.Label(status_frame, text= "Accumulator: +0000", width=20, anchor='w')
        self.accumlator_label.pack(side=tk.LEFT, padx=10)
        
        self.instruction_label = ttk.Label(status_frame, text= "Instruction #: 00", width=20, anchor='w')
        self.instruction_label.pack(side=tk.LEFT, padx=10)

        ## Creates the Submit Input text box and button
        input_frame = ttk.Frame(root)
        input_frame.pack(pady=5)
        self.input_entry = ttk.Entry(input_frame, width=10)
        self.input_entry.pack(side=tk.LEFT, padx=(0,5))
        self.input_button = ttk.Button(input_frame, text="Submit Input", command=lambda: self.controller.submit_input()).pack(side=tk.LEFT)


        ## Creates the Run, Step, Pause, and Reset buttons and has their layout
        control_frame = ttk.Frame(root)
        control_frame.pack(fill=tk.X)
        ttk.Button(control_frame, text="Run", command=lambda: self.controller.run()).pack(side=tk.LEFT, padx=30)
        ttk.Button(control_frame, text="Step", command=lambda: self.controller.step()).pack(side=tk.LEFT, padx=80)
        ttk.Button(control_frame, text="Pause", command=lambda: self.controller.pause()).pack(side=tk.LEFT, padx=80)
        ttk.Button(control_frame, text="Reset", command=lambda: self.controller.reset()).pack(side=tk.LEFT, padx=30)

        ## Creates the Load Program Button
        ttk.Button(root, text="Load Program", command=lambda: self.controller.load_program()).pack(pady=5)

        ## Creates the Output label and its box
        ttk.Label(root, text="Output:").pack()
        self.output_box= tk.Text(root, height=8, width=50, state='disabled')
        self.output_box.pack()

        ## Creates the save file button
        ttk.Button(root, text="Save File", command= lambda: self.controller.save_file()).pack(pady=5)
        self.update_display()

    def bind_controller(self, controller):
        self.controller = controller

    def update_display(self):
        self.update_memory_display()
        self.update_status()
    def update_memory_display(self):
        # Update memory display for addresses from memory_start to memory_start+9
        for i, row_labels in enumerate(self.labels):
            for j, (addr_label, val_label) in enumerate(row_labels):
                mem_index = self.mem_start + i*5 + j
                try:
                    value = self.memory.get(mem_index)
                    # Make it a signed 4 digit value
                    value_str = f"{value:+05d}"
                except IndexError:
                    value_str = "----"
                
                addr_label.config(text=f"Addr: {mem_index:02d}")
                val_label.config(text=f"Value: {value_str}")
    def update_status(self):
        # Update accumulator label
        acc_value = getattr(self.cpu, "accumulator", 0)
        self.accumlator_label.config(text=f"Accumulator: {acc_value:+05d}")

        # Update instruction number label
        instr_num = getattr(self.cpu, "instruction_count", 0)
        if (instr_num > 0):
            instr_num -= 1
        self.instruction_label.config(text=f"Instruction #: {instr_num:02d}")


    #Prints messages to the Output location
    def print_output(self, message):
        self.output_box.config(state='normal')
        self.output_box.insert(tk.END, message + "\n")
        self.output_box.see(tk.END)
        self.output_box.config(state='disabled')
      

    def setup_styles(self, primary_color, off_color):
        self.style.configure('Primary.TFrame', background=primary_color)
        self.style.configure('Custom.TLabel', background=primary_color, foreground='black')
        self.style.configure('Custom.TButton', background=off_color, foreground='black')
        self.style.configure('Custom.TEntry', fieldbackground=off_color, foreground='black')
    #sets the theme for the UVSIMGUI
    def set_theme(self, primary_color, off_color):

        """
        Updates the GUIs background and its widgets to have the theme applied to them as well.\
        """
        self.root.configure(bg =primary_color)
        self.setup_styles(primary_color, off_color)

        for widget in self.root.winfo_children():
            if isinstance(widget, tk.LabelFrame) and not widget.cget("text"):
                try:
                    widget.config(highlightbackground= "black", highlightthickness= 2, bd = 0, relief= 'flat')
                except tk.TclError:
                    pass
            if isinstance(widget, ttk.Frame) or isinstance(widget, ttk.LabelFrame):
                widget.configure(style='Primary.TFrame')
                for child in widget.winfo_children():
                    self._apply_theme_to_widget(child, primary_color, off_color)
            else:
                self._apply_theme_to_widget(widget, primary_color, off_color)

    def _apply_theme_to_widget(self, widget, primary_color, off_color):

        """
        Applies the theme colors to specific widgets based on its type. 
        """
        if isinstance(widget, ttk.Label):
            widget.configure(style='Custom.TLabel')
        elif isinstance(widget, ttk.Button):
            widget.configure(style ="Custome.TButton")
        elif isinstance(widget, ttk.Entry):
            widget.configure(style="Custom.TEntry")
        elif isinstance(widget, tk.Entry):
            widget.configure(bg=off_color, fg="black", insertbackground="black")
        elif isinstance(widget, tk.Text):
            widget.configure(bg=off_color, fg="black", insertbackground="black", state='normal')
            widget.config(state='disabled')
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