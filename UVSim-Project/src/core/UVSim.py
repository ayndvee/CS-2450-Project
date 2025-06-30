#Names: Anthony, Brandon, Andie
#Project: Milestone 2 UVSIM


## IMPORTS
import sys
from typing import Callable


MEMORYSIZE = 100
WORD_DIGITS = 4

class UVSIM:
    def __init__(self) -> None:
        """Set up memory and accumulator"""
        self.memory = [0] * MEMORYSIZE
        self.accumulator = 0
        self.instruction_count = 0
        self.running = True

    def read_file(self, file: str) -> bool:
        """Opens and reads the file that is input on the Command Line"""

        """Opens the file and reads it line by line"""
        with open(file, 'r') as filename:
            lines = filename.readlines()

        """Enumerate adds a counter to the lines so we can count how many we have, so we don't go over the memory limit"""
        for i, line in enumerate(lines):
            """If we go over the memory limit we will just end the program"""
            if i >= MEMORYSIZE:
                print("Error too many lines for memory capacity")
                return False
            """Next we will just get rid of the white space on the lines so we are only dealing with text"""
            line = line.strip()

            """We have reached the end of the file so just stop and don't try to include it"""
            if line == '-99999':
                break

            """If there is an empty line (end the program for now)"""
            if not line:
                print(f"Error on line {i}: there is no line")
                return False
            
            """If we are reading a line and there is not signed number (end it for now)"""
            if not line[0] in '+-':
                print(f"Error on line {i}: must be signed with + or -")
                return False
            
            """If we are reading after the +- sign and it isn't a number (end the program for now)"""
            if not line[1:].isdigit():
                print(f"Error on line {i}: must be numbers after the sign")
                return False
            """Make sure that we are only reading lines that have only 4 numbers after the sign"""
            if len(line[1:]) != WORD_DIGITS:
                print(f"Error on line {i}: must be exactly 4 numbers after the sign")
                return False

            
            """Store the results in memory"""
            self.memory[i] = int(line)
        return True

    OPCODES: dict[int, Callable[["UVSIM", int], None]] = {
        10: "read",
        11: "write",
        20: "load",
        21: "store",
        30: "add",
        31: "subtract",
        32: "multiply",
        33: "divide",
        40: "branch",
        41: "branchNeg",
        42: "branchZero",
        43: "halt"
    }

    def execute(self) -> None:
        #Loops through the memory and performs the action for each opcode

        """
        My thoughts would be to have something like and if statement to find the correct
        opcode and then just call the operation on it as its own function.
        """
        while self.running:
            if self.instruction_count >= MEMORYSIZE:
                print("Error: Instruction pointer out of memory bounds.")
                self.halt()
                break
            code, op = divmod(self.memory[self.instruction_count], 100)
    
            method = self.OPCODES.get(code)
            if method is None:
                raise RuntimeError(f"Unknown opcode: {code} at Instruction: {self.instruction_count}")
            handler = getattr(self, method)
            handler(op)

            self.instruction_count += 1


    #### I/O Operations ####
    def read(self, address: int) -> None:
        """Reads a signed 4-digit number from user and stores it in memory"""
        value = input(f"Enter a signed 4-digit number for memory[{address}]: ")
        while not (value.startswith(('+', '-')) and value[1:].isdigit() and len(value) == 5):
            print("Invalid input. Please enter a signed 4-digit number like +1234 or -5678.")
            value = input(f"Enter a signed 4-digit number for memory[{address}]: ")
        self.memory[address] = int(value)

    def write(self, address: int) -> None:
        """Prints the value stored at the given memory address"""
        print(f"{self.memory[address]}")


    #### LOAD/STORE Operations ####
    def load(self, address: int) -> None:
        """Loads the value from memory into the accumulator"""
        self.accumulator = self.memory[address]

    def store(self, address: int) -> None:
        """Stores the value from the accumulator into memory"""
        self.memory[address] = self.accumulator

    #### Arithmetic Operations ####
        """Add the value in memory to the accumulator"""
    def add(self, operand: int) -> None:
        self.accumulator += self.memory[operand]

    #Subtract the value in memory from the accumulator
    def subtract(self, operand: int) -> None:
        self.accumulator -= self.memory[operand]

    #Divide the accumulator by the value in memory
    def divide(self, operand: int) -> None:
        #Check for division by zero
        if self.memory[operand] == 0:
            raise ZeroDivisionError("Error: Division by zero")
        self.accumulator //= self.memory[operand]

    #Multiply the accumulator by the value in memory
    def multiply(self, operand: int) -> None:
        self.accumulator *= self.memory[operand]
        
    #### Control Operations ####
    def branch(self, operand: int) -> None:
        """Check to make sure operand is in the bounds of memory"""
        if 0 <= operand < len(self.memory):
            self.instruction_count = operand
        #If it isn't aren't stop the program 
        else:
            print("Invalid operand: Out of Memory Range")
            self.halt()
    def branchNeg(self, operand: int) -> None:
        """If the accumulator is negative branch to the new location in memory"""
        if self.accumulator < 0:
            self.branch(operand)
        
    def branchZero(self, operand: int) -> None:
        """If the accumulator is 0, just to the new location in memory"""
        if self.accumulator == 0:
            self.branch(operand)
        
    def halt(self, _=None) -> None:
        """Set running to false because we are stopping the program."""
        self.running = False

