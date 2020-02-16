##This function detects the parent units affected by the multi-time definition and add stream members to the following:
    ## identifying all the affected layers
    ## first setting all the direction as in
    ## copying the same information, setting the same variable as out in the next time-step, associating it with the layer in the next time-step
    
def modifying_storage_for_multi_time (storagelist, streams, time_steps, thermal_loss):
    
    import pandas as pd

    ##storagelist --- the list of all the storages    
    ##streams --- the list of all the streams
    ##time_steps --- the number of time_steps 
    ##thermal_loss --- the coefficients for thermal losses
    
    ##Identifying all affected layers
    dim_storagelist = storagelist.shape 
    storage_unit_names = []
    
    for i in range (0, dim_storagelist[0]):
        storage_unit_names.append(storagelist['Name'][i])
        
    ##Determining the length of thermal_loss list to search through
    dim_thermal_loss = thermal_loss.shape
        
    ##Fixing the streams to append the multi-time association 
    streams_column_labels = ['Parent', 'Type', 'Name', 'Layer', 'Stream_coeff_v1_2', 'Stream_coeff_v1_1', 'Stream_coeff_v2_2', 'Stream_coeff_v2_1', 'Stream_coeff_v1_v2', 'Stream_coeff_cst', 'InOut']
    streams_new = pd.DataFrame(columns = streams_column_labels)
    
    dim_streams = streams.shape
    
    for i in range (0, dim_streams[0]):
        
        if streams['Parent'][i] in storage_unit_names:
            
            ##For i = time_steps case, only 'in' case
            check_last = 'time' + str(time_steps - 1)
            
            ##Modifying the stream name 
            curr_name_wo_ts = streams['Name'][i][0 : (len(streams['Name'][i]) - 5)]           ##5 is for timeX addition to the name
            curr_name_ts = streams['Name'][i][(len(streams['Name'][i]) - 5):]
            curr_ts = streams['Name'][i][(len(streams['Name'][i]) - 1)]
            next_ts = int(curr_ts) + 1
    
            if check_last in streams['Parent'][i]:
                
                input_name1 = curr_name_wo_ts + 'in_' + curr_name_ts
                temp_data1 = [streams['Parent'][i], streams['Type'][i], input_name1, streams['Layer'][i], streams['Stream_coeff_v1_2'][i], streams['Stream_coeff_v1_1'][i], streams['Stream_coeff_v2_2'][i], 
                              streams['Stream_coeff_v2_1'][i], streams['Stream_coeff_v1_v2'][i], streams['Stream_coeff_cst'][i], 'in']
                temp_df1 = pd.DataFrame(data = [temp_data1], columns = streams_column_labels)
                streams_new = streams_new.append(temp_df1, ignore_index = True)

            else:
                ##The charging case
                input_name1 = curr_name_wo_ts + 'in_' + curr_name_ts                
                temp_data1 = [streams['Parent'][i], streams['Type'][i], input_name1, streams['Layer'][i], streams['Stream_coeff_v1_2'][i], streams['Stream_coeff_v1_1'][i], streams['Stream_coeff_v2_2'][i], 
                              streams['Stream_coeff_v2_1'][i], streams['Stream_coeff_v1_v2'][i], streams['Stream_coeff_cst'][i], 'in']
                temp_df1 = pd.DataFrame(data = [temp_data1], columns = streams_column_labels)
                streams_new = streams_new.append(temp_df1, ignore_index = True)
                
                ##The discharging case
                input_name2 = curr_name_wo_ts + 'out_time' + str(next_ts)
                layer_name_wo_ts = streams['Layer'][i][0 : (len(streams['Layer'][i]) - 5)]
                next_layer_name = layer_name_wo_ts + 'time' + str(int(streams['Layer'][i][len(streams['Layer'][i]) - 1]) + 1)
                
                ##Determining which set of storage coefficients to search for 
                req_index = '-'
                for j in range (0, dim_thermal_loss[0]):
                    if thermal_loss['Name'][j] == streams['Parent'][i]:
                        req_index = j
                        break
                
                ##Modifying stream coefficients 
                s_c_v1_2 = streams['Stream_coeff_v1_2'][i] * thermal_loss['Coeff_v1_2'][req_index]
                s_c_v1_1 = streams['Stream_coeff_v1_1'][i] * thermal_loss['Coeff_v1_1'][req_index]
                s_c_v2_2 = streams['Stream_coeff_v2_2'][i] * thermal_loss['Coeff_v2_2'][req_index]
                s_c_v2_1 = streams['Stream_coeff_v2_1'][i] * thermal_loss['Coeff_v2_1'][req_index]
                s_c_v1_v2 = streams['Stream_coeff_v1_v2'][i] * thermal_loss['Coeff_v1_v2'][req_index]
                s_c_cst = streams['Stream_coeff_cst'][i] * thermal_loss['Coeff_cst'][req_index]
                
                temp_data2 = [streams['Parent'][i], streams['Type'][i], input_name2, next_layer_name, s_c_v1_2, s_c_v1_1, s_c_v2_2, s_c_v2_1, s_c_v1_v2, s_c_cst, 'out']
                temp_df2 = pd.DataFrame(data = [temp_data2], columns = streams_column_labels)
                streams_new = streams_new.append(temp_df2, ignore_index = True)                
            
        ##Not affected case
        else:
            temp_data1 = [streams['Parent'][i], streams['Type'][i], streams['Name'][i], streams['Layer'][i], streams['Stream_coeff_v1_2'][i], streams['Stream_coeff_v1_1'][i], streams['Stream_coeff_v2_2'][i], 
                          streams['Stream_coeff_v2_1'][i], streams['Stream_coeff_v1_v2'][i], streams['Stream_coeff_cst'][i], streams['InOut'][i]]
            temp_df1 = pd.DataFrame(data = [temp_data1], columns = streams_column_labels)
            streams_new = streams_new.append(temp_df1, ignore_index = True)            
        
    return streams_new