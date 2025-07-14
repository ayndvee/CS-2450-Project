# Class Definition Documentation

# Class UVSIM

## Purpose
The UVSIM class helps provide a simple computer simulator that can execute basic machine instructions. It handles the program memory, instruction execution, input/output, and control flow.

## Features
- memory - Represents the computer memory (up to a limit of 100)
- accumulator - Stores the result of operations
- instruction_counter - Keeps track of the current instruction being executed
- running - Indicates if the simulator is running
- gui - Flag to indicate if running in GUI mode
- input - Holds input from the user in GUI mode
- output - Determines if the program is outputting to the gui
- outputValue - Holds output value for GUI display



# Functions

# __init__(self)
- Purpose
	- Initialize the simulator with empty memory and states
- Post Condition
	- Memory is clear, accumulator and instruction count are zero
# read_file(self, file_path)
- Purpose:
	- Reads a BasicML program from a file and loads it into memory
- Parameters:
	- file_path - Path to the input file
- Return:
	- True if the file is successfully loaded
	- False otherwise
- Post Condition:
	- Memory has all the program values

# reset(self)
- Purpose:
	- Resets the program to initial state
- Post Condition:
	- Simulator has accumulator and instruction count set to 0.
# execute(self)
- Purpose:
	- Continuously execute the instructions form memory until a HALT instruction or an error happens
- Post Condition:
	- Executes instructions and updates memory

# read(self, address)
- Purpose:
	- Prompt the user to input a signed 4 digit integer
- Parameters: 
	- Address -memory index
- Post Condition:
	- Value is stored in memory at the specific address

# write(self, address)
- Purpose:
	- Output the value stored at a specific memory address
- Parameters: 
	- Address -memory index
- Post Condition:
	- Value is printed to the console
# load(self, address)
- Purpose:
	- Loads value from memory into accumulator
- Parameters: 
	- Address -memory index
- Post Condition:
	- Accumulator is updated

# store(self, address)
- Purpose:
	- Store the current value in accumulator to memory
- Parameters: 
	- Address -memory index
- Post Condition:
	- Memory is updated
# add(self, operand)
- Purpose:
	- Adds value in memory to the accumulator
- Parameters: 
	-operand -memory index
- Post Condition:
	- Accumulator is updated
# subtract(self, operand)
- Purpose:
	- Subtracts value in memory to the accumulator
- Parameters: 
	-operand -memory index
- Post Condition:
	- Accumulator is updated

# multiply(self, operand)
- Purpose:
	- Multiplies value in memory to the accumulator
- Parameters: 
	-operand -memory index
- Post Condition:
	- Accumulator is updated

# divide(self, operand)
- Purpose:
	- Divides value in memory to the accumulator
- Parameters: 
	-operand -memory index
- Post Condition:
	- Accumulator is updated or exception if divide by zero

# branch(self, operand)
- Purpose:
	- Sets instruction counter to specified memory address
- Parameters: 
	-operand -memory index
- Post Condition:
	- Next instruction jumps to the operand

# branchNeg(self, operand)
- Purpose:
	- Sets instruction counter to specified memory address if accumulator is negative
- Parameters: 
	-operand -memory index
- Post Condition:
	- Updates the instruction counter

# branchZero(self, operand)
- Purpose:
	- Sets instruction counter to specified memory address is zero
- Parameters: 
	-operand -memory index
- Post Condition:
	-Updates the instruction counter

# halt(self, \__=None)
- Purpose:
	- Stop the simulation
- Post Conditions:
	- Running is set to false and simulation stops

# Class: UVSIMGUI

## Purpose
The UVSIMGUI class helps provide a graphical user interface for the UVSIM simulator by using Tkinter. It allows the user to load BasicML programs, view memory, input values, and step through the process of the simulation. The class only handles user interaction and display of the logic.

## Features
- root - The main Tkinter window for display
- sim - An instance of UVSIM class
- labels = a 2D list of tuples to hold memory addresses and value labels
- mem_start = The starting memory address in the memory grid
- waiting_input = Flag to tell if we are waiting for user input or not
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
- Purpose:
	- Starts a continous execution of the simulator in a thread until paused or halted
- Post Conditions:
	- The simulator runs instruction by instruction automatically, updating the GUI

# step(self)
- Purpose:
	- Executes a single instruction of the simulator and updates the GUI
- Post Conditions
	- One instruction is done at a time and displays are updated accordingly

# pause(self)
- Purpose:
	- Pause the program
- Post Conditions:
 	- The simulator is paused and the GUI and simulator stop running

# reset(self)
- Purpose:
	- Resets the simulator and the GUI to intial state
- Post Conditions:
	- The simulator and memory are reset back to initial file state

# submit_input(self)
- Purpose:
	- Submits the input that the user has input
- Post Conditions:
	- User input is now in the simulator and execution continues and the GUI is updated


# Notes
- The class only really has UI responsibilities and doesn't contain any core logic
- The state is managed by the UVSIM core.
- All user interaction goes through the GUI controls and updates the visuals only
