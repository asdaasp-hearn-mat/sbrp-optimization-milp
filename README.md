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

## 🛠️ Tech Stack & Prerequisites

* **Language:** Python 3.10+
* **Optimization Library:** `docplex` (IBM Decision Optimization CPLEX Modeling for Python)
* **Mathematical Solver:** IBM ILOG CPLEX Optimizer (Community or Commercial edition)

##  Repository Structure

```text
.
├── LICENSE                # MIT License
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
├── data/
│   └── sample_instance.json  # Dummy dataset for testing constraints
└── src/
    ├── __init__.py
    ├── tmz_model.py       # A.1: TMZ Formulation implementation
    ├── dfj_model.py       # A.2: DFJ Base implementation
    └── iterative_solver.py# A.3: Custom iterative cutting-plane loop
