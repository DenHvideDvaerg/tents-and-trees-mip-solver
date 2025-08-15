# Tents and Trees MIP Solver

A Tents and Trees puzzle solver using mathematical programming.

<!-- TODO: 
- Verify example and output (output is definitely wrong...)
- Add badges
- Test python versions (using github actions?)
- Add link to streamlit app (probably after publishing)
- A description of the model (whole Algorithm Details section needs to be reworked, Maybe have a new md file and link to it?)
- Probably delete Features section?
 -->

## Overview

Tents and Trees is a logic puzzle where you must place tents on a grid according to specific rules:

- **Each tree must have exactly one adjacent tent** (horizontally or vertically)
- **Each tent must be adjacent to exactly one tree**  
- **Tents cannot touch each other** (even diagonally)
- **Row and column constraints** specify how many tents must be in each row/column

This solver models the puzzle as a **Mixed Integer Programming (MIP)** problem to find solutions.

<!-- ## Features

- 🧩 **Complete puzzle modeling** with all Tents and Trees rules
- ⚡ **Fast solving** using Google OR-Tools optimization
- ✅ **Solution validation** to verify correctness
- 🎯 **Handles complex scenarios** including multiple tree groups -->

## Installation

```bash
pip install tents-and-trees-mip-solver
```

## Requirements

- Python 3.13+
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
    print(f"\nSolver consists of {info['variables']} variables and {info['constraints']} constraints")
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

The solver models the puzzle as a **Mixed Integer Programming** problem with:

### Variables
- **Binary variables** for each potential tent position

### Constraints
1. **Row sum constraints:** Each row has the required number of tents
2. **Column sum constraints:** Each column has the required number of tents  
3. **Tree adjacency:** Each tree has exactly one adjacent tent
4. **Tent isolation:** No tent can be adjacent to another tent
5. **Valid positions:** Tents only in positions adjacent to trees

The solver uses **Google OR-Tools** with the SCIP optimizer for efficient constraint solving.

## License

This project is open source and available under the [MIT License](LICENSE).
