# Final System Test Report - UVSIM

## Overview
This document contains the functional, non-functional, and regressional testing performed for the UVSim project.
It includes test outcomes, observations, and any issues encountered and resolved.
All of the testing was done through unittest.

# Functional Tests:
Here are some examples of some of our functional test cases:
| **Test Description**                  | **Expected Result**                        | **Actual Result**       | **Status** |
|--------------------------------------|--------------------------------------------|--------------------------|------------|
| `branch(42)` sets instruction pointer | `instruction_count` becomes 42             | ✅ Matches               | ✅ Pass     |
| `add(30)` with memory[30] = 1000      | Accumulator increases by 1000              | ✅ Acc = 1500            | ✅ Pass     |
| `divide(30)` with memory[30] = 0      | Raises `ZeroDivisionError`                 | ✅ Exception raised      | ✅ Pass     |
| `read(5)` stores +3456                | Memory[5] updated to 3456                  | ✅ Matches               | ✅ Pass     |
| `halt()` stops execution              | `cpu.running` becomes `False`              | ✅ Matches               | ✅ Pass     |



# Non-Functional Tests:
Here are some example of some of our non-functional test cases:
| Description                  | Expected Result             | Actual Result           | Status |
|------------------------------|-----------------------------|-------------------------|--------|
| Load time for 100-line file  | Under 2 seconds             | <1 second               | ✅ Pass |
| App runs without crashing    | No crashes in normal use    | No crashes occurred     | ✅ Pass |
| UI responsiveness            | UI buttons respond instantly| Immediate response       | ✅ Pass |
| Theme switching              | Theme updates UI colors     | All tabs update color   | ✅ Pass |

# Regression Testing
We performed regression testing thorugh the development by re-running our unittest tests after we added new features or functionality was modified.
This helped to ensure that core features were still working as intended after code changes.

| Description                                  | Expected Result                           | Actual Result                          | Status  |
|----------------------------------------------|--------------------------------------------|-----------------------------------------|---------|
| Load and run previously working file         | File loads and runs without error          | File loaded and ran successfully        | ✅ Pass  |
| Theme switching after UI changes             | Theme applies to all tabs and elements     | Theme updated across all UI elements    | ✅ Pass  |
| Tab switching works after tab system update  | Can switch between tabs without issues     | Tab switching functional                | ✅ Pass  |
| Error handling after input validation edits  | Invalid input shows correct error message  | Error popup displayed as expected       | ✅ Pass  |
| Clear memory button after refactor           | Clears output and memory without crashing  | Output and memory cleared successfully  | ✅ Pass  |


# Observation

We observed that the program behaves as expected when used normally.
All of the major featues ran as expected under our testing.
The user interface was responsive and consistent even after updates.
No crashs or unexpected behavior were encountered during or after testing.

# Resolved Issues

There were a couple of issues we ran into while trying to test some features of the project:
    - Fixed an issue where the tab color wasn't updating with the rest of the theme.
    - Resolved an issue where output console wasn't showing all the relevant information on the screen.
    - Fixed an issue where program where loading memory from the editor wouldn't update memory slots, but still ran.

# Code Coverage

We ran a code coverage report and it gave us the result of 81% of all our code was tested
For a visual result of the tests: ![Code Coverage](code_coverage.md)

# Conclusion

The system is functional across expected use cases. Our functional, non-functional, and regression testing shows that UVSim program meets design goals. Future testing could include more edge cases or checking more performance on larger files. The program is ready for submission.