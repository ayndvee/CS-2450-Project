import unittest
from src.UVSim import UVSIM

### HERE is how to run the tests PYTHONPATH=src python -m unittest discover -s tests ###



class TestUVSIM(unittest.TestCase):

    def setUp(self):
        ## This sets up a UVSim instance for each test case
        self.sim = UVSIM()
        self.sim.running = True
        self.sim.instruction_count = 0

    ## Here we would create the functions for testing each of our use cases.


    ## An example of what a unittest would look like
    def test_branch_instruction_count(self):
        ## Expected to update the instruction_count to the operand value
        self.sim.branch(42)
        self.assertEqual(self.sim.instruction_count, 42)
    pass
