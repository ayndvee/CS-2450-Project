# Software Requirements Specification
## For UVSim Project

Version 0.1  
Prepared by Brandon Walton 
Group G1
6/23/25

## Functional:
* UVSim can read in a program of 100 or fewer words written in BasicML and run it.
* UVSim can detect improper input in the provided program and provide a corresponding error message instead of attempting to run it.
* While running a program, UVSim can use a read operation to store a word from the keyboard to a specific location in memory.
* While running a program, UVSim can use a write operation to write a word from a specific location in memory to the screen.
* While running a program, UVSim can use a load operation to load a word from a specific location in memory into the accumulator.
* While running a program, UVSim can use a store operation to store a word from the accumulator in a specific location in memory.
* While running a program, UVSim can use an add operation to add the values of two words together, storing the result in the accumulator.
* While running a program, UVSim can use a subtract operation to subtract the value of one word from the value of another, storing the result in the accumulator.
* While running a program, UVSim can use a multiply operation to multiply the value of two words together, storing the result in the accumulator.
* While running a program, UVSim can use a divide operation to divide the value of a word by the value of another, storing the result in the accumulator and ignoring the remainder if one exists.
* While running a program, UVSim can ignore a divide operation if it will cause a divide by 0.
* While running a program, UVSim can use a branch operation to jump to a specific word in memory, executing its instruction next.
* While running a program, UVSim can use a conditional branch operation that jumps to a specific word in memory if the value in the accumulator is negative.
* While running a program, UVSim can use a conditional branch operation that jumps to a specific word in memory if the value in the accumulator is 0.
* While running a program, UVSim can use a halt operation to stop running the program.
 
## Nonfunctional:
* UVSim should be able to load and begin running a properly formatted program in under a second.
* UVSim should run without problems on the vast majority of modern computing systems.
* UVSim should run entirely on the client-side and as such should remain available in any situation where the user's system is functional.
