#Names:
#Project:
#Description:

## IMPORTS
import sys


class UVSIM:
    def __init__(self):
        #Set up memory and accumulator
        self.memory = [0] * 100
        self.instruction_count = 0
        self.accumulator = 0
        self.running = True

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
            #Make sure that we are only reading lines that have only 4 numbers after the sign
            if len(line[1:]) != 4:
                print(f"Error on line {i}: must be exactly 4 numbers after the sign")
                break

            
            ## Store the results in memory
            self.memory[i] = int(line)

    def execute(self):
        #Loops through the memory and performs the action for each opcode

        """
        My thoughts would be to have something like and if statement to find the correct
        opcode and then just call the operation on it as its own function.
        """
        instruction = self.memory[self.instruction_count]
        opcode = instruction // 100
        operand = instruction % 100
        
        if opcode == 10:
            pass
        elif opcode == 11:
            pass
        elif opcode == 20:
            pass
        elif opcode == 21:
            pass
        elif opcode == 30:
            pass
        elif opcode == 31:
            pass
        elif opcode == 32:
            pass
        elif opcode == 33:
            pass
        elif opcode == 40:
            self.branch(operand)
        elif opcode ==41:
            self.branchNeg(operand)
        elif opcode == 42:
            self.branchZero(operand)
        elif opcode == 43:
            self.halt()
        else:
            print("Not valid opcode")
            return
        self.instruction_count +=1

    #### I/O Operations ####

    #### LOAD/STORE Operations ####

    #### Arithmetic Operations ####

    #### Control Operations ####
    def branch(self, operand):
        self.instruction_count = operand
    def branchNeg(self, operand):
        #If the accumulator is negative branch to the new location in memory
        if self.accumulator < 0:
            self.instruction_count = operand
        #Otherwise just move onto the next instruction
        else:
            self.instruction_count += 1
    def branchZero(self, operand):
        #If the accumulator is 0, just to the new location in memory
        if self.accumulator == 0:
            self.instruction_count = operand
        #Otherwise just move onto the next instruction
        else:
            self.instruction_count +=1
    def halt(self):
        #Set running to false because we are stopping the program.
        self.running = False

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