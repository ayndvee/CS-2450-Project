from globals.Util import Globals


class IOHandler:
    def __init__(self, gui_mode: bool = False):
        self.gui = gui_mode
        self.input = Globals.STOP
        self.output = False
        self.outputValue = ""

    def read(self, address: int, memory) -> bool:
        if self.gui:
            if self.input != Globals.STOP:
                value = self.input
                if (value.startswith(('+', '-')) and value[1:].isdigit() and len(value) in (Globals.MINWORDLEN+1, Globals.MAXWORDLEN+1)):
                    memory.set(address, int(value))
                    self.input = Globals.STOP
                    return True
                return False
            return False
        else:
            value = input(f"Enter a signed 4-digit number for memory[{address}]: ")
            while not (value.startswith(('+', '-')) and value[1:].isdigit() and len(value) == Globals.MINWORDLEN+1):
                print("Invalid input. Please enter a signed 4-digit number like +1234 or -5678.")
                value = input(f"Enter a signed 4-digit number for memory[{address}]: ")
            memory.set(address, int(value))
            return True

    def write(self, address: int, memory):
        self.outputValue = f"{memory.get(address):+0{memory.word_length+1}d}"
        self.output = True
        print(f"{memory.get(address)}")
