import numpy as np 
import cvxpy as cp
import rospy



def get_dcbf(u_hat:np.ndarray, del_pij:np.ndarray, alpha_i:float, alpha_j:float, del_vij:np.ndarray, Ds:float, gamma:float):
    control = cp.Variable(2)  

    # dcbf constraint
    A = del_pij.T
    h_ij = np.sqrt(2*(alpha_i+alpha_j)*(np.linalg.norm(del_pij, ord=2)-Ds)) + (del_pij.T)@(del_vij)/np.linalg.norm(del_pij, ord=2)
    b = (alpha_i/(alpha_i+alpha_j))* (gamma* (h_ij**3)*np.linalg.norm(del_pij, ord=2) 
                                    - (del_vij.T@del_pij)/(np.linalg.norm(del_pij, ord=2)**2)
                                    + (alpha_i+alpha_j)*(del_vij.T@del_pij)/np.sqrt(2*(alpha_i+alpha_j)*(np.linalg.norm(del_pij, ord=2)-Ds))
                                    + np.linalg.norm(del_vij, ord=2)
                                    )

    # DCBF constraint
    dcbf_constraint = [ A@control <= b]


    # control limits constraints (infinity norm)
    control_limits_constraint = [control[i] >= -alpha_i for i in range(2)]
    control_limits_constraint += [control[i] <= alpha_i for i in range(2)]

    # Cost function to be minimized
    cost = cp.Minimize(cp.sum_squares(control - u_hat))

    # Optimization problem
    problem = cp.Problem(cost, 
                        dcbf_constraint +
                        control_limits_constraint )

    problem.solve()

    optimal_states = control.value
    print(control.value)

    return control.value



