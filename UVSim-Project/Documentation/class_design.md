# Class Definition Documentation

# Class UVSIM

## Purpose
The UVSIM class acts as the main simulator. It helps coordinate the CPU, memory and IO components. It provides methods to 
load programs, reset the state and execute instructions through CPU.

## Features
- memory - an instance of the Memory class
- io - An instance of the IOHandler class
- cpu - An instance of the CPU class

# Functions

# __init__(self, gui = false)
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
 - # save_file(self, file_path)
- Purpose:
	- Reads a BasicML program from memory and loads it into a file
- Parameters:
	- file_path - Path to the output file
- Return:
	- True if the file is successfully saved
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


# Class CPU

## Purpose
This represents the CPU of the UVSim, it is responsible for executing the instructions in memory.
It also manages the accumulator, instruction counter and execution flow.

## Features
- memory: Reference to the Memory Instance
- io: Reference to the IOHandler Instance
- accumulator - Stores the result of operations
- instruction_counter - Keeps track of the current instruction being executed
- running - Indicates if the simulator is running
- OPCODES - dictionary mapping Opcode enum to string method names.

# Functions

# __init__(self, memory, io_handler)
- Purpose:
	- Initialize the CPU
	- sets accumulator and instruction count to 0
	- sets running flag to true
- Post Condition: 
	- CPU is ready to execute instruction

# execute(self)
- Purpose: 
	- Continously geet instructions from memory until halted or error
- Post Condition:
	- Instructions are read
	- Errors are handled if they occur
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
 	- If the value reached would exceed 4 digits, the 4 least significant digits are kept
# subtract(self, operand)
- Purpose:
	- Subtracts value in memory to the accumulator
- Parameters: 
	-operand -memory index
- Post Condition:
	- Accumulator is updated
 	- If the value reached would exceed 4 digits, the 4 least significant digits are kept
# multiply(self, operand)
- Purpose:
	- Multiplies value in memory to the accumulator
- Parameters: 
	-operand -memory index
- Post Condition:
	- Accumulator is updated
 	- If the value reached would exceed 4 digits, the 4 least significant digits are kept
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

# reset(self)
- Purpose:
	- Reset the CPU to initial state
- Post Condition:
	- Accumulator and instruction count set to 0
	- Running is set to True

# Class: Memory 
## Purpose
This acts as the Main Memory for the UVSim. It handles loading and getting and setting memory
## Features
- load_program: loads the program from a file
- reset - resets the program to initial state
- get : gets the value at a memory address
- set : sets the valuge at a memory address
- get_all : returns all the memory address values
# Functions

# __init__(self)
- Purpose:
	- Initialize memory and spareMemory arrays with zeroed values.
- Post Condition:
	- memory and spareMemory contain 100 zeros each.

# load_program(self, lines: list[str]) -> bool
- Purpose:
	- Load a program from a list of signed string instructions into memory.
	- Validate each line for proper format.

- Post Condition:
	- Valid lines loaded into memory and saved in spareMemory.
	- Returns True if successful; False if error encountered.

# getLines(self) -> bool
- Purpose:
	- Get a list of lines from memory to save the current program to a file.

- Post Condition:
	- Returns a list of signed string instructions.

# reset(self)
- Purpose:
	- Reset memory contents back to the original program stored in spareMemory.

- Post Condition:
	- memory restored to initial program state.

# get(self, address: int) -> int
- Purpose:
	- Get the value stored at a specific memory address
- Parameters:
	- address
- Post Condition:
	- Returns the value stored at the address

# set(self, address: int, value: int) -> None
- Purpose:
	- Store a value at specific memory address
- Parameters:
	- address
	- value
- Post Condition:
	- Memory at address updated with value

# get_all(self) -> list[int]
- Purpose:
	- Return a copy of the entire memory contents
- Post Conditiion:
	- Returns a list of all memory values

# Class: IOHanlder

## Purpose
This hanldes the user interaction for both the GUI and console. It handles the reading of input and writing them into memory.
## Features
- gui : a flag for whether we are in the gui or not
- input : storesd the user input in gui mode
- output: Flag to indicate that output is ready
- outputValue: a string of the last output value

## Functions
# __init__(self, gui_mode: bool = False)
- Purpose:
	- Initialize the IOHandler class
- Post Conditions:
	- Sets default values and sets up flags

# read(self, address: int, memory)
- Purpose:
	- Prompts the user for a signed 4-digit number ans stores it in the given address.
- Parameters:
	- address
	- memory
- Post Condition:
	- True if the input was valid
	- False if the were errors or invalid input

# write(self, address: int, memory)
- Purpose:
	- Gets a value from memory and display it
- Parameters:
	- address
	- memory
- Post Condition:
	- sets output to True and formats the output to be printed to Gui or console

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

# def set_theme(self, primary_color, off_color)
- Purpose:
	- Updates the GUIs background and its widgets to have the theme applied to them as well.
- Post Condition:
	- Theme is now applied to GUI and its widgets

# def _apply_theme_to_widget(self, widget, primary_color, off_color)
- Purpose:
	- Applies the theme colors to specific widgets based on its type. 
