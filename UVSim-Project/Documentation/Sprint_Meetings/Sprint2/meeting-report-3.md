# Meeting Report

**Date:** June 6, 2025  
**Attendees:** Anthony, Brandon, Andie

## Agenda
- Review User Stories and user cases. 

## Action Items
Check the user cases and user stories for the design document.
- **Andie:**  
  - 1 user story and 2–4, user cases
- **Brandon:**  
  - 1 user story and 2–4, user cases
- **Anthony:**  
  - 1 user story and 2–4, user cases 

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

