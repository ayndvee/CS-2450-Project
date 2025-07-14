class IOHandler:
    def __init__(self, gui_mode: bool = False):
        self.gui = gui_mode
        self.input = -99999
        self.output = False
        self.outputValue = ""

    def read(self, address: int, memory) -> bool:
        if self.gui:
            if self.input != -99999:
                value = self.input
                if value.startswith(('+', '-')) and value[1:].isdigit() and len(value) == 5:
                    memory.set(address, int(value))
                    self.input = -99999
                    return True
                return False
            return False
        else:
            value = input(f"Enter a signed 4-digit number for memory[{address}]: ")
            while not (value.startswith(('+', '-')) and value[1:].isdigit() and len(value) == 5):
                print("Invalid input. Please enter a signed 4-digit number like +1234 or -5678.")
                value = input(f"Enter a signed 4-digit number for memory[{address}]: ")
            memory.set(address, int(value))
            return True

    def write(self, address: int, memory):
        self.outputValue = f"{memory.get(address):+04d}"
        self.output = True
        print(f"{memory.get(address)}")
