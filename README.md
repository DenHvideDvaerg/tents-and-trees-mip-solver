# Tents and Trees MIP Solver

[![CI](https://github.com/DenHvideDvaerg/tents-and-trees-mip-solver/actions/workflows/CI.yml/badge.svg)](https://github.com/DenHvideDvaerg/tents-and-trees-mip-solver/actions/workflows/CI.yml)
<!-- [![Code Coverage](https://img.shields.io/codecov/c/github/DenHvideDvaerg/tents-and-trees-mip-solver?color=blue)](https://codecov.io/gh/DenHvideDvaerg/tents-and-trees-mip-solver) -->
<!-- [![PyPI version](https://img.shields.io/pypi/v/tents-and-trees-mip-solver?color=green)](https://pypi.org/project/tents-and-trees-mip-solver/) -->
<!-- [![Python](https://img.shields.io/pypi/pyversions/tents-and-trees-mip-solver?color=blue)](https://pypi.org/project/tents-and-trees-mip-solver/) -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Tents and Trees puzzle solver using mathematical programming.

## Overview

Tents and Trees is a logic puzzle where you must place tents on a grid according to specific rules:

- **Each tree must have exactly one adjacent tent** (horizontally or vertically)
- **Each tent must be adjacent to exactly one tree**  
- **Tents cannot touch each other** (even diagonally)
- **Row and column constraints** specify how many tents must be in each row/column

This solver models the puzzle as a **Mixed Integer Programming (MIP)** problem to find solutions.

## Installation

```bash
pip install tents-and-trees-mip-solver
```

## Requirements

- Python 3.9+
- Google OR-Tools
- pytest (for testing)

## Usage

```python
from puzzle import TentsAndTreesPuzzle
from solver import TentsAndTreesSolver

# Define a puzzle
puzzle = TentsAndTreesPuzzle(
    row_sums=[1, 1, 0, 2, 1],           # Tents per row
    col_sums=[2, 0, 1, 1, 1],           # Tents per column  
    tree_positions={(1,1), (1,3), (3,0), (3,1), (4,4)}  # Tree locations
)

# Display the puzzle
print("Puzzle:")
print(puzzle.display_board())

# Solve the puzzle
solver = TentsAndTreesSolver(puzzle)
solution = solver.solve()

if solution:
    print(f"\nSolution found! Tent positions: {solution}")
    
    # Validate the solution
    is_valid, errors = puzzle.validate_solution(solution)
    print(f"Solution is valid: {is_valid}")
    
    # Display the solved board
    print("\nSolved puzzle:")
    print(puzzle.display_board(tent_positions=solution))
    
    # Get solver information
    info = solver.get_solver_info()
    print(f"\nModel consists of {info['variables']} variables and {info['constraints']} constraints")
else:
    print("No solution exists")
```

### Output

```
Puzzle:
  2 0 1 1 1
1 _ _ _ _ _
1 _ T _ T _
0 _ _ _ _ _
2 T T _ _ _
1 _ _ _ _ T

Solution found! Tent positions: {(4, 0), (3, 4), (0, 3), (1, 0), (3, 2)}
Solution is valid: True

Solved puzzle:
  2 0 1 1 1
1 _ _ _ @ _
1 @ T _ T _
0 _ _ _ _ _
2 T T @ _ @
1 @ _ _ _ T

Model consists of 13 variables and 36 constraints

Legend: T=Tree, @=Tent, _=Empty
```

## Testing

The project uses pytest for testing:

```bash
pytest                           # Run all tests
pytest --cov=puzzle --cov=solver # Run with coverage
```

## Algorithm Details

The solver uses **Mixed Integer Programming (MIP)** to model the puzzle with:

- **Binary decision variables** for each potential tent position
- **Seven constraint types** ensuring all puzzle rules are satisfied:
  1. Tent-tree balance (equal counts)
  2. Tree adjacency (each tree has ≥1 adjacent tent)  
  3. Tent separation (no adjacent tents)
  4. Row sum constraints
  5. Column sum constraints
  6. Tree group balance constraints
  7. Unshared tile constraints

**Solver Backend**: Uses Google OR-Tools with SCIP optimizer by default.

**Mathematical Model**: See the complete formulation in **[Mathematical Model Documentation](model.md)**.

## License

This project is open source and available under the [MIT License](LICENSE).
