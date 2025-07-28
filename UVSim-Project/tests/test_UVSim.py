import unittest
from model.UVSim import UVSIM
from unittest.mock import patch
from io import StringIO

### HERE is how to run the tests PYTHONPATH=./src python -m unittest discover -s tests ###



class TestUVSIM(unittest.TestCase):

    def setUp(self):
        ## This sets up a UVSim instance for each test case
        self.sim = UVSIM()
        self.sim.cpu.running = True
        self.sim.cpu.instruction_count = 0
        self.sim.cpu.accumulator = 0

    ## Here we would create the functions for testing each of our use cases.


   ## An example of what a unittest would look like
    def test_branch_instruction_count(self):
        ## Expected to update the instruction_count to the operand value
        self.sim.cpu.branch(42)
        self.assertEqual(self.sim.cpu.instruction_count, 42)
    def test_branch_out_of_bounds(self):
        ## Expected to set running to False if we have operand out of bounds
        self.sim.cpu.branch(999)
        self.assertFalse(self.sim.cpu.running)
    def test_branchNeg_negative_accumulator(self):
        ## Expected to branch if the accumulator is negative 
        self.sim.cpu.accumulator = -5
        self.sim.cpu.branchNeg(20)
        self.assertEqual(self.sim.cpu.instruction_count, 20)
    def test_branchNeg_positive_accumulator(self):
        ## Expected to update instruction count if accumulator is not negative
        self.sim.cpu.accumulator = 5
        self.sim.cpu.instruction_count = 1
        self.sim.cpu.branchNeg(72)
        self.assertEqual(self.sim.cpu.instruction_count, 1)
    def test_branchZero_accumulator_zero(self):
        ## Expected to branch if accumulator is 0
        self.sim.cpu.accumulator = 0
        self.sim.cpu.branchZero(44)
        self.assertEqual(self.sim.cpu.instruction_count, 44)
    def test_branchZero_accumulator_positive(self):
        ## Expected to update instruction count if accumulator is not 0
        self.sim.cpu.accumulator = 12
        self.sim.cpu.instruction_count = 4
        self.sim.cpu.branchZero(12)
        self.assertEqual(self.sim.cpu.instruction_count, 4)
    def test_halt_running_false(self):
        # Expected that the self.running would be false after halt
        self.sim.cpu.halt()
        self.assertFalse(self.sim.cpu.running)
    def test_halt_branch_after(self):
        ## Expected that after a halt call no other input is used.
        self.sim.cpu.word_length = 4
        self.sim.memory.memory[0] = 4300
        self.sim.memory.memory[1] = 4015
        self.sim.cpu.execute()
        self.assertEqual(self.sim.cpu.instruction_count, 1)

    def test_invalid_instruction_format(self):
        ## Expected that it should halt if there is a 5 digit number
        self.sim.cpu.word_length = 6
        self.sim.memory.memory[0] = 99999  # Invalid 5-digit number
        with self.assertRaises(RuntimeError):
            self.sim.cpu.execute()

    def test_memory_limit_overflow(self):
        # Expected that it should fail after after the instruction count goes out of memory limit
        self.sim.cpu.instruction_count = 100
        self.sim.cpu.execute()
        self.assertFalse(self.sim.cpu.running)

    def test_add(self):
        # memory[30] = 1000, expect accumulator = 1000 after add
        self.sim.memory.memory[30] = 1000
        self.sim.cpu.accumulator = 500
        self.sim.cpu.add(30)
        self.assertEqual(self.sim.cpu.accumulator, 1500)

    def test_add_negative(self):
        # memory[30] = -2000, expect accumulator = -1500 after add
        self.sim.memory.memory[30] = -2000
        self.sim.cpu.accumulator = 500
        self.sim.cpu.add(30)
        self.assertEqual(self.sim.cpu.accumulator, -1500)

    def test_subtract(self):
        # memory[30] = 1000, expect accumulator = -500 after subtract
        self.sim.memory.memory[30] = 1000
        self.sim.cpu.accumulator = 500
        self.sim.cpu.subtract(30)
        self.assertEqual(self.sim.cpu.accumulator, -500)

    def test_subtract_negative(self):
        # memory[30] = -2000, expect accumulator = 2500 after subtract
        self.sim.memory.memory[30] = -2000
        self.sim.cpu.accumulator = 500
        self.sim.cpu.subtract(30)
        self.assertEqual(self.sim.cpu.accumulator, 2500)

    def test_multiply(self):
        # memory[30] = 3, expect accumulator = 1500 after multiply
        self.sim.memory.memory[30] = 3
        self.sim.cpu.accumulator = 500
        self.sim.cpu.multiply(30)
        self.assertEqual(self.sim.cpu.accumulator, 1500)

    def test_multiply_zero(self):
        # memory[30] = 0, expect accumulator = 0 after multiply
        self.sim.memory.memory[30] = 0
        self.sim.cpu.accumulator = 500
        self.sim.cpu.multiply(30)
        self.assertEqual(self.sim.cpu.accumulator, 0)

    def test_multiply_negative(self):
        # memory[30] = -2, expect accumulator = -1000 after multiply
        self.sim.memory.memory[30] = -2
        self.sim.cpu.accumulator = 500
        self.sim.cpu.multiply(30)
        self.assertEqual(self.sim.cpu.accumulator, -1000)

    def test_divide(self):
        # memory[30] = 2, expect accumulator = 250 after divide
        self.sim.memory.memory[30] = 2
        self.sim.cpu.accumulator = 500
        self.sim.cpu.divide(30)
        self.assertEqual(self.sim.cpu.accumulator, 250)

    def test_divide_zero(self):
        # memory[30] = 0, expect no change in accumulator and error message
        self.sim.memory.memory[30] = 0
        self.sim.cpu.accumulator = 500
        with self.assertRaises(ZeroDivisionError):
            self.sim.cpu.divide(30) 

     # --- LOAD / STORE Tests ---

    def test_load(self):
        # memory[10] = 1234, expect accumulator = 1234 after load
        self.sim.memory.memory[10] = 1234
        self.sim.cpu.load(10)
        self.assertEqual(self.sim.cpu.accumulator, 1234)

    def test_store(self):
        # accumulator = -5678, expect memory[20] = -5678 after store
        self.sim.cpu.accumulator = -5678
        self.sim.cpu.store(20)
        self.assertEqual(self.sim.memory.memory[20], -5678)

    # --- I/O Tests ---

    @patch('builtins.input', return_value='+3456')
    def test_read(self, mock_input):
        # Simulates user entering "3456" as input
        self.sim.io.read(5, self.sim.memory)
        self.assertEqual(self.sim.memory.memory[5], 3456)

    @patch('sys.stdout', new_callable=StringIO)
    def test_write(self, mock_stdout):
        # memory[7] = -2222, expect output "-2222\n"
        self.sim.memory.memory[7] = -2222
        self.sim.io.write(7,self.sim.memory)
        self.assertEqual(mock_stdout.getvalue(), "-2222\n")