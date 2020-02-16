##This function writes the parameters and master decision variables into a csv file for the slave to read

def prepare_slave_param_csv_vtest2 (var_converted, demand, weather_and_ct_coeff, piecewise_steps):
    
    mdv_slave_param = prep_mdv_chiller_only_optimization (var_converted, demand, weather_and_ct_coeff, piecewise_steps)
        
    return mdv_slave_param

############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################
##Additional functions 

##A function to prepare the return values if the network choice is 3
def prep_mdv_chiller_only_optimization (var_converted, demand, weather_and_ct_coeff, piecewise_steps):

    import pandas as pd
    
    ##Initiate dataframe to hold the written values 
    mdv_slave_param = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    ##############################################################################################################
    ##chiller_evap_flow_consol 
    input_value = {}
    input_value['Name'] = 'chiller_evap_flow_consol_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)              
    
    ##############################################################################################################    
    ##chiller_ret
    input_value = {}
    input_value['Name'] = 'chiller_ret_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################
    ##chiller1_evap
    input_value = {}
    input_value['Name'] = 'chiller1_evap_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    input_value = {}
    input_value['Name'] = 'chiller1_evap_ctin' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)      
    
    input_value = {}
    input_value['Name'] = 'chiller1_evap_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'chiller1_evap_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################    
    ##chiller1_evap_nwk
    input_value = {}
    input_value['Name'] = 'chiller1_evap_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller1_evap_nwk_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)

    ##############################################################################################################
    ##chiller1_evap_pump       
    input_value = {}
    input_value['Name'] = 'chiller1_evap_pump_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    ##############################################################################################################    
    ##chiller2_evap
    input_value = {}
    input_value['Name'] = 'chiller2_evap_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller2_evap_ctin' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)      
    
    input_value = {}
    input_value['Name'] = 'chiller2_evap_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'chiller2_evap_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################    
    ##chiller2_evap_nwk
    input_value = {}
    input_value['Name'] = 'chiller2_evap_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller2_evap_nwk_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##############################################################################################################
    ##chiller2_evap_pump        
    input_value = {}
    input_value['Name'] = 'chiller2_evap_pump_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)        
    
    ##############################################################################################################    
    ##chiller3_evap
    input_value = {}
    input_value['Name'] = 'chiller3_evap_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller3_evap_ctin' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)      
    
    input_value = {}
    input_value['Name'] = 'chiller3_evap_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'chiller3_evap_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################    
    ##chiller3_evap_nwk
    input_value = {}
    input_value['Name'] = 'chiller3_evap_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller3_evap_nwk_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##############################################################################################################
    ##chiller3_evap_pump   
    input_value = {}
    input_value['Name'] = 'chiller3_evap_pump_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##############################################################################################################
    ##cp_nwk
    input_value = {}
    input_value['Name'] = 'cp_nwk_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    ##############################################################################################################
    ##dist_nwk_pump   
    input_value = {}
    input_value['Name'] = 'dist_nwk_pump_nwk_choice' 
    input_value['Value'] = var_converted[3]
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)       
    
    input_value = {}
    input_value['Name'] = 'dist_nwk_pump_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################
    ##gv2_nwk   
    input_value = {}
    input_value['Name'] = 'gv2_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'gv2_nwk_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  

    ##############################################################################################################
    ##gv2_substation  
    input_value = {}
    input_value['Name'] = 'gv2_substation_demand' 
    input_value['Value'] = demand['ss_gv2_demand'][0]
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'gv2_substation_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    ##############################################################################################################
    ##hsb_nwk 
    input_value = {}
    input_value['Name'] = 'hsb_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'hsb_nwk_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  

    ##############################################################################################################
    ##hsb_substation  
    input_value = {}
    input_value['Name'] = 'hsb_substation_demand' 
    input_value['Value'] = demand['ss_hsb_demand'][0]
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'hsb_substation_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    ##############################################################################################################
    ##ice_nwk
    input_value = {}
    input_value['Name'] = 'ice_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'ice_nwk_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
    
    ##############################################################################################################
    ##pfa_nwk  
    input_value = {}
    input_value['Name'] = 'pfa_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'pfa_nwk_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  

    ##############################################################################################################
    ##pfa_substation  
    input_value = {}
    input_value['Name'] = 'pfa_substation_demand' 
    input_value['Value'] = demand['ss_pfa_demand'][0]
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'pfa_substation_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################
    ##ser_nwk  
    input_value = {}
    input_value['Name'] = 'ser_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'ser_nwk_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  

    ##############################################################################################################
    ##ser_substation  
    input_value = {}
    input_value['Name'] = 'ser_substation_demand' 
    input_value['Value'] = demand['ss_pfa_demand'][0]
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'ser_substation_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    ##############################################################################################################
    ##tro_nwk  
    input_value = {}
    input_value['Name'] = 'tro_nwk_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'tro_nwk_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    return mdv_slave_param