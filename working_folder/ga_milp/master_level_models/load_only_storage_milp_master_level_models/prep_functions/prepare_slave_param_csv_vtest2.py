##This function writes the parameters and master decision variables into a csv file for the slave to read

def prepare_slave_param_csv_vtest2 (var_converted, demand, weather_and_ct_coeff, piecewise_steps):
    
    ##Determine the network choice 
    nwk_choice = var_converted[4]
    
    if int(nwk_choice) == 3:
        mdv_slave_param = nwk_choice_3_mdv (var_converted, demand, weather_and_ct_coeff, piecewise_steps)
        
    return mdv_slave_param

############################################################################################################################################################################
############################################################################################################################################################################
############################################################################################################################################################################
##Additional functions 

##A function to prepare the return values if the network choice is 3
def nwk_choice_3_mdv (var_converted, demand, weather_and_ct_coeff, piecewise_steps):
    
    import numpy as np
    import pandas as pd

    ##Determining the total condenser network flowrate 
    total_cond_flow = determine_total_cond_flow (int(var_converted[3]))
    
    ##Determining the weather and appropriate cooling tower coefficients 
    #ct_coeff_weather_selected = determine_ct_coeff_and_weather (var_converted[3], weather_and_ct_coeff)
  
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
    input_value['Value'] = var_converted[4]
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
    input_value['Value'] = demand['ss_pfa_demand'][0]
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
     
    ##############################################################################################################    
    ##chiller_cond_flow_consol_4nc
    input_value = {}
    input_value['Name'] = 'chiller_cond_flow_consol_4nc_tcnwkflow' 
    input_value['Value'] = total_cond_flow
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    ##############################################################################################################      
    ##chiller1_cond_4nc
    input_value = {}
    input_value['Name'] = 'chiller1_cond_4nc_tcnwkflow' 
    input_value['Value'] = total_cond_flow
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    input_value = {}
    input_value['Name'] = 'chiller1_cond_4nc_ctin' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
    
    ##############################################################################################################
    ##chiller1_cond_nwk_4nc    
    input_value = {}
    input_value['Name'] = 'chiller1_cond_nwk_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    input_value = {}
    input_value['Name'] = 'chiller1_cond_nwk_4nc_tcnwkflow' 
    input_value['Value'] = total_cond_flow
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
    
    ##############################################################################################################
    ##chiller1_cond_pump_4nc   
    input_value = {}
    input_value['Name'] = 'chiller1_cond_pump_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
    
    ##############################################################################################################      
    ##chiller2_cond_4nc
    input_value = {}
    input_value['Name'] = 'chiller2_cond_4nc_tcnwkflow' 
    input_value['Value'] = total_cond_flow
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    input_value = {}
    input_value['Name'] = 'chiller2_cond_4nc_ctin' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
    
    ##############################################################################################################
    ##chiller2_cond_nwk_4nc    
    input_value = {}
    input_value['Name'] = 'chiller2_cond_nwk_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    input_value = {}
    input_value['Name'] = 'chiller2_cond_nwk_4nc_tcnwkflow' 
    input_value['Value'] = total_cond_flow
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
    
    ##############################################################################################################
    ##chiller2_cond_pump_4nc   
    input_value = {}
    input_value['Name'] = 'chiller2_cond_pump_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    ##############################################################################################################      
    ##chiller3_cond_4nc
    input_value = {}
    input_value['Name'] = 'chiller3_cond_4nc_tcnwkflow' 
    input_value['Value'] = total_cond_flow
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    input_value = {}
    input_value['Name'] = 'chiller3_cond_4nc_ctin' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
    
    ##############################################################################################################
    ##chiller3_cond_nwk_4nc    
    input_value = {}
    input_value['Name'] = 'chiller3_cond_nwk_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
    
    input_value = {}
    input_value['Name'] = 'chiller3_cond_nwk_4nc_tcnwkflow' 
    input_value['Value'] = total_cond_flow
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
    
    ##############################################################################################################
    ##chiller3_cond_pump_4nc   
    input_value = {}
    input_value['Name'] = 'chiller3_cond_pump_4nc_piecewise_steps' 
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = '-'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     

    ##############################################################################################################
