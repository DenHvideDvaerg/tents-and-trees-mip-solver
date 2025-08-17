import pytest
from tents_and_trees_mip_solver import TentsAndTreesPuzzle


class TestTentsAndTreesPuzzleInitialization:
    """Test puzzle initialization and input validation."""
    
    def test_valid_initialization(self):
        """Test successful initialization with valid inputs."""
        row_sums = [1, 1, 0, 2, 1]
        col_sums = [2, 0, 1, 1, 1]
        tree_positions = {(1, 1), (1, 3), (3, 0), (3, 1), (4, 4)}
        
        puzzle = TentsAndTreesPuzzle(row_sums, col_sums, tree_positions)
        
        assert puzzle.row_sums == row_sums
        assert puzzle.col_sums == col_sums
        assert puzzle.tree_positions == tree_positions
        assert puzzle.num_rows == 5
        assert puzzle.num_cols == 5

    def test_empty_row_sums_raises_error(self):
        """Test that empty row_sums raises ValueError."""
        with pytest.raises(ValueError, match="Row and column sums cannot be empty"):
            TentsAndTreesPuzzle([], [1, 2], {(0, 0)})
    
    def test_empty_col_sums_raises_error(self):
        """Test that empty col_sums raises ValueError."""
        with pytest.raises(ValueError, match="Row and column sums cannot be empty"):
            TentsAndTreesPuzzle([1, 2], [], {(0, 0)})
    
    def test_negative_row_sum_raises_error(self):
        """Test that negative row sums raise ValueError."""
        with pytest.raises(ValueError, match="Row and column sums must be non-negative"):
            TentsAndTreesPuzzle([-1, 2], [1, 2], {(0, 0)})
    
    def test_negative_col_sum_raises_error(self):
        """Test that negative column sums raise ValueError."""
        with pytest.raises(ValueError, match="Row and column sums must be non-negative"):
            TentsAndTreesPuzzle([1, 2], [1, -2], {(0, 0)})
    
    def test_unequal_row_col_sums_raises_error(self):
        """Test that unequal total row and column sums raise ValueError."""
        with pytest.raises(ValueError, match="Total row sums must equal total column sums"):
            TentsAndTreesPuzzle([1, 2], [1, 1], {(0, 0)})

    def test_tree_outside_boundaries_raises_error(self):
        """Test that tree positions outside puzzle boundaries raise ValueError."""
        with pytest.raises(ValueError, match="Tree position \\(3, 0\\) is outside puzzle boundaries"):
            TentsAndTreesPuzzle([2, 1], [1, 2], {(3, 0)})
    
    def test_empty_tree_positions(self):
        """Test initialization with no trees."""
        puzzle = TentsAndTreesPuzzle([0, 0], [0, 0], set())
        assert len(puzzle.tree_positions) == 0
        assert len(puzzle.tent_candidate_tiles) == 0


class TestTentsAndTreesPuzzleProperties:
    """Test computed properties and cached values."""
    
    
    def test_tent_candidate_tiles(self):
        """Test tent candidate tiles are calculated correctly."""
        puzzle = TentsAndTreesPuzzle(
            row_sums=[1, 2, 1, 0, 1], 
            col_sums=[2, 0, 1, 1, 1], 
            tree_positions={(0, 1), (1,0), (1,3), (2, 2), (4,4)}
        )
        
        candidates = puzzle.tent_candidate_tiles
        
        # Should include adjacent tiles to trees
        expected_candidates = {
            (0, 0), (0, 2), (0, 3),
            (1, 1), (1, 2), (1, 4),
            (2, 0), (2, 1), (2, 3),
            (3, 2), (3, 4),
            (4, 3)
        }
        
        assert candidates == expected_candidates
    
    def test_tree_groups_single_trees(self):
        """Test tree groups with isolated trees."""
        puzzle = TentsAndTreesPuzzle(
            row_sums=[1, 0, 1], 
            col_sums=[1, 0, 1], 
            tree_positions={(0, 0), (2, 2)}
        )
        
        groups = puzzle.tree_groups
        assert len(groups) == 2
        assert {(0, 0)} in groups
        assert {(2, 2)} in groups
    
    def test_tree_groups_connected_trees(self):
        """Test tree groups with connected trees."""
        puzzle = TentsAndTreesPuzzle(
            row_sums=[1, 2, 1, 0, 1], 
            col_sums=[2, 0, 1, 1, 1], 
            tree_positions={(0, 1), (1,0), (1,3), (2, 2), (4,4)}
        )
        
        groups = puzzle.tree_groups
        assert len(groups) == 3

        expected_groups = [
            {(0, 1), (1, 0)},      # Connected group 1
            {(1, 3), (2, 2)},      # Connected group 2  
            {(4, 4)}               # Isolated tree
        ]

        for expected_group in expected_groups:
            assert expected_group in groups


