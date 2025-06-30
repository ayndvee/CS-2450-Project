# Class Definition Documentation

# Class: UVSIMGUI

## Purpose
The UVSIMGUI class helps provide a graphical user interface for the UVSIM simulator by using Tkinter. It allows the user to load BasicML programs, view memory, input values, and step through the process of the simulation. The class only handles user interaction and display of the logic.

## Features
- root - The main Tkinter window for display
- sim - An instance of UVSIM class
- labels = a 2D list of tuples to hold memory addresses and value labels
- mem_start = The starting memory address in the memory grid
- input_entry = Allows for user input
- accumulator_label = Label that shows the current accumulator value
- intruction_label = Label that shows the current instruction count value
- output_box = Text box that will be used to display error messages and output from the program.

# Functions

# __init__(self, root, sim)
- Purpose
	- To create and set up the GUI and its features and connect buttons to their methods.
- Parameters
	- root: Tkinter Window
	- sim: A UVSIM instance
- Post Conditions
	- GUI fully made and memory and status displays are correct.

# update_display(self)
- Purpose:
	- Update the GUI for memory display, accumulator, and instruction count indicators.
- Post Conditions
	- GUI has up to date information for both memory and status.

# update_memory_display(self)
- Purpose
	- Updates the current 10 memory cells on the GUI..
- Post Conditions
	- Address and value labels are updated and formatted in the memory content.

# update_status(self)
- Purpose
	- Updates the Accumulator and Instruction count display labels based on the current state.
- Post Conditions
	- GUI shows the correct values based on the simulator

# load_program(self)
- Purpose
	- Opens a file picker dialog and attempts to load the program into the simulator
- Post Conditions
	- On Success: simulator memory is updates and GUI shows that new state
	- On Failure: an error message is printed in the output box
- Inputs
	- User selected .txt file containing a proper BasicML program

# prev_memory(self)
- Purpose
	- Changes the memory display for the previous 10 addresses
- Post Conditions
	- mem_start is updated, but not below 0, and memory view is updated

# next_memory(self)
- Purpose
	- Changes the memory display for the next 10 addresses
- Post Conditions
	- mem_start is updated, but not above memory limit, and memory view is updated.

# print_output(self, message)
- Purpose
	- Prints a single line of output to the output box
- Parameters
	- message- The string that will be displayed
- Post Conditions
	- Previous text message is cleared and then the new message is displayed.
	- Output box is then set to read-only until print_output is called again.

# run(self)
- Purpose
- Post Conditions

# step(self)
- Purpose
- Post Conditions

# pause(self)
- Purpose
- Post Conditions

# reset(self)
- Purpose
- Post Conditions

# submit_input(self)
- Purpose
- Post Conditions


# Notes
- The class only really has UI responsibilities and doesn't contain any core logic
- The state is managed by the UVSIM core.
- All user interaction goes through the GUI controls and updates the visuals only
