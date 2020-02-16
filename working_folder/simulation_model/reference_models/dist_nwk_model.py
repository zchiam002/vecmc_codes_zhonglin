def dist_nwk_org (consumer_demand, m_total, perc_split, nwk_pump_select, tin_dist_nwk):
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\add_on_functions\\')
    from golden_section import golden_section_dist 
    from dist_network_models_sub import dist_nwk_pump_select
    import pandas as pd
    
    ##consumer_demand[0] --- gv2_demand (kWh)
    ##consumer_demand[1] --- hsb_demand (kWh)
    ##consumer_demand[2] --- pfa_demand (kWh)
    ##consumer_demand[3] --- ser_demand (kWh)
    ##consumer_demand[4] --- fir_demand (kWh)
    
    ##m_total --- the total flowrate throught the entire network (m3/h)
    
    ##perc_split[0] --- the split of flowrate to gv2 (%)
    ##perc_split[1] --- the split of flowrate to hsb (%)
    ##perc_split[2] --- the split of flowrate to pfa (%)
    ##perc_split[3] --- the split of flowrate to ser (%)
    ##perc_split[4] --- the split of flowrate to fir (%)

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
    fir_coeff = 0.005697674418604649
    
    ##Preparing the flowrates 
    gv2_flow = perc_split[0] * m_total
    hsb_flow = perc_split[1] * m_total
    pfa_flow = perc_split[2] * m_total
    ser_flow = perc_split[3] * m_total
    fir_flow = perc_split[4] * m_total

    ice_flow = gv2_flow + hsb_flow 
    tro_flow = pfa_flow + ser_flow 

    ##Obtaining pump parameters 
    network_pump_param = dist_nwk_pump_select(nwk_pump_select)
    
    ##Maximum flow, to act as bounds for the search based function 
    max_flow = 1300
    
    ##Checking which network choice 
    
    ##All individual branches served by their own pumps
    if network_pump_param['nwk_choice'] == 0:
        ##ice_branch calcualtions 
        
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        delp_ice_sys = max(gv2_delp, hsb_delp)
        ##This is true based on the current split ratio
        ice_sys_coeff = delp_ice_sys / pow(ice_flow, 1.852)
        ice_flow_bounds = [0, max_flow]
        ##Using the golden section to determine the intersection point of the system and pump curves
        ice_max_sys_flow = golden_section_dist(pump_sys_int_dist, ice_flow_bounds, ice_sys_coeff, network_pump_param['ice_branch_pump_delp'])
        ice_max_elect_cons = (network_pump_param['ice_branch_pump_elect'][0] * pow(ice_max_sys_flow, 3)) + (network_pump_param['ice_branch_pump_elect'][1] * pow(ice_max_sys_flow, 2)) + (network_pump_param['ice_branch_pump_elect'][2] * ice_max_sys_flow) + network_pump_param['ice_branch_pump_elect'][3]
        ##Assuming linear relationship with flowrate 
        if ice_max_sys_flow != 0:
            ice_pump_elect_cons = (ice_max_elect_cons / ice_max_sys_flow) * ice_flow
        else:
            ice_pump_elect_cons = 0

        return_values['ice_max_flow'] = ice_max_sys_flow
        return_values['ice_delp'] = delp_ice_sys
        return_values['ice_elect_cons'] = ice_pump_elect_cons

        ##tro_branch calcualtions 
        
        ##Determining the composite system curve parameters 
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        delp_tro_sys = max(pfa_delp, ser_delp)
        ##This is true based on the current split ratio
        tro_sys_coeff = delp_tro_sys / pow(tro_flow, 1.852)
        tro_flow_bounds = [0, max_flow]
        ##Using the golden section to determine the intersection point of the system and pump curves
        tro_max_sys_flow = golden_section_dist(pump_sys_int_dist, tro_flow_bounds, tro_sys_coeff, network_pump_param['tro_branch_pump_delp'])
        tro_max_elect_cons = (network_pump_param['tro_branch_pump_elect'][0] * pow(tro_max_sys_flow, 3)) + (network_pump_param['tro_branch_pump_elect'][1] * pow(tro_max_sys_flow, 2)) + (network_pump_param['tro_branch_pump_elect'][2] * tro_max_sys_flow) + network_pump_param['tro_branch_pump_elect'][3]
        ##Assuming linear relationship with flowrate 
        if tro_max_sys_flow != 0:
            tro_pump_elect_cons = (tro_max_elect_cons / tro_max_sys_flow) * tro_flow
        else:
            tro_pump_elect_cons = 0

        return_values['tro_max_flow'] = tro_max_sys_flow
        return_values['tro_delp'] = delp_tro_sys
        return_values['tro_elect_cons'] = tro_pump_elect_cons

        ##fir_branch calculations 
        
        delp_fir_sys = fir_coeff * pow(fir_flow, 1.852)
        fir_flow_bounds = [0, max_flow]
        ##Using the golden section to determine the intersection point of the system and pump curves 
        fir_max_sys_flow = golden_section_dist(pump_sys_int_dist, fir_flow_bounds, fir_coeff, network_pump_param['fir_branch_pump_delp'])
        fir_max_elect_cons = (network_pump_param['fir_branch_pump_elect'][0] * pow(fir_max_sys_flow, 3)) + (network_pump_param['fir_branch_pump_elect'][1] * pow(fir_max_sys_flow, 2)) + (network_pump_param['fir_branch_pump_elect'][2] * fir_max_sys_flow) + network_pump_param['fir_branch_pump_elect'][3]
        ##Assuming linear relationship with flowrate 
        if fir_max_sys_flow != 0:
            fir_pump_elect_cons = (fir_max_elect_cons / fir_max_sys_flow) * fir_flow
        else:
            fir_pump_elect_cons = 0

        return_values['fir_max_flow'] = fir_max_sys_flow
        return_values['fir_delp'] = delp_fir_sys
        return_values['fir_elect_cons'] = fir_pump_elect_cons        
        
        ##Populating return values in the DataFrame format for ease of display 
        return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
        
        data_temp = ['ice_max_flow', return_values['ice_max_flow'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)   
        data_temp = ['ice_delp', return_values['ice_delp'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
        data_temp = ['ice_elect_cons', return_values['ice_elect_cons'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)      
        
        data_temp = ['tro_max_flow', return_values['tro_max_flow'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)   
        data_temp = ['tro_delp', return_values['tro_delp'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
        data_temp = ['tro_elect_cons', return_values['tro_elect_cons'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
        
        data_temp = ['fir_max_flow', return_values['fir_max_flow'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)   
        data_temp = ['fir_delp', return_values['fir_delp'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
        data_temp = ['fir_elect_cons', return_values['fir_elect_cons'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
        
    ##ice and tro share pumps, fir has its own pump
    elif network_pump_param['nwk_choice'] == 1:
        ##ice_tro_branch calcualtions
        
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))        
        delp_ice_tro_sys = max(gv2_delp, hsb_delp, pfa_delp, ser_delp)
        
        ##This is true based on the current split ratio
        ice_tro_sys_coeff = delp_ice_tro_sys / pow(ice_flow + tro_flow, 1.852)
        ice_tro_flow_bounds = [0, max_flow]
        
        ##Using the golden section to determine the intersection point of the system and pump curves
        ice_tro_max_sys_flow = golden_section_dist(pump_sys_int_dist, ice_tro_flow_bounds, ice_tro_sys_coeff, network_pump_param['ice_tro_branch_pump_delp'])
        ice_tro_max_elect_cons = (network_pump_param['ice_tro_branch_pump_elect'][0] * pow(ice_tro_max_sys_flow, 3)) + (network_pump_param['ice_tro_branch_pump_elect'][1] * pow(ice_tro_max_sys_flow, 2)) + (network_pump_param['ice_tro_branch_pump_elect'][2] * ice_tro_max_sys_flow) + network_pump_param['ice_tro_branch_pump_elect'][3]
        ##Assuming linear relationship with flowrate 
        if ice_tro_max_sys_flow != 0:
            ice_tro_pump_elect_cons = (ice_tro_max_elect_cons / ice_tro_max_sys_flow) * (ice_flow + tro_flow)
        else:
            ice_tro_pump_elect_cons = 0

        return_values['ice_tro_max_flow'] = ice_tro_max_sys_flow
        return_values['ice_tro_delp'] = delp_ice_tro_sys
        return_values['ice_tro_elect_cons'] = ice_tro_pump_elect_cons        

        ##fir_branch calculations 
        
        delp_fir_sys = fir_coeff * pow(fir_flow, 1.852)
        fir_flow_bounds = [0, max_flow]
        ##Using the golden section to determine the intersection point of the system and pump curves 
        fir_max_sys_flow = golden_section_dist(pump_sys_int_dist, fir_flow_bounds, fir_coeff, network_pump_param['fir_branch_pump_delp'])
        fir_max_elect_cons = (network_pump_param['fir_branch_pump_elect'][0] * pow(fir_max_sys_flow, 3)) + (network_pump_param['fir_branch_pump_elect'][1] * pow(fir_max_sys_flow, 2)) + (network_pump_param['fir_branch_pump_elect'][2] * fir_max_sys_flow) + network_pump_param['fir_branch_pump_elect'][3]
        ##Assuming linear relationship with flowrate 
        if fir_max_sys_flow != 0:
            fir_pump_elect_cons = (fir_max_elect_cons / fir_max_sys_flow) * fir_flow
        else:
            fir_pump_elect_cons = 0

        return_values['fir_max_flow'] = fir_max_sys_flow
        return_values['fir_delp'] = delp_fir_sys
        return_values['fir_elect_cons'] = fir_pump_elect_cons  

        ##Populating return values in the DataFrame format for ease of display 
        return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])

        data_temp = ['ice_tro_max_flow', return_values['ice_tro_max_flow'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)   
        data_temp = ['ice_tro_delp', return_values['ice_tro_delp'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
        data_temp = ['ice_tro_elect_cons', return_values['ice_tro_elect_cons'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
        
        data_temp = ['fir_max_flow', return_values['fir_max_flow'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)   
        data_temp = ['fir_delp', return_values['fir_delp'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
        data_temp = ['fir_elect_cons', return_values['fir_elect_cons'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)
        
    ##ice is served by its own pump, tro and fir share pumps   
    elif network_pump_param['nwk_choice'] == 2:
        ##ice_branch calcualtions 
        
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        delp_ice_sys = max(gv2_delp, hsb_delp)
        ##This is true based on the current split ratio
        ice_sys_coeff = delp_ice_sys / pow(ice_flow, 1.852)
        ice_flow_bounds = [0, max_flow]
        ##Using the golden section to determine the intersection point of the system and pump curves
        ice_max_sys_flow = golden_section_dist(pump_sys_int_dist, ice_flow_bounds, ice_sys_coeff, network_pump_param['ice_branch_pump_delp'])
        ice_max_elect_cons = (network_pump_param['ice_branch_pump_elect'][0] * pow(ice_max_sys_flow, 3)) + (network_pump_param['ice_branch_pump_elect'][1] * pow(ice_max_sys_flow, 2)) + (network_pump_param['ice_branch_pump_elect'][2] * ice_max_sys_flow) + network_pump_param['ice_branch_pump_elect'][3]
        ##Assuming linear relationship with flowrate 
        if ice_max_sys_flow != 0:
            ice_pump_elect_cons = (ice_max_elect_cons / ice_max_sys_flow) * ice_flow
        else:
            ice_pump_elect_cons = 0

        return_values['ice_max_flow'] = ice_max_sys_flow
        return_values['ice_delp'] = delp_ice_sys
        return_values['ice_elect_cons'] = ice_pump_elect_cons        
        
        ##tro_fir_branch calcualtions 
        
        ##Determining the composite system curve parameters 
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))        
        fir_delp = fir_coeff * pow(fir_flow, 1.852)
        delp_tro_fir_sys = max(pfa_delp, ser_delp, fir_delp)
        ##This is true based on the current split ratio
        tro_fir_sys_coeff = delp_tro_fir_sys / pow(tro_flow + fir_flow, 1.852)
        tro_fir_flow_bounds = [0, max_flow]
        ##Using the golden section to determine the intersection point of the system and pump curves
        tro_fir_max_sys_flow = golden_section_dist(pump_sys_int_dist, tro_fir_flow_bounds, tro_fir_sys_coeff, network_pump_param['tro_fir_branch_pump_delp'])
        tro_fir_max_elect_cons = (network_pump_param['tro_fir_branch_pump_elect'][0] * pow(tro_fir_max_sys_flow, 3)) + (network_pump_param['tro_fir_branch_pump_elect'][1] * pow(tro_fir_max_sys_flow, 2)) + (network_pump_param['tro_fir_branch_pump_elect'][2] * tro_fir_max_sys_flow) + network_pump_param['tro_fir_branch_pump_elect'][3]
        ##Assuming linear relationship with flowrate 
        if tro_fir_max_sys_flow != 0:
            tro_fir_pump_elect_cons = (tro_fir_max_elect_cons / tro_fir_max_sys_flow) * (tro_flow + fir_flow)
        else:
            tro_fir_pump_elect_cons = 0

        return_values['tro_fir_max_flow'] = tro_fir_max_sys_flow
        return_values['tro_fir_delp'] = delp_tro_fir_sys
        return_values['tro_fir_elect_cons'] = tro_fir_pump_elect_cons   
     
        ##Populating return values in the DataFrame format for ease of display 
        return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])        
        
        data_temp = ['ice_max_flow', return_values['ice_max_flow'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)   
        data_temp = ['ice_delp', return_values['ice_delp'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
        data_temp = ['ice_elect_cons', return_values['ice_elect_cons'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)      
        
        data_temp = ['tro_fir_max_flow', return_values['tro_fir_max_flow'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)   
        data_temp = ['tro_fir_delp', return_values['tro_fir_delp'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)  
        data_temp = ['tro_fir_elect_cons', return_values['tro_fir_elect_cons'], 'm3/h']
        data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
        return_values_df = return_values_df.append(data_temp_df, ignore_index = True)          
      
    ##All networks share the same pump
    elif network_pump_param['nwk_choice'] == 3:

        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))        
        fir_delp = fir_coeff * pow(fir_flow, 1.852)    
        delp_ice_tro_fir_sys = max(gv2_delp, hsb_delp, pfa_delp, ser_delp, fir_delp)
        ##This is true based on the current split ratio
        ice_tro_fir_sys_coeff = delp_ice_tro_fir_sys / pow(ice_flow + tro_flow + fir_flow, 1.852)
        ice_tro_fir_flow_bounds = [0, max_flow]
        ##Using the golden section to determine the intersection point of the system and pump curves
        ice_tro_fir_max_sys_flow = golden_section_dist(pump_sys_int_dist, ice_tro_fir_flow_bounds, ice_tro_fir_sys_coeff, network_pump_param['ice_tro_fir_branch_pump_delp'])
        ice_tro_fir_max_elect_cons = (network_pump_param['ice_tro_fir_branch_pump_elect'][0] * pow(ice_tro_fir_max_sys_flow, 3)) + (network_pump_param['ice_tro_fir_branch_pump_elect'][1] * pow(ice_tro_fir_max_sys_flow, 2)) + (network_pump_param['ice_tro_fir_branch_pump_elect'][2] * ice_tro_fir_max_sys_flow) + network_pump_param['ice_tro_fir_branch_pump_elect'][3]
        
        ##Assuming linear relationship with flowrate 
        if ice_tro_fir_max_sys_flow != 0:
            ice_tro_fir_pump_elect_cons = (ice_tro_fir_max_elect_cons / ice_tro_fir_max_sys_flow) * (ice_flow + tro_flow + fir_flow)
        else:
            ice_tro_fir_pump_elect_cons = 0

        return_values['ice_tro_fir_max_flow'] = ice_tro_fir_max_sys_flow
        return_values['ice_tro_fir_delp'] = delp_ice_tro_fir_sys
        return_values['ice_tro_fir_elect_cons'] = ice_tro_fir_pump_elect_cons  

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
        
    ##Calculating the temperature outlet from the distribution network 
    ##This is with the assumption that all the heat is transferred to the substations.
    
    ##Converting all flowrates to kg/s
    gv2_flow_kgs = (gv2_flow / 3600) * 998.2
    hsb_flow_kgs = (hsb_flow / 3600) * 998.2
    pfa_flow_kgs = (pfa_flow / 3600) * 998.2
    ser_flow_kgs = (ser_flow / 3600) * 998.2
    fir_flow_kgs = (fir_flow / 3600) * 998.2

    if gv2_flow_kgs != 0:
        gv2_tout = (consumer_demand[0] / (gv2_flow_kgs * 4.2)) + tin_dist_nwk
    else:
        gv2_tout = 'undefined'   
        
    if hsb_flow_kgs != 0:   
        hsb_tout = (consumer_demand[1] / (hsb_flow_kgs * 4.2)) + tin_dist_nwk
    else:
        hsb_tout = 'undefined'        
        
    if pfa_flow_kgs != 0:
        pfa_tout = (consumer_demand[2] / (pfa_flow_kgs * 4.2)) + tin_dist_nwk
    else:
        pfa_tout = 'undefined'           
        
    if ser_flow_kgs != 0:
        ser_tout = (consumer_demand[3] / (ser_flow_kgs * 4.2)) + tin_dist_nwk
    else:
        ser_tout = 'undefined'
           
    if fir_flow_kgs != 0:
        fir_tout = (consumer_demand[4] / (fir_flow_kgs * 4.2)) + tin_dist_nwk
    else:
        fir_tout = 'undefined'
        
    return_values['gv2_tout'] = gv2_tout
    return_values['hsb_tout'] = hsb_tout
    return_values['pfa_tout'] = pfa_tout
    return_values['ser_tout'] = ser_tout
    return_values['fir_tout'] = fir_tout

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
    data_temp = ['fir_tout', return_values['fir_tout'], 'K']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True) 

    tout_gv2xperc_split = 0
    tout_hsbxperc_split = 0
    tout_pfaxperc_split = 0
    tout_serxperc_split = 0
    tout_firxperc_split = 0

    if perc_split[0] != 0:
        tout_gv2xperc_split = (perc_split[0]*gv2_tout)
    if perc_split[1] != 0:
        tout_hsbxperc_split = (perc_split[1]*hsb_tout)
    if perc_split[2] != 0:
        tout_pfaxperc_split = (perc_split[2]*pfa_tout)
    if perc_split[3] != 0:
        tout_serxperc_split = (perc_split[3]*ser_tout)
    if perc_split[4] != 0:
        tout_firxperc_split = (perc_split[4]*fir_tout)
    
    tout_dist_nwk =  tout_gv2xperc_split + tout_hsbxperc_split + tout_pfaxperc_split + tout_serxperc_split + tout_firxperc_split
    return_values['tout_dist_nwk'] = tout_dist_nwk
    data_temp = ['tout_dist_nwk', return_values['tout_dist_nwk'], 'K']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)      
        
    return return_values, return_values_df