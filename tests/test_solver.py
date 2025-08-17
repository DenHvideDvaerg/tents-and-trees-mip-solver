"""
Simplified test suite for the TentsAndTreesSolver class.

This module tests the mathematical programming solver that uses OR-Tools
to find solutions to Tents and Trees puzzles.
"""

import pytest
from tents_and_trees_mip_solver import TentsAndTreesPuzzle, TentsAndTreesSolver


class TestTentsAndTreesSolverInitialization:
    """Test solver initialization and input validation."""
    
    def test_solver_creation_with_valid_puzzle(self):
        """Test creating a solver with a valid puzzle."""
        puzzle = TentsAndTreesPuzzle([1, 0], [0, 1], {(0, 0)})
        solver = TentsAndTreesSolver(puzzle)
        
        assert solver.puzzle == puzzle
        assert len(solver.tent_vars) == 2  # Two potential tent positions
        assert solver.solver.NumConstraints() > 0

    def test_solver_with_invalid_puzzle_type(self):
        """Test solver rejects non-TentsAndTreesPuzzle input."""
        with pytest.raises(ValueError, match="Puzzle must be a TentsAndTreesPuzzle instance"):
            TentsAndTreesSolver("not a puzzle")
    
    def test_solver_with_empty_puzzle(self):
        """Test solving a puzzle with no trees (all zeros)."""
        puzzle = TentsAndTreesPuzzle(
            row_sums=[0, 0], 
            col_sums=[0, 0], 
            tree_positions=set()
        )
        
        # This should raise an error since no tent candidates exist
        with pytest.raises(ValueError, match="No valid tent positions found"):
            TentsAndTreesSolver(puzzle)

    def test_solver_with_all_trees_no_tent_candidates(self):
        """Test solver with puzzle where all cells are trees (no tent candidates)."""
        puzzle = TentsAndTreesPuzzle(
            row_sums=[0, 0], 
            col_sums=[0, 0], 
            tree_positions={(0, 0), (0, 1), (1, 0), (1, 1)}  # All cells are trees
        )
        
        # This should raise an error since no tent candidates exist
        with pytest.raises(ValueError, match="No valid tent positions found"):
            TentsAndTreesSolver(puzzle)

    def test_solver_creation_with_invalid_solver_type(self):
        """Test that invalid solver type raises appropriate error."""
        puzzle = TentsAndTreesPuzzle([1], [1], {(0, 0)})
        with pytest.raises(ValueError, match="Could not create solver of type"):
            TentsAndTreesSolver(puzzle, solver_type="NONEXISTENT")

class TestTentsAndTreesSolverSolving:
    """Test core solving functionality with key scenarios."""
    
    def test_solve_impossible_puzzle(self):
        """Test solver behavior with an impossible puzzle."""
        # Create a puzzle where sums don't match
        puzzle = TentsAndTreesPuzzle(
            row_sums=[2, 0], 
            col_sums=[2, 0], 
            tree_positions={(0, 0)}
        )
        solver = TentsAndTreesSolver(puzzle)
        
        solution = solver.solve()
        assert solution is None  # Should return None for unsolvable puzzles
        
    def test_solve_valid_puzzle(self):
        """Test solver with a valid puzzle configuration."""
        puzzle = TentsAndTreesPuzzle(
            row_sums=[1, 1, 0, 2, 1], 
            col_sums=[2, 0, 1, 1, 1], 
            tree_positions={(1, 1), (1, 3), (3, 0), (3, 1), (4, 4)}
        )
        solver = TentsAndTreesSolver(puzzle)
        
        solution = solver.solve()
        expected_solution = {(0, 3), (1, 0), (3, 2), (3, 4), (4, 0)}

        assert solution is not None, "Valid puzzle should be solvable"
        assert solution == expected_solution, f"Expected {expected_solution}, got {solution}"
        
        # Verify solution is valid
        is_valid, errors = puzzle.validate_solution(solution)
        assert is_valid, f"Solution is invalid: {errors}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
