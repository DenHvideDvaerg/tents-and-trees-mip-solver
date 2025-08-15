# Mathematical Model Documentation

This document provides a formal mathematical programming formulation of the Tents and Trees puzzle as a Mixed Integer Programming (MIP) problem.

## Problem Definition

Given:
- An **m × n** grid representing the puzzle board
- **Row constraints** R = {r₁, r₂, ..., rₘ} specifying required tents per row
- **Column constraints** C = {c₁, c₂, ..., cₙ} specifying required tents per column  
- **Tree positions** T ⊆ {(i,j) : 1 ≤ i ≤ m, 1 ≤ j ≤ n}

**Objective:** Find tent positions that satisfy all Tents and Trees rules.

## Sets and Indices

| Symbol | Definition |
|--------|------------|
| **I** | Set of row indices: I = {1, 2, ..., m} |
| **J** | Set of column indices: J = {1, 2, ..., n} |
| **T** | Set of tree positions: T ⊆ I × J |
| **P** | Set of potential tent positions (tent candidates) |
| **A(i,j)** | Adjacent cells to position (i,j): horizontally and vertically neighboring |
| **S(i,j)** | Surrounding cells to position (i,j): all 8 neighboring positions |

### Tent Candidate Set
The set of valid tent positions is defined as:

```
P = {(i,j) ∈ I × J : (i,j) ∉ T and A(i,j) ∩ T ≠ ∅}
```

This ensures tents can only be placed adjacent to at least one tree.

## Decision Variables

| Variable | Domain | Definition |
|----------|--------|------------|
| **x_{i,j}** | {0, 1} | 1 if a tent is placed at position (i,j) ∈ P, 0 otherwise |

## Objective Function

Since this is a constraint satisfaction problem, we use a feasibility objective:

```
minimize 0
```

Alternatively, for solution uniqueness or preference:

```
minimize Σ_{(i,j) ∈ P} x_{i,j}
```

## Constraints

### 1. Row Sum Constraints
Each row must contain exactly the required number of tents:

```
Σ_{j: (i,j) ∈ P} x_{i,j} = r_i    ∀i ∈ I
```

### 2. Column Sum Constraints  
Each column must contain exactly the required number of tents:

```
Σ_{i: (i,j) ∈ P} x_{i,j} = c_j    ∀j ∈ J
```

### 3. Tree Adjacency Constraints
Each tree must have exactly one adjacent tent:

```
Σ_{(k,l) ∈ A(i,j) ∩ P} x_{k,l} = 1    ∀(i,j) ∈ T
```

### 4. Tent Isolation Constraints
No tent can be adjacent to another tent (including diagonally):

```
Σ_{(k,l) ∈ S(i,j) ∩ P} x_{k,l} ≤ M(1 - x_{i,j})    ∀(i,j) ∈ P
```

Where M is a large constant (typically M = 8, the maximum number of surrounding cells).

Alternatively, using pairwise constraints:

```
x_{i,j} + x_{k,l} ≤ 1    ∀(i,j) ∈ P, ∀(k,l) ∈ S(i,j) ∩ P
```

## Complete MIP Formulation

**Variables:**
```
x_{i,j} ∈ {0,1}    ∀(i,j) ∈ P
```

**Objective:**
```
minimize Σ_{(i,j) ∈ P} x_{i,j}
```

**Subject to:**
```
Σ_{j: (i,j) ∈ P} x_{i,j} = r_i                          ∀i ∈ I     (Row sums)

Σ_{i: (i,j) ∈ P} x_{i,j} = c_j                          ∀j ∈ J     (Column sums)

Σ_{(k,l) ∈ A(i,j) ∩ P} x_{k,l} = 1                      ∀(i,j) ∈ T (Tree adjacency)

x_{i,j} + x_{k,l} ≤ 1                                    ∀(i,j) ∈ P, ∀(k,l) ∈ S(i,j) ∩ P (Tent isolation)

x_{i,j} ∈ {0,1}                                          ∀(i,j) ∈ P (Binary variables)
```
