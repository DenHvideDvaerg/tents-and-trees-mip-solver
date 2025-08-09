from puzzle import TentsAndTreesPuzzle
from solver import TentsAndTreesSolver

## TODO: 
# - Add basic unit tests
# - Publish to PyPI
# - Get ImageParser cleaned up in other repo
# - Make streamlit app 


# Example puzzle data
# 5A1
# row_sums = [1, 1, 0, 2, 1]
# col_sums = [2, 0, 1, 1, 1]
# tree_positions = {(1, 1), (1, 3), (3, 0), (3, 1), (4, 4)}

# 7x7_daily
row_sums = [2,1,2,1,2,2,0]
col_sums = [2,1,2,1,1,1,2]
tree_positions = {(0,0), (1,2),(1,6),(2,4),(3,0),(4,2),(4,5),(4,6),(5,0),(6,2)}

puzzle = TentsAndTreesPuzzle(row_sums, col_sums, tree_positions)
solver = TentsAndTreesSolver(puzzle)


print("Solver info:", solver.get_solver_info())
print("Model:")
print(solver.export_model())
print("\nPuzzle:")
puzzle.print_board()

solution = solver.solve(verbose=True)

if solution:
    print("\nSolution:")
    puzzle.print_board(tent_positions=solution)
    
    # Validate the solution
    is_valid, errors = puzzle.validate_solution(solution)
    if is_valid:
        print("Solution is valid!")
    else:
        print("Solution has errors:")
        for error in errors:
            print(f"  - {error}")
else:
    print("No solution found")