- Post Condition:
	- Theme is applied to specific widgets

# Class: UVSIM_Controller

## Purpose
The UVSIM_Controller class acts as the bridge between the simulation logic (model) and the graphical interface (view). It handles user interactions, manages the execution flow, processes input/output, and updates the GUI state accordingly.

## Features
-  sim : Instance of the simulator, containing memory, CPU, and IO handler.
-  cpu : Reference to the simulator's CPU instance.
-  memory : Reference to the simulator's Memory instance.
-  io : Reference to the simulator's IOHandler instance.
-  view : GUI instance bound to the controller.
-  running : Boolean flag for simulation's running state.
-  paused : Boolean flag for simulation's paused state.
-  waiting_input : Indicates whether the simulator is waiting for user input.
-  recieved_input : Indicates whether user input has been received.
-  root : Tkinter root window, used to schedule repeated execution steps.

# Functions

 #  __init__(self, sim, view) 
-  Purpose:
    - Initializes the controller and connects simulation and GUI components.
-  Post Condition:
    - The simulation and GUI are connected and ready. Theme is applied.

 #  run(self) 
-  Purpose: 
    - Starts continuous execution of the program using  Tk.after() .
-  Post Condition: 
    - Execution continues until paused or halted.
 #  _execute_step(self) 
-  Purpose: 
    - Helper function to run one instruction and reschedule itself.
-  Post Condition: 
    - Executes a step, updates the GUI, and schedules the next step if still running.

 #  step(self) 
-  Purpose: 
    - Executes a single instruction and updates the GUI.
-  Post Condition:
    - One instruction is processed, memory and display are updated.

 #  pause(self) 
-  Purpose: 
    - Pauses the execution of the simulator.
-  Post Condition:
    - All running flags are disabled. Output printed to GUI.

 #  reset(self) 
-  Purpose:
    - Resets simulator and GUI to the initial state.
-  Post Condition:
    - Simulator returns to its loaded state and GUI is updated.

 #  load_program(self) 
-  Purpose:
    - Opens file dialog and loads a program file into memory.
-  Post Condition:
    - If successful, memory and display are updated. Else, an error message is shown.

 # load_from_editor(self)
- Purpose:
	- Validates the entries in the memory text editor and sends it into memory
- Post Condition:
	- If successful updates the memory display with new info
	- If failure gives an error message

 # cut_text(self, event =none)
 - Purpose:
	- Allows the user to be able to cut  text in the editor
- Post Condition:
	- If selected it will copy the item to clipboard and delete on editor

 # copy_text(self, event =none)
 - Purpose:
	- Allows the user to be able to copy text in the editor
- Post Condition:
	- If selected it will copy the item to clipboard

 # paste_text(self, event =none)
 - Purpose:
	- Allows the user to be able to paste text in the editor
- Post Condition:
	- If selected it will paste the item in the editor

 #  prev_memory(self) 
-  Purpose:
    - Navigates the memory display to show 10 previous addresses.
-  Post Condition:  
    - Updates GUI display starting from a lower address range.

 #  next_memory(self) 
-  Purpose:
    - Navigates the memory display to show 10 next addresses.
-  Post Condition:
    - Updates GUI display starting from a higher address range.

 #  submit_input(self) 
-  Purpose:
    - Submits input from the GUI input box to the simulator.
-  Post Condition:
    - Input is stored, simulator resumes, and GUI updates.

 #  apply_theme(self) 
-  Purpose: 
    - Applies saved or default theme to the GUI.
-  Post Condition:
    - GUI colors are updated.

 #  load_theme(self) 
-  Purpose:
    - Loads the theme from a configuration file.
-  Post Condition:
    - Returns theme data or default values.

 #  change_theme(self) 
-  Purpose:
    - Opens a color picker dialog to update GUI theme colors.
-  Post Condition:
    - Colors are applied and saved to configuration.

 #  save_theme(self, primary_color, off_color) 
-  Purpose:
    - Saves chosen theme colors to configuration file.
-  Post Condition:
    - Config file is updated and theme is applied.

# reset_theme(self)
- Purpose:
	- Resets the theme to the default colors
- Post Condition:
	- GUI and widgets are back to the original theme colors

 #  save_file(self) 
-  Purpose:
    - Saves the current memory state to a file.
-  Post Condition:
    - File of user's choice is created or updated with a copy of the current program's memory state.



# Notes
- The class only really has UI responsibilities and doesn't contain any core logic
- The state is managed by the UVSIM core.
- All user interaction goes through the GUI controls and updates the visuals only

# Class: Globals

## Purpose
The Globals class holds various global variables.

## Features
-  MAX_VALUE : Placeholder for the maximum value an instruction in memory can hold, currently unused.
-  MIN_VALUE : Placeholder for the minimum value an instruction in memory can hold, currently unused.
-  STOP : Contains the value of the "end of file" instruction.
-  MEMORYSIZE : Contains the maximum size of a valid BasicML program.
-  DEFAULT_PRIMARY : Contains the default primary color.
-  DEFAULT_OFF : Contains the default off color.
-  INTERVAL : Determines the amount of time between instruction execution as a program is running.
