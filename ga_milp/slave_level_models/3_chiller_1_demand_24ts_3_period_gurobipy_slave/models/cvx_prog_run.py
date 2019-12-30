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

def cvx_prog_run(parallel_thread_num, bilinear_pieces, solver_choice, obj_weights, time_steps):
        
    import sys 
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\')
    from slave_convex_backend_v3 import slave_convex_backend_v3
    import pandas as pd 
    
    slave_models_location = 'C:\\Optimization_zlc\\slave_level_models\\3_chiller_1_demand_24ts_3_period_gurobipy_slave\\models\\'
    package_name = 'models'
    files = pd.DataFrame(columns = ['Filename'])
    
    ##Auxillary files 

    
    ##Chiller models 
        
    ##File 1
    inputmodel = pd.DataFrame(data = ['chiller1'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 2
    inputmodel = pd.DataFrame(data = ['chiller2'], columns = ['Filename'])                   
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 3
    inputmodel = pd.DataFrame(data = ['chiller3'], columns = ['Filename'])                   
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 4
    inputmodel = pd.DataFrame(data = ['combined_substation'], columns = ['Filename'])         
    files = files.append(inputmodel, ignore_index=True)     
    
    ##File 5
    inputmodel = pd.DataFrame(data = ['chiller_ret'], columns = ['Filename'])               
    files = files.append(inputmodel, ignore_index=True)        
    
    ##File 6
    inputmodel = pd.DataFrame(data = ['chiller_evap_flow_consol'], columns = ['Filename'])              
    files = files.append(inputmodel, ignore_index=True)   

    ##File 7
    inputmodel = pd.DataFrame(data = ['layers'], columns = ['Filename'])              
    files = files.append(inputmodel, ignore_index=True)   
    
    ##File 8
    inputmodel = pd.DataFrame(data = ['cp_network'], columns = ['Filename'])              
    files = files.append(inputmodel, ignore_index=True)   
    
    ##File 9
    inputmodel = pd.DataFrame(data = ['splitter1_temp'], columns = ['Filename'])               
    files = files.append(inputmodel, ignore_index=True)   

    ##File 10
    inputmodel = pd.DataFrame(data = ['splitter2_temp'], columns = ['Filename'])             
    files = files.append(inputmodel, ignore_index=True)   
    ##Multi-time problem definition
    ##By multi-time, this means that the multi-time problem is transferred to the slave
    ##If the multi-time part is handled by the master optimizer, multi-time should be 0
    ##The values can only be 1(yes) or 0(no)
    multi_time = 0
    
    ##Objective function definition 
    ##The values can be either of the following 
    ##1. 'investment_cost'
    ##2. 'operation_cost'
    ##3. 'power'
    ##4. 'impact'
    
    #Put them in a list
    obj_func = 'power'
    
    ##Preferred solver 
    obj_value, results, results_y = slave_convex_backend_v3(files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice, obj_weights, time_steps)
    
    
    return obj_value, results, results_y
