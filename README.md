# SBRP Exact Solver (School Bus Routing Problem)

An exact mathematical optimization solver written in Python using IBM ILOG CPLEX (`docplex`) to solve variants of the School Bus Routing Problem (SBRP). This project implements mixed-integer linear programming (MILP) models designed to minimize total transit time while ensuring student safety, capacity constraints, and strict punctuality.

## Project Overview

Routing logistics for educational institutions heavily impact both operational costs and student safety. This repository provides an exact algorithmic approach to determine the optimal sequence of stops and routes for a fleet of buses, given fixed student locations and potential bus stops. 

Because finding exact solutions to routing problems is computationally expensive ($NP$-hard), this solver implements and compares two classical subtour elimination approaches, utilizing a custom iterative constraints-generation loop to handle combinatorial explosions efficiently.

## Technical Architecture & Features

The solver implements three distinct components derived from academic optimization models:

1. **TMZ Model (`src/tmz_model.py`)**: Implements the Tucker-Mendoza-Zelty formulation for subtour elimination using a fixed number of binary and continuous tracking variables. Ideal for baseline testing on smaller problem instances.
2. **DFJ Model (`src/dfj_model.py`)**: Implements the Dantzig-Fulkerson-Johnson formulation. While mathematically tighter, it inherently contains an exponential number of subtour elimination constraints.
3. **Iterative Solver (`src/iterative_solver.py`)**: A customized cutting-plane loop that resolves the DFJ limitation. Instead of injecting all constraints upfront, it acts as a dynamic supervisor that solves a relaxed version of the problem, identifies violated subtours programmatically, and injects specific lazy constraints on-the-fly until convergence to the true global optimum.

## Prerequisites

* Language:Python 3.10+
* Optimization Library: `docplex` (IBM Decision Optimization CPLEX Modeling for Python)
* Graph Analytics: `NetworkX`
* Mathematical Solver: IBM ILOG CPLEX Optimizer (Community or Commercial edition)

## Mathematical Formulations

The core challenge of the SBRP is preventing independent closed loops (subtours) that do not connect to the main depot (node 0).

### 1. Dantzig-Fulkerson-Johnson (DFJ) Formulation
The DFJ approach eliminates subtours by ensuring that the flow leaving any proper subset of nodes $S$ is sufficient to maintain global connectivity. It introduces a set of constraints based on subset cardinality:

$$\sum_{i \in S} \sum_{j \in S} x_{ijd} \le |S| - 1 \quad \forall S \subseteq V \setminus \{0\}, |S| \ge 2, \forall d \in K$$

Evaluating all subsets $S$ upfront leads to an exponential growth of constraints ($2^n - 2$). To mitigate this, our implementation utilizes a dynamic cutting-plane algorithm that injects these inequalities only when a subtour is programmatically detected during relaxation steps.

### 2. Tucker-Mendoza-Zelty (TMZ) Formulation
The TMZ approach avoids exponential growth by introducing continuous auxiliary variables $u_{ik}$ that track the vehicle load or sequential order of stops along the route. The formulation bounds the variables linearly using the following bounding inequalities:

$$u_{ik} - u_{jk} + M \cdot x_{ijk} \le M - 1 \quad \forall i, j \in V \setminus \{0\}, i \neq j, \forall k \in K$$

Where $M$ represents the total number of nodes in the vertex set $V$. While this formulation increases variable density, it remains static and bounded.

### 1. Static TMZ Constraints (src/tmz_model.py)
Implements the `apply_tmz_constraints` function. It introduces the continuous decision variables into the docplex model and establishes the initialization states at the depot node along with regularized bounding conditions.

### 2. Brute-Force DFJ Constraints (src/dfj_model.py)
Implements the `apply_dfj_brute_force_constraints` function. It uses combinatorial iterators to generate every proper subset of vertices. This module is intended exclusively as an exact mathematical baseline for small-scale validation instances.

### 3. Graph-Based Iterative Solver (src/iterative_solver.py)
Implements the `solve_with_iterative_dfj` function, executing a cutting-plane framework. The algorithm operates through the following pipeline:

1. Relaxation: Solves the mathematical model omitting initial subtour constraints.
2. Graph Mapping: Parses the active binary routing matrix from the solver output into a directed graph structure using NetworkX.
3. Subtour Detection: Algorithmically extracts simple directed cycles. Cycles that do not intersect with the main depot (node 0) are flagged as illegal subtours.
4. Cut Injection: Programmatically constructs the mathematical inequalities required to break the detected cycles, appends them to the active model instance, and re-solves.
5. Termination: The loop breaks when zero illegal cycles are detected, guaranteeing convergence to the true global optimum.
##  Repository Structure

```text
├── LICENSE                # MIT License
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── src/
    ├── __init__.py        # Package initialization and function exports
    ├── tmz_model.py       # TMZ formulation implementation
    ├── dfj_model.py       # Brute-force DFJ implementation for benchmarks
    └── iterative_solver.py# Custom iterative cutting-plane loop 
