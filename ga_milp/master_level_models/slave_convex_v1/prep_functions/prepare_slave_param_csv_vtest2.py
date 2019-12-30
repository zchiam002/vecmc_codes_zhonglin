##This function writes the parameters and master decision variables into a csv file for the slave to read

def prepare_slave_param_csv_vtest2 (var_converted, evap_cond_pump_lincoeff, dist_pump_1, dist_pump_2, dist_pump_3, weather, demand, nwk_choice, piecewise_steps):

    import pandas as pd
    
    ##Initiate dataframe to hold the written values 
    mdv_slave_param = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    ##1
    input_value = {}
    input_value['Name'] = 'chiller1_nwk_choice_' + str(nwk_choice) + '_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)

    ##2
    input_value = {}
    input_value['Name'] = 'chiller1_nwk_choice_' + str(nwk_choice) + '_ctin' 
    input_value['Value'] = var_converted[1]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##3
    input_value = {}
    input_value['Name'] = 'chiller1_nwk_choice_' + str(nwk_choice) + '_tenwkflow' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit']) 
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##4
    input_value = {}
    input_value['Name'] = 'chiller1_nwk_choice_' + str(nwk_choice) + '_tcnwkflow'
    input_value['Value'] = var_converted[3]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    

    ##5
    input_value = {}
    input_value['Name'] = 'chiller1_nwk_choice_' + str(nwk_choice) + '_piecewise_steps'
    input_value['Value'] = piecewise_steps
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##6
    input_value = {}
    input_value['Name'] = 'gv2_substation_nwk_choice_' + str(nwk_choice) + '_demand' 
    input_value['Value'] = demand['ss_gv2_demand'][0]
    input_value['Unit'] = 'kWh'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##7
    input_value = {}
    input_value['Name'] = 'gv2_substation_nwk_choice_' + str(nwk_choice) + '_totalflownwk' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    ##8
    input_value = {}
    input_value['Name'] = 'chiller_ret_nwk_choice_' + str(nwk_choice) + '_etret' 
    input_value['Value'] = var_converted[0]
    input_value['Unit'] = 'K'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 

    ##9
    input_value = {}
    input_value['Name'] = 'chiller_evap_flow_consol_nwk_choice_' + str(nwk_choice) + '_tf' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    

    ##10
    input_value = {}
    input_value['Name'] = 'cp_network_nwk_choice_' + str(nwk_choice) + '_tf' 
    input_value['Value'] = var_converted[2]
    input_value['Unit'] = 'm3/h'
    
    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)       
