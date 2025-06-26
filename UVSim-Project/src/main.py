from core.UVSim import UVSIM
from gui.UVSim_Gui import UVSIMGUI
import tkinter as tk
import sys

def run_commandline(file):
    sim = UVSIM()
    sim.read_file(file)
    sim.execute()

def run_gui():
    root = tk.Tk()
    gui = UVSIMGUI(root, sim)
    root.mainloop()

if __name__ == "__main__":
    sim = UVSIM()
    if len(sys.argv) == 2:
        run_commandline(sys.argv[1])
    else:
        run_gui()