from tents_and_trees_mip_solver import TentsAndTreesPuzzle, TentsAndTreesSolver

# 5A1
row_sums = [1, 1, 0, 2, 1]      # Terns per row
col_sums = [2, 0, 1, 1, 1]      # Terns per column
tree_positions = {(1, 1), (1, 3), (3, 0), (3, 1), (4, 4)} # Tree positions

puzzle = TentsAndTreesPuzzle(row_sums, col_sums, tree_positions)

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

exit()