##This function takes in string names from the model folder, imports and runs functions dynamically 
##The input strings are in the form of pandas dataframe 



def get_values_models(files, multi_time):
    import pandas as pd
    import importlib
    from process_master_var import process_master_var
    
    ##Imports the multi_time dataset 
    if multi_time == 1:
        from process_multi_time import process_multi_time 
    
    
    ##Deals with layers 
    layerslist = pd.DataFrame(columns = ['Type', 'Name'])                     ##Initiate a list to get essential values from the layers file 
    utilitylist = pd.DataFrame(columns = ['Name', 'Fmin', 'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    processlist = pd.DataFrame(columns = ['Name', 'Fmin', 'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    streams = pd.DataFrame(columns = ['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    cons_eqns = pd.DataFrame(columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns_terms = pd.DataFrame(columns = ['Name', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient'])
    
    
    rows=len(files.index) 
    
    for i in range (0,rows):
        #from layers import layers
        
        j=importlib.import_module(files['Filename'][i])                     ##Importing the relevant module for the models
            
        unit_type = ''                                                      ##Checking for the correct unit type 
        unit_type = getattr(j,'checktype')(unit_type)
        
        if unit_type == 'layers':                                           ##Populating the associated dataframes for GLPK input file 
            layerslist = getattr(j, files['Filename'][i])(layerslist)
            
        elif unit_type == 'utility':
            mdv = process_master_var(files['Filename'][i])
            utilitylist, streams, cons_eqns, cons_eqns_terms = getattr(j, files['Filename'][i])(mdv, 
                                                                            utilitylist, streams, cons_eqns, 
                                                                            cons_eqns_terms)
        elif unit_type == 'utility_mt':
            ##This one takes in multi time values 
            
            print(1)
            
        elif unit_type == 'process':
            mdv = process_master_var(files['Filename'][i])
            processlist, streams, cons_eqns, cons_eqns_terms = getattr(j, files['Filename'][i])(mdv, 
                                                                           processlist, streams, cons_eqns, 
                                                                           cons_eqns_terms)
        else:
            print('Input file error...')
    
#    layerslist.to_csv('C:\\Optimization_zlc\\layerslist.csv', sep=',', encoding='utf-8')
#    utilitylist.to_csv('C:\\Optimization_zlc\\utilitylist.csv', sep=',', encoding='utf-8')
#    processlist.to_csv('C:\\Optimization_zlc\\processlist.csv', sep=',', encoding='utf-8')
#    streams.to_csv('C:\\Optimization_zlc\\streams.csv', sep=',', encoding='utf-8')
#    cons_eqns.to_csv('C:\\Optimization_zlc\\cons_eqns.csv', sep=',', encoding='utf-8')
#    cons_eqns_terms.to_csv('C:\\Optimization_zlc\\cons_eqns_terms.csv', sep=',', encoding='utf-8')
    return layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms
