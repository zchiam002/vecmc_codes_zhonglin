##This function takes in string names from the model folder, imports and runs functions dynamically 
##The input strings are in the form of pandas dataframe 

##This is the gurobi qp edition


def get_values_models(files, parallel_thread_num, models_location):
    
    ##files                     --- a dataframe containing the names of all the model files 
    ##parallel_thread_num       --- unique parallel thread identifier
    ##models_location           --- the location of the models 
    
    import pandas as pd
    import importlib
    from process_master_var import process_master_var
    import sys
    sys.path.append(models_location)
    
    ##Initiating empty dataframes to extract values from the model files 
    layerslist = pd.DataFrame(columns = ['Type', 'Name'])                     
    utilitylist = pd.DataFrame(columns = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                         'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                         'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                         'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    processlist = pd.DataFrame(columns = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                         'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                         'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                         'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    streams = pd.DataFrame(columns = ['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                     'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    cons_eqns = pd.DataFrame(columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns_terms = pd.DataFrame(columns = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2',
                                              'Coeff_cst'])
    
    
    rows=len(files.index) 
    
    for i in range (0,rows):
        ##from layers import layers, etc.
        module_loc = files['Filename'][i]
        j=importlib.import_module(module_loc)                                                    ##Importing the relevant module for the models
            
        unit_type = ''                                                                           ##Checking for the correct unit type 
        unit_type = getattr(j,'checktype_' + files['Filename'][i])(unit_type)
        
        if unit_type == 'layers':                                                                ##Populating the associated dataframes for LP input file 
            layerslist = getattr(j, files['Filename'][i])(layerslist)
            
        elif unit_type == 'utility':
            mdv = process_master_var(files['Filename'][i], parallel_thread_num)
            utilitylist, streams, cons_eqns, cons_eqns_terms = getattr(j, files['Filename'][i])(mdv, utilitylist, streams, cons_eqns, cons_eqns_terms)

            
        elif unit_type == 'process':
            mdv = process_master_var(files['Filename'][i], parallel_thread_num)
            processlist, streams, cons_eqns, cons_eqns_terms = getattr(j, files['Filename'][i])(mdv, processlist, streams, cons_eqns, cons_eqns_terms)
        else:
            print('Input file error...')
    

    return layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms
