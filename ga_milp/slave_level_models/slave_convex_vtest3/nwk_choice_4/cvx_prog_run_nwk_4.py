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

def cvx_prog_run_nwk_4(parallel_thread_num, bilinear_pieces, solver_choice):
        
    import sys 
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\')
    from slave_convex_backend import slave_convex_backend
    import pandas as pd 
    
    slave_models_location = 'C:\\Optimization_zlc\\slave_level_models\\slave_convex_vtest3\\nwk_choice_4\\'
    package_name = 'nwk_choice_4'
    files = pd.DataFrame(columns = ['Filename'])
    
    ##Auxillary files 

    
    ##Chiller models 
        
    ##File 1
    inputmodel = pd.DataFrame(data = ['chiller1_nwk_choice_4'], columns = ['Filename'])                      ##Chiller 1 model 
    files = files.append(inputmodel, ignore_index=True)
    
    ##File 2
    inputmodel = pd.DataFrame(data = ['gv2_substation_nwk_choice_4'], columns = ['Filename'])                ##gv2_substation 
    files = files.append(inputmodel, ignore_index=True)    
    
    ##File 3
    inputmodel = pd.DataFrame(data = ['chiller_ret_nwk_choice_4'], columns = ['Filename'])                ##gv2_substation 
    files = files.append(inputmodel, ignore_index=True)        
    
    ##File 4
    inputmodel = pd.DataFrame(data = ['chiller_evap_flow_consol_nwk_choice_4'], columns = ['Filename'])              ##gv2_substation 
    files = files.append(inputmodel, ignore_index=True)   

    ##File 5
    inputmodel = pd.DataFrame(data = ['layers_nwk_choice_4'], columns = ['Filename'])              ##gv2_substation 
    files = files.append(inputmodel, ignore_index=True)   
    
    ##File 6
    inputmodel = pd.DataFrame(data = ['cp_network_nwk_choice_4'], columns = ['Filename'])              ##gv2_substation 
    files = files.append(inputmodel, ignore_index=True)   
    
    ##File 7
    inputmodel = pd.DataFrame(data = ['splitter1_temp_nwk_choice_4'], columns = ['Filename'])              ##gv2_substation 
    files = files.append(inputmodel, ignore_index=True)   

    ##File 8
    inputmodel = pd.DataFrame(data = ['splitter2_temp_nwk_choice_4'], columns = ['Filename'])              ##gv2_substation 
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
    obj_value, results, results_y = slave_convex_backend(files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice)
    
    
    return obj_value, results, results_y
