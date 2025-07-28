from globals.Util import Globals

from enum import IntEnum

class Opcode(IntEnum):
    READ = 10
    WRITE = 11
    LOAD = 20
    STORE = 21
    ADD = 30
    SUBTRACT = 31
    MULTIPLY = 32
    DIVIDE = 33
    BRANCH = 40
    BRANCHNEG = 41
    BRANCHZERO = 42
    HALT = 43

class CPU:
    """
    A simple CPU that executes instructions from memory
    
    """
    def __init__(self, memory, io_handler):
        """
        Sets up the CPU with memory and I/O Handler
        """
        self.memory = memory
        self.io = io_handler
        self.accumulator = 0
        self.instruction_count = 0
        self.word_length = None
        self.running = True

        self.OPCODES = {
            Opcode.READ: "read",
            Opcode.WRITE: "write",
            Opcode.LOAD: 'load',
            Opcode.STORE: 'store',
            Opcode.ADD: 'add',
            Opcode.SUBTRACT: "subtract",
            Opcode.MULTIPLY: "multiply",
            Opcode.DIVIDE: "divide",
            Opcode.BRANCH: "branch",
            Opcode.BRANCHNEG: "branchNeg",
            Opcode.BRANCHZERO: "branchZero",
            Opcode.HALT: "halt"
        }

    def execute(self):
        """
        Begins the execution cycle: getting the instruction, finding the opcode that matches, and then executing
        that instruction until a HALT instruction or error occurs.
        
        """
        while self.running:
            if self.instruction_count >= Globals.MEMORYSIZE:
                print("Error: Instruction pointer out of memory bounds.")
                self.halt()
                break
            if (self.word_length == 4):
                code, op = divmod(self.memory.get(self.instruction_count), Globals.MEMORYSIZE)
                method = self.OPCODES.get(code)
                if method is None:
                    raise RuntimeError(f"Unknown opcode: {code} at Instruction: {self.instruction_count}")
                handler = getattr(self, method)
                handler(op)
                self.instruction_count += 1
            if (self.word_length == 6):
                code, op = divmod(self.memory.get(self.instruction_count), Globals.MEMORYSIZE * 10)
                method = self.OPCODES.get(code)
                if method is None:
                    raise RuntimeError(f"Unknown opcode: {code} at Instruction: {self.instruction_count}")
                handler = getattr(self, method)
                handler(op)
                self.instruction_count += 1

    # I/O
    def read(self, addr):
        """
        Read input from the user and store it in memory at the specified address.
        """
        self.running = self.io.read(addr, self.memory)
    def write(self, addr):
        """
        Output the value from memory at the specified address.
        """
        self.io.write(addr, self.memory)

    # Load/Store
    def load(self, addr):
        """
        Load a value from memory into the accumulator.
        """
        self.accumulator = self.memory.get(addr)
    def store(self, addr):
        """
        Store the value from the accumulator into memory.
        """
        self.memory.set(addr, self.accumulator)

    # Math
    def add(self, addr):
        """
        Add the value from memory to the accumulator.
        """
        self.accumulator += self.memory.get(addr)
        if (self.accumulator < 0):
            self.accumulator = self.accumulator * -1
            if (self.word_length == 4):
                self.accumulator %= Globals.MODULO
            else:
                self.accumulator %= Globals.MODULO_LARGE
            self.accumulator = self.accumulator * -1
        else:
            self.accumulator %= Globals.MODULO
    def subtract(self, addr):
        """
        Subtract the value from memory to the accumulator.
        """
        self.accumulator -= self.memory.get(addr)
        if (self.accumulator < 0):
            self.accumulator = self.accumulator * -1
            if (self.word_length == 4):
                self.accumulator %= Globals.MODULO
            else:
                self.accumulator %= Globals.MODULO_LARGE
            self.accumulator = self.accumulator * -1
        else:
            self.accumulator %= Globals.MODULO
    def divide(self, addr):
        """
        Divide the accumulator by the value from memory.

        Raises ZeroDivisionError if the value is zero.
        """
        if self.memory.get(addr) == 0:
            raise ZeroDivisionError("Error: Division by zero")
        self.accumulator //= self.memory.get(addr)
        if (self.accumulator < 0):
            self.accumulator = self.accumulator * -1
            if (self.word_length == 4):
                self.accumulator %= Globals.MODULO
            else:
                self.accumulator %= Globals.MODULO_LARGE
            self.accumulator = self.accumulator * -1
        else:
            self.accumulator %= Globals.MODULO
    def multiply(self, addr):
        """
        Multiply the accumulator by the value from memory.
        """
        self.accumulator *= self.memory.get(addr)
        if (self.accumulator < 0):
            self.accumulator = self.accumulator * -1
            if (self.word_length == 4):
                self.accumulator %= Globals.MODULO
            else:
                self.accumulator %= Globals.MODULO_LARGE
            self.accumulator = self.accumulator * -1
        else:
            self.accumulator %= Globals.MODULO

    # Control
    def branch(self, operand: int) -> None:
        """
        Unconditionally jump to a specific memory address.
        """
        if 0 <= operand < len(self.memory.memory):
            self.instruction_count = operand
        #If it isn't stop the program 
        else:
            print("Invalid operand: Out of Memory Range")
            self.halt()
    def branchNeg(self, operand: int) -> None:
        """
        Conditionally jump if the accumulator is negative
        """
        if self.accumulator < 0:
            self.branch(operand)
        
    def branchZero(self, operand: int) -> None:
        """
        Conditionally jump if the accumulator is zero.
        """
        if self.accumulator == 0:
            self.branch(operand)
        
    def halt(self, _=None) -> None:
        """Halt execution of the CPU"""
        self.running = False

    def reset(self):
        """
        Reset the CPU state to its initial state.
        """
        self.accumulator = 0
        self.instruction_count = 0
        self.running = True
