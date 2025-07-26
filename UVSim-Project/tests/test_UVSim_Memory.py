import unittest
from model.Memory import Memory
from globals.Util import Globals

"""
How to run:
PYTHONPATH=./src python -m unittest discover -s tests
"""

class TestMemory(unittest.TestCase):
    def setUp(self):
        # Create a fresh Memory instance before each test
        self.mem = Memory()

    def test_valid_4digit_program(self):
        lines = ["+1234", "-4321", "+0001"]
        self.assertTrue(self.mem.load_program(lines))
        self.assertEqual(self.mem.memory[0], 1234)
        self.assertEqual(self.mem.memory[1], -4321)

    def test_valid_6digit_program(self):
        lines = ["+001234", "-000567", "+000001"]
        self.assertTrue(self.mem.load_program(lines))
        self.assertEqual(self.mem.memory[0], 1234)
        self.assertEqual(self.mem.memory[1], -567)

    def test_mixed_format_rejected(self):
        lines = ["+1234", "+000567"]
        self.assertFalse(self.mem.load_program(lines))

    def test_invalid_missing_sign(self):
        lines = ["1234", "+4321"]
        self.assertFalse(self.mem.load_program(lines))

    def test_invalid_non_digits(self):
        lines = ["+12a4", "+4321"]
        self.assertFalse(self.mem.load_program(lines))

    def test_unsupported_word_length(self):
        lines = ["+123", "+4321"]  # 3-digit number not supported
        self.assertFalse(self.mem.load_program(lines))

    def test_stop_instruction_stops_loading(self):
        lines = ["+1234", str(Globals.STOP), "+9999"]
        self.assertTrue(self.mem.load_program(lines))
        self.assertEqual(self.mem.memory[0], 1234)
        # After STOP, next lines should not be loaded (default 0)
        self.assertEqual(self.mem.memory[1], 0)

    def test_exceeding_memory_size(self):
        lines = ["+1234"] * (Globals.MEMORYSIZE + 1)
        self.assertFalse(self.mem.load_program(lines))

    def test_getLines_returns_correct_format(self):
        lines = ["+1234", "-4321"]
        self.mem.load_program(lines)
        output_lines = self.mem.getLines()
        self.assertEqual(output_lines[0], "+1234")
        self.assertEqual(output_lines[1], "-4321")

if __name__ == "__main__":
    unittest.main()
