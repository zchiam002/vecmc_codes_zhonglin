##This is the distribution network model 

def dist_nwk_org (consumer_demand, m_total, perc_split, nwk_pump_select, tin_dist_nwk):
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
    import sys 
    sys.path.append(current_path + 'ecoenergies_models\\add_on_functions\\')
    from golden_section import golden_section_dist 
    from auxillary_functions import pump_sys_int_dist
    from dist_network_models_sub import dist_nwk_pump_select
    import pandas as pd
    
    ##consumer_demand[0] --- gv2_demand (kWh)
    ##consumer_demand[1] --- hsb_demand (kWh)
    ##consumer_demand[2] --- pfa_demand (kWh)
    ##consumer_demand[3] --- ser_demand (kWh)
    
    ##m_total --- the total flowrate throught the entire network (m3/h)
    
    ##perc_split[0] --- the split of flowrate to gv2 (%)
    ##perc_split[1] --- the split of flowrate to hsb (%)
    ##perc_split[2] --- the split of flowrate to pfa (%)
    ##perc_split[3] --- the split of flowrate to ser (%)

    ##nwk_pump_select --- a choice from 0 to 40 each corresponding to a different pump and netwrok combination 

    ##tin_dist_nwk --- the temperature of fluid entering the distribution network 
    
    return_values = {}
    
    ##Individual network pressure drop coefficients, they are all determined in the form of delp = A*m^1.852 
    ice_main_coeff = 0.00011627906976743445
    gv2_coeff = 0.00034883720930232456
    hsb_coeff = 0.05046511627906977
    tro_main_coeff = 0.001162790697674419
    pfa_coeff = 0.0029069767441860417
    ser_coeff = 0.00023255813953487953
    
    ##Preparing the flowrates 
    gv2_flow = perc_split[0] * m_total
    hsb_flow = perc_split[1] * m_total
    pfa_flow = perc_split[2] * m_total
    ser_flow = perc_split[3] * m_total

    ice_flow = gv2_flow + hsb_flow 
    tro_flow = pfa_flow + ser_flow 

    ##Obtaining pump parameters 
    network_pump_param = dist_nwk_pump_select(nwk_pump_select)
    
    ##Maximum flow, to act as bounds for the search based function 
    max_flow = 2600
    
    ##All networks share the same pump
        ##The flowrates maybe = 0
    if (ice_flow != 0) and (tro_flow != 0): 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))           
        delp_ice_tro_fir_sys = max(gv2_delp, hsb_delp, pfa_delp, ser_delp)
        ##This is true based on the current split ratio
        ice_tro_fir_sys_coeff = delp_ice_tro_fir_sys / pow(ice_flow + tro_flow, 1.852)
        ice_tro_fir_flow_bounds = [0, max_flow]
        ##Using the golden section to determine the intersection point of the system and pump curves
        ice_tro_fir_max_sys_flow = golden_section_dist(pump_sys_int_dist, ice_tro_fir_flow_bounds, ice_tro_fir_sys_coeff, network_pump_param['ice_tro_fir_branch_pump_delp'])
        ice_tro_fir_max_elect_cons = (network_pump_param['ice_tro_fir_branch_pump_elect'][0] * pow(ice_tro_fir_max_sys_flow, 3)) + (network_pump_param['ice_tro_fir_branch_pump_elect'][1] * pow(ice_tro_fir_max_sys_flow, 2)) + (network_pump_param['ice_tro_fir_branch_pump_elect'][2] * ice_tro_fir_max_sys_flow) + network_pump_param['ice_tro_fir_branch_pump_elect'][3]
        
        ##Assuming linear relationship with flowrate 
        if ice_tro_fir_max_sys_flow > 0:
            ice_tro_fir_pump_elect_cons = (ice_tro_fir_max_elect_cons / ice_tro_fir_max_sys_flow) * (ice_flow + tro_flow)
            flow_violation = 0
        elif ice_tro_fir_max_sys_flow < 0:
            ice_tro_fir_pump_elect_cons = float('inf')
            flow_violation = abs(ice_tro_fir_max_sys_flow) / max_flow
        else:
            ice_tro_fir_pump_elect_cons = 0
            flow_violation = 0
    
        return_values['ice_tro_fir_max_flow'] = ice_tro_fir_max_sys_flow
        return_values['ice_tro_fir_delp'] = delp_ice_tro_fir_sys
        return_values['ice_tro_fir_elect_cons'] = ice_tro_fir_pump_elect_cons
        return_values['flow_violation'] = flow_violation
    
    else:
        return_values['ice_tro_fir_max_flow'] = 0
        return_values['ice_tro_fir_delp'] = 0
        return_values['ice_tro_fir_elect_cons'] = 0
        return_values['flow_violation'] = 0        
    

    ##Populating return values in the DataFrame format for ease of display 
    return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])        
    
    data_temp = ['ice_tro_fir_max_flow', return_values['ice_tro_fir_max_flow'], 'm3/h']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)   
    data_temp = ['ice_tro_fir_delp', return_values['ice_tro_fir_delp'], 'm3/h']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
    data_temp = ['ice_tro_fir_elect_cons', return_values['ice_tro_fir_elect_cons'], 'm3/h']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  

    data_temp = ['flow_violation', return_values['flow_violation'], '%']    
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)
         
        
    ##Calculating the temperature outlet from the distribution network 
    ##This is with the assumption that all the heat is transferred to the substations.
    
    ##Converting all flowrates to kg/s
    gv2_flow_kgs = (gv2_flow / 3600) * 998.2
    hsb_flow_kgs = (hsb_flow / 3600) * 998.2
    pfa_flow_kgs = (pfa_flow / 3600) * 998.2
    ser_flow_kgs = (ser_flow / 3600) * 998.2

    if gv2_flow_kgs != 0:
        gv2_tout = (consumer_demand[0] / (gv2_flow_kgs * 4.2)) + tin_dist_nwk
    else:
        gv2_tout = -1   
        
    if hsb_flow_kgs != 0:   
        hsb_tout = (consumer_demand[1] / (hsb_flow_kgs * 4.2)) + tin_dist_nwk
    else:
        hsb_tout = -1        
        
    if pfa_flow_kgs != 0:
        pfa_tout = (consumer_demand[2] / (pfa_flow_kgs * 4.2)) + tin_dist_nwk
    else:
        pfa_tout = -1           
        
    if ser_flow_kgs != 0:
        ser_tout = (consumer_demand[3] / (ser_flow_kgs * 4.2)) + tin_dist_nwk
    else:
        ser_tout = -1
        
        
    return_values['gv2_tout'] = gv2_tout
    return_values['hsb_tout'] = hsb_tout
    return_values['pfa_tout'] = pfa_tout
    return_values['ser_tout'] = ser_tout

    data_temp = ['gv2_tout', return_values['gv2_tout'], 'K']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)          
    data_temp = ['hsb_tout', return_values['hsb_tout'], 'K']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
    data_temp = ['pfa_tout', return_values['pfa_tout'], 'K']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
    data_temp = ['ser_tout', return_values['ser_tout'], 'K']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)   

    tout_gv2xperc_split = 0
    tout_hsbxperc_split = 0
    tout_pfaxperc_split = 0
    tout_serxperc_split = 0

    if perc_split[0] != 0:
        tout_gv2xperc_split = (perc_split[0]*gv2_tout)
    if perc_split[1] != 0:
        tout_hsbxperc_split = (perc_split[1]*hsb_tout)
    if perc_split[2] != 0:
        tout_pfaxperc_split = (perc_split[2]*pfa_tout)
    if perc_split[3] != 0:
        tout_serxperc_split = (perc_split[3]*ser_tout)

    
    tout_dist_nwk =  tout_gv2xperc_split + tout_hsbxperc_split + tout_pfaxperc_split + tout_serxperc_split
    return_values['tout_dist_nwk'] = tout_dist_nwk
    data_temp = ['tout_dist_nwk', return_values['tout_dist_nwk'], 'K']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)      
        
    return return_values, return_values_df