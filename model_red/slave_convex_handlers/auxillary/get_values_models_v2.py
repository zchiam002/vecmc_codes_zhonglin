##This function takes in string names from the model folder, imports and runs functions dynamically 
##The input strings are in the form of pandas dataframe 

##This is the gurobi qp edition

def get_values_models_v2(files, package_name, parallel_thread_num, slave_models_location, time_steps):
    import pandas as pd
    import importlib
    from process_master_var import process_master_var_v2
    import sys
    sys.path.append(slave_models_location)
    
    ##Dataframe headers
    layers_headers = ['Type', 'Name']
    utilitylist_headers = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                         'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                         'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                         'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst']
    processlist_headers = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                         'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                         'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                         'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst']
    storagelist_headers = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                         'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                         'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                         'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst']
    streams_headers = ['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                     'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut']
    cons_eqns_headers = ['Name', 'Type', 'Sign', 'RHS_value']
    cons_eqns_terms_headers = ['Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2',
                                              'Coeff_cst']
    
    ##Only for the use with storage units 
    thermal_loss_headers = ['Name', 'Variable1', 'Variable2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 'Coeff_cst']
    
    layerslist_temp = pd.DataFrame(columns = layers_headers)
    utilitylist_temp = pd.DataFrame(columns = utilitylist_headers)
    processlist_temp = pd.DataFrame(columns = processlist_headers)
    storagelist_temp = pd.DataFrame(columns = storagelist_headers)
    streams_temp = pd.DataFrame(columns = streams_headers)
    cons_eqns_temp = pd.DataFrame(columns = cons_eqns_headers)
    cons_eqns_terms_temp = pd.DataFrame(columns = cons_eqns_terms_headers)
    
    ##Only for the use with storage units 
    thermal_loss_temp = pd.DataFrame(columns = thermal_loss_headers)
    
    rows=len(files.index) 
    
    for k in range (0, time_steps):
    
        ##The current time step
        curr_time_step = k
    
        for i in range (0,rows):
            #from layers import layers
            module_loc = package_name + '.' + files['Filename'][i]
            j=importlib.import_module(module_loc)                               ##Importing the relevant module for the models
                
            unit_type = ''                                                      ##Checking for the correct unit type 
            unit_type = getattr(j,'checktype_' + files['Filename'][i])(unit_type)
            
            if unit_type == 'layers':                                           ##Populating the associated dataframes for LP input file 
                layerslist_temp = getattr(j, files['Filename'][i])(layerslist_temp)
                
            elif unit_type == 'utility':
                mdv = process_master_var_v2(files['Filename'][i], parallel_thread_num, curr_time_step)
                utilitylist_temp, streams_temp, cons_eqns_temp, cons_eqns_terms_temp = getattr(j, files['Filename'][i])(mdv, 
                                                                                utilitylist_temp, streams_temp, cons_eqns_temp, 
                                                                                cons_eqns_terms_temp)
            elif unit_type == 'storage':
                ##Storage modules make the problem multi-time
                mdv = process_master_var_v2(files['Filename'][i], parallel_thread_num, curr_time_step)
                storagelist_temp, streams_temp, cons_eqns_temp, cons_eqns_terms_temp, thermal_loss_temp = getattr(j, files['Filename'][i])(mdv, 
                                                                                storagelist_temp, streams_temp, cons_eqns_temp, 
                                                                                cons_eqns_terms_temp, thermal_loss_temp)
        
            elif unit_type == 'process':
                mdv = process_master_var_v2(files['Filename'][i], parallel_thread_num, curr_time_step)
                processlist_temp, streams_temp, cons_eqns_temp, cons_eqns_terms_temp = getattr(j, files['Filename'][i])(mdv, 
                                                                               processlist_temp, streams_temp, cons_eqns_temp, 
                                                                               cons_eqns_terms_temp)
            else:
                print('Input file error...')
    
    ##Appending the necessary variable names for the collected data
    
    dim_layerslist_temp = layerslist_temp.shape
    dim_utilitylist_temp = utilitylist_temp.shape    
    dim_processlist_temp = processlist_temp.shape    
    dim_storagelist_temp = storagelist_temp.shape    
    dim_streams_temp = streams_temp.shape 
    dim_cons_eqns_temp = cons_eqns_temp.shape 
    dim_cons_eqns_terms_temp = cons_eqns_terms_temp.shape 
    dim_thermal_loss_temp = thermal_loss_temp.shape

    ##Determining the number of elements per time-step in each list 
    elem_layerslist_ts = dim_layerslist_temp[0] / time_steps
    elem_utilitylist_ts = dim_utilitylist_temp[0] / time_steps
    elem_processlist_ts = dim_processlist_temp[0] / time_steps
    elem_storagelist_ts = dim_storagelist_temp[0] / time_steps
    elem_streams_ts = dim_streams_temp[0] / time_steps
    elem_cons_eqns_ts = dim_cons_eqns_temp[0] / time_steps
    elem_cons_eqns_terms_ts = dim_cons_eqns_terms_temp[0] / time_steps
    elem_thermal_loss_ts = dim_thermal_loss_temp[0] / time_steps

    layerslist = pd.DataFrame(columns = layers_headers)
    utilitylist = pd.DataFrame(columns = utilitylist_headers)
    processlist = pd.DataFrame(columns = processlist_headers)
    storagelist = pd.DataFrame(columns = storagelist_headers)
    streams = pd.DataFrame(columns = streams_headers)
    cons_eqns = pd.DataFrame(columns = cons_eqns_headers)
    cons_eqns_terms = pd.DataFrame(columns = cons_eqns_terms_headers)
    thermal_loss = pd.DataFrame(columns = thermal_loss_headers)                                             
    
    for i in range (0, time_steps):
    
        ##Handling layerslist
        s1 = i * elem_layerslist_ts
        e1 = s1 + elem_layerslist_ts
        
        for j in range (int(s1), int(e1)):
            mod1 = layerslist_temp['Name'][j] + '_time' + str(i)
            temp_data = [layerslist_temp['Type'][j], mod1]
            temp_df = pd.DataFrame(data = [temp_data], columns = layers_headers)
            layerslist = layerslist.append(temp_df, ignore_index = True)
        
        ##Handling utilitylist
        s2 = i * elem_utilitylist_ts
        e2 = s2 + elem_utilitylist_ts
        
        for j in range (int(s2), int(e2)):
            mod2 = utilitylist_temp['Name'][j] + '_time' + str(i)
            temp_data = [mod2, utilitylist_temp['Variable1'][j], utilitylist_temp['Variable2'][j], utilitylist_temp['Fmin_v1'][j], utilitylist_temp['Fmax_v1'][j], utilitylist_temp['Fmin_v2'][j], 
                         utilitylist_temp['Fmax_v2'][j], utilitylist_temp['Coeff_v1_2'][j], utilitylist_temp['Coeff_v1_1'][j], utilitylist_temp['Coeff_v2_2'][j], utilitylist_temp['Coeff_v2_1'][j],
                         utilitylist_temp['Coeff_v1_v2'][j], utilitylist_temp['Coeff_cst'][j], utilitylist_temp['Fmin'][j], utilitylist_temp['Fmax'][j], utilitylist_temp['Cost_v1_2'][j], 
                         utilitylist_temp['Cost_v1_1'][j], utilitylist_temp['Cost_v2_2'][j], utilitylist_temp['Cost_v2_1'][j], utilitylist_temp['Cost_v1_v2'][j], utilitylist_temp['Cost_cst'][j], 
                         utilitylist_temp['Cinv_v1_2'][j], utilitylist_temp['Cinv_v1_1'][j], utilitylist_temp['Cinv_v2_2'][j], utilitylist_temp['Cinv_v2_1'][j], utilitylist_temp['Cinv_v1_v2'][j], 
                         utilitylist_temp['Cinv_cst'][j], utilitylist_temp['Power_v1_2'][j], utilitylist_temp['Power_v1_1'][j], utilitylist_temp['Power_v2_2'][j], utilitylist_temp['Power_v2_1'][j], 
                         utilitylist_temp['Power_v1_v2'][j], utilitylist_temp['Power_cst'][j], utilitylist_temp['Impact_v1_2'][j], utilitylist_temp['Impact_v1_1'][j], utilitylist_temp['Impact_v2_2'][j], 
                         utilitylist_temp['Impact_v2_1'][j], utilitylist_temp['Impact_v1_v2'][j], utilitylist_temp['Impact_cst'][j]]
            temp_df = pd.DataFrame(data = [temp_data], columns = utilitylist_headers)
            utilitylist = utilitylist.append(temp_df, ignore_index = True)
        
        ##Handling processlist 
        s3 = i * elem_processlist_ts
        e3 = s3 + elem_processlist_ts
        
        for j in range (int(s3), int(e3)):
            mod3 = processlist_temp['Name'][j] + '_time' + str(i)
            temp_data = [mod3, processlist_temp['Variable1'][j], processlist_temp['Variable2'][j], processlist_temp['Fmin_v1'][j], processlist_temp['Fmax_v1'][j], processlist_temp['Fmin_v2'][j], 
                         processlist_temp['Fmax_v2'][j], processlist_temp['Coeff_v1_2'][j], processlist_temp['Coeff_v1_1'][j], processlist_temp['Coeff_v2_2'][j], processlist_temp['Coeff_v2_1'][j],
                         processlist_temp['Coeff_v1_v2'][j], processlist_temp['Coeff_cst'][j], processlist_temp['Fmin'][j], processlist_temp['Fmax'][j], processlist_temp['Cost_v1_2'][j], 
                         processlist_temp['Cost_v1_1'][j], processlist_temp['Cost_v2_2'][j], processlist_temp['Cost_v2_1'][j], processlist_temp['Cost_v1_v2'][j], processlist_temp['Cost_cst'][j], 
                         processlist_temp['Cinv_v1_2'][j], processlist_temp['Cinv_v1_1'][j], processlist_temp['Cinv_v2_2'][j], processlist_temp['Cinv_v2_1'][j], processlist_temp['Cinv_v1_v2'][j], 
                         processlist_temp['Cinv_cst'][j], processlist_temp['Power_v1_2'][j], processlist_temp['Power_v1_1'][j], processlist_temp['Power_v2_2'][j], processlist_temp['Power_v2_1'][j], 
                         processlist_temp['Power_v1_v2'][j], processlist_temp['Power_cst'][j], processlist_temp['Impact_v1_2'][j], processlist_temp['Impact_v1_1'][j], processlist_temp['Impact_v2_2'][j], 
                         processlist_temp['Impact_v2_1'][j], processlist_temp['Impact_v1_v2'][j], processlist_temp['Impact_cst'][j]]
            temp_df = pd.DataFrame(data = [temp_data], columns = processlist_headers)
            processlist = processlist.append(temp_df, ignore_index = True)        
        
        ##Handling storagelist 
        s4 = i * elem_storagelist_ts
        e4 = s4 + elem_storagelist_ts
        
        for j in range (int(s4), int(e4)):
            mod4 = storagelist_temp['Name'][j] + '_time' + str(i)
            temp_data = [mod4, storagelist_temp['Variable1'][j], storagelist_temp['Variable2'][j], storagelist_temp['Fmin_v1'][j], storagelist_temp['Fmax_v1'][j], storagelist_temp['Fmin_v2'][j], 
                         storagelist_temp['Fmax_v2'][j], storagelist_temp['Coeff_v1_2'][j], storagelist_temp['Coeff_v1_1'][j], storagelist_temp['Coeff_v2_2'][j], storagelist_temp['Coeff_v2_1'][j],
                         storagelist_temp['Coeff_v1_v2'][j], storagelist_temp['Coeff_cst'][j], storagelist_temp['Fmin'][j], storagelist_temp['Fmax'][j], storagelist_temp['Cost_v1_2'][j], 
                         storagelist_temp['Cost_v1_1'][j], storagelist_temp['Cost_v2_2'][j], storagelist_temp['Cost_v2_1'][j], storagelist_temp['Cost_v1_v2'][j], storagelist_temp['Cost_cst'][j], 
                         storagelist_temp['Cinv_v1_2'][j], storagelist_temp['Cinv_v1_1'][j], storagelist_temp['Cinv_v2_2'][j], storagelist_temp['Cinv_v2_1'][j], storagelist_temp['Cinv_v1_v2'][j], 
                         storagelist_temp['Cinv_cst'][j], storagelist_temp['Power_v1_2'][j], storagelist_temp['Power_v1_1'][j], storagelist_temp['Power_v2_2'][j], storagelist_temp['Power_v2_1'][j], 
                         storagelist_temp['Power_v1_v2'][j], storagelist_temp['Power_cst'][j], storagelist_temp['Impact_v1_2'][j], storagelist_temp['Impact_v1_1'][j], storagelist_temp['Impact_v2_2'][j], 
                         storagelist_temp['Impact_v2_1'][j], storagelist_temp['Impact_v1_v2'][j], storagelist_temp['Impact_cst'][j]]
            temp_df = pd.DataFrame(data = [temp_data], columns = storagelist_headers)
            storagelist = storagelist.append(temp_df, ignore_index = True)
            
        ##Handling streams
        s5 = i * elem_streams_ts
        e5 = s5 + elem_streams_ts
        
        for j in range (int(s5), int(e5)):
            mod5 = streams_temp['Parent'][j] + '_time' + str(i)
            mod6 = streams_temp['Name'][j] + '_time' + str(i)
            mod7 = streams_temp['Layer'][j] + '_time' + str(i)
            temp_data = [mod5, streams_temp['Type'][j], mod6, mod7, streams_temp['Stream_coeff_v1_2'][j], streams_temp['Stream_coeff_v1_1'][j], streams_temp['Stream_coeff_v2_2'][j], 
                         streams_temp['Stream_coeff_v2_1'][j], streams_temp['Stream_coeff_v1_v2'][j], streams_temp['Stream_coeff_cst'][j], streams_temp['InOut'][j]]
            temp_df = pd.DataFrame(data = [temp_data], columns = streams_headers)   
            streams = streams.append(temp_df, ignore_index = True)
            
        ##Handling cons_eqns
        s6 = i * elem_cons_eqns_ts
        e6 = s6 + elem_cons_eqns_ts

        for j in range (int(s6), int(e6)):
            mod8 = cons_eqns_temp['Name'][j] + '_time' + str(i)
            temp_data = [mod8, cons_eqns_temp['Type'][j], cons_eqns_temp['Sign'][j], cons_eqns_temp['RHS_value'][j]]
            temp_df = pd.DataFrame(data = [temp_data], columns = cons_eqns_headers)   
            cons_eqns = cons_eqns.append(temp_df, ignore_index = True)     
            
        ##Handling cons_eqn_terms 
        s7 = i * elem_cons_eqns_terms_ts
        e7 = s7 + elem_cons_eqns_terms_ts

        for j in range (int(s7), int(e7)): 
            mod9 = cons_eqns_terms_temp['Parent_unit'][j] + '_time' + str(i)
            mod10 = cons_eqns_terms_temp['Parent_eqn'][j] + '_time' + str(i)
            
            if cons_eqns_terms_temp['Parent_stream'][j] != '-':
                mod11 = cons_eqns_terms_temp['Parent_stream'][j] + '_time' + str(i)
            else:
                mod11 = cons_eqns_terms_temp['Parent_stream'][j]
            temp_data = [mod9, mod10, mod11, cons_eqns_terms_temp['Coefficient'][j], cons_eqns_terms_temp['Coeff_v1_2'][j], cons_eqns_terms_temp['Coeff_v1_1'][j], cons_eqns_terms_temp['Coeff_v2_2'][j],
                         cons_eqns_terms_temp['Coeff_v2_1'][j], cons_eqns_terms_temp['Coeff_v1_v2'][j], cons_eqns_terms_temp['Coeff_cst'][j]]
            temp_df = pd.DataFrame(data = [temp_data], columns = cons_eqns_terms_headers)
            cons_eqns_terms = cons_eqns_terms.append(temp_df, ignore_index = True)
            
        ##Handling thermal_loss
        s8 = i * elem_thermal_loss_ts
        e8 = s8 + elem_thermal_loss_ts
        
        for j in range (int(s8), int(e8)):
            mod12 = thermal_loss_temp['Name'][j] + '_time' + str(i)
            temp_data = [mod12, thermal_loss_temp['Variable1'][j], thermal_loss_temp['Variable2'][j], thermal_loss_temp['Coeff_v1_2'][j], thermal_loss_temp['Coeff_v1_1'][j], thermal_loss_temp['Coeff_v2_2'][j], 
                         thermal_loss_temp['Coeff_v2_1'][j], thermal_loss_temp['Coeff_v1_v2'][j], thermal_loss_temp['Coeff_cst'][j]]
            temp_df = pd.DataFrame(data = [temp_data], columns = thermal_loss_headers)
            thermal_loss = thermal_loss.append(temp_df, ignore_index = True)
        

    return layerslist, utilitylist, storagelist, processlist, streams, cons_eqns, cons_eqns_terms, thermal_loss
