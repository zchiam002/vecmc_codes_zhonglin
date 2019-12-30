##This is the evaporator network model

def evap_nwk_org (chiller_input, chiller_onoff):
    import sys
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\add_on_functions\\')
    from golden_section import golden_section_evap_cond 
    from auxillary_functions import pump_sys_int_evap_cond
    import pandas as pd 
    
    ##chiller_input is a dataframe with labels ['Name'] and ['Value']
    ##chiller_input['Name'][0] --- chiller_1_flow (m3/h)
    ##chiller_input['Name'][1] --- chiller_1_supply_temperature (K)
    ##chiller_input['Name'][2] --- chiller_2_flow (m3/h)
    ##chiller_input['Name'][3] --- chiller_2_supply_temperature (K)
    ##chiller_input['Name'][4] --- chiller_3_flow (m3/h)
    ##chiller_input['Name'][5] --- chiller_3_supply_temperature (K)
    ##Retrieve the values from the corresponding ['Value'] with appropriate key
    
    ##chiller_onoff['chiller1_onoff'] --- a binary variable to indicate if a chiller is on or off
    ##chiller_onoff['chiller2_onoff'] --- a binary variable to indicate if a chiller is on or off
    ##chiller_onoff['chiller3_onoff'] --- a binary variable to indicate if a chiller is on or off    
    
    return_values = {} 

    ##Calculating the pressure_drop associated with each branch of the evaporator network
    
    ##Network Parameters
    ch1_nwk_coeff = 0.000246472
    ch2_nwk_coeff = 3.07492E-05
    ch3_nwk_coeff = 3.07492E-05
    common_nwk_coeff = 1.66667E-05
    ##Pump parameters 
    evap_pump_1_delp = [-0.0001266405, 0.0112272822, 12.3463827922]                 ##Listed in terms of x2, x and cst coeff
    evap_pump_2_delp = [-0.0000136254, 0.0001647403, 21.4327511013]
    evap_pump_3_delp = [-0.0000136254, 0.0001647403, 21.4327511013]
    ##This is the cubic form, which is more accurate only within the range 
    evap_pump_1_elect = [-0.0000003355, 0.0001014045, 0.0053863673, 3.8221779914]   ##Listed in terms of x3, x2, x and cst coeff
    evap_pump_2_elect = [0, -0.0000106288, 0.0310754128, 18.9432666214]
    evap_pump_3_elect = [0, -0.0000106288, 0.0310754128, 18.9432666214]

    ##Flow limits 
    ch1_evap_nwk_flow_limit = 250
    ch2_evap_nwk_flow_limit = 900   
    ch3_evap_nwk_flow_limit = 900
    
    ##Pressure drop calcualtion for the common network  
    total_evap_nwk_flow = chiller_input['Value'][0] + chiller_input['Value'][2] + chiller_input['Value'][4]
    delp_common_nwk = common_nwk_coeff * pow(total_evap_nwk_flow, 1.852)

    
    if chiller_onoff['chiller1_onoff'] == 1:
        ##Pressure drop and electricity calculation for chiller 1 evap nwk 
        delp_chl_evap_nwk = (ch1_nwk_coeff * pow(chiller_input['Value'][0], 1.852)) + delp_common_nwk
        if chiller_input['Value'][0] != 0:
            flow_bounds = [0, ch1_evap_nwk_flow_limit]
            max_flow = golden_section_evap_cond(pump_sys_int_evap_cond, flow_bounds, ch1_nwk_coeff, evap_pump_1_delp, delp_common_nwk)
            max_elect = (evap_pump_1_elect[0]*pow(max_flow, 3)) + (evap_pump_1_elect[1]*pow(max_flow, 2)) + (evap_pump_1_elect[2]*max_flow) + (evap_pump_1_elect[3])
            ##Assuming linear relationship between elect and rpm of the pump,
            grad_elect_flow = max_elect / max_flow 
            elect_cons = grad_elect_flow * chiller_input['Value'][0]
            delp = delp_chl_evap_nwk
        else:
            elect_cons = 0
            delp = 0
            max_flow= 0
        
        return_values['Chiller1_evap_pump_delp'] = delp
        return_values['Chiller1_evap_pump_max_flow'] = max_flow
        return_values['Chiller1_evap_pump_elect_cons'] = elect_cons
    else:
        return_values['Chiller1_evap_pump_delp'] = 0
        return_values['Chiller1_evap_pump_max_flow'] = 0
        return_values['Chiller1_evap_pump_elect_cons'] = 0        


    if chiller_onoff['chiller2_onoff'] == 1:        
        ##Pressure drop calculation for chiller 2 evap nwk
        delp_ch2_evap_nwk = (ch2_nwk_coeff * pow(chiller_input['Value'][2], 1.852)) + delp_common_nwk
        if chiller_input['Value'][2] != 0:
            flow_bounds = [0, ch2_evap_nwk_flow_limit]
            max_flow = golden_section_evap_cond(pump_sys_int_evap_cond, flow_bounds, ch2_nwk_coeff, evap_pump_2_delp, delp_common_nwk)
            max_elect = (evap_pump_2_elect[0]*pow(max_flow, 3)) + (evap_pump_2_elect[1]*pow(max_flow, 2)) + (evap_pump_2_elect[2]*max_flow) + (evap_pump_2_elect[3])
            ##Assuming linear relationship between elect and rpm of the pump,
            grad_elect_flow = max_elect / max_flow 
            elect_cons = grad_elect_flow * chiller_input['Value'][2]
            delp = delp_ch2_evap_nwk
        else:
            elect_cons = 0
            delp = 0
            
        return_values['Chiller2_evap_pump_delp'] = delp
        return_values['Chiller2_evap_pump_max_flow'] = max_flow
        return_values['Chiller2_evap_pump_elect_cons'] = elect_cons  
    else:
        return_values['Chiller2_evap_pump_delp'] = 0
        return_values['Chiller2_evap_pump_max_flow'] = 0
        return_values['Chiller2_evap_pump_elect_cons'] = 0
        
        
    if chiller_onoff['chiller3_onoff'] == 1:        
        ##Pressure drop calculation for chiller 3 evap nwk 
        delp_ch3_evap_nwk = (ch3_nwk_coeff * pow(chiller_input['Value'][4], 1.852)) + delp_common_nwk
        if chiller_input['Value'][4] != 0:
            flow_bounds = [0, ch3_evap_nwk_flow_limit]
            max_flow = golden_section_evap_cond(pump_sys_int_evap_cond, flow_bounds, ch3_nwk_coeff, evap_pump_3_delp, delp_common_nwk)
            max_elect = (evap_pump_3_elect[0]*pow(max_flow, 3)) + (evap_pump_3_elect[1]*pow(max_flow, 2)) + (evap_pump_3_elect[2]*max_flow) + (evap_pump_3_elect[3])
            ##Assuming linear relationship between elect and rpm of the pump,
            grad_elect_flow = max_elect / max_flow 
            elect_cons = grad_elect_flow * chiller_input['Value'][4]
            delp = delp_ch3_evap_nwk
        else:
            elect_cons = 0
            delp = 0
            
        return_values['Chiller3_evap_pump_delp'] = delp
        return_values['Chiller3_evap_pump_max_flow'] = max_flow
        return_values['Chiller3_evap_pump_elect_cons'] = elect_cons   
    else:
        return_values['Chiller3_evap_pump_delp'] = 0
        return_values['Chiller3_evap_pump_max_flow'] = 0
        return_values['Chiller3_evap_pump_elect_cons'] = 0 
        
    ##Calculating exiting to the distribution network and the common pipe 
    if total_evap_nwk_flow != 0:
        tout_ch1 = chiller_input['Value'][1]
        tout_ch2 = chiller_input['Value'][3]
        tout_ch3 = chiller_input['Value'][5]
        flow_ch1 = chiller_input['Value'][0] * chiller_onoff['chiller1_onoff']
        flow_ch2 = chiller_input['Value'][2] * chiller_onoff['chiller2_onoff']
        flow_ch3 = chiller_input['Value'][4] * chiller_onoff['chiller3_onoff']
        tout_evap_nwk = ((flow_ch1*tout_ch1) + (flow_ch2*tout_ch2) + (flow_ch3*tout_ch3)) / total_evap_nwk_flow
    else:
        tout_evap_nwk = 'Undefined'
        
    return_values['Exit_temperature'] = tout_evap_nwk

    ##Populating return values in the DataFrame format for ease of display 
    return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    data_temp = ['Chiller1_evap_pump_delp', return_values['Chiller1_evap_pump_delp'], 'mH2O']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)   
    data_temp = ['Chiller1_evap_pump_max_flow', return_values['Chiller1_evap_pump_max_flow'], 'm3/h']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)    
    data_temp = ['Chiller1_evap_pump_elect_cons', return_values['Chiller1_evap_pump_elect_cons'], 'kWh']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)     
    
    data_temp = ['Chiller2_evap_pump_delp', return_values['Chiller2_evap_pump_delp'], 'mH2O']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)
    data_temp = ['Chiller2_evap_pump_max_flow', return_values['Chiller2_evap_pump_max_flow'], 'm3/h']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)    
    data_temp = ['Chiller2_evap_pump_elect_cons', return_values['Chiller2_evap_pump_elect_cons'], 'kWh']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True) 
    
    data_temp = ['Chiller3_evap_pump_delp', return_values['Chiller3_evap_pump_delp'], 'mH2O']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)
    data_temp = ['Chiller3_evap_pump_max_flow', return_values['Chiller3_evap_pump_max_flow'], 'm3/h']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)    
    data_temp = ['Chiller3_evap_pump_elect_cons', return_values['Chiller3_evap_pump_elect_cons'], 'kWh']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True) 
    
    data_temp = ['Exit_temperature', return_values['Exit_temperature'], 'K']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True) 
    
    return return_values, return_values_df