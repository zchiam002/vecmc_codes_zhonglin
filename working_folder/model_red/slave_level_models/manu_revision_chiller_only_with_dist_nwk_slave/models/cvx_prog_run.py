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

def cvx_prog_run(parallel_thread_num, bilinear_pieces, solver_choice):

    import os
    current_path = os.path.dirname(os.path.abspath(__file__))[:-72] + '\\'
               
    import sys 
    sys.path.append(current_path + 'slave_convex_handlers\\')
    from slave_convex_backend import slave_convex_backend
    import pandas as pd 
    
    slave_models_location = current_path + 'slave_level_models\\manu_revision_chiller_only_with_dist_nwk_slave\\models\\'
    package_name = 'models'
    files = pd.DataFrame(columns = ['Filename'])
    
    ##Layers module
    inputmodel = pd.DataFrame(data = ['layers'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)
    
    
    ##Chiller evaporator modules 
    inputmodel = pd.DataFrame(data = ['chiller1_evap'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)    
    
    inputmodel = pd.DataFrame(data = ['chiller2_evap'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)        
    
    inputmodel = pd.DataFrame(data = ['chiller3_evap'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)  


    ##Evaporator network modules 
    inputmodel = pd.DataFrame(data = ['chiller1_evap_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)      
    
    inputmodel = pd.DataFrame(data = ['chiller2_evap_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)  

    inputmodel = pd.DataFrame(data = ['chiller3_evap_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)  


    ##Evaporator pump modules 
    inputmodel = pd.DataFrame(data = ['chiller1_evap_pump'], columns = ['Filename'])               
    files = files.append(inputmodel, ignore_index=True)

    inputmodel = pd.DataFrame(data = ['chiller2_evap_pump'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    inputmodel = pd.DataFrame(data = ['chiller3_evap_pump'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)


    ##Distribution network modules 
    inputmodel = pd.DataFrame(data = ['splitter1_temp'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)    
    
    inputmodel = pd.DataFrame(data = ['cp_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    inputmodel = pd.DataFrame(data = ['ice_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    inputmodel = pd.DataFrame(data = ['gv2_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True) 
    
    inputmodel = pd.DataFrame(data = ['hsb_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    inputmodel = pd.DataFrame(data = ['tro_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['pfa_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)
    
    inputmodel = pd.DataFrame(data = ['ser_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    inputmodel = pd.DataFrame(data = ['parallel_nwk_consol'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)
    
    
    ##Distribution pump modules 
    inputmodel = pd.DataFrame(data = ['dist_nwk_pump'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)    
    
    
    ##Substation modules 
    inputmodel = pd.DataFrame(data = ['gv2_substation'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)    
    
    inputmodel = pd.DataFrame(data = ['hsb_substation'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True) 

    inputmodel = pd.DataFrame(data = ['pfa_substation'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True) 

    inputmodel = pd.DataFrame(data = ['ser_substation'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True) 

    
    ##Substation temperature consolidation module 
    inputmodel = pd.DataFrame(data = ['splitter2_temp'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)     

    
    ##Process modules 
    inputmodel = pd.DataFrame(data = ['chiller_evap_flow_consol'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)      
    
    inputmodel = pd.DataFrame(data = ['chiller_ret'], columns = ['Filename'])                
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
