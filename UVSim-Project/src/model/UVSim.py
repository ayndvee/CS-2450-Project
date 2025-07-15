from .Memory import Memory
from .IOHandler import IOHandler
from .CPU import CPU


class UVSIM:
    def __init__(self, gui=False):
        """Set up the components: memory, IO handler, CPU"""
        self.memory = Memory()
        self.io = IOHandler(gui)
        self.cpu = CPU(self.memory, self.io)

    def read_file(self, file: str) -> bool:
        """Open and read the file into memory"""
        with open(file, 'r') as filename:
            lines = filename.readlines()
        return self.memory.load_program(lines)
    
    def save_file(self, file: str) -> bool:
        """Save the current memory state to a file"""
        try:
            with open(file, 'w') as filename:
                lines = self.memory.getLines()
                for i in range(len(lines)):
                    filename.write(f"{lines[i]}\n")
            return True
        except Exception as e:
            return False

    def reset(self):
        """Reset the machine to initial state"""
        self.memory.reset()
        self.cpu.reset()

    def execute(self):
        """Start executing instructions"""
        self.cpu.execute()
