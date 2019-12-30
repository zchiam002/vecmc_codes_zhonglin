##This function writes the parameters and master decision variables into a csv file for the slave to read

def prepare_slave_param_csv_vtest2 (var_converted, demand, piecewise_steps):

    import pandas as pd
    
    ##Initiate dataframe to hold the written values 
    mdv_slave_param = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    ##1
    input_value = {}
    input_value['Name'] = 'chiller1_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)

    ##2
    input_value = {}
    input_value['Name'] = 'chiller1_ctin' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##3
    input_value = {}
    input_value['Name'] = 'chiller1_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit']) 
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  

    ##4
    input_value = {}
    input_value['Name'] = 'chiller1_piecewise_steps'
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##5
    input_value = {}
    input_value['Name'] = 'chiller2_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)

    ##6
    input_value = {}
    input_value['Name'] = 'chiller2_ctin' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##7
    input_value = {}
    input_value['Name'] = 'chiller2_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit']) 
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    

    ##8
    input_value = {}
    input_value['Name'] = 'chiller2_piecewise_steps'
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)   

    ##9
    input_value = {}
    input_value['Name'] = 'chiller3_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)

    ##10
    input_value = {}
    input_value['Name'] = 'chiller3_ctin' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##11
    input_value = {}
    input_value['Name'] = 'chiller3_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit']) 
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  

    ##12
    input_value = {}
    input_value['Name'] = 'chiller3_piecewise_steps'
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
    
    ##13
    input_value = {}
    input_value['Name'] = 'combined_substation_demand' 
    input_value['Value'] = demand['ss_gv2_demand'][0] + demand['ss_hsb_demand'][0] + demand['ss_pfa_demand'][0] + demand['ss_ser_demand'][0] + demand['ss_fir_demand'][0]
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##14
    input_value = {}
    input_value['Name'] = 'combined_substation_totalflownwk' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##15
    input_value = {}
    input_value['Name'] = 'chiller_ret_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    ##16
    input_value = {}
    input_value['Name'] = 'chiller_evap_flow_consol_tf' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    

    ##17
    input_value = {}
    input_value['Name'] = 'cp_network_nwk_choice_tf' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)       

    
    return mdv_slave_param
    
    