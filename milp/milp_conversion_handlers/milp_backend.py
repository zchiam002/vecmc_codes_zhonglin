##This function handles all the backend operation for communicating with GLPK

def milp_backend(files, obj_func, parallel_thread_num, models_location, bilinear_pieces, solver_choice):
    
    ##files                     --- dataframe of all the file names of the models 
    ##obj_func                  --- the chosen objective function to be evaluated against 
    ##parallel_thread_num       --- unique parallel thread identifier
    ##models_location           --- the location of the models 
    ##bilinear_pieces           --- the number of bilinear pieces for linearization of bilinear variables 
    ##solver_choice             --- only GLPK is available for now
    
    import pandas as pd
    import os 
    current_path = os.path.dirname(__file__) + '//'  
    import sys 
    sys.path.append(current_path + 'auxillary//')
    sys.path.append(models_location)
    from get_values_models import get_values_models
    
    ##Getting the values from the models 
    layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms = get_values_models(files, parallel_thread_num, models_location)     
    
    
    return 

