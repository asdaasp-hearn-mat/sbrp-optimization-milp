"""
Graph-based Iterative Cutting-Plane Solver for DFJ Formulation.
"""
import networkx as nx

def solve_with_iterative_dfj(mdl, V, K, x, y, max_iterations=100):
    """
    Executes a Cutting-Plane loop using NetworkX to find programmatic subtours
    and dynamically injects required DFJ constraints on-the-fly.
    
    Returns the final solution object and the total computation time.
    """
    total_solve_time = 0.0
    iteration = 1
    
    while iteration <= max_iterations:
        # 1. Solve the current relaxation
        solution = mdl.solve(log_output=False)
        if not solution:
            print("[!] Model became infeasible or could not be solved.")
            return None, total_solve_time
            
        total_solve_time += mdl.get_solve_details().time
        
        # 2. Extract active arcs per bus
        bus_arcs = {}
        for d in K:
            active_arcs = [
                (i, j) for (i, j, k) in x 
                if x[i, j, k].solution_value > 0.9 and k == d
            ]
            bus_arcs[d] = active_arcs
            
        # 3. Detect invalid subtours using directed graph structures
        pending_constraints = {}
        for bus, arcs in bus_arcs.items():
            G = nx.DiGraph()
            G.add_edges_from(arcs)
            
            all_cycles = list(nx.simple_cycles(G))
            # Safe filtration without modifying list during iteration
            subtours = [cycle for cycle in all_cycles if 0 not in cycle]
            
            if subtours:
                pending_constraints[bus] = subtours
                
        # 4. Convergence Check
        if not pending_constraints:
            print(f"[✓] Convergence achieved at iteration {iteration}. Optimal solution found.")
            break
            
        # 5. Cut Injection
        for bus, subtours in pending_constraints.items():
            for subconj in subtours:
                for d in K:
                    mdl.add_constraint(
                        mdl.sum(x[i, j, d] for i in subconj for j in V if j not in subconj) >= y[subconj[0], d]
                    )
                    
        iteration += 1
        
    return solution, total_solve_time
