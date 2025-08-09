"""
Tents and Trees Puzzle representation and utilities.

This module provides the TentsAndTreesPuzzle class which represents a Tents and Trees puzzle
and includes methods for puzzle analysis and constraint generation.
"""

from typing import List, Set, Tuple, Optional


class TentsAndTreesPuzzle:
    """
    Represents a Tents and Trees puzzle.
    
    The puzzle contains:
    - Row and column tent count requirements
    - Tree positions
    - Methods for analyzing spatial relationships between tiles
    """
    
    def __init__(self, row_sums: List[int], col_sums: List[int], tree_positions: Set[Tuple[int, int]]):
        """
        Initialize the puzzle.
        
        Args:
            row_sums: List of required tent counts for each row
            col_sums: List of required tent counts for each column  
            tree_positions: Set of (row, col) tuples indicating tree locations
            
        Raises:
            ValueError: If dimensions don't match or invalid positions provided
        """
        # Validate inputs
        if not row_sums or not col_sums:
            raise ValueError("Row and column sums cannot be empty")
        
        if any(s < 0 for s in row_sums + col_sums):
            raise ValueError("Row and column sums must be non-negative")
        
        self.num_rows = len(row_sums)
        self.num_cols = len(col_sums)
        
        # Validate tree positions
        for row, col in tree_positions:
            if not self.is_valid_position(row, col):
                raise ValueError(f"Tree position ({row}, {col}) is outside puzzle boundaries")
        
        self.row_sums = row_sums
        self.col_sums = col_sums
        self.tree_positions = set(tree_positions)
        
        # Offset patterns for different types of tile relationships
        self._adjacent_offsets = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        self._diagonal_offsets = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        self._cross_offsets = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Adjacent
            (-2, 0), (2, 0), (0, -2), (0, 2),  # Two steps away
            (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
        ]
        
        # Computed properties
        self._tent_candidate_tiles = None
        self._tree_groups = None
    
    @property
    def tent_candidate_tiles(self) -> Set[Tuple[int, int]]:
        """
        Get all tiles where tents could potentially be placed.
        
        Returns:
            Set of (row, col) tuples representing valid tent positions
        """
        if self._tent_candidate_tiles is None:
            candidates = set()
            for tree in self.tree_positions:
                candidates.update(self.get_adjacent_tiles(tree))
            # Remove tree positions and invalid tiles
            self._tent_candidate_tiles = candidates - self.tree_positions - {None}
        return self._tent_candidate_tiles
    
    @property
    def tree_groups(self) -> List[Set[Tuple[int, int]]]:
        """
        Get groups of trees that are connected within cross-tile distance.
        
        Returns:
            List of sets, where each set contains trees that form a connected group
        """
        if self._tree_groups is None:
            # Compute connected groups of trees using depth-first search
            # Trees are considered connected if they are within cross-tile distance of each other
            visited = set()
            groups = []
            
            def dfs(tree: Tuple[int, int], current_group: Set[Tuple[int, int]]):
                visited.add(tree)
                current_group.add(tree)
                
                # Check all trees within cross-tile distance
                cross_tiles = self.get_cross_tiles(tree)
                nearby_trees = cross_tiles & self.tree_positions
                
                for nearby_tree in nearby_trees:
                    if nearby_tree not in visited:
                        dfs(nearby_tree, current_group)
            
            for tree in self.tree_positions:
                if tree not in visited:
                    group = set()
                    dfs(tree, group)
                    groups.append(group)
            
            self._tree_groups = groups
        return self._tree_groups
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if the given position is within puzzle boundaries."""
        return 0 <= row < self.num_rows and 0 <= col < self.num_cols
    
    def get_tile_by_offset(self, position: Tuple[int, int], offset: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """
        Get the tile at the specified offset from the given position.
        
        Args:
            position: Starting (row, col) position
            offset: (row_delta, col_delta) offset
            
        Returns:
            (row, col) tuple if valid position, None otherwise
        """
        row, col = position
        new_row, new_col = row + offset[0], col + offset[1]
        return (new_row, new_col) if self.is_valid_position(new_row, new_col) else None
    
    def get_tiles_by_offsets(self, position: Tuple[int, int], offsets: List[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """
        Get all valid tiles at the specified offsets from the given position.
        
        Args:
            position: Starting (row, col) position
            offsets: List of (row_delta, col_delta) offsets
            
        Returns:
            Set of valid (row, col) tuples (excludes None values)
        """
        tiles = {self.get_tile_by_offset(position, offset) for offset in offsets}
        return tiles - {None}
    
    def get_adjacent_tiles(self, position: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """Get tiles directly adjacent (up, down, left, right) to the given position."""
        return self.get_tiles_by_offsets(position, self._adjacent_offsets)
    
    def get_diagonal_tiles(self, position: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """Get tiles diagonally adjacent to the given position."""
        return self.get_tiles_by_offsets(position, self._diagonal_offsets)
    
    def get_surrounding_tiles(self, position: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """Get all tiles surrounding (adjacent + diagonal) the given position."""
        return self.get_adjacent_tiles(position) | self.get_diagonal_tiles(position)
    
    def get_cross_tiles(self, position: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """
        Get tiles in a cross pattern around the given position.
        
        This includes adjacent, diagonal, and tiles two steps away in adjacent directions.
        """
        return self.get_tiles_by_offsets(position, self._cross_offsets)
    
    def get_row_tiles(self, row: int) -> Set[Tuple[int, int]]:
        """Get all valid tent candidate tiles in the specified row."""
        return {(row, col) for col in range(self.num_cols) if (row, col) in self.tent_candidate_tiles}
    
    def get_col_tiles(self, col: int) -> Set[Tuple[int, int]]:
        """Get all valid tent candidate tiles in the specified column."""
        return {(row, col) for row in range(self.num_rows) if (row, col) in self.tent_candidate_tiles}
    
    def get_unshared_adjacent_tiles(self, tree: Tuple[int, int], tree_group: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
        """
        Get adjacent tiles of a tree that are not shared with other trees in the same group.
        
        Args:
            tree: The tree position
            tree_group: Set of trees in the same connected group
            
        Returns:
            Set of adjacent tiles that are exclusive to this tree
        """
        tree_adjacent = self.get_adjacent_tiles(tree)
        
        # Find tiles that are adjacent to other trees in the group
        shared_tiles = set()
        for other_tree in tree_group:
            if other_tree != tree:
                shared_tiles.update(tree_adjacent & self.get_adjacent_tiles(other_tree))
        
        # Return tiles adjacent to this tree but not shared with others, excluding tree positions
        return tree_adjacent - shared_tiles - tree_group
    
    def display_board(self, tent_positions: Optional[Set[Tuple[int, int]]] = None, 
                     show_indices: bool = False) -> str:
        """
        Create a string representation of the puzzle.
        
        Args:
            tent_positions: Optional set of tent positions to display
            show_indices: Whether to show row/column indices
            
        Returns:
            String representation of the puzzle
        """
        tent_positions = tent_positions or set()
        lines = []
        
        # Header with column indices and sums
        if show_indices:
            header = "    " + " ".join(str(i) for i in range(self.num_cols))
            lines.append(header)
            col_sums_line = "    " + " ".join(str(s) for s in self.col_sums)
        else:
            col_sums_line = "  " + " ".join(str(s) for s in self.col_sums)
        
        lines.append(col_sums_line)
        
        # Board rows
        for row in range(self.num_rows):
            row_parts = []
            
            if show_indices:
                row_parts.append(str(row))
            
            row_parts.append(str(self.row_sums[row]))
            
            for col in range(self.num_cols):
                pos = (row, col)
                if pos in self.tree_positions:
                    row_parts.append('T')
                elif pos in tent_positions:
                    row_parts.append('@')
                else:
                    row_parts.append('_')
            
            lines.append(' '.join(row_parts))
        
        return '\n'.join(lines)
    
    def print_board(self, tent_positions: Optional[Set[Tuple[int, int]]] = None, 
                   show_indices: bool = False):
        """Print the puzzle to console."""
        print(self.display_board(tent_positions, show_indices))
    
    def validate_solution(self, tent_positions: Set[Tuple[int, int]]) -> Tuple[bool, List[str]]:
        """
        Validate a proposed solution.
        
        Args:
            tent_positions: Set of proposed tent positions
            
        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []
        
        # Check if all tent positions are valid candidates
        invalid_positions = tent_positions - self.tent_candidate_tiles
        if invalid_positions:
            errors.append(f"Invalid tent positions: {invalid_positions}")
        
        # Check row sums - count all tents in each row
        for row in range(self.num_rows):
            row_tent_count = sum(1 for r, _ in tent_positions if r == row)
            if row_tent_count != self.row_sums[row]:
                errors.append(f"Row {row}: expected {self.row_sums[row]} tents, got {row_tent_count}")
        
        # Check column sums - count all tents in each column
        for col in range(self.num_cols):
            col_tent_count = sum(1 for _, c in tent_positions if c == col)
            if col_tent_count != self.col_sums[col]:
                errors.append(f"Column {col}: expected {self.col_sums[col]} tents, got {col_tent_count}")
        
        # Check that tents don't touch each other
        for tent in tent_positions:
            surrounding = self.get_surrounding_tiles(tent)
            touching_tents = surrounding & tent_positions
            if touching_tents:
                errors.append(f"Tent at {tent} touches other tents: {touching_tents}")
        
        # Check that each tree has at least one adjacent tent
        for tree in self.tree_positions:
            adjacent_tents = self.get_adjacent_tiles(tree) & tent_positions
            if not adjacent_tents:
                errors.append(f"Tree at {tree} has no adjacent tents")
        
        return len(errors) == 0, errors