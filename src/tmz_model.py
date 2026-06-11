"""
TMZ Subtour Elimination Formulation for SBRP.
"""

def apply_tmz_constraints(mdl, V, K, x, y):
    """
    Applies the Tucker-Mendoza-Zelty (TMZ) static subtour elimination constraints.
    Increases model size linearly by introducing continuous tracking variables (u).
    """
    M = len(V)
    
    # Variables Definition
    u = {(i, k): mdl.integer_var(lb=0, ub=M-1, name=f'u_{i}_{k}') for i in V for k in K}
    
    # Regularization constraints for tracking variables
    for i in V:
        for k in K:
            mdl.add_constraint(u[i, k] <= M * y[i, k])
            
    # Core TMZ bounding inequalities
    for i in V:
        for j in V:
            if i != j and j != 0:
                for k in K:
                    mdl.add_constraint(u[i, k] - u[j, k] + M * x[i, j, k] <= M - 1)
                    
    # Depot initialization (Routes start at the school)
    for k in K:
        mdl.add_constraint(u[0, k] == 0)
        
    return mdl
