
def sorting_linear_and_bilinear_terms (layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms):
    
    import pandas as pd
    
    ##utilitylist data 
    objective_function_utility_bilinear = pd.DataFrame(columns = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 
                                                                  'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 
                                                                  'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2', 'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 
                                                                  'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2', 'Power_cst', 'Impact_v1_2', 
                                                                  'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    dual_variable_constraint_utility_bilinear = pd.DataFrame(columns = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 
                                                                        'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 
                                                                        'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2', 'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 
                                                                        'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2', 'Power_cst', 'Impact_v1_2', 
                                                                        'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    
    objective_function_utility_linear = pd.DataFrame(columns = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 
                                                                'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 
                                                                'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2', 'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 
                                                                'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2', 'Power_cst', 'Impact_v1_2', 
                                                                'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])    
    
    ##processlist data 
    objective_function_process_bilinear = pd.DataFrame(columns = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 
                                                                  'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 
                                                                  'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2', 'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 
                                                                  'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2', 'Power_cst', 'Impact_v1_2', 
                                                                  'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    dual_variable_constraint_process_bilinear = pd.DataFrame(columns = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 
                                                                        'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 
                                                                        'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2', 'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 
                                                                        'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2', 'Power_cst', 'Impact_v1_2', 
                                                                        'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    
    objective_function_process_linear = pd.DataFrame(columns = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 
                                                                'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 
                                                                'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2', 'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 
                                                                'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2', 'Power_cst', 'Impact_v1_2', 
                                                                'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])  
    
    ##streams data 
    streams_bilinear = pd.DataFrame(columns = ['Parent', 'Parent_v1_name', 'Parent_v2_name', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 
                                               'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1', 'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    streams_linear = pd.DataFrame(columns = ['Parent', 'Parent_v1_name', 'Parent_v2_name', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                               'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    
    ##cons_eqn_terms_data 
    
    cons_eqn_terms_bilinear = pd.DataFrame(columns = ['Parent_unit', 'Parent_v1_name', 'Parent_v2_name', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 
                                                      'Coeff_v2_1', 'Coeff_v1v2', 'Coeff_cst'])
    
    cons_eqn_terms_linear = pd.DataFrame(columns = ['Parent_unit', 'Parent_v1_name', 'Parent_v2_name', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2', 'Coeff_cst'])

    ##The nature of the bilinear terms have to specified manually 
    ##The functions below sorts the variables into linear and bilinear ones. The bilinear ones will be later processed using relaxation techniques 
        
    ##Scanning through the utility list 
    dim_utilitylist = utilitylist.shape
    
    for i in range (0, dim_utilitylist[0]):
        ##Gathering all the bilinear terms in the objective function 
        if (utilitylist['Cost_v1_v2'][i] != 0) or (utilitylist['Cinv_v1_v2'][i] != 0) or (utilitylist['Power_v1_v2'][i] != 0) or (utilitylist['Impact_v1_v2'][i] != 0):
            
            temp_ul_data = [utilitylist['Name'][i], utilitylist['Variable1'][i], utilitylist['Variable2'][i], utilitylist['Fmin_v1'][i], utilitylist['Fmax_v1'][i], utilitylist['Fmin_v2'][i], utilitylist['Fmax_v2'][i], utilitylist['Coeff_v1_2'][i], 
                            utilitylist['Coeff_v1_1'][i], utilitylist['Coeff_v2_2'][i], utilitylist['Coeff_v2_1'][i], utilitylist['Coeff_v1_v2'][i], utilitylist['Coeff_cst'][i], utilitylist['Fmin'][i], utilitylist['Fmax'][i], utilitylist['Cost_v1_2'][i], 
                            utilitylist['Cost_v1_1'][i], utilitylist['Cost_v2_2'][i], utilitylist['Cost_v2_1'][i], utilitylist['Cost_v1_v2'][i], utilitylist['Cost_cst'][i], utilitylist['Cinv_v1_2'][i], utilitylist['Cinv_v1_1'][i], utilitylist['Cinv_v2_2'][i], 
                            utilitylist['Cinv_v2_1'][i], utilitylist['Cinv_v1_v2'][i], utilitylist['Cinv_cst'][i], utilitylist['Power_v1_2'][i], utilitylist['Power_v1_1'][i], utilitylist['Power_v2_2'][i], utilitylist['Power_v2_1'][i], 
                            utilitylist['Power_v1_v2'][i], utilitylist['Power_cst'][i], utilitylist['Impact_v1_2'][i], utilitylist['Impact_v1_1'][i], utilitylist['Impact_v2_2'][i], utilitylist['Impact_v2_1'][i], utilitylist['Impact_v1_v2'][i], 
                            utilitylist['Impact_cst'][i]]   
            temp_ul_df = pd.DataFrame(data = [temp_ul_data], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
            objective_function_utility_bilinear = objective_function_utility_bilinear.append(temp_ul_df, ignore_index=True)
        
        ##Gathering all the linear terms in the objective function 
        else:
            
            temp_ul_data = [utilitylist['Name'][i], utilitylist['Variable1'][i], utilitylist['Variable2'][i], utilitylist['Fmin_v1'][i], utilitylist['Fmax_v1'][i], utilitylist['Fmin_v2'][i], utilitylist['Fmax_v2'][i], utilitylist['Coeff_v1_2'][i], 
                            utilitylist['Coeff_v1_1'][i], utilitylist['Coeff_v2_2'][i], utilitylist['Coeff_v2_1'][i], utilitylist['Coeff_v1_v2'][i], utilitylist['Coeff_cst'][i], utilitylist['Fmin'][i], utilitylist['Fmax'][i], utilitylist['Cost_v1_2'][i], 
                            utilitylist['Cost_v1_1'][i], utilitylist['Cost_v2_2'][i], utilitylist['Cost_v2_1'][i], utilitylist['Cost_v1_v2'][i], utilitylist['Cost_cst'][i], utilitylist['Cinv_v1_2'][i], utilitylist['Cinv_v1_1'][i], utilitylist['Cinv_v2_2'][i], 
                            utilitylist['Cinv_v2_1'][i], utilitylist['Cinv_v1_v2'][i], utilitylist['Cinv_cst'][i], utilitylist['Power_v1_2'][i], utilitylist['Power_v1_1'][i], utilitylist['Power_v2_2'][i], utilitylist['Power_v2_1'][i], 
                            utilitylist['Power_v1_v2'][i], utilitylist['Power_cst'][i], utilitylist['Impact_v1_2'][i], utilitylist['Impact_v1_1'][i], utilitylist['Impact_v2_2'][i], utilitylist['Impact_v2_1'][i], utilitylist['Impact_v1_v2'][i], 
                            utilitylist['Impact_cst'][i]]   
            temp_ul_df = pd.DataFrame(data = [temp_ul_data], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
            objective_function_utility_linear = objective_function_utility_linear.append(temp_ul_df, ignore_index=True)
            
        ##Gathering all the bilinear terms in the relationship between the 2 variables of the each utility 
        if (utilitylist['Coeff_v1_v2'][i] != 0):
            
            temp_ul_data = [utilitylist['Name'][i], utilitylist['Variable1'][i], utilitylist['Variable2'][i], utilitylist['Fmin_v1'][i], utilitylist['Fmax_v1'][i], utilitylist['Fmin_v2'][i], utilitylist['Fmax_v2'][i], utilitylist['Coeff_v1_2'][i], 
                            utilitylist['Coeff_v1_1'][i], utilitylist['Coeff_v2_2'][i], utilitylist['Coeff_v2_1'][i], utilitylist['Coeff_v1_v2'][i], utilitylist['Coeff_cst'][i], utilitylist['Fmin'][i], utilitylist['Fmax'][i], utilitylist['Cost_v1_2'][i], 
                            utilitylist['Cost_v1_1'][i], utilitylist['Cost_v2_2'][i], utilitylist['Cost_v2_1'][i], utilitylist['Cost_v1_v2'][i], utilitylist['Cost_cst'][i], utilitylist['Cinv_v1_2'][i], utilitylist['Cinv_v1_1'][i], utilitylist['Cinv_v2_2'][i], 
                            utilitylist['Cinv_v2_1'][i], utilitylist['Cinv_v1_v2'][i], utilitylist['Cinv_cst'][i], utilitylist['Power_v1_2'][i], utilitylist['Power_v1_1'][i], utilitylist['Power_v2_2'][i], utilitylist['Power_v2_1'][i], 
                            utilitylist['Power_v1_v2'][i], utilitylist['Power_cst'][i], utilitylist['Impact_v1_2'][i], utilitylist['Impact_v1_1'][i], utilitylist['Impact_v2_2'][i], utilitylist['Impact_v2_1'][i], utilitylist['Impact_v1_v2'][i], 
                            utilitylist['Impact_cst'][i]]   
            temp_ul_df = pd.DataFrame(data = [temp_ul_data], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
            dual_variable_constraint_utility_bilinear = dual_variable_constraint_utility_bilinear.append(temp_ul_df, ignore_index=True)
    
    
    ##Scanning through the process list
    dim_processlist = processlist.shape
    
    for i in range (0, dim_processlist[0]):
        ##Gathering all the bilinear terms in the objective function 
        if (processlist['Cost_v1_v2'][i] != 0) or (processlist['Cinv_v1_v2'][i] != 0) or (processlist['Power_v1_v2'][i] != 0) or (processlist['Impact_v1_v2'][i] != 0):
            temp_pr_data = [processlist['Name'][i], processlist['Variable1'][i], processlist['Variable2'][i], processlist['Fmin_v1'][i], processlist['Fmax_v1'][i], processlist['Fmin_v2'][i], processlist['Fmax_v2'][i], processlist['Coeff_v1_2'][i], 
                            processlist['Coeff_v1_1'][i], processlist['Coeff_v2_2'][i], processlist['Coeff_v2_1'][i], processlist['Coeff_v1_v2'][i], processlist['Coeff_cst'][i], processlist['Fmin'][i], processlist['Fmax'][i], processlist['Cost_v1_2'][i], 
                            processlist['Cost_v1_1'][i], processlist['Cost_v2_2'][i], processlist['Cost_v2_1'][i], processlist['Cost_v1_v2'][i], processlist['Cost_cst'][i], processlist['Cinv_v1_2'][i], processlist['Cinv_v1_1'][i], processlist['Cinv_v2_2'][i], 
                            processlist['Cinv_v2_1'][i], processlist['Cinv_v1_v2'][i], processlist['Cinv_cst'][i], processlist['Power_v1_2'][i], processlist['Power_v1_1'][i], processlist['Power_v2_2'][i], processlist['Power_v2_1'][i], 
                            processlist['Power_v1_v2'][i], processlist['Power_cst'][i], processlist['Impact_v1_2'][i], processlist['Impact_v1_1'][i], processlist['Impact_v2_2'][i], processlist['Impact_v2_1'][i], processlist['Impact_v1_v2'][i], 
                            processlist['Impact_cst'][i]]   
            temp_pr_df = pd.DataFrame(data = [temp_pr_data], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
            objective_function_process_bilinear = objective_function_process_bilinear.append(temp_pr_df, ignore_index=True)
        
        ##Gathering all the linear terms in the objective function 
        else:
            
            temp_pr_data = [processlist['Name'][i], processlist['Variable1'][i], processlist['Variable2'][i], processlist['Fmin_v1'][i], processlist['Fmax_v1'][i], processlist['Fmin_v2'][i], processlist['Fmax_v2'][i], processlist['Coeff_v1_2'][i], 
                            processlist['Coeff_v1_1'][i], processlist['Coeff_v2_2'][i], processlist['Coeff_v2_1'][i], processlist['Coeff_v1_v2'][i], processlist['Coeff_cst'][i], processlist['Fmin'][i], processlist['Fmax'][i], processlist['Cost_v1_2'][i], 
                            processlist['Cost_v1_1'][i], processlist['Cost_v2_2'][i], processlist['Cost_v2_1'][i], processlist['Cost_v1_v2'][i], processlist['Cost_cst'][i], processlist['Cinv_v1_2'][i], processlist['Cinv_v1_1'][i], processlist['Cinv_v2_2'][i], 
                            processlist['Cinv_v2_1'][i], processlist['Cinv_v1_v2'][i], processlist['Cinv_cst'][i], processlist['Power_v1_2'][i], processlist['Power_v1_1'][i], processlist['Power_v2_2'][i], processlist['Power_v2_1'][i], 
                            processlist['Power_v1_v2'][i], processlist['Power_cst'][i], processlist['Impact_v1_2'][i], processlist['Impact_v1_1'][i], processlist['Impact_v2_2'][i], processlist['Impact_v2_1'][i], processlist['Impact_v1_v2'][i], 
                            processlist['Impact_cst'][i]]   
            temp_pr_df = pd.DataFrame(data = [temp_pr_data], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
            objective_function_process_linear = objective_function_process_linear.append(temp_pr_df, ignore_index=True)  

        ##Gathering all the bilinear terms in the relationship between the 2 variables of each process
        if (processlist['Coeff_v1_v2'][i] != 0):
            
            temp_pr_data = [processlist['Name'][i], processlist['Variable1'][i], processlist['Variable2'][i], processlist['Fmin_v1'][i], processlist['Fmax_v1'][i], processlist['Fmin_v2'][i], processlist['Fmax_v2'][i], processlist['Coeff_v1_2'][i], 
                            processlist['Coeff_v1_1'][i], processlist['Coeff_v2_2'][i], processlist['Coeff_v2_1'][i], processlist['Coeff_v1_v2'][i], processlist['Coeff_cst'][i], processlist['Fmin'][i], processlist['Fmax'][i], processlist['Cost_v1_2'][i], 
                            processlist['Cost_v1_1'][i], processlist['Cost_v2_2'][i], processlist['Cost_v2_1'][i], processlist['Cost_v1_v2'][i], processlist['Cost_cst'][i], processlist['Cinv_v1_2'][i], processlist['Cinv_v1_1'][i], processlist['Cinv_v2_2'][i], 
                            processlist['Cinv_v2_1'][i], processlist['Cinv_v1_v2'][i], processlist['Cinv_cst'][i], processlist['Power_v1_2'][i], processlist['Power_v1_1'][i], processlist['Power_v2_2'][i], processlist['Power_v2_1'][i], 
                            processlist['Power_v1_v2'][i], processlist['Power_cst'][i], processlist['Impact_v1_2'][i], processlist['Impact_v1_1'][i], processlist['Impact_v2_2'][i], processlist['Impact_v2_1'][i], processlist['Impact_v1_v2'][i], 
                            processlist['Impact_cst'][i]]   
            temp_pr_df = pd.DataFrame(data = [temp_pr_data], columns=['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                                      'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                                      'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                                      'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
            dual_variable_constraint_process_bilinear = dual_variable_constraint_process_bilinear.append(temp_pr_df, ignore_index=True)            
        
    
    ##Scanning through the streams list
    dim_streams = streams.shape
    
    ##Modifying the streams data to add in information about the names of variables 1 and 2 according to the corresponding parent unit
    streams_new_data = pd.DataFrame(columns = ['Parent', 'Parent_v1_name', 'Parent_v2_name', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                               'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
    ##Combining the utility and process list 
    combined_list = pd.DataFrame(columns = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 
                                            'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2', 'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2', 'Power_cst', 'Impact_v1_2', 
                                            'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    combined_list = combined_list.append(utilitylist, ignore_index=True)
    combined_list = combined_list.append(processlist, ignore_index=True)
    dim_combined_list = combined_list.shape
    
    for i in range (0, dim_streams[0]):
        for j in range (0, dim_combined_list[0]):
            if combined_list['Name'][j] == streams['Parent'][i]:
                streams_new_temp_data = [streams['Parent'][i], combined_list['Variable1'][j], combined_list['Variable2'][j], combined_list['Fmin_v1'][j], combined_list['Fmax_v1'][j], combined_list['Fmin_v2'][j], combined_list['Fmax_v2'][j], streams['Type'][i], 
                                         streams['Name'][i], streams['Layer'][i], streams['Stream_coeff_v1_2'][i], streams['Stream_coeff_v1_1'][i], streams['Stream_coeff_v2_2'][i], streams['Stream_coeff_v2_1'][i], streams['Stream_coeff_v1_v2'][i], streams['Stream_coeff_cst'][i], 
                                         streams['InOut'][i]]
                streams_new_temp_df = pd.DataFrame(data = [streams_new_temp_data], columns = ['Parent', 'Parent_v1_name', 'Parent_v2_name', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 
                                                                                              'Stream_coeff_v2_1', 'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
                streams_new_data = streams_new_data.append(streams_new_temp_df, ignore_index=True)
    
    for i in range (0, dim_streams[0]):
        ##Gathering all the bilinear terms in the stream constraint
        if (streams_new_data['Stream_coeff_v1_v2'][i] != 0):
            temp_st_data = [streams_new_data['Parent'][i], streams_new_data['Parent_v1_name'][i], streams_new_data['Parent_v2_name'][i], streams_new_data['Fmin_v1'][i], streams_new_data['Fmax_v1'][i], streams_new_data['Fmin_v2'][i], streams_new_data['Fmax_v2'][i], streams_new_data['Type'][i], 
                            streams_new_data['Name'][i], streams_new_data['Layer'][i], streams_new_data['Stream_coeff_v1_2'][i], streams_new_data['Stream_coeff_v1_1'][i], streams_new_data['Stream_coeff_v2_2'][i], streams_new_data['Stream_coeff_v2_1'][i], 
                            streams_new_data['Stream_coeff_v1_v2'][i], streams_new_data['Stream_coeff_cst'][i], streams_new_data['InOut'][i]]
            temp_st_df = pd.DataFrame(data = [temp_st_data], columns = ['Parent', 'Parent_v1_name', 'Parent_v2_name', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                                        'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
            streams_bilinear = streams_bilinear.append(temp_st_df, ignore_index=True)
            
        ##Gathering all the linear terms in the stream constraints             
        else:
            temp_st_data = [streams_new_data['Parent'][i], streams_new_data['Parent_v1_name'][i], streams_new_data['Parent_v2_name'][i], streams_new_data['Type'][i], streams_new_data['Name'][i], streams_new_data['Layer'][i], streams_new_data['Stream_coeff_v1_2'][i], 
                            streams_new_data['Stream_coeff_v1_1'][i], streams_new_data['Stream_coeff_v2_2'][i], streams_new_data['Stream_coeff_v2_1'][i], streams_new_data['Stream_coeff_v1_v2'][i], streams_new_data['Stream_coeff_cst'][i], streams_new_data['InOut'][i]]
            temp_st_df = pd.DataFrame(data = [temp_st_data], columns = ['Parent', 'Parent_v1_name', 'Parent_v2_name', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1',
                                                                        'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut'])
            streams_linear = streams_linear.append(temp_st_df, ignore_index=True)
    
    ##Scanning through the cons_eqns_terms list
    dim_con_eqns_terms = cons_eqns_terms.shape
    
    ##Modifying the cons_eqns_terms data to add in information about the names of variables 1 and 2 according to the corresponding parent unit 
    cons_eqns_terms_new_data = pd.DataFrame(columns = ['Parent_unit', 'Parent_v1_name', 'Parent_v2_name', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2', 'Coeff_cst'])
    
    for i in range (0, dim_con_eqns_terms[0]):
        for j in range (0, dim_combined_list[0]):
            if combined_list['Name'][j] == cons_eqns_terms['Parent_unit'][i]:
                cons_eqns_terms_new_temp_data = [cons_eqns_terms['Parent_unit'][i], combined_list['Variable1'][j], combined_list['Variable2'][j], combined_list['Fmin_v1'][j], combined_list['Fmax_v1'][j], combined_list['Fmin_v2'][j], combined_list['Fmax_v2'][j], cons_eqns_terms['Parent_eqn'][i], 
                                                 cons_eqns_terms['Parent_stream'][i], cons_eqns_terms['Coefficient'][i], cons_eqns_terms['Coeff_v1_2'][i], cons_eqns_terms['Coeff_v1_1'][i], cons_eqns_terms['Coeff_v2_2'][i], cons_eqns_terms['Coeff_v2_1'][i], cons_eqns_terms['Coeff_v1v2'][i], 
                                                 cons_eqns_terms['Coeff_cst'][i]]
                cons_eqns_terms_new_temp_df = pd.DataFrame(data = [cons_eqns_terms_new_temp_data], columns = ['Parent_unit', 'Parent_v1_name', 'Parent_v2_name', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 
                                                                                                              'Coeff_v2_1', 'Coeff_v1v2', 'Coeff_cst'])
                
                cons_eqns_terms_new_data = cons_eqns_terms_new_data.append(cons_eqns_terms_new_temp_df, ignore_index=True)
    
                
    for i in range (0, dim_con_eqns_terms[0]):
        ##Gathering all the bilinear terms in the cons_eqns_terms list
        if (cons_eqns_terms_new_data['Coeff_v1v2'][i] != 0):
            temp_cet_data = [cons_eqns_terms_new_data['Parent_unit'][i], cons_eqns_terms_new_data['Parent_v1_name'][i], cons_eqns_terms_new_data['Parent_v2_name'][i], cons_eqns_terms_new_data['Fmin_v1'][i], cons_eqns_terms_new_data['Fmax_v1'][i], cons_eqns_terms_new_data['Fmin_v2'][i], 
                             cons_eqns_terms_new_data['Fmax_v2'][i], cons_eqns_terms_new_data['Parent_eqn'][i], cons_eqns_terms_new_data['Parent_stream'][i], cons_eqns_terms_new_data['Coefficient'][i], cons_eqns_terms_new_data['Coeff_v1_2'][i], cons_eqns_terms_new_data['Coeff_v1_1'][i], 
                             cons_eqns_terms_new_data['Coeff_v2_2'][i], cons_eqns_terms_new_data['Coeff_v2_1'][i], cons_eqns_terms_new_data['Coeff_v1v2'][i], cons_eqns_terms_new_data['Coeff_cst'][i]]
            temp_cet_df = pd.DataFrame(data = [temp_cet_data], columns = ['Parent_unit', 'Parent_v1_name', 'Parent_v2_name', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2', 'Coeff_cst'])
            
            cons_eqn_terms_bilinear = cons_eqn_terms_bilinear.append(temp_cet_df, ignore_index=True)
        else:
        ##Gathering all the linear terms cons_eqns_terms 
            temp_cet_data = [cons_eqns_terms_new_data['Parent_unit'][i], cons_eqns_terms_new_data['Parent_v1_name'][i], cons_eqns_terms_new_data['Parent_v2_name'][i], cons_eqns_terms_new_data['Parent_eqn'][i], cons_eqns_terms_new_data['Parent_stream'][i], cons_eqns_terms_new_data['Coefficient'][i], 
                             cons_eqns_terms_new_data['Coeff_v1_2'][i], cons_eqns_terms_new_data['Coeff_v1_1'][i], cons_eqns_terms_new_data['Coeff_v2_2'][i], cons_eqns_terms_new_data['Coeff_v2_1'][i], cons_eqns_terms_new_data['Coeff_v1v2'][i], cons_eqns_terms_new_data['Coeff_cst'][i]]
            temp_cet_df = pd.DataFrame(data = [temp_cet_data], columns = ['Parent_unit', 'Parent_v1_name', 'Parent_v2_name', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1v2', 'Coeff_cst'])
            
            cons_eqn_terms_linear = cons_eqn_terms_linear.append(temp_cet_df, ignore_index=True)
            
    ##Initiate a dictionary to hold the values 
    sorted_terms = {}
    sorted_terms['objective_function_utility_bilinear'] = objective_function_utility_bilinear
    sorted_terms['dual_variable_constraint_utility_bilinear'] = dual_variable_constraint_utility_bilinear
    sorted_terms['objective_function_utility_linear'] = objective_function_utility_linear
    sorted_terms['objective_function_process_bilinear'] = objective_function_process_bilinear
    sorted_terms['dual_variable_constraint_process_bilinear'] = dual_variable_constraint_process_bilinear
    sorted_terms['objective_function_process_linear'] = objective_function_process_linear
    sorted_terms['streams_bilinear'] = streams_bilinear
    sorted_terms['streams_linear'] = streams_linear
    sorted_terms['cons_eqn_terms_bilinear'] = cons_eqn_terms_bilinear
    sorted_terms['cons_eqn_terms_linear'] = cons_eqn_terms_linear
    
    return sorted_terms