#    ##5
#    input_value = {}
#    input_value['Name'] = 'chiller2_etret' 
#    input_value['Value'] = var_converted[0]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#
#    ##6
#    input_value = {}
#    input_value['Name'] = 'chiller2_ctin' 
#    input_value['Value'] = var_converted[1]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit']) 
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##7
#    input_value = {}
#    input_value['Name'] = 'chiller2_tenwkflow' 
#    input_value['Value'] = var_converted[2]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit']) 
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##8
#    input_value = {}
#    input_value['Name'] = 'chiller2_tcnwkflow'
#    input_value['Value'] = var_converted[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])  
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##9
#    input_value = {}
#    input_value['Name'] = 'chiller3_etret' 
#    input_value['Value'] = var_converted[0]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#
#    ##10
#    input_value = {}
#    input_value['Name'] = 'chiller3_ctin' 
#    input_value['Value'] = var_converted[1]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit']) 
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##11
#    input_value = {}
#    input_value['Name'] = 'chiller3_tenwkflow' 
#    input_value['Value'] = var_converted[2]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit']) 
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##12
#    input_value = {}
#    input_value['Name'] = 'chiller3_tcnwkflow' 
#    input_value['Value'] = var_converted[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])  
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##13
#    input_value = {}
#    input_value['Name'] = 'ch1_evap_pump_p_coeff' 
#    input_value['Value'] = evap_cond_pump_lincoeff['p_coeff'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])  
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    ##14
#    input_value = {}
#    input_value['Name'] = 'ch1_evap_pump_m_coeff' 
#    input_value['Value'] = evap_cond_pump_lincoeff['m_coeff'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#    
#    ##15
#    input_value = {}
#    input_value['Name'] = 'ch1_evap_pump_cst' 
#    input_value['Value'] = evap_cond_pump_lincoeff['cst'][0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##16
#    input_value = {}
#    input_value['Name'] = 'ch1_evap_pump_max_m' 
#    input_value['Value'] = evap_cond_pump_lincoeff['max_flow'][0]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##17
#    input_value = {}
#    input_value['Name'] = 'ch2_evap_pump_p_coeff' 
#    input_value['Value'] = evap_cond_pump_lincoeff['p_coeff'][1]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])  
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    ##18
#    input_value = {}
#    input_value['Name'] = 'ch2_evap_pump_m_coeff' 
#    input_value['Value'] = evap_cond_pump_lincoeff['m_coeff'][1]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#    
#    ##19
#    input_value = {}
#    input_value['Name'] = 'ch2_evap_pump_cst' 
#    input_value['Value'] = evap_cond_pump_lincoeff['cst'][1]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##20
#    input_value = {}
#    input_value['Name'] = 'ch2_evap_pump_max_m' 
#    input_value['Value'] = evap_cond_pump_lincoeff['max_flow'][1]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##21
#    input_value = {}
#    input_value['Name'] = 'ch3_evap_pump_p_coeff' 
#    input_value['Value'] = evap_cond_pump_lincoeff['p_coeff'][2]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])  
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    ##22
#    input_value = {}
#    input_value['Name'] = 'ch3_evap_pump_m_coeff' 
#    input_value['Value'] = evap_cond_pump_lincoeff['m_coeff'][2]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#    
#    ##23
#    input_value = {}
#    input_value['Name'] = 'ch3_evap_pump_cst' 
#    input_value['Value'] = evap_cond_pump_lincoeff['cst'][2]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##24
#    input_value = {}
#    input_value['Name'] = 'ch3_evap_pump_max_m' 
#    input_value['Value'] = evap_cond_pump_lincoeff['max_flow'][2]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    