#    ##cooling_tower1_4nc
#    input_value = {}
#    input_value['Name'] = 'cooling_tower1_4nc_twb' 
#    input_value['Value'] = ct_coeff_weather_selected['T_WB'][0] + 273.15
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#
#    input_value = {}
#    input_value['Name'] = 'cooling_tower1_4nc_c0' 
#    input_value['Value'] = ct_coeff_weather_selected['c0'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower1_4nc_c1' 
#    input_value['Value'] = ct_coeff_weather_selected['c1'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower1_4nc_c2' 
#    input_value['Value'] = ct_coeff_weather_selected['c2'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower1_4nc_c3' 
#    input_value['Value'] = ct_coeff_weather_selected['c3'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#
#    input_value = {}
#    input_value['Name'] = 'cooling_tower1_4nc_tcnwkflow' 
#    input_value['Value'] = total_cond_flow
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##############################################################################################################
#    ##cooling_tower2_4nc
#    input_value = {}
#    input_value['Name'] = 'cooling_tower2_4nc_twb' 
#    input_value['Value'] = ct_coeff_weather_selected['T_WB'][0] + 273.15
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#
#    input_value = {}
#    input_value['Name'] = 'cooling_tower2_4nc_c0' 
#    input_value['Value'] = ct_coeff_weather_selected['c0'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower2_4nc_c1' 
#    input_value['Value'] = ct_coeff_weather_selected['c1'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower2_4nc_c2' 
#    input_value['Value'] = ct_coeff_weather_selected['c2'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower2_4nc_c3' 
#    input_value['Value'] = ct_coeff_weather_selected['c3'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#
#    input_value = {}
#    input_value['Name'] = 'cooling_tower2_4nc_tcnwkflow' 
#    input_value['Value'] = total_cond_flow
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    ##############################################################################################################
#    ##cooling_tower3_4nc
#    input_value = {}
#    input_value['Name'] = 'cooling_tower3_4nc_twb' 
#    input_value['Value'] = ct_coeff_weather_selected['T_WB'][0] + 273.15
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#
#    input_value = {}
#    input_value['Name'] = 'cooling_tower3_4nc_c0' 
#    input_value['Value'] = ct_coeff_weather_selected['c0'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower3_4nc_c1' 
#    input_value['Value'] = ct_coeff_weather_selected['c1'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower3_4nc_c2' 
#    input_value['Value'] = ct_coeff_weather_selected['c2'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower3_4nc_c3' 
#    input_value['Value'] = ct_coeff_weather_selected['c3'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#
#    input_value = {}
#    input_value['Name'] = 'cooling_tower3_4nc_tcnwkflow' 
#    input_value['Value'] = total_cond_flow
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)     
#    
#    ##############################################################################################################
#    ##cooling_tower4_4nc
#    input_value = {}
#    input_value['Name'] = 'cooling_tower4_4nc_twb' 
#    input_value['Value'] = ct_coeff_weather_selected['T_WB'][0] + 273.15
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#
#    input_value = {}
#    input_value['Name'] = 'cooling_tower4_4nc_c0' 
#    input_value['Value'] = ct_coeff_weather_selected['c0'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower4_4nc_c1' 
#    input_value['Value'] = ct_coeff_weather_selected['c1'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower4_4nc_c2' 
#    input_value['Value'] = ct_coeff_weather_selected['c2'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower4_4nc_c3' 
#    input_value['Value'] = ct_coeff_weather_selected['c3'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#
#    input_value = {}
#    input_value['Name'] = 'cooling_tower4_4nc_tcnwkflow' 
#    input_value['Value'] = total_cond_flow
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##############################################################################################################
#    ##cooling_tower5_4nc
#    input_value = {}
#    input_value['Name'] = 'cooling_tower5_4nc_twb' 
#    input_value['Value'] = ct_coeff_weather_selected['T_WB'][0] + 273.15
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#
#    input_value = {}
#    input_value['Name'] = 'cooling_tower5_4nc_c0' 
#    input_value['Value'] = ct_coeff_weather_selected['c0'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower5_4nc_c1' 
#    input_value['Value'] = ct_coeff_weather_selected['c1'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower5_4nc_c2' 
#    input_value['Value'] = ct_coeff_weather_selected['c2'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    input_value = {}
#    input_value['Name'] = 'cooling_tower5_4nc_c3' 
#    input_value['Value'] = ct_coeff_weather_selected['c3'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#
#    input_value = {}
#    input_value['Name'] = 'cooling_tower5_4nc_tcnwkflow' 
#    input_value['Value'] = total_cond_flow
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##############################################################################################################
#    ##chiller_ret_cond_4nc
#
#    input_value = {}
#    input_value['Name'] = 'chiller_ret_cond_4nc_ctin' 
#    input_value['Value'] = var_converted[2]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    return mdv_slave_param

##A function to determine the total condenser flowrate 
def determine_total_cond_flow (choice):
    
    if choice == 0:
        total_cond_flow = 407
    elif choice == 1:
        total_cond_flow = 1476
    elif choice == 2:
        total_cond_flow = 407 + 1476
    elif choice == 3:
        total_cond_flow = 1476 + 1476
    elif choice == 4:
        total_cond_flow = 407 + 1476 + 1476

    return total_cond_flow    

##A function to determine the corresponding weather conditions and the cooling tower coefficients 
def determine_ct_coeff_and_weather (key, weather_and_ct_coeff):
    
    import pandas as pd    

    ##key --- condenser flowrate choice
    ##weather_and_ct_coeff --- the information about weather and cooling tower coefficients 
    
    temp_data = [weather_and_ct_coeff['T_DB'][0], weather_and_ct_coeff['T_WB'][0],
                 weather_and_ct_coeff['f' + str(key) + '_c0'][0], weather_and_ct_coeff['f' + str(key) + '_c1'][0], 
                 weather_and_ct_coeff['f' + str(key) + '_c2'][0], weather_and_ct_coeff['f' + str(key) + '_c3'][0]]
    
    return_dataframe = pd.DataFrame(data = [temp_data], columns = ['T_DB', 'T_WB', 'c0', 'c1', 'c2', 'c3'])    
    
    return return_dataframe