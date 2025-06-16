import unittest
from unittest.mock import patch
from io import StringIO
from src.UVSim import UVSIM

#Run PYTHONPATH=src python3 -m unittest discover -s tests -p "test_load.py"

class TestUVSIM(unittest.TestCase):

    def setUp(self):
        self.sim = UVSIM()
        self.sim.running = True
        self.sim.instruction_count = 0
        self.sim.accumulator = 0

    # --- LOAD / STORE Tests ---

    def test_load(self):
        # memory[10] = 1234, expect accumulator = 1234 after load
        self.sim.memory[10] = 1234
        self.sim.load(10)
        self.assertEqual(self.sim.accumulator, 1234)

    def test_store(self):
        # accumulator = -5678, expect memory[20] = -5678 after store
        self.sim.accumulator = -5678
        self.sim.store(20)
        self.assertEqual(self.sim.memory[20], -5678)

    # --- I/O Tests ---

    @patch('builtins.input', return_value='+3456')
    def test_read(self, mock_input):
        # Simulates user entering "3456" as input
        self.sim.read(5)
        self.assertEqual(self.sim.memory[5], 3456)

    @patch('sys.stdout', new_callable=StringIO)
    def test_write(self, mock_stdout):
        # memory[7] = -2222, expect output "-2222\n"
        self.sim.memory[7] = -2222
        self.sim.write(7)
        self.assertEqual(mock_stdout.getvalue(), "-2222\n")
