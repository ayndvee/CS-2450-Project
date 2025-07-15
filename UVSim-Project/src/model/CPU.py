from Util import Globals\

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
    def __init__(self, memory, io_handler):
        self.memory = memory
        self.io = io_handler
        self.accumulator = 0
        self.instruction_count = 0
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
        while self.running:
            if self.instruction_count >= Globals.MEMORYSIZE:
                print("Error: Instruction pointer out of memory bounds.")
                self.halt()
                break
            code, op = divmod(self.memory.get(self.instruction_count), Globals.MEMORYSIZE)
            method = self.OPCODES.get(code)
            if method is None:
                raise RuntimeError(f"Unknown opcode: {code} at Instruction: {self.instruction_count}")
            handler = getattr(self, method)
            handler(op)   
            self.instruction_count += 1

    # I/O
    def read(self, addr): self.running = self.io.read(addr, self.memory)
    def write(self, addr): self.io.write(addr, self.memory)

    # Load/Store
    def load(self, addr): self.accumulator = self.memory.get(addr)
    def store(self, addr): self.memory.set(addr, self.accumulator)

    # Math
    def add(self, addr): self.accumulator += self.memory.get(addr)
    def subtract(self, addr): self.accumulator -= self.memory.get(addr)
    def divide(self, addr):
        if self.memory.get(addr) == 0:
            raise ZeroDivisionError("Error: Division by zero")
        self.accumulator //= self.memory.get(addr)
    def multiply(self, addr): self.accumulator *= self.memory.get(addr)

    # Control
    def branch(self, operand: int) -> None:
        """Check to make sure operand is in the bounds of memory"""
        if 0 <= operand < len(self.memory.memory):
            self.instruction_count = operand
        #If it isn't stop the program 
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

    def reset(self):
        self.accumulator = 0
        self.instruction_count = 0
        self.running = True
