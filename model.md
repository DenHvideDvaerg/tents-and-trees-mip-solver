# Mathematical Model Documentation

This document provides a formal mathematical programming formulation of the Tents and Trees puzzle as a Mixed Integer Programming (MIP) problem.

## Problem Definition

Given:
- An **m × n** grid representing the puzzle board
- **Row tent requirements** R = {r₁, r₂, ..., rₘ} where rᵢ is the required number of tents in row i
- **Column tent requirements** C = {c₁, c₂, ..., cₙ} where cⱼ is the required number of tents in column j
- **Tree positions** T ⊆ {(i,j) : 1 ≤ i ≤ m, 1 ≤ j ≤ n} representing the locations of all trees on the board

**Objective:** Find tent positions that satisfy all Tents and Trees puzzle rules.

## Sets and Indices

| Symbol | Definition |
|--------|------------|
| **I** | Set of row indices: I = {1, 2, ..., m} |
| **J** | Set of column indices: J = {1, 2, ..., n} |
| **T** | Set of tree positions: T ⊆ I × J |
| **P** | Set of potential tent positions (tent candidates) |
| **G** | Set of tree groups: G = {G₁, G₂, ..., Gₖ} where each Gᵢ ⊆ T |
| **A(i,j)** | Adjacent cells to position (i,j): horizontally and vertically neighboring |
| **S(i,j)** | Surrounding cells to position (i,j): all 8 neighboring positions |
| **C(i,j)** | Cross-pattern cells around (i,j): adjacent + diagonal + two-steps away in adjacent direction |
| **U(t,G)** | Unshared adjacent tiles for tree t in group G |

### Tent Candidate Set
The set of valid tent positions is defined as:

```
P = {(i,j) ∈ I × J : (i,j) ∉ T and A(i,j) ∩ T ≠ ∅}
```

This ensures tents can only be placed adjacent to at least one tree.

### Tree Groups
Trees are grouped based on cross-pattern connectivity:

```
Gₖ = connected component of trees where ∀t₁,t₂ ∈ Gₖ, ∃ path through cross-pattern adjacency
```

### Unshared Adjacent Tiles
For tree t in group G, unshared adjacent tiles are:

```
U(t,G) = A(t) \ (⋃_{t'∈G,t'≠t} A(t) ∩ A(t')) \ G
```

## Decision Variables

| Variable | Domain | Definition |
|----------|--------|------------|
| **x_{i,j}** | {0, 1} | 1 if a tent is placed at position (i,j) ∈ P, 0 otherwise |

## Objective Function

This is a constraint satisfaction problem with a tent-tree balance constraint:

```
minimize 0
```

## Constraints

### 1. Tent-Tree Balance Constraint
The total number of tents must equal the number of trees:

```
Σ_{(i,j) ∈ P} x_{i,j} = |T|
```

### 2. Tree Adjacency Constraints
Each tree must have at least one adjacent tent:

```
Σ_{(k,l) ∈ A(i,j) ∩ P} x_{k,l} ≥ 1    ∀(i,j) ∈ T
```

### 3. Tent Separation Constraints
No tent can be placed adjacent to another tent (including diagonally):

```
Σ_{(k,l) ∈ S(i,j) ∩ P} x_{k,l} ≤ M · (1 - x_{i,j})    ∀(i,j) ∈ P
```

Where M = |S(i,j) ∩ P| is the number of surrounding tent candidates.

### 4. Row Sum Constraints
Each row must contain exactly the required number of tents:

```
Σ_{j: (i,j) ∈ P} x_{i,j} = rᵢ    ∀i ∈ I
```

### 5. Column Sum Constraints  
Each column must contain exactly the required number of tents:

```
Σ_{i: (i,j) ∈ P} x_{i,j} = cⱼ    ∀j ∈ J
```

### 6. Tree Group Constraints
For each group of connected trees, the number of tents in their combined adjacent area equals the group size:

```
Σ_{(k,l) ∈ (⋃_{t∈Gₖ} A(t)) ∩ P} x_{k,l} = |Gₖ|    ∀Gₖ ∈ G
```

### 7. Unshared Tile Constraints
For trees with unshared adjacent tiles, limit to at most one tent in unshared positions:

```
Σ_{(k,l) ∈ U(t,Gₖ)} x_{k,l} ≤ 1    ∀t ∈ Gₖ, ∀Gₖ ∈ G, |U(t,Gₖ)| > 1
```



## Complete MIP Formulation

**Variables:**
```
x_{i,j} ∈ {0,1}    ∀(i,j) ∈ P
```

**Objective:**
```
minimize 0
```

**Subject to:**
```
Σ_{(i,j) ∈ P} x_{i,j} = |T|                                     (Tent-tree balance)

Σ_{(k,l) ∈ A(i,j) ∩ P} x_{k,l} ≥ 1                              ∀(i,j) ∈ T     (Tree adjacency)

Σ_{(k,l) ∈ S(i,j) ∩ P} x_{k,l} ≤ |S(i,j) ∩ P| · (1 - x_{i,j})   ∀(i,j) ∈ P     (Tent separation)

Σ_{j: (i,j) ∈ P} x_{i,j} = rᵢ                                   ∀i ∈ I         (Row sums)

Σ_{i: (i,j) ∈ P} x_{i,j} = cⱼ                                   ∀j ∈ J         (Column sums)

Σ_{(k,l) ∈ (⋃_{t∈Gₖ} A(t)) ∩ P} x_{k,l} = |Gₖ|                  ∀Gₖ ∈ G        (Tree groups)

Σ_{(k,l) ∈ U(t,Gₖ)} x_{k,l} ≤ 1                                 ∀t ∈ Gₖ, ∀Gₖ ∈ G, |U(t,Gₖ)| > 1  (Unshared trees)

x_{i,j} ∈ {0,1}                                                 ∀(i,j) ∈ P     (Binary variables)
```

## Implementation Notes

- **Mathematical indexing**: This formulation uses 1-based indexing for mathematical clarity (rows 1 to m, columns 1 to n)
- **Implementation mapping**: The actual Python implementation uses 0-based indexing (rows 0 to m-1, columns 0 to n-1)
- **Tree grouping**: Trees are grouped using depth-first search on cross-pattern connectivity  
- **Constraint naming**: Each constraint type has systematic naming in the solver for easy identification
- **Big-M formulation**: Tent separation uses the actual count of surrounding candidates rather than a fixed M
- **Solver type**: Defaults to using SCIP optimizer through OR-Tools
