## UVSim GUI

## IMPORTS
import sys
import os
import tkinter as tk
import threading
import time
from tkinter import filedialog, messagebox, ttk
from view.UVSim_TabManager import TabManager
from model.UVSim import UVSIM
try:
    from tkmacosx import Button
except ImportError:
    # fallback to tk.Button if tkmacosx isn't available
    Button = tk.Button

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
        self.style = ttk.Style(self.root)
        self.style.theme_use("clam")   
        root.title("UVSIM")

        
        
        ## Create the memory title and the memory layout
        header_frame = tk.Frame(root)
        header_frame.pack(fill=tk.X, pady=(10, 0), padx=10)
        Button(header_frame, text= "Reset Theme", command= lambda: self.controller.reset_theme()).pack(side = tk.LEFT)
        Button(header_frame, text="Change Theme", command=lambda: self.controller.change_theme()).pack(side=tk.RIGHT)

        self.tab_manager = TabManager(self.root)
        #self.apply_notebook_style()
        self.tab_manager.bind_tab_change(self.on_tab_changed)
        tk.Label(root, text="Memory Edit").pack(pady=(10,0))
        Button(self.root, text="Load to Memory", command=lambda: self.controller.load_from_editor()).pack(pady=10)

        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)

        Button(button_frame, text="New File", command=lambda: self.tab_manager.add_tab()).pack(side=tk.LEFT)
        Button(button_frame, text="Close File", command=lambda: self.tab_manager.close_tab()).pack(side=tk.LEFT)

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

        prev_button = Button(navigation, text="Prev 10", command=lambda: self.controller.prev_memory())
        prev_button.grid(row=0, column=0, sticky='w', padx=10)

        next_button = Button(navigation, text="Next 10", command=lambda: self.controller.next_memory())
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
        self.input_button = Button(input_frame, text="Submit Input", command=lambda: self.controller.submit_input()).pack(side=tk.LEFT)


        ## Creates the Run, Step, Pause, and Reset buttons and has their layout
        control_frame = tk.Frame(root)
        control_frame.pack(fill=tk.X)
        Button(control_frame, text="Run", command=lambda: self.controller.run()).pack(side=tk.LEFT, padx=30, expand=True)
        Button(control_frame, text="Step", command=lambda: self.controller.step()).pack(side=tk.LEFT, padx=80,expand=True)
        Button(control_frame, text="Pause", command=lambda: self.controller.pause()).pack(side=tk.LEFT, padx=80,expand=True)
        Button(control_frame, text="Reset", command=lambda: self.controller.reset()).pack(side=tk.LEFT, padx=30,expand=True)

        ## Creates the Load Program Button
        Button(root, text="Load Program", command=lambda: self.controller.load_program()).pack(pady=5)

        ## Creates the Output label and its box
        tk.Label(root, text="Output:").pack()
        self.output_box= tk.Text(root, height=8, width=50, state='disabled')
        self.output_box.pack()

        ## Creates the save file button
        Button(root, text="Save File", command= lambda: self.controller.save_file()).pack(pady=5)
        self.update_display()

    def get_current_editor(self):
        """Get the active text editor widget."""
        return self.tab_manager.get_active_text_widget()

    def bind_controller(self, controller):
        """Bind controller to the GUI and set up key bindings."""
        self.controller = controller
        editor = self.get_current_editor()
        if editor:
            editor.bind("<Control-c>", self.controller.copy_text)
            editor.bind("<Control-x>", self.controller.cut_text)
            editor.bind("<Control-v>", self.controller.paste_text)
        self.tab_manager.notebook.bind("<<NotebookTabChanged>>", lambda e: self._rebind_editor_keys(), add= "+")
    
    def _rebind_editor_keys(self):
        """Rebind key shortcuts for the current editor tab."""
        editor = self.get_current_editor()
        if editor:
            editor.bind("<Control-c>", self.controller.copy_text)
            editor.bind("<Control-x>", self.controller.cut_text)
            editor.bind("<Control-v>", self.controller.paste_text)

    def update_display(self):
        """Update memory display and status labels."""
        self.update_memory_display()
        self.update_status()
    def update_memory_display(self):
        """Update the visible memory address and value labels."""
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
        """Update the accumulator and instruction number labels."""
        acc_value = getattr(self.cpu, "accumulator", 0)
        self.accumlator_label.config(text=f"Accumulator: {acc_value:+05d}")

        
        instr_num = getattr(self.cpu, "instruction_count", 0)
        if (instr_num > 0):
            instr_num -= 1
        self.instruction_label.config(text=f"Instruction #: {instr_num:02d}")


    
    def print_output(self, message):
        """Print a message to the output text box."""
        self.output_box.config(state='normal')
        self.output_box.insert(tk.END, message + "\n")
        self.output_box.see(tk.END)
        self.output_box.config(state='disabled')
      
    def build_theme(self, primary_color, off_color):
        """Build and return the theme dictionary based on given colors."""
        return {
            "*": {
                "bg": primary_color,
                "fg": "black"
            },
            "Label": {
                "bg": primary_color,
                "fg": "black"
            },
            "Button": {
                "bg": off_color,
                "fg": "black",
                "activebackground": primary_color
            },
            "Entry": {
                "bg": off_color,
                "fg": "black",
                "insertbackground": "black"
            },
            "Text": {
                "bg": off_color,
                "fg": "black",
                "insertbackground": "black"
            },
            "LabelFrame": {
                "bg": primary_color,
                "highlightbackground": "black",
                "highlightthickness": 2,
                "bd": 0,
                "relief": "flat"
            },
            "Frame": {
                "bg": primary_color
            },
            "CustomButton": {
                "bg": off_color,
                "fg": "black",
                "activebackground": primary_color,
                "bd": 1,
                "highlightthickness": 0,
                "highlightbackground": off_color
            }
        }
    def set_theme(self, primary_color, off_color):

        """
        Updates the GUIs background and its widgets to have the theme applied to them as well.
        """
        theme = self.build_theme(primary_color, off_color)
        self.root.configure(bg =primary_color)

        for widget in self.root.winfo_children():
            self._apply_theme_to_widget(widget, theme)

        self.set_notebook_theme(primary_color, off_color)
    
    def set_notebook_theme(self, primary_color, off_color):
        """Configure the notebook widget's style for the theme."""
        self.style.configure("Custom.TNotebook", background=primary_color, borderwidth=0)
        self.style.configure("Custom.TNotebook.Tab", background=off_color, foreground="black", padding=[10,5])
        self.style.configure("Custom.TNotebook.focus", background=off_color)
        self.style.configure("Custom.TNotebook.label", background=off_color)
        self.style.configure("Custom.TNotebook.padding", background=off_color)
        self.style.map("Custom.TNotebook.Tab",
            background=[("selected", off_color)],
            foreground=[("selected", "black"), ("!selected", "gray20")]
        )
        self.tab_manager.notebook.configure(style="Custom.TNotebook")
        self.tab_manager.notebook.update_idletasks()

    def _apply_theme_to_widget(self, widget, theme):

        """
        Applies the theme colors to specific widgets based on its type. 
        """
        widget_type = widget.winfo_class()
        for option, value in theme.get("*", {}).items():
            try:
                widget[option] = value
            except tk.TclError:
                pass

        if widget_type in theme:
            for option, value in theme[widget_type].items():
                try:
                    widget[option] = value
                except tk.TclError:
                    pass
        for child in widget.winfo_children():
            self._apply_theme_to_widget(child, theme)

    def on_tab_changed(self, event):
        """Handle event when the notebook tab changes, reloading editor content."""
        editor = self.get_current_editor()
        if editor:
            content = editor.get("1.0", tk.END).strip().splitlines()
            if self.controller:
                self.controller.reload_memory_from_editor(content)
        else:
            self.print_output("No active editor tab found.")
