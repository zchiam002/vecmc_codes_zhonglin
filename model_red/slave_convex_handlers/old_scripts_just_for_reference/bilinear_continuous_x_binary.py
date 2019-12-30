
def bilinear_continuous_x_binary (streams, utilitylist, processlist):
    
    import pandas as pd 
    
    ##Since at this point in time, only the network parallel stream uses this feature, I will only focus on the network streams 
    
    ##Initializing a new DataFrame to hold the sorted values 
    streams_bilin_contbin_new = pd.DataFrame(columns = ['Parent', 'Parent_v1_name', 'Parent_v2_name', 'P_fmin_v1', 'P_fmax_v1', 'P_fmin_v2', 'P_fmax_v2', 'Type', 'Name', 'Layer', 
                                                        'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1', 'Stream_coeff_v1_v2', 'Stream_coeff_cst', 
                                                        'InOut', 'Temp_name'])
    
    ##Sorting out those affected layers
    dim_streams = streams.shape
    
    ##Additonal feature for adding in the names of parent variables into the output dataframe 
    combined_utilproc = pd.DataFrame(columns = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 'Coeff_v2_2', 'Coeff_v2_1',
                                                'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2',
                                                'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2',
                                                'Power_cst', 'Impact_v1_2', 'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    combined_utilproc = combined_utilproc.append(utilitylist, ignore_index=True)
    combined_utilproc = combined_utilproc.append(processlist, ignore_index = True)
    dim_combined_utilproc = combined_utilproc.shape
    
    ##There is an enforcement that the network parallel type of layer can only handle strictly linear terms 
    for i in range (0, dim_streams[0]):
        if streams['Type'][i] == 'network_parallel':
            temp_name = streams['Layer'][i] + '_' + streams['Parent'][i]

            for j in range (0, dim_combined_utilproc[0]):
                if combined_utilproc['Name'][j] == streams['Parent'][i]:
                    pn_v1 = combined_utilproc['Variable1'][j]
                    pn_v2 = combined_utilproc['Variable2'][j]
                    fmin_v1 = combined_utilproc['Fmin_v1'][j]
                    fmax_v1 = combined_utilproc['Fmax_v1'][j]
                    fmin_v2 = combined_utilproc['Fmin_v2'][j]
                    fmax_v2 = combined_utilproc['Fmax_v1'][j]
                    break
                
            temp_data = [streams['Parent'][i], pn_v1, pn_v2, fmin_v1, fmax_v1, fmin_v2, fmax_v2, streams['Type'][i], streams['Name'][i], streams['Layer'][i], streams['Stream_coeff_v1_2'][i], 
                         streams['Stream_coeff_v1_1'][i], streams['Stream_coeff_v2_2'][i], streams['Stream_coeff_v2_1'][i], streams['Stream_coeff_v1_v2'][i], streams['Stream_coeff_cst'][i], 
                         streams['InOut'][i],temp_name]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Parent', 'Parent_v1_name', 'Parent_v2_name', 'P_fmin_v1', 'P_fmax_v1', 'P_fmin_v2', 'P_fmax_v2', 'Type', 'Name', 'Layer', 
                                                                  'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1', 'Stream_coeff_v1_v2', 'Stream_coeff_cst', 
                                                                  'InOut', 'Temp_name'])
            streams_bilin_contbin_new = streams_bilin_contbin_new.append(temp_df, ignore_index=True)
            
    return streams_bilin_contbin_new