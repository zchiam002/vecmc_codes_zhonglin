##This function writes the parameters and master decision variables into a csv file for the slave to read

def prepare_slave_param_csv_vtest2 (var_converted, demand, weather_data, piecewise_steps):

    ##var_converted     --- essentially just the master decision variables 
    ##demand            --- demand data 
    ##weather_data      --- weather data 
    ##piecewise_steps   --- the piecewise linear steps
    
    mdv_slave_param = nwk_choice_3_mdv (var_converted, demand, weather_data, piecewise_steps)
        
    return mdv_slave_param

############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################
##Additional functions 

##A function to prepare the return values if the network choice is 3
def nwk_choice_3_mdv (var_converted, demand, weather_and_ct_coeff, piecewise_steps):

    ##var_converted     --- essentially just the master decision variables 
    ##demand            --- demand data 
    ##weather_data      --- weather data 
    ##piecewise_steps   --- the piecewise linear steps
    
    import pandas as pd
  
    ##Initiate dataframe to hold the written values 
    mdv_slave_param = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    ##############################################################################################################
    ##chiller_evap_flow_consol_4nc    
    input_value = {}
    input_value['Name'] = 'chiller_evap_flow_consol_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)              
    
    ##############################################################################################################    
    ##chiller_ret_4nc
    input_value = {}
    input_value['Name'] = 'chiller_ret_4nc_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################
    ##chiller1_evap_4nc    
    input_value = {}
    input_value['Name'] = 'chiller1_evap_4nc_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    input_value = {}
    input_value['Name'] = 'chiller1_evap_4nc_ctin' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)      
    
    input_value = {}
    input_value['Name'] = 'chiller1_evap_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'chiller1_evap_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################    
    ##chiller1_evap_nwk_4nc
    input_value = {}
    input_value['Name'] = 'chiller1_evap_nwk_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller1_evap_nwk_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)

    ##############################################################################################################
    ##chiller1_evap_pump_4nc        
    input_value = {}
    input_value['Name'] = 'chiller1_evap_pump_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    ##############################################################################################################    
    ##chiller2_evap_4nc
    input_value = {}
    input_value['Name'] = 'chiller2_evap_4nc_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller2_evap_4nc_ctin' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)      
    
    input_value = {}
    input_value['Name'] = 'chiller2_evap_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'chiller2_evap_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################    
    ##chiller2_evap_nwk_4nc
    input_value = {}
    input_value['Name'] = 'chiller2_evap_nwk_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller2_evap_nwk_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##############################################################################################################
    ##chiller2_evap_pump_4nc        
    input_value = {}
    input_value['Name'] = 'chiller2_evap_pump_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)        
    
    ##############################################################################################################    
    ##chiller3_evap_4nc
    input_value = {}
    input_value['Name'] = 'chiller3_evap_4nc_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller3_evap_4nc_ctin' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)      
    
    input_value = {}
    input_value['Name'] = 'chiller3_evap_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'chiller3_evap_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################    
    ##chiller3_evap_nwk_4nc
    input_value = {}
    input_value['Name'] = 'chiller3_evap_nwk_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'chiller3_evap_nwk_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##############################################################################################################
    ##chiller3_evap_pump_4nc        
    input_value = {}
    input_value['Name'] = 'chiller3_evap_pump_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##############################################################################################################
    ##cp_nwk_4nc    
    input_value = {}
    input_value['Name'] = 'cp_nwk_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    ##############################################################################################################
    ##dist_nwk_pump_4nc    
    input_value = {}
    input_value['Name'] = 'dist_nwk_pump_4nc_nwk_choice' 
    input_value['Value'] = 3
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)       
    
    input_value = {}
    input_value['Name'] = 'dist_nwk_pump_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################
    ##gv2_nwk_4nc   
    input_value = {}
    input_value['Name'] = 'gv2_nwk_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'gv2_nwk_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  

    ##############################################################################################################
    ##gv2_substation_4nc  
    input_value = {}
    input_value['Name'] = 'gv2_substation_4nc_demand' 
    input_value['Value'] = demand['ss_gv2_demand'][0]
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'gv2_substation_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    ##############################################################################################################
    ##hsb_nwk_4nc   
    input_value = {}
    input_value['Name'] = 'hsb_nwk_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'hsb_nwk_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  

    ##############################################################################################################
    ##hsb_substation_4nc  
    input_value = {}
    input_value['Name'] = 'hsb_substation_4nc_demand' 
    input_value['Value'] = demand['ss_hsb_demand'][0]
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'hsb_substation_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    ##############################################################################################################
    ##ice_nwk_4nc   
    input_value = {}
    input_value['Name'] = 'ice_nwk_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'ice_nwk_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
    
    ##############################################################################################################
    ##pfa_nwk_4nc   
    input_value = {}
    input_value['Name'] = 'pfa_nwk_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'pfa_nwk_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  

    ##############################################################################################################
    ##pfa_substation_4nc  
    input_value = {}
    input_value['Name'] = 'pfa_substation_4nc_demand' 
    input_value['Value'] = demand['ss_pfa_demand'][0]
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'pfa_substation_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################
    ##ser_nwk_4nc   
    input_value = {}
    input_value['Name'] = 'ser_nwk_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'ser_nwk_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  

    ##############################################################################################################
    ##ser_substation_4nc  
    input_value = {}
    input_value['Name'] = 'ser_substation_4nc_demand' 
    input_value['Value'] = demand['ss_ser_demand'][0]
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    input_value = {}
    input_value['Name'] = 'ser_substation_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    ##############################################################################################################
    ##tro_nwk_4nc   
    input_value = {}
    input_value['Name'] = 'tro_nwk_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    input_value = {}
    input_value['Name'] = 'tro_nwk_4nc_tenwkflow' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
         
    return mdv_slave_param
 
