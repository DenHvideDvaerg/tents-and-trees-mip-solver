"""
Tents and Trees Puzzle Solver using Mathematical Programming.

This module provides the TentsAndTreesSolver class which uses OR-Tools
to solve Tents and Trees puzzles through mathematical programming.
"""

from typing import Dict, Set, Tuple, Optional
from ortools.linear_solver import pywraplp
from puzzle import TentsAndTreesPuzzle


class TentsAndTreesSolver:
    """
    Mathematical programming solver for Tents and Trees puzzles.
    
    Uses Google OR-Tools to model the puzzle as an integer linear programming
    problem with constraints for tent placement rules.
    """
    
    def __init__(self, puzzle: TentsAndTreesPuzzle, solver_type: str = 'SCIP'):
        """
        Initialize the solver with a puzzle.
        
        Args:
            puzzle: The TentsAndTreesPuzzle instance to solve
            solver_type: The OR-Tools solver to use (default: 'SCIP')
            
        Raises:
            ValueError: If puzzle is invalid or solver creation fails
        """
        if not isinstance(puzzle, TentsAndTreesPuzzle):
            raise ValueError("puzzle must be a TentsAndTreesPuzzle instance")
        
        self.puzzle = puzzle
        self.solver = pywraplp.Solver.CreateSolver(solver_type)
        if not self.solver:
            raise ValueError(f"Could not create solver of type '{solver_type}'")
        
        # Variables: one binary variable per potential tent position
        self.tent_vars: Dict[Tuple[int, int], pywraplp.Variable] = {}
        self._setup_variables()
        
        # Validate that we have tent candidates
        if not self.tent_vars:
            raise ValueError("No valid tent positions found - puzzle may be unsolvable")

        # Add constraints
        self._add_all_constraints()

    
    def _setup_variables(self):
        """Create binary variables for each potential tent position."""
        for tile in self.puzzle.tent_candidate_tiles:
            var_name = f'tent_{tile[0]}_{tile[1]}'
            self.tent_vars[tile] = self.solver.IntVar(0, 1, var_name)
    
    def _add_tent_tree_balance_constraint(self):
        """Ensure the total number of tents equals the number of trees."""
        total_tents = sum(self.tent_vars.values())
        total_trees = len(self.puzzle.tree_positions)
        self.solver.Add(total_tents == total_trees, 'tent_tree_balance')
    
    def _add_tree_adjacency_constraints(self):
        """Ensure each tree has at least one adjacent tent."""
        for i, tree in enumerate(self.puzzle.tree_positions):
            adjacent_tiles = self.puzzle.get_adjacent_tiles(tree)
            adjacent_vars = [self.tent_vars[tile] for tile in adjacent_tiles 
                           if tile in self.tent_vars]
            
            constraint_name = f'tree_adjacency_{i}'
            self.solver.Add(sum(adjacent_vars) >= 1, constraint_name)
    
    def _add_tent_separation_constraints(self):
        """Ensure tents cannot be placed in adjacent or diagonal positions."""
        for tile, tent_var in self.tent_vars.items():
            surrounding_tiles = self.puzzle.get_surrounding_tiles(tile)
            surrounding_vars = [self.tent_vars[pos] for pos in surrounding_tiles 
                              if pos in self.tent_vars]
            
            if surrounding_vars:
                # If this tile has a tent (tent_var = 1), then no surrounding tiles can have tents
                M = len(surrounding_vars)
                constraint_name = f'tent_separation_{tile[0]}_{tile[1]}'
                self.solver.Add(sum(surrounding_vars) <= M * (1 - tent_var), constraint_name)
    
    def _add_row_sum_constraints(self):
        """Ensure each row has the correct number of tents."""
        for row in range(self.puzzle.num_rows):
            row_tiles = self.puzzle.get_row_tiles(row)
            row_vars = [self.tent_vars[tile] for tile in row_tiles if tile in self.tent_vars]
            
            constraint_name = f'row_sum_{row}'
            self.solver.Add(sum(row_vars) == self.puzzle.row_sums[row], constraint_name)
    
    def _add_col_sum_constraints(self):
        """Ensure each column has the correct number of tents."""
        for col in range(self.puzzle.num_cols):
            col_tiles = self.puzzle.get_col_tiles(col)
            col_vars = [self.tent_vars[tile] for tile in col_tiles if tile in self.tent_vars]
            
            constraint_name = f'col_sum_{col}'
            self.solver.Add(sum(col_vars) == self.puzzle.col_sums[col], constraint_name)
    
    def _add_tree_group_constraints(self):
        """
        For each group of connected trees, ensure the number of tents 
        in their combined adjacent area equals the number of trees in the group.
        """
        for i, tree_group in enumerate(self.puzzle.tree_groups):
            # Get all tiles adjacent to any tree in this group
            group_adjacent_tiles = set()
            for tree in tree_group:
                group_adjacent_tiles.update(self.puzzle.get_adjacent_tiles(tree))
            
            # Get variables for these tiles (excluding tree positions)
            group_vars = [self.tent_vars[tile] for tile in group_adjacent_tiles 
                         if tile in self.tent_vars]
            
            if group_vars:
                constraint_name = f'tree_group_{i}'
                self.solver.Add(sum(group_vars) == len(tree_group), constraint_name)
    
    def _add_unshared_tree_constraints(self):
        """
        For trees with unshared adjacent tiles (tiles not adjacent to other trees 
        in the same group), limit to at most one tent in those unshared positions.
        """
        for group_idx, tree_group in enumerate(self.puzzle.tree_groups):
            for tree_idx, tree in enumerate(tree_group):
                unshared_tiles = self.puzzle.get_unshared_adjacent_tiles(tree, tree_group)
                unshared_vars = [self.tent_vars[tile] for tile in unshared_tiles 
                               if tile in self.tent_vars]
                
                if len(unshared_vars) > 1:
                    constraint_name = f'unshared_tree_{group_idx}_{tree_idx}'
                    self.solver.Add(sum(unshared_vars) <= 1, constraint_name)
    
    def _add_all_constraints(self):
        """Add all constraint types to the solver."""
        self._add_tent_tree_balance_constraint()
        self._add_tree_adjacency_constraints()
        self._add_tent_separation_constraints()
        self._add_row_sum_constraints()
        self._add_col_sum_constraints()
        self._add_tree_group_constraints()
        self._add_unshared_tree_constraints()
    
    def solve(self, verbose: bool = False) -> Optional[Set[Tuple[int, int]]]:
        """
        Solve the puzzle and return tent positions.
        
        Args:
            verbose: If True, print solver information
            
        Returns:
            Set of (row, col) tuples representing tent positions, or None if no solution
        """
        if verbose:
            print(f"Number of variables: {self.solver.NumVariables()}")
            print(f"Number of constraints: {self.solver.NumConstraints()}")
        
        # Solve
        status = self.solver.Solve()
        
        if status == pywraplp.Solver.OPTIMAL:
            # Extract solution
            tent_positions = {
                tile for tile, var in self.tent_vars.items() 
                if var.solution_value() == 1
            }
            
            if verbose:
                print(f"Solution found with {len(tent_positions)} tents")
            
            return tent_positions
        
        elif status == pywraplp.Solver.FEASIBLE:
            # This should not happen since the problem doesn't have an objective function
            raise RuntimeError("What the... Solver returned FEASIBLE status for a constraint satisfaction problem??")
        
        else:
            if verbose:
                print(f"No solution found. Status: {status}")
            return None
    
    def export_model(self) -> str:
        """
        Export the constraint model in LP format for debugging.
        
        Returns:
            String representation of the linear programming model
        """
        return self.solver.ExportModelAsLpFormat(False)
    
    def get_solver_info(self) -> Dict[str, int]:
        """
        Get information about the solver state.
        
        Returns:
            Dictionary with solver statistics
        """
        return {
            'variables': self.solver.NumVariables(),
            'constraints': self.solver.NumConstraints(),
            'tent_candidates': len(self.tent_vars),
            'trees': len(self.puzzle.tree_positions),
            'tree_groups': len(self.puzzle.tree_groups)
        }