class TestTentsAndTreesPuzzleSpatialMethods:
    """Test spatial relationship methods."""
    
    @pytest.fixture
    def puzzle_3x3(self):
        """Create a 3x3 puzzle for spatial testing."""
        return TentsAndTreesPuzzle(
            row_sums=[1, 0, 0], 
            col_sums=[0, 1, 0], 
            tree_positions={(1, 1)}  # Center tree
        )
    
    def test_is_within_bounds(self, puzzle_3x3):
        """Test position validation."""
        # Test valid positions
        assert puzzle_3x3.is_within_bounds(0, 0)
        assert puzzle_3x3.is_within_bounds(2, 2)
        assert puzzle_3x3.is_within_bounds(1, 1)

        # Test invalid positions
        assert not puzzle_3x3.is_within_bounds(-1, 0)
        assert not puzzle_3x3.is_within_bounds(0, -1)
        assert not puzzle_3x3.is_within_bounds(3, 0)
        assert not puzzle_3x3.is_within_bounds(0, 3)
    
    def test_get_adjacent_tiles(self, puzzle_3x3):
        """Test getting adjacent tiles."""
        # Center
        adjacent = puzzle_3x3.get_adjacent_tiles((1, 1))
        assert adjacent == {(0, 1), (2, 1), (1, 0), (1, 2)}
        
        # Corner
        adjacent_corner = puzzle_3x3.get_adjacent_tiles((0, 0))
        assert adjacent_corner == {(0, 1), (1, 0)}
        
        # Edge
        adjacent_edge = puzzle_3x3.get_adjacent_tiles((1, 0))
        assert adjacent_edge == {(0, 0), (2, 0), (1, 1)}
    
    def test_get_diagonal_tiles(self, puzzle_3x3):
        """Test getting diagonal tiles."""
        # Center
        diagonal = puzzle_3x3.get_diagonal_tiles((1, 1))
        assert diagonal == {(0, 0), (0, 2), (2, 0), (2, 2)}
        
        # Corner
        diagonal_corner = puzzle_3x3.get_diagonal_tiles((0, 0))
        assert diagonal_corner == {(1, 1)}
    
    def test_get_surrounding_tiles(self, puzzle_3x3):
        """Test getting all surrounding tiles (adjacent + diagonal)."""
        surrounding = puzzle_3x3.get_surrounding_tiles((1, 1))
        expected = {(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}
        assert surrounding == expected
    
    def test_get_row_tiles_and_col_tiles(self, puzzle_3x3):
        """Test getting tent candidates by row and column."""
        # Row 1 should have tent candidates adjacent to center tree
        row_1_tiles = puzzle_3x3.get_row_tiles(1)
        assert (1, 0) in row_1_tiles
        assert (1, 2) in row_1_tiles
        assert (1, 1) not in row_1_tiles  # Tree position excluded
        
        # Column 1 should have tent candidates adjacent to center tree
        col_1_tiles = puzzle_3x3.get_col_tiles(1)
        assert (0, 1) in col_1_tiles
        assert (2, 1) in col_1_tiles
        assert (1, 1) not in col_1_tiles  # Tree position excluded


class TestTentsAndTreesPuzzleSolutionValidation:
    """Test solution validation functionality."""
    
    @pytest.fixture
    def validation_puzzle(self):
        """Create a puzzle for validation testing."""
        return TentsAndTreesPuzzle(
            row_sums=[1, 0, 1], 
            col_sums=[1, 1, 0], 
            tree_positions={(0, 0), (2, 1)}
        )
    
    def test_valid_solution(self, validation_puzzle):
        """Test validation of a correct solution."""
        # Valid solution: tents at (0,1) and (2,0)
        tent_positions = {(0, 1), (2, 0)}
        is_valid, errors = validation_puzzle.validate_solution(tent_positions)
        
        assert is_valid
        assert len(errors) == 0
    
    def test_invalid_tent_position(self, validation_puzzle):
        """Test validation catches invalid tent positions."""
        # Invalid: tent not adjacent to any tree
        tent_positions = {(0, 1), (0, 2)}  # (0,2) is not a valid candidate
        is_valid, errors = validation_puzzle.validate_solution(tent_positions)
        
        assert not is_valid
        assert errors
    
    def test_wrong_row_sum(self, validation_puzzle):
        """Test validation catches incorrect row sums."""
        # Wrong row sum: missing tent in row 2
        tent_positions = {(0, 1)}  # Only one tent, but row 2 needs 1
        is_valid, errors = validation_puzzle.validate_solution(tent_positions)
        
        assert not is_valid
        assert errors
    
    def test_wrong_col_sum(self, validation_puzzle):
        """Test validation catches incorrect column sums."""
        # Wrong col sum: both tents in column 0
        tent_positions = {(1, 0)}  # Only one tent, but col 1 needs 1
        is_valid, errors = validation_puzzle.validate_solution(tent_positions)
        
        assert not is_valid
        assert errors
    
    def test_touching_tents(self):
        """Test validation catches touching tents."""
        puzzle = TentsAndTreesPuzzle(
            row_sums=[2, 0], 
            col_sums=[1, 1], 
            tree_positions={(0, 0), (0, 1)}
        )
        
        # Touching tents
        tent_positions = {(1, 0), (1, 1)}  # Adjacent positions
        is_valid, errors = puzzle.validate_solution(tent_positions)
        
        assert not is_valid
        assert errors
    
    def test_tree_without_adjacent_tent(self):
        """Test validation catches trees without adjacent tents."""
        puzzle = TentsAndTreesPuzzle(
            row_sums=[1, 0, 0], 
            col_sums=[1, 0, 0], 
            tree_positions={(0, 0), (2, 2)}  # Trees far apart
        )
        
        # Only one tent at (0,1) - tree at (2,2) won't have adjacent tent
        tent_positions = {(0, 1)}
        is_valid, errors = puzzle.validate_solution(tent_positions)
        
        assert not is_valid
        assert errors

if __name__ == "__main__":
    pytest.main([__file__])
