# UVSim - Use Cases and User Stories

## User Stories

- **As a student**, I want to write and run programs in BasicML so that I can learn to use machine language.
- **As a student**, I want to be able to load and store values into memory, so I can manipulate data.
- **As a CS student**, I want error messages if there are invalid inputs, so that I can fix errors and learn why it went wrong.
- **As a teacher**, I want to run student-made programs written in BasicML so that I can grade their work.

---

## Use Cases

### Discover and Understand UVSim
**Actor**: Student  
**Goal**: Learn about UVSim  
**System Steps**:
- Student finds UVSim
- Student sees README file
- Student reads README file
- Student understands how to write and run programs with UVSim

---

### Write and Run a Program
**Actor**: Student  
**Goal**: Run a BasicML program and see the result  
**System Steps**:
- Student writes and saves a program for UVSim
- Student runs UVSim from the command line
- Command line opens UVSim and passes the program file as an argument
- UVSim reads the program and executes instructions
- Student sees output and submits file for grading

---

### Grade Student Work
**Actor**: Professor  
**Goal**: Run student program to grade it  
**System Steps**:
- Professor gives student an assignment
- Student submits the program file
- Professor runs UVSim from the command line
- UVSim loads and runs the program file
- Professor sees output and evaluates it

---

### Run Addition Example
**Actor**: Student  
**Goal**: Solve a math problem using UVSim  
**System Steps**:
- Student runs UVSim and loads a program:
    ```
    1099
    2099
    1099
    3099
    2199
    1199
    4300
    ```
- UVSim prompts student for two numbers
- Student enters values
- UVSim adds them, stores result in memory, writes it to console

---

### Load BasicML File
**Actor**: User  
**Goal**: Load a `.txt` file with BasicML instructions  
**System Steps**:
- UVSim opens the file
- UVSim reads each line and stores it in memory

---

### Validate Instruction Format
**Actor**: UVSim  
**Goal**: Ensure all instructions are valid  
**System Steps**:
- UVSim checks each line is a signed 4-digit number
- If invalid, print error and stop

---

### Handle 100-Word Memory Limit
**Actor**: UVSim  
**Goal**: Prevent overflow  
**System Steps**:
- UVSim checks instruction count
- If over 100, print error and halt

---

### Run from Command Line
**Actor**: User  
**Goal**: Execute UVSim with a file argument  
**System Steps**:
- User enters filename in terminal
- UVSim reads and executes it

---

### Handle Invalid Opcode
**Actor**: UVSim  
**Goal**: Report unrecognized opcodes  
**System Steps**:
- If opcode is invalid, print error and stop execution

---

### Branch Command
**Actor**: UVSim  
**Goal**: Jump to a different memory address  
**System Steps**:
- UVSim sets the instruction counter to the operand value

---

### BranchNeg Command
**Actor**: UVSim  
**Goal**: Conditional jump if accumulator is negative  
**System Steps**:
- If accumulator < 0, set instruction counter to operand
- Else, increment instruction counter

---

### BranchZero Command
**Actor**: UVSim  
**Goal**: Conditional jump if accumulator is zero  
**System Steps**:
- If accumulator == 0, set instruction counter to operand
- Else, increment instruction counter

---

### Halt Command
**Actor**: UVSim  
**Goal**: Stop program execution  
**System Steps**:
- Set running flag to false and end program

---

### Command Line Error Reporting
**Actor**: UVSim  
**Goal**: Report errors during execution  
**System Steps**:
- UVSim prints descriptive errors to console

---

### Arithmetic: Add
**Actor**: UVSim  
**Goal**: Add two values  
**System Steps**:
- Add value in memory to accumulator
- Store result in accumulator

---

### Arithmetic: Subtract
**Actor**: UVSim  
**Goal**: Subtract value from accumulator  
**System Steps**:
- Subtract memory value from accumulator
- Store result

---

### Arithmetic: Multiply
**Actor**: UVSim  
**Goal**: Multiply values  
**System Steps**:
- Multiply accumulator and memory value
- Store result in accumulator

---

### Arithmetic: Divide
**Actor**: UVSim  
**Goal**: Divide values  
**System Steps**:
- Divide accumulator by memory value
- Store result in accumulator (truncate remainder)

---

### Divide by Zero
**Actor**: UVSim  
**Goal**: Prevent undefined operations  
**System Steps**:
- If divisor is zero, throw error and stop

---

### READ Input from User
**Actor**: Student  
**Goal**: Provide value during execution  
**System Steps**:
- UVSim prompts user
- User enters signed 4-digit number
- UVSim stores it in memory

---

### WRITE Output to Console
**Actor**: UVSim  
**Goal**: Display value during execution  
**System Steps**:
- UVSim retrieves value from memory
- UVSim prints value to console

---

### LOAD Value into Accumulator
**Actor**: UVSim  
**Goal**: Prepare data for computation  
**System Steps**:
- UVSim reads value from memory
- UVSim stores it in accumulator

---

### STORE Accumulator Value
**Actor**: UVSim  
**Goal**: Save current value to memory  
**System Steps**:
- UVSim writes accumulator value to memory
