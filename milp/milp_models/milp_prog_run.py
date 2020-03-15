##Interface for optimization using MILP, up to the bilinear level

##The process is as follows 
    ##Take in values from the Genetic Algorithm 
        ##Passes in a list of GA variables with the respective tag names to act as parameters for the MILP phase 
    ##Mixed integer bilinear/linear phase  
        ##A parameter list
        ##Models 
        ##Script to arrange into standard lp form 
        ##Script to extract the answers from the solver 
        ##Returning the objective function values to the master solver

def milp_prog_run(parallel_thread_num, bilinear_pieces, solver_choice):
    
    ##parallel_thread_num       --- the unique parallel thread number assigned for file referencing 
    ##bilinear_pieces           --- the number of pieces used to linearize the binlinear variables 
    ##solver_choice             --- the choice of solver used
    
    import os 
    current_path = os.path.dirname(__file__)[:-13] + '//'    
    import sys 
    sys.path.append(current_path + 'milp_conversion_handlers//')
    from milp_backend import milp_backend
    import pandas as pd 
    
    models_location = current_path + 'milp_models\\'
    files = pd.DataFrame(columns = ['Filename'])
    
    ##Layers module
    inputmodel = pd.DataFrame(data = ['layers'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)
    
    ##############################################################################################################    
    ##Chiller evaporator modules 
    inputmodel = pd.DataFrame(data = ['chiller1'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)    
    
    inputmodel = pd.DataFrame(data = ['chiller2'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)        
    
    ##############################################################################################################
    ##Evaporator network modules 
    inputmodel = pd.DataFrame(data = ['chiller1_evap_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)      
    
    inputmodel = pd.DataFrame(data = ['chiller2_evap_nwk'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)  

    ##############################################################################################################
    ##Evaporator pump modules 
    inputmodel = pd.DataFrame(data = ['chiller1_evap_pump'], columns = ['Filename'])               
    files = files.append(inputmodel, ignore_index=True)

    inputmodel = pd.DataFrame(data = ['chiller2_evap_pump'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)

    ##############################################################################################################
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

    inputmodel = pd.DataFrame(data = ['parallel_nwk_consol'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)
    
    ##############################################################################################################
    ##Distribution pump modules 
    inputmodel = pd.DataFrame(data = ['dist_nwk_pump'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)    
    
    ##############################################################################################################
    ##Substation modules 
    inputmodel = pd.DataFrame(data = ['gv2_substation'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)    
    
    inputmodel = pd.DataFrame(data = ['hsb_substation'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True) 

    ##############################################################################################################
    ##Process modules 
    inputmodel = pd.DataFrame(data = ['chiller_evap_flow_consol'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True)      
    
    inputmodel = pd.DataFrame(data = ['chiller_ret'], columns = ['Filename'])                
    files = files.append(inputmodel, ignore_index=True) 

    
    ##Objective function definition 
    ##The values can be either of the following 
    ##1. 'investment_cost'
    ##2. 'operation_cost'
    ##3. 'power'
    ##4. 'impact'
    
    #Put them in a list
    obj_func = 'power'
    
    ##Preferred solver 
    obj_value, results, results_y = milp_backend(files, obj_func, parallel_thread_num, models_location, bilinear_pieces, solver_choice)
    
    return obj_value, results, results_y