#    
#    ##26
#    input_value = {}
#    input_value['Name'] = 'chiller1_evap_nwk_tf' 
#    input_value['Value'] = var_converted[2]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##27
#    input_value = {}
#    input_value['Name'] = 'chiller2_evap_nwk_tf' 
#    input_value['Value'] = var_converted[2]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#
#    ##28
#    input_value = {}
#    input_value['Name'] = 'chiller3_evap_nwk_tf' 
#    input_value['Value'] = var_converted[2]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#   
#    
#    ##30
#    input_value = {}
#    input_value['Name'] = 'chiller2_ret_etret' 
#    input_value['Value'] = var_converted[0]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##31
#    input_value = {}
#    input_value['Name'] = 'chiller3_ret_etret' 
#    input_value['Value'] = var_converted[0]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##32
#    input_value = {}
#    input_value['Name'] = 'ch1_cond_pump_p_coeff' 
#    input_value['Value'] = evap_cond_pump_lincoeff['p_coeff'][3]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])  
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    ##33
#    input_value = {}
#    input_value['Name'] = 'ch1_cond_pump_m_coeff' 
#    input_value['Value'] = evap_cond_pump_lincoeff['m_coeff'][3]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#    
#    ##34
#    input_value = {}
#    input_value['Name'] = 'ch1_cond_pump_cst' 
#    input_value['Value'] = evap_cond_pump_lincoeff['cst'][3]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##35
#    input_value = {}
#    input_value['Name'] = 'ch1_cond_pump_max_m' 
#    input_value['Value'] = evap_cond_pump_lincoeff['max_flow'][3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##36
#    input_value = {}
#    input_value['Name'] = 'ch2_cond_pump_p_coeff' 
#    input_value['Value'] = evap_cond_pump_lincoeff['p_coeff'][4]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])  
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    ##37
#    input_value = {}
#    input_value['Name'] = 'ch2_cond_pump_m_coeff' 
#    input_value['Value'] = evap_cond_pump_lincoeff['m_coeff'][4]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#    
#    ##38
#    input_value = {}
#    input_value['Name'] = 'ch2_cond_pump_cst' 
#    input_value['Value'] = evap_cond_pump_lincoeff['cst'][4]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##39
#    input_value = {}
#    input_value['Name'] = 'ch2_cond_pump_max_m' 
#    input_value['Value'] = evap_cond_pump_lincoeff['max_flow'][4]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##40
#    input_value = {}
#    input_value['Name'] = 'ch3_cond_pump_p_coeff' 
#    input_value['Value'] = evap_cond_pump_lincoeff['p_coeff'][5]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])  
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    ##41
#    input_value = {}
#    input_value['Name'] = 'ch3_cond_pump_m_coeff' 
#    input_value['Value'] = evap_cond_pump_lincoeff['m_coeff'][5]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#    
#    ##42
#    input_value = {}
#    input_value['Name'] = 'ch3_cond_pump_cst' 
#    input_value['Value'] = evap_cond_pump_lincoeff['cst'][5]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##43
#    input_value = {}
#    input_value['Name'] = 'ch3_cond_pump_max_m' 
#    input_value['Value'] = evap_cond_pump_lincoeff['max_flow'][5]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##44
#    input_value = {}
#    input_value['Name'] = 'chiller_cond_ret_mflow_mret' 
#    input_value['Value'] = var_converted[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##45
#    input_value = {}
#    input_value['Name'] = 'chiller1_cond_nwk_tf' 
#    input_value['Value'] = var_converted[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##46
#    input_value = {}
#    input_value['Name'] = 'chiller2_cond_nwk_tf' 
#    input_value['Value'] = var_converted[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##47
#    input_value = {}
#    input_value['Name'] = 'chiller3_cond_nwk_tf' 
#    input_value['Value'] = var_converted[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##48
#    input_value = {}
#    input_value['Name'] = 'cp_network_tf' 
#    input_value['Value'] = var_converted[2]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##49
#    input_value = {}
#    input_value['Name'] = 'dist_pump1_p_coeff' 
#    input_value['Value'] = dist_pump_1[1]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])  
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    ##50
#    input_value = {}
#    input_value['Name'] = 'dist_pump1_m_coeff' 
#    input_value['Value'] = dist_pump_1[0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#    
#    ##51
#    input_value = {}
#    input_value['Name'] = 'dist_pump1_cst' 
#    input_value['Value'] = dist_pump_1[2]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##52
#    input_value = {}
#    input_value['Name'] = 'dist_pump1_max_m' 
#    input_value['Value'] = dist_pump_1[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##53
#    input_value = {}
#    input_value['Name'] = 'dist_pump2_p_coeff' 
#    input_value['Value'] = dist_pump_2[1]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])  
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    ##54
#    input_value = {}
#    input_value['Name'] = 'dist_pump2_m_coeff' 
#    input_value['Value'] = dist_pump_2[0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#    
#    ##55
#    input_value = {}
#    input_value['Name'] = 'dist_pump2_cst' 
#    input_value['Value'] = dist_pump_2[2]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##56
#    input_value = {}
#    input_value['Name'] = 'dist_pump2_max_m' 
#    input_value['Value'] = dist_pump_2[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##57
#    input_value = {}
#    input_value['Name'] = 'dist_pump3_p_coeff' 
#    input_value['Value'] = dist_pump_3[1]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])  
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)    
#    
#    ##58
#    input_value = {}
#    input_value['Name'] = 'dist_pump3_m_coeff' 
#    input_value['Value'] = dist_pump_3[0]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)  
#    
#    ##59
#    input_value = {}
#    input_value['Name'] = 'dist_pump3_cst' 
#    input_value['Value'] = dist_pump_3[2]
#    input_value['Unit'] = '-'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True) 
#    
#    ##60
#    input_value = {}
#    input_value['Name'] = 'dist_pump3_max_m' 
#    input_value['Value'] = dist_pump_3[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    

