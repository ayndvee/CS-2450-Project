MEMORYSIZE = 100

class Memory:
    def __init__(self) -> None:
        """Set up memory and spareMemory"""
        self.memory = [0] * MEMORYSIZE
        self.spareMemory = [0] * MEMORYSIZE

    def load_program(self, lines: list[str]) -> bool:
        """Loads a program from a list of strings into memory"""
        for i, line in enumerate(lines):
            if i >= MEMORYSIZE:
                print("Error too many lines for memory capacity")
                return False

            line = line.strip()

            if line == '-99999':
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
            if len(line[1:]) != 4:
                print(f"Error on line {i}: must be exactly 4 numbers after the sign")
                return False

            self.memory[i] = int(line)
            self.spareMemory[i] = int(line)
        return True
    
    def getLines(self) -> list[str]:
        """Returns the memory as a list of strings"""
        return [f"{value:+05d}" for value in self.memory]

    def reset(self):
        """Reset memory to original spare copy"""
        for i in range(MEMORYSIZE):
            self.memory[i] = self.spareMemory[i]

    def get(self, address: int) -> int:
        return self.memory[address]

    def set(self, address: int, value: int) -> None:
        self.memory[address] = value

    def get_all(self) -> list[int]:
        return self.memory[:]
