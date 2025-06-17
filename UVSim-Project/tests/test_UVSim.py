import unittest
from src.UVSim import UVSIM

### HERE is how to run the tests PYTHONPATH=src python -m unittest discover -s tests ###



class TestUVSIM(unittest.TestCase):

    def setUp(self):
        ## This sets up a UVSim instance for each test case
        self.sim = UVSIM()
        self.sim.running = True
        self.sim.instruction_count = 0
        self.sim.accumulator = 0

    ## Here we would create the functions for testing each of our use cases.


    ## An example of what a unittest would look like
    def test_branch_instruction_count(self):
        ## Expected to update the instruction_count to the operand value
        self.sim.branch(42)
        self.assertEqual(self.sim.instruction_count, 42)
    def test_branch_out_of_bounds(self):
        ## Expected to set running to False if we have operand out of bounds
        self.sim.branch(101)
        self.assertFalse(self.sim.running)
    def test_branchNeg_negative_accumulator(self):
        ## Expected to branch if the accumulator is negative 
        self.sim.accumulator = -5
        self.sim.branchNeg(20)
        self.assertEqual(self.sim.instruction_count, 20)
    def test_branchNeg_positive_accumulator(self):
        ## Expected to update instruction count if accumulator is not negative
        self.sim.accumulator = 5
        self.sim.instruction_count = 1
        self.sim.branchNeg(72)
        self.assertEqual(self.sim.instruction_count, 2)
    def test_branchZero_accumulator_zero(self):
        ## Expected to branch if accumulator is 0
        self.sim.accumulator = 0
        self.sim.branchZero(44)
        self.assertEqual(self.sim.instruction_count, 44)
    def test_branchZero_accumulator_positive(self):
        ## Expected to update instruction count if accumulator is not 0
        self.sim.accumulator = 12
        self.sim.instruction_count = 4
        self.sim.branchZero(12)
        self.assertEqual(self.sim.instruction_count, 5)
    def test_halt_running_false(self):
        # Expected that the self.running would be false after halt
        self.sim.halt()
        self.assertFalse(self.sim.running)
    def test_halt_branch_after(self):
        ## Expected that after a halt call no other input is used.
        self.sim.memory[0] = 4300
        self.sim.memory[1] = 4015
        self.sim.execute()
        self.assertEqual(self.sim.instruction_count, 1)

    def test_add(self):
        # memory[30] = 1000, expect accumulator = 1000 after add
        self.sim.memory[30] = 1000
        self.sim.accumulator = 500
        self.sim.add(30)
        self.assertEqual(self.sim.accumulator, 1500)
    
    def test_add_negative(self):
        # memory[30] = -2000, expect accumulator = -1500 after add
        self.sim.memory[30] = -2000
        self.sim.accumulator = 500
        self.sim.add(30)
        self.assertEqual(self.sim.accumulator, -1500)

    def test_subtract(self):
        # memory[30] = 1000, expect accumulator = -500 after subtract
        self.sim.memory[30] = 1000
        self.sim.accumulator = 500
        self.sim.subtract(30)
        self.assertEqual(self.sim.accumulator, -500)

    def test_subtract_negative(self):
        # memory[30] = -2000, expect accumulator = 2500 after subtract
        self.sim.memory[30] = -2000
        self.sim.accumulator = 500
        self.sim.subtract(30)
        self.assertEqual(self.sim.accumulator, 2500)

    def test_multiply(self):
        # memory[30] = 3, expect accumulator = 1500 after multiply
        self.sim.memory[30] = 3
        self.sim.accumulator = 500
        self.sim.multiply(30)
        self.assertEqual(self.sim.accumulator, 1500)

    def test_multiply_zero(self):
        # memory[30] = 0, expect accumulator = 0 after multiply
        self.sim.memory[30] = 0
        self.sim.accumulator = 500
        self.sim.multiply(30)
        self.assertEqual(self.sim.accumulator, 0)

    def test_multiply_negative(self):
        # memory[30] = -2, expect accumulator = -1000 after multiply
        self.sim.memory[30] = -2
        self.sim.accumulator = 500
        self.sim.multiply(30)
        self.assertEqual(self.sim.accumulator, -1000)

    def test_divide(self):
        # memory[30] = 2, expect accumulator = 250 after divide
        self.sim.memory[30] = 2
        self.sim.accumulator = 500
        self.sim.divide(30)
        self.assertEqual(self.sim.accumulator, 250)

    def test_divide_zero(self):
        # memory[30] = 0, expect no change in accumulator and error message
        self.sim.memory[30] = 0
        self.sim.accumulator = 500
        self.sim.divide(30)
        #Error message is printed, but we can't capture it in this test
        self.assertEqual(self.sim.accumulator, 500) 