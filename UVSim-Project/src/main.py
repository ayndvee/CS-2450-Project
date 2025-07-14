from model.UVSim import UVSIM
from view.UVSim_Gui import UVSIMGUI
from controller.UVSim_Controller import UVSIM_Controller
import tkinter as tk
import sys

def run_commandline(file):
    sim = UVSIM()
    sim.read_file(file)
    sim.execute()

def run_gui():
    sim = UVSIM()
    root = tk.Tk()
    gui = UVSIMGUI(root, sim)
    controller = UVSIM_Controller(sim, gui)
    gui.bind_controller(controller)
    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) == 2:
        run_commandline(sys.argv[1])
    else:
        run_gui()