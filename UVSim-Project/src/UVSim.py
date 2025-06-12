#Names:
#Project:
#Description:

## IMPORTS
import sys


class UVSIM:
    def __init__(self):
        #Set up memory and accumulator
        self.memory = [0] * 100
        self.accumulator = 0 
        self.instruction_counter = 0


    def read_file(self, file):
        #Opens and reads the file that is input on the Command Line

        ## Opens the file and reads it line by line
        with open(file, 'r') as filename:
            lines = filename.readlines()

        ## Enumerate adds a counter to the lines so we can count how many we have, so we don't go over the memory limit
        for i, line in enumerate(lines):
            ## If we go over the memory limit we will just end the program 
            if i >=100:
                print("Error too many lines for memory capacity")
                return
            ## Next we will just get rid of the white space on the lines so we are only dealing with text
            line = line.strip()

            ## If there is an empty line (end the program for now)
            if not line:
                print(f"Error on line {i}: there is no line")
                return
            
            ## If we are reading a line and there is not signed number (end it for now)
            if not line[0] in '+-':
                print(f"Error on line {i}: must be signed with + or -")
                return
            
            ## If we are reading after the +- sign and it isn't a number (end the program for now)
            if not line[1:].isdigit():
                print(f"Error on line {i}: must be numbers after the sign")
                return
            
            ## Store the results in memory
            self.memory[i] = int(line)

    def execute(self):
        #Loops through the memory and performs the action for each opcode

        """
        My thoughts would be to have something like and if statement to find the correct
        opcode and then just call the operation on it as its own function.
        """
        while True:
            instruction = self.memory[self.instruction_counter]
            opcode = instruction // 100
            operand = instruction % 100

            if opcode == 10:
                self.read(operand)
            elif opcode == 11:
                self.write(operand)
            elif opcode == 20:
                self.load(operand)
            elif opcode == 21:
                self.store(operand)
            elif opcode == 43:
                print("Program halted.")
                break
            else:
                print(f"Unknown opcode {opcode} at memory[{self.instruction_counter}]")
                break

            self.instruction_counter += 1

    #### I/O Operations ####
    def read(self, address):
        #Reads a signed 4-digit number from user and stores it in memory
        value = input(f"Enter a signed 4-digit number for memory[{address}]: ")
        while not (value.startswith(('+', '-')) and value[1:].isdigit() and len(value) == 5):
            print("Invalid input. Please enter a signed 4-digit number like +1234 or -5678.")
            value = input(f"Enter a signed 4-digit number for memory[{address}]: ")
        self.memory[address] = int(value)

    def write(self, address):
        #Prints the value stored at the given memory address
        print(f"Output from memory[{address}]: {self.memory[address]}")

    #### LOAD/STORE Operations ####
    def load(self, address):
        #Loads the value from memory into the accumulator
        self.accumulator = self.memory[address]

    def store(self, address):
        #Stores the value from the accumulator into memory
        self.memory[address] = self.accumulator

    #### Arithmetic Operations ####

    #### Control Operations ####


def run(file):
    sim = UVSIM()
    sim.read_file(file)
    sim.execute()

if __name__ == "__main__":
    ## Check to make sure that a file was input on the Command line
    ## If not then we tell the user the usage and exit the program
    ## Otherwise we just run the program with the file.
    if len(sys.argv) != 2:
        print("Usage: python UVSim.py <filename>")
        sys.exit(1)
    run(sys.argv[1])