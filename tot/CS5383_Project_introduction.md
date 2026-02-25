# CS5383 Project Introduction

This folder contains the **CS5383 Theory of Computation project**: a finite automaton specification and supporting materials. The project is used in collaboration with **Professor Namin** in the **Software Verification and Validation** course. The V&V course site and weekly modules live in the [software-vv](https://github.com/sweeden-ttu/software-vv) repository.

## Project Artifacts

| File | Description |
|------|-------------|
| **CS5383_Project.pdf** | Full project description and requirements. |
| **CS5383_Project_algorithm_ideas.pdf** | Algorithm ideas and design notes for the project. |
| **CS5383_Project_Machine.txt** | Machine definition and **test inputs** `(1101, 0001, 1110)`. |
| **CS5383_Project_Machine-1.txt** | Same machine definition with **no test inputs** `()`. |

## Machine Specification (NFA)

The project defines an NFA \( M = (\Sigma, K, s, F, \Delta) \) as follows:

- **Alphabet:** \(\Sigma = \{0, 1\}\)
- **States:** \(K = \{q_0, q_1, q_2\}\)
- **Start state:** \(s = q_0\)
- **Accept states:** \(F = \{q_2\}\)
- **Transition relation \(\Delta\):**
  - \((q_0, 0, q_0)\)
  - \((q_0, 1, q_0)\)
  - \((q_0, 0, q_1)\)
  - \((q_1, 1, q_2)\)

So from \(q_0\) we can stay on 0 or 1, or move to \(q_1\) on 0; from \(q_1\) we move to \(q_2\) on 1. A string is accepted iff there exists a run from \(q_0\) to \(q_2\) consuming the entire string.

**Test inputs** (in `CS5383_Project_Machine.txt`): `1101`, `0001`, `1110`. These are used to validate an implementation or simulator of the machine.

## Alignment with Software Verification and Validation

The Software V&V course ([software-vv](https://github.com/sweeden-ttu/software-vv)) applies verification and validation techniques to real specifications and implementations. This CS5383 project provides:

1. **Specification** – The NFA above is a formal, unambiguous specification (states, alphabet, transitions, accept set).
2. **Test data** – The given strings are used for **dynamic testing** (unit, integration, system) of any simulator or checker.
3. **Formal model** – The same machine can be used in **model checking** (Week 8) and **formal methods** (Week 9) as a finite-state model to verify properties (e.g., “every accepted string has a run ending in \(q_2\)”).

Weekly modules in software-vv (Introduction, Testing Basics, Unit/Integration/System/Regression Testing, Static Analysis, Model Checking, Formal Methods, Performance & Security, Final Project) are filled to reference this project where appropriate, so that the same artifact is specified once (here) and verified and validated across the V&V course.

## References

- **Project PDF and algorithm ideas:** See `CS5383_Project.pdf` and `CS5383_Project_algorithm_ideas.pdf` in this folder.
- **Machine and test inputs:** `CS5383_Project_Machine.txt`, `CS5383_Project_Machine-1.txt`.
- **Software Verification and Validation (Professor Namin):** [software-vv repository](https://github.com/sweeden-ttu/software-vv).
