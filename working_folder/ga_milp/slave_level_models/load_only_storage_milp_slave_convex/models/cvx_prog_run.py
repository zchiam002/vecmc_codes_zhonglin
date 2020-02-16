##Interface for convex optimization with/without relaxations

##The process is as follows 
    ##Take in values from the master optimization 
        ##Passes in a list of master variables with the respective tag names to act as constants for the quadratic programming phase 
    ##Convex programming phase 
        ##A master list
        ##Models 
        ##Script to arrange into standard lp form 
        ##Script to extract the answers from the solver 
        ##Returning the objective function values to the master solver

def cvx_prog_run_lo(parallel_thread_num, bilinear_pieces, solver_choice, time_steps, obj_weight):
        
    import sys 
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\')
    from slave_convex_backend_v2 import slave_convex_backend_v2
    import pandas as pd 
    
    ##parallel_thread_num --- the associated location for reading the master decision variable values 
    ##bilinear_pieces --- the number of bilinear pieces
    ##solver_choice --- gurobi or GLPK
    ##time_steps --- the associated number of time-steps for the multi-time problem
    ##obj_weight --- the associated weights to each of the objective functions
    
    slave_models_location = 'C:\\Optimization_zlc\\slave_level_models\\load_only_storage_milp_slave_convex\\models'
    package_name = 'models'
    files = pd.DataFrame(columns = ['Filename'])
    
    ##Layers module
    inputmodel = pd.DataFrame(data = ['layers'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)
    
    
    ##Chiller modules
    inputmodel = pd.DataFrame(data = ['chiller1'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)    
    
    inputmodel = pd.DataFrame(data = ['chiller2'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)  

    inputmodel = pd.DataFrame(data = ['chiller3'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    ##Pump modules 
    inputmodel = pd.DataFrame(data = ['evap_pump1'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    inputmodel = pd.DataFrame(data = ['evap_pump2'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    inputmodel = pd.DataFrame(data = ['evap_pump3'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)    

    inputmodel = pd.DataFrame(data = ['cond_pump1'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    inputmodel = pd.DataFrame(data = ['cond_pump2'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    inputmodel = pd.DataFrame(data = ['cond_pump3'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    inputmodel = pd.DataFrame(data = ['dist_nwk_pump'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    ##Network modules 
    inputmodel = pd.DataFrame(data = ['evap_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)      

    inputmodel = pd.DataFrame(data = ['cond_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)
    
    ##Substation modules 
    inputmodel = pd.DataFrame(data = ['combined_substation'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    ##Storage modules 
#    inputmodel = pd.DataFrame(data = ['chilled_water_storage'], columns = ['Filename'])                
#    files = files.append(inputmodel, ignore_index=True)   
    
    ##Cooling tower modules 
    inputmodel = pd.DataFrame(data = ['cooling_towers'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)       
    
    ##Multi-time problem definition
    ##By multi-time, this means that the multi-time problem is transferred to the slave
    ##If the multi-time part is handled by the master optimizer, multi-time should be 0
    ##The values can only be 1(yes) or 0(no)
    multi_time = 1
    
    ##Objective function definition 
    ##The values can be either of the following 
    ##1. 'investment_cost'
    ##2. 'operation_cost'
    ##3. 'power'
    ##4. 'impact'
    
    ##Put them in a list
    obj_func = ['power', 'operation_cost']
    
    ##The weights for multi-objective optimization
        ##Sum of weights = 1
    obj_weights = [obj_weight[0], obj_weight[1]]
    
    ##Preferred solver 
    obj_value, results, results_y, ind_obj_value, obj_func_table_dict = slave_convex_backend_v2 (files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice, obj_weights, time_steps)
    
    
    return obj_value, results, results_y, ind_obj_value, obj_func_table_dict
