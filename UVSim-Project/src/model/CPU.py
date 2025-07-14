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
            Opcode.READ: self.read,
            Opcode.WRITE: self.write,
            Opcode.LOAD: self.load,
            Opcode.STORE: self.store,
            Opcode.ADD: self.add,
            Opcode.SUBTRACT: self.subtract,
            Opcode.MULTIPLY: self.multiply,
            Opcode.DIVIDE: self.divide,
            Opcode.BRANCH: self.branch,
            Opcode.BRANCHNEG: self.branchNeg,
            Opcode.BRANCHZERO: self.branchZero,
            Opcode.HALT: self.halt
        }

    def execute(self):
        while self.running:
            if self.instruction_count >= 100:
                print("Error: Instruction pointer out of memory bounds.")
                self.halt()
                break
            code, op = divmod(self.memory.get(self.instruction_count), 100)
            method = self.OPCODES.get(code)
            if method is None:
                raise RuntimeError(f"Unknown opcode: {code} at Instruction: {self.instruction_count}")
            method(op)
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
    def branch(self, addr): self.instruction_count = addr
    def branchNeg(self, addr): 
        if self.accumulator < 0: self.branch(addr)
    def branchZero(self, addr): 
        if self.accumulator == 0: self.branch(addr)
    def halt(self, _=None): self.running = False

    def reset(self):
        self.accumulator = 0
        self.instruction_count = 0
        self.running = True
