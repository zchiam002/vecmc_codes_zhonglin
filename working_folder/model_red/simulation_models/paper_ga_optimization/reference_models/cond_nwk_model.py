def cond_nwk_org (chiller_input, num_cooling_towers):
    import sys
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\add_on_functions\\')
    from golden_section import golden_section_evap_cond 
    import pandas as pd 
    
    ##chiller_input is a dataframe with labels ['Name'] and ['Value']
    ##chiller_input['Name'][0] --- chiller_1_cond_flow (m3/h)
    ##chiller_input['Name'][1] --- chiller_1_cond_exit_temperature (K)
    ##chiller_input['Name'][2] --- chiller_2_cond_flow (m3/h)
    ##chiller_input['Name'][3] --- chiller_2_cond_exit_temperature (K)
    ##chiller_input['Name'][4] --- chiller_3_cond_flow (m3/h)
    ##chiller_input['Name'][5] --- chiller_3_cond_exit_temperature (K)
    ##Retrieve the values from the corresponding ['Value'] with appropriate key
    
    ##num_cooling_towers --- the number of cooling towers connected tothe chiller configuration 
    
    return_values = {} 

    ##Calculating the pressure_drop associated with each branch of the evaporator network
    
    ##Network Parameters
    ch1_nwk_coeff = 0.000133743
    ch2_nwk_coeff = 1.78251E-05
    ch3_nwk_coeff = 1.78251E-05
    common_nwk_coeff = 6.62983425414365E-07
    ##Pump parameters 
    cond_pump_1_delp = [-0.0000552287, 0.0127459461, 28.8570326545]                 ##Listed in terms of x2, x and cst coeff
    cond_pump_2_delp = [-0.0000090818, 0.0029568794, 45.1880038403]    
    cond_pump_3_delp = [-0.0000090818, 0.0029568794, 45.1880038403]
    ##This is the cubic form, which is more accurate only within the range 
    ##cond_pump_1_elect = [0, -0.0000218828, 0.0599176697, 22.8337836011]             ##Listed in terms of x3, x2, x and cst coeff
    ##cond_pump_2_elect = [0, -0.0000228942, 0.0721558792, 76.4863706961]
    ##cond_pump_3_elect = [0, -0.0000228942, 0.0721558792, 76.4863706961]
    ##This is the linear form, better confidence with extrapolation
    cond_pump_1_elect = [0, 0, 0.0452342766, 24.2119090656]             ##Listed in terms of x3, x2, x and cst coeff
    cond_pump_2_elect = [0, 0, 0.0308747009, 87.4546362071]
    cond_pump_3_elect = [0, 0, 0.0308747009, 87.4546362071]
    
    ##Flow limits 
    ch1_cond_nwk_flow_limit = 3200
    ch2_cond_nwk_flow_limit = 3200    
    ch3_cond_nwk_flow_limit = 3200
    
    ##Pressure drop calcualtion for the common network  
    total_cond_nwk_flow = chiller_input['Value'][0] + chiller_input['Value'][2] + chiller_input['Value'][4]
    delp_common_nwk = common_nwk_coeff * pow(total_cond_nwk_flow, 1.852)

    ##Pressure drop and electricity calculation for chiller 1 cond nwk 
    delp_chl_cond_nwk = (ch1_nwk_coeff * pow(chiller_input['Value'][0], 1.852)) + delp_common_nwk
    if chiller_input['Value'][0] != 0:
        flow_bounds = [0, ch1_cond_nwk_flow_limit]
        max_flow = golden_section_evap_cond(pump_sys_int_evap_cond, flow_bounds, ch1_nwk_coeff, cond_pump_1_delp, delp_common_nwk)
        max_elect = (cond_pump_1_elect[0]*pow(max_flow, 3)) + (cond_pump_1_elect[1]*pow(max_flow, 2)) + (cond_pump_1_elect[2]*max_flow) + (cond_pump_1_elect[3])
        ##Assuming linear relationship between elect and rpm of the pump,
        grad_elect_flow = max_elect / max_flow 
        elect_cons = grad_elect_flow * chiller_input['Value'][0]
        delp = delp_chl_cond_nwk
    else:
        elect_cons = 0
        delp = 0
        max_flow = 0
    
    return_values['Chiller1_cond_pump_delp'] = delp
    return_values['Chiller1_cond_pump_max_flow'] = max_flow
    return_values['Chiller1_cond_pump_elect_cons'] = elect_cons
        
    ##Pressure drop calculation for chiller 2 cond nwk
    delp_ch2_cond_nwk = (ch2_nwk_coeff * pow(chiller_input['Value'][2], 1.852)) + delp_common_nwk
    if chiller_input['Value'][2] != 0:
        flow_bounds = [0, ch2_cond_nwk_flow_limit]
        max_flow = golden_section_evap_cond(pump_sys_int_evap_cond, flow_bounds, ch2_nwk_coeff, cond_pump_2_delp, delp_common_nwk)
        max_elect = (cond_pump_2_elect[0]*pow(max_flow, 3)) + (cond_pump_2_elect[1]*pow(max_flow, 2)) + (cond_pump_2_elect[2]*max_flow) + (cond_pump_2_elect[3])
        ##Assuming linear relationship between elect and rpm of the pump,
        grad_elect_flow = max_elect / max_flow 
        elect_cons = grad_elect_flow * chiller_input['Value'][2]
        delp = delp_ch2_cond_nwk
    else:
        elect_cons = 0
        delp = 0
        
    return_values['Chiller2_cond_pump_delp'] = delp
    return_values['Chiller2_cond_pump_max_flow'] = max_flow
    return_values['Chiller2_cond_pump_elect_cons'] = elect_cons    

    ##Pressure drop calculation for chiller 3 cond nwk 
    delp_ch3_cond_nwk = (ch3_nwk_coeff * pow(chiller_input['Value'][4], 1.852)) + delp_common_nwk
    if chiller_input['Value'][4] != 0:
        flow_bounds = [0, ch3_cond_nwk_flow_limit]
        max_flow = golden_section_evap_cond(pump_sys_int_evap_cond, flow_bounds, ch3_nwk_coeff, cond_pump_3_delp, delp_common_nwk)
        max_elect = (cond_pump_3_elect[0]*pow(max_flow, 3)) + (cond_pump_3_elect[1]*pow(max_flow, 2)) + (cond_pump_3_elect[2]*max_flow) + (cond_pump_3_elect[3])
        ##Assuming linear relationship between elect and rpm of the pump,
        grad_elect_flow = max_elect / max_flow 
        elect_cons = grad_elect_flow * chiller_input['Value'][4]
        delp = delp_ch3_cond_nwk
    else:
        elect_cons = 0
        delp = 0
        
    return_values['Chiller3_cond_pump_delp'] = delp
    return_values['Chiller3_cond_pump_max_flow'] = max_flow
    return_values['Chiller3_cond_pump_elect_cons'] = elect_cons       
    
    ##Calculating exiting to the distribution network and the common pipe 
    if total_cond_nwk_flow != 0:
        tout_ch1 = chiller_input['Value'][1]
        tout_ch2 = chiller_input['Value'][3]
        tout_ch3 = chiller_input['Value'][5]
        flow_ch1 = chiller_input['Value'][0]
        flow_ch2 = chiller_input['Value'][2]
        flow_ch3 = chiller_input['Value'][4]
        tout_cond_nwk = ((flow_ch1*tout_ch1) + (flow_ch2*tout_ch2) + (flow_ch3*tout_ch3)) / total_cond_nwk_flow
    else:
        tout_cond_nwk = 'Undefined'
        
    return_values['Exit_temperature'] = tout_cond_nwk
    return_values['Flowrate_to_cooling_tower'] = total_cond_nwk_flow / num_cooling_towers

    ##Populating return values in the DataFrame format for ease of display 
    return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    data_temp = ['Chiller1_cond_pump_delp', return_values['Chiller1_cond_pump_delp'], 'mH2O']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)   
    data_temp = ['Chiller1_cond_pump_max_flow', return_values['Chiller1_cond_pump_max_flow'], 'm3/h']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)    
    data_temp = ['Chiller1_cond_pump_elect_cons', return_values['Chiller1_cond_pump_elect_cons'], 'kWh']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)     
    
    data_temp = ['Chiller2_cond_pump_delp', return_values['Chiller2_cond_pump_delp'], 'mH2O']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)
    data_temp = ['Chiller2_cond_pump_max_flow', return_values['Chiller2_cond_pump_max_flow'], 'm3/h']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)    
    data_temp = ['Chiller2_cond_pump_elect_cons', return_values['Chiller2_cond_pump_elect_cons'], 'kWh']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True) 
    
    data_temp = ['Chiller3_cond_pump_delp', return_values['Chiller3_cond_pump_delp'], 'mH2O']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)
    data_temp = ['Chiller3_cond_pump_max_flow', return_values['Chiller3_cond_pump_max_flow'], 'm3/h']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)    
    data_temp = ['Chiller3_cond_pump_elect_cons', return_values['Chiller3_cond_pump_elect_cons'], 'kWh']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True) 
    
    data_temp = ['Exit_temperature', return_values['Exit_temperature'], 'K']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True) 
    data_temp = ['Flowrate_to_cooling_tower', return_values['Flowrate_to_cooling_tower'], 'm3/h']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True) 
    
    return return_values, return_values_df