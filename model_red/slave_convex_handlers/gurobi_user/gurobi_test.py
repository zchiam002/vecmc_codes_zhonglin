##This is a test script of the gurobi python interface 


##This script is the main function 
def run_gurobipy ():
    
    import gurobipy as grb 
    
    ##Create a new Gurobi model 
    example_model = grb.Model('test_model')
    
    ##Add variables 
    example_model, example_var = create_groubipy_variables (example_model)
    example_model.update()
    ##Set the objective function 
    example_model = set_gurobipy_objective_function (example_model, example_var)
    example_model.update()    
    ##Adding the constraints 
    example_model = add_constraints_gurobipy_model (example_model, example_var)
    example_model.update()
    example_model.write('C:\\Optimization_zlc\\slave_convex_handlers\\gurobi_user\\model.lp')
    ##Solving the model 
    example_model.optimize()
    
    # Print the feasible solution if optimal.
    if example_model.status == grb.GRB.Status.OPTIMAL:
        print('Obj Function:', example_model.objVal)
        for v in example_model.getVars():
            print(v.varName, v.x)
    # Another way to print the variable
        print("Optimal Solution:")
        print(example_var[0].varName, example_var[0].x)
        print(example_var[1].varName, example_var[1].x)        
    else:
        print(example_model.status)    
    
    return 

##This function adds variables 
def create_groubipy_variables (grb_model):
    
    import gurobipy as grb 
    
    ##grb_model --- a groubi model 
    
    ##Creating a list of variables 
    grb_var = []
    
    grb_var.append(grb_model.addVar(lb=0, ub = 9, vtype = grb.GRB.CONTINUOUS, name ='x'))
    grb_model.update()
    grb_var.append(grb_model.addVar(lb=0, vtype = grb.GRB.CONTINUOUS, name ='y')) 
    grb_model.update()
    return grb_model, grb_var

##This function sets the objective function 
def set_gurobipy_objective_function (grb_model, grb_var):
        
    import gurobipy as grb 
    
    ##grb_model --- a gurobi model 
    ##grb_var --- a list of gurobi variables 
    
    ##Setting objective function coefficients 
    grb_obj_func_coeff = [10, 26]
    dim_grb_obj_func_coeff = len(grb_obj_func_coeff)
    
    cum_obj_fun = 0
    
    for i in range (0, dim_grb_obj_func_coeff):
        cum_obj_fun = cum_obj_fun + grb_var[i] * grb_obj_func_coeff[i]
    
    ##Adding the objective function into the model 
    grb_model.setObjective(cum_obj_fun, grb.GRB.MINIMIZE)
            
    return grb_model

##This function adds the constraints to the model 
def add_constraints_gurobipy_model (grb_model, grb_var):
    
    import gurobipy as grb 

    ##grb_model --- a gurobi model 
    ##grb_var --- a list of gurobi variables 

    ##Creating the dictionary of constraint lists, rhs values and sign 
    constraint_coeff = {}
    constraint_rhs = {}
    
    curr_index = 0
    
    constraint_coeff[str(curr_index)] = [11, 3]
    constraint_rhs[str(curr_index)] = 21
    
    for i in range (0, len(constraint_coeff[str(curr_index)])):
        if i == 0:
            cum_curr_constr = constraint_coeff[str(curr_index)][i] * grb_var[i]
        else:
            cum_curr_constr = cum_curr_constr + (constraint_coeff[str(curr_index)][i] * grb_var[i])
    
    grb_model.addConstr(cum_curr_constr >= constraint_rhs[str(curr_index)], 'c' + str(curr_index))
    
    curr_index = curr_index + 1

    constraint_coeff[str(curr_index)] = [6, 20]
    constraint_rhs[str(curr_index)] = 39
    
    for i in range (0, len(constraint_coeff[str(curr_index)])):
        if i == 0:
            cum_curr_constr = constraint_coeff[str(curr_index)][i] * grb_var[i]
        else:
            cum_curr_constr = cum_curr_constr + (constraint_coeff[str(curr_index)][i] * grb_var[i])
    
    grb_model.addConstr(cum_curr_constr >= constraint_rhs[str(curr_index)], 'c' + str(curr_index))    
    
    return grb_model

     
 

################################################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    run_gurobipy()









