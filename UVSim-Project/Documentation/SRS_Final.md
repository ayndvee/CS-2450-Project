# SRS Document
Authored by: Anthony, Andie, and Brandon


# Functional Requirements
1. The system shall load a proper BasicML program up to 100 instructions from a file into memory starting with location 00.
2. The system shall have up to 100 word memory limit.
3. The system shall execute the READ instruction, to store a signed 4 digit integer from the user into memory.
4. The system shall execute the WRITE instruction, to write a signed 4 digit integer from specific location in memory to the screen.
5. The system shall execute the LOAD instruction, to load a specific location in memory to the accumulator
6. The system shall execute the STORE instruction, to save the accumulator contents into a specific location in memory.
7. The system shall execute the ADD instruction, to add by a value from memory into the accumulator and store the result in the accumulator.
8. The system shall execute the SUBTRACT instruction, to subtracts by a value from memory from the accumulator and store the result in the accumulator
9. The system shall execute the MULTIPLY instruction, to multiply by a value from memory with the value in the accumulator and store the result in the accumulator
10. The system shall execute the DIVIDE instruction, to divide by a value from memory with the value in the accumulator and store the result in the accumulator.
11. The system shall detect a divide by zero and skip it, resulting in an error message on the screen.
12. The system shall execute a BRANCH instruction, jumping to a specific location in memory and continuing the program.
13. The system shall execute a BRANCHNEG and BRANCHZERO instructions
	+ BRANCHNEG: if the accumulator is negative
	+ BRANCHZERO: if the accumulator is zero
14. The system shall execute the HALT instruction, which will stop running instructions when it is encountered. 
15. The system shall detect invalid or unknown instructions and display an error message on the screen.
16. The system shall check the loaded program for invalid formatting or instructions and prevent it from running, if errors are found.
17. The system shall visually display the currently executing instruction and memory state in the GUI.
18. The system shall allow the user to reset the memory and accumulator to their initial state


# Non-Functional Requirements
1. The system shall begin running a valid BasicML program within 2 seconds of being loaded.
2. The system shall run on most modern computers without special configuration.
3. The system shall be written in Python using a modular structure to support future updates.
4. The system shall have data integrity while running, making sure that the memory and accumulator are not corrupted.