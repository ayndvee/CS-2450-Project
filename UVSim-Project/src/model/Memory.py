from globals.Util import Globals

class Memory:
    def __init__(self) -> None:
        """Set up memory and spareMemory"""
        self.memory = [0] * Globals.MEMORYSIZE_LARGE
        self.spareMemory = [0] * Globals.MEMORYSIZE_LARGE
        self.word_length = None

    def load_program(self, lines: list[str]) -> bool:
        """Loads a program from a list of strings into memory.
        Supports both 4-digit and 6-digit signed words (e.g., +1234 or +001234),
        but does NOT allow mixing formats in the same file.
        Returns True if loading is successful, False otherwise.
        """


        for i, line in enumerate(lines):

            line = line.strip()

            if line == str(Globals.STOP):
                break
            if not line:
                print(f"Error on line {i}: there is no line")
                return False
            if not line[0] in '+-':
                print(f"Error on line {i}: must be signed with + or -")
                return False
            if not line[1:].isdigit():
                print(f"Error on line {i}: must be numbers after the sign")
                return False
            
            # Determine and enforce consistent word length across the file
            current_length = len(line[1:])
            if self.word_length is None:
                if current_length not in (4, 6):
                    print(f"Error on line {i}: unsupported word length {current_length}")
                    return False
                self.word_length = current_length
            elif current_length != self.word_length:
                # Later lines must match the original length
                print(f"Error on line {i}: inconsistent word length (expected {self.word_length}, got {current_length})")
                return False

            # Memory check overflow
            if (self.word_length == 4 and i >= Globals.MEMORYSIZE) or (self.word_length == 6 and i >= Globals.MEMORYSIZE_LARGE):
                print("Error: too many lines for memory capacity")
                return False
            
            try:
                value = int(line)
            except ValueError:
                print(f"Error on line {i}: invalid integer format")
                return False

            self.memory[i] = int(line)
            self.spareMemory[i] = int(line)
        return True
    
    def getLines(self) -> list[str]:
        """Returns the memory as a list of strings"""
        if self.word_length == 4:
            return [f"{value:+05d}" for value in self.memory]
        else:
            return [f"{value:+07d}" for value in self.memory]
    
    def clear(self):
        """Clears memory when updating new tab"""
        for i in range(Globals.MEMORYSIZE):
            self.memory[i] = 0
            self.spareMemory[i] = 0

    def reset(self):
        """Reset memory to original spare copy"""
        for i in range(Globals.MEMORYSIZE):
            self.memory[i] = self.spareMemory[i]

    def get(self, address: int) -> int:
        return self.memory[address]

    def set(self, address: int, value: int) -> None:
        self.memory[address] = value

    def get_all(self) -> list[int]:
        return self.memory[:]