#    
#    ##63
#    input_value = {}
#    input_value['Name'] = 'hsb_substation_demand' 
#    input_value['Value'] = demand['ss_hsb_demand'][0]
#    input_value['Unit'] = 'kWh'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##64
#    input_value = {}
#    input_value['Name'] = 'hsb_substation_totalflownwk' 
#    input_value['Value'] = var_converted[2]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##65
#    input_value = {}
#    input_value['Name'] = 'pfa_substation_demand' 
#    input_value['Value'] = demand['ss_pfa_demand'][0]
#    input_value['Unit'] = 'kWh'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##66
#    input_value = {}
#    input_value['Name'] = 'pfa_substation_totalflownwk' 
#    input_value['Value'] = var_converted[2]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#
#    ##67
#    input_value = {}
#    input_value['Name'] = 'ser_substation_demand' 
#    input_value['Value'] = demand['ss_ser_demand'][0]
#    input_value['Unit'] = 'kWh'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##68
#    input_value = {}
#    input_value['Name'] = 'ser_substation_totalflownwk' 
#    input_value['Value'] = var_converted[2]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##69
#    input_value = {}
#    input_value['Name'] = 'fir_substation_demand' 
#    input_value['Value'] = demand['ss_fir_demand'][0]
#    input_value['Unit'] = 'kWh'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##70
#    input_value = {}
#    input_value['Name'] = 'fir_substation_totalflownwk' 
#    input_value['Value'] = var_converted[2]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##71
#    input_value = {}
#    input_value['Name'] = 'cooling_tower1_tmfr' 
#    input_value['Value'] = var_converted[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##72
#    input_value = {}
#    input_value['Name'] = 'cooling_tower1_mfr' 
#    input_value['Value'] = 0.2
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##73
#    input_value = {}
#    input_value['Name'] = 'cooling_tower1_twb' 
#    input_value['Value'] = weather['T_WB'][0]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##74
#    input_value = {}
#    input_value['Name'] = 'cooling_tower2_tmfr' 
#    input_value['Value'] = var_converted[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##75
#    input_value = {}
#    input_value['Name'] = 'cooling_tower2_mfr' 
#    input_value['Value'] = 0.2
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##76
#    input_value = {}
#    input_value['Name'] = 'cooling_tower2_twb' 
#    input_value['Value'] = weather['T_WB'][0]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##77
#    input_value = {}
#    input_value['Name'] = 'cooling_tower3_tmfr' 
#    input_value['Value'] = var_converted[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##78
#    input_value = {}
#    input_value['Name'] = 'cooling_tower3_mfr' 
#    input_value['Value'] = 0.2
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##79
#    input_value = {}
#    input_value['Name'] = 'cooling_tower3_twb' 
#    input_value['Value'] = weather['T_WB'][0]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##80
#    input_value = {}
#    input_value['Name'] = 'cooling_tower4_tmfr' 
#    input_value['Value'] = var_converted[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##81
#    input_value = {}
#    input_value['Name'] = 'cooling_tower4_mfr' 
#    input_value['Value'] = 0.2
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##82
#    input_value = {}
#    input_value['Name'] = 'cooling_tower4_twb' 
#    input_value['Value'] = weather['T_WB'][0]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##83
#    input_value = {}
#    input_value['Name'] = 'cooling_tower5_tmfr' 
#    input_value['Value'] = var_converted[3]
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##84
#    input_value = {}
#    input_value['Name'] = 'cooling_tower5_mfr' 
#    input_value['Value'] = 0.2
#    input_value['Unit'] = 'm3/h'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##85
#    input_value = {}
#    input_value['Name'] = 'cooling_tower5_twb' 
#    input_value['Value'] = weather['T_WB'][0]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
#    
#    ##86
#    input_value = {}
#    input_value['Name'] = 'cooling_tower_ret_tret' 
#    input_value['Value'] = var_converted[1]
#    input_value['Unit'] = 'K'
#    
#    temp_values = [input_value['Name'], input_value['Value'], input_value['Unit']]
#    temp_df = pd.DataFrame(data = [temp_values], columns = ['Name', 'Value', 'Unit'])   
#    mdv_slave_param = mdv_slave_param.append(temp_df, ignore_index=True)
    
    return mdv_slave_param
    
    