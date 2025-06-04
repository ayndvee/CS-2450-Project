# Meeting Report

**Date:** June 3, 2025  
**Attendees:** Anthony, Brandon, Andie

## Agenda
- Overview of the project
- Assign feature areas (I/O, arithmetic, control) 
- Propose a design for each assigned area   

## Action Items
All team members will draft 1 user story and 2–4, and contribute to early project planning.
- **Andie:**  
  - I/O and load/store operations
- **Brandon:**  
  - Arithmetic operations
- **Anthony:**  
  - Control operations
  - Create and assign issues in ZenHub   

---

# Project Requirements: UVSim Simulator

A client has hired our company to develop a software simulator called **UVSim** for computer science students to learn machine language and computer architecture. Students can execute their machine language programs on the simulator.

The UVSim is a simple but powerful virtual machine that interprets a machine language called **BasicML**.

### System Description:
- UVSim contains a CPU, register, and main memory.
- **Accumulator:** A register holding information for calculations or evaluation.
- All data is handled in terms of **words** — signed four-digit decimal numbers (e.g., +1234, -5678).
- Memory size: 100 words (addressed 00 to 99).
- The BasicML program loads starting at memory location 00 before execution.
- Each instruction is one word, always positive (+), while data words can be positive or negative.
- Each memory location may contain instructions, data values, or unused space.
- Instruction format: First two digits = operation code; last two digits = operand (memory address).

# Project Design Proposal

Each team member will come up with a design proposal including:  
- 1 user story  
- 2 to 4 use cases  

### Assigned Focus Areas:
- **Andie:** I/O and load/store operations  
- **Brandon:** Arithmetic operations  
- **Anthony:** Control operations

# Question Raised

**What is the difference between a user story and a use case?**

- **User Story:** A brief, high-level description of what a user wants to achieve.  
- **Use Case:** A detailed step-by-step description of how the system and user interact to accomplish a goal.