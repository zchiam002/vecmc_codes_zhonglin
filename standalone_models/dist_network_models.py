##This script contains all the distribution network models, the input and output of all the models should be the same 
##The entire model is built based on 

##Condenser side 

##Model 1: Original distribution network model 
##Model 2: Piecewise linearization of pressure drop 
##Model 3: Regression of pump and network electricity consumption
##Model 4: Lp relaxation of the temperature mixing  

##Model 1: Original distribution network model 
def dist_nwk_org (consumer_demand, m_total, perc_split, nwk_pump_select, tin_dist_nwk):

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
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'      
    import sys 
    sys.path.append(current_path + 'add_on_functions\\')
    from golden_section import golden_section_dist 
    from dist_network_models_sub import dist_nwk_pump_select
    import pandas as pd
    
    ##Dictionary for housing the return values
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

###############################################################################################################################################################################
############################################################################################################################################################################### 
##Model 2: Piecewise linearization of pressure drop 
def dist_nwk_piecewise_pressure (consumer_demand, m_total, perc_split, nwk_pump_select, tin_dist_nwk, steps):
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'      
    import sys 
    sys.path.append(current_path + 'add_on_functions\\')
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
    
    ##steps --- number of linear pieces
    
    return_values = {}
    tighter_flow_upper_bounds = pd.DataFrame(columns = ['Nwk_pump_select', 'Name', 'Value'])
    
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
    
    ##Refercence flow 
    ref_flow = 500                  ##Just need a non-zero flowrate for calculating the pressure coefficients
    max_flow = 3200                 ##for the use with the golden_section search function
    
    ##Checking which network choice
    
    ##All branches served by their own pumps 
    if network_pump_param['nwk_choice'] == 0:
        
        ##ice network 
        
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        
        ##Expressing hsb flowrate in terms of gv2 flowrate
        mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
        ##Expressing total flowrate as a function as gv2 flowrate
        mgv2_intermsof_mice_coeff = 1 + mhsb_intermsof_mgv2_coeff
        
        total_flow = ref_flow 
        gv2_flow_temp = total_flow / mgv2_intermsof_mice_coeff
        pressure = ice_main_coeff*pow(total_flow, 1.852) +  gv2_coeff*pow(gv2_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]
        
        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['ice_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'ice_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        delp_ice_sys = max(gv2_delp, hsb_delp)
        ##This is true based on the current split ratio
        ice_sys_coeff = delp_ice_sys / pow(ice_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(ice_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, ice_flow)
        ##Finding the intersection between the pwl pieces and the pump curve at max rpm
        intersect_data = pwl_pieces_pump_int (pwl_table, network_pump_param['ice_branch_pump_delp'])
        ##Finding the maximum electricity 
        ice_max_sys_flow = intersect_data[0]
        ice_max_elect_cons = (network_pump_param['ice_branch_pump_elect'][0] * pow(ice_max_sys_flow, 3)) + (network_pump_param['ice_branch_pump_elect'][1] * pow(ice_max_sys_flow, 2)) + (network_pump_param['ice_branch_pump_elect'][2] * ice_max_sys_flow) + network_pump_param['ice_branch_pump_elect'][3]        

        ##Assuming linear relationship with flowrate 
        if ice_max_sys_flow != 0:
            ice_pump_elect_cons = (ice_max_elect_cons / ice_max_sys_flow) * ice_flow
        else:
            ice_pump_elect_cons = 0
        
        return_values['ice_max_flow'] = ice_max_sys_flow
        return_values['ice_delp'] = est_pressure
        return_values['ice_elect_cons'] = ice_pump_elect_cons

        ##tro network 

        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        
        ##Expressing ser flowrate in terms of pfa flowrate 
        mser_intermsof_mpfa_coeff = pow(pfa_coeff / ser_coeff, 1/1.852)
        ##Expressing total flowrate as a function as pfa flowrate
        mpfa_intermsof_mtro_coeff = 1 + mser_intermsof_mpfa_coeff        
        
        total_flow = ref_flow 
        pfa_flow_temp = total_flow / mpfa_intermsof_mtro_coeff
        pressure = tro_main_coeff*pow(total_flow, 1.852) +  pfa_coeff*pow(pfa_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]        

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['tro_branch_pump_delp'])        

        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1

        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'tro_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)   
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        delp_tro_sys = max(pfa_delp, ser_delp)
        ##This is true based on the current split ratio
        tro_sys_coeff = delp_tro_sys / pow(tro_flow, 1.852)        
        pwl_table = pwl_generate_table_pressure(tro_sys_coeff, 0, max_config_flow, steps)        
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, tro_flow)        
        ##Finding the intersection between the pwl pieces and the pump curve at max rpm
        intersect_data = pwl_pieces_pump_int (pwl_table, network_pump_param['tro_branch_pump_delp'])
        ##Finding the maximum electricity 
        tro_max_sys_flow = intersect_data[0]
        tro_max_elect_cons = (network_pump_param['tro_branch_pump_elect'][0] * pow(tro_max_sys_flow, 3)) + (network_pump_param['tro_branch_pump_elect'][1] * pow(tro_max_sys_flow, 2)) + (network_pump_param['tro_branch_pump_elect'][2] * tro_max_sys_flow) + network_pump_param['tro_branch_pump_elect'][3]  

        ##Assuming linear relationship with flowrate 
        if tro_max_sys_flow != 0:
            tro_pump_elect_cons = (tro_max_elect_cons / tro_max_sys_flow) * tro_flow
        else:
            tro_pump_elect_cons = 0
        
        return_values['tro_max_flow'] = tro_max_sys_flow
        return_values['tro_delp'] = est_pressure
        return_values['tro_elect_cons'] = tro_pump_elect_cons

        ##fir network 

        ##Finding a tighter upper bound 
        ##determining the lowest pressure case, this is just a single curve 
        search_bounds = [0, max_flow]                 

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, fir_coeff, network_pump_param['fir_branch_pump_delp'])      
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'fir_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)  
        
        ##Generating the pwl table 
        pwl_table = pwl_generate_table_pressure(fir_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, fir_flow)                    
        ##Finding the intersection between the pwl pieces and the pump curve at max rpm
        intersect_data = pwl_pieces_pump_int (pwl_table, network_pump_param['fir_branch_pump_delp'])
        ##Finding the maximum electricity 
        fir_max_sys_flow = intersect_data[0]
        fir_max_elect_cons = (network_pump_param['fir_branch_pump_elect'][0] * pow(fir_max_sys_flow, 3)) + (network_pump_param['fir_branch_pump_elect'][1] * pow(fir_max_sys_flow, 2)) + (network_pump_param['fir_branch_pump_elect'][2] * fir_max_sys_flow) + network_pump_param['fir_branch_pump_elect'][3]
  
        ##Assuming linear relationship with flowrate 
        if fir_max_sys_flow != 0:
            fir_pump_elect_cons = (fir_max_elect_cons / fir_max_sys_flow) * fir_flow
        else:
            fir_pump_elect_cons = 0
        
        return_values['fir_max_flow'] = fir_max_sys_flow
        return_values['fir_delp'] = est_pressure
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
    
    ##ice and tro share pumps, fir is served by own pump
    elif network_pump_param['nwk_choice'] == 1:
        
        ##ice and tro network 
        
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        ##Expressing hsb flowrate in terms of gv2 flowrate
        mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
        ##Expressing pfa flowrate in terms of gv2 flowrate 
        term1 = pow(gv2_coeff/hsb_coeff, 1/1.852)
        term2 = ice_main_coeff*pow(1 + term1, 1.852) + gv2_coeff
        term3 = pow(pfa_coeff/ser_coeff, 1/1.852)
        term4 = tro_main_coeff*pow(1 + term3, 1.852) + pfa_coeff
        mpfa_intermaof_mgv2_coeff = pow(term2/term4, 1/1.852)
        ##Expressing ser flowrate in terms of gv2 flowrate 
        term5 = pow(ser_coeff/pfa_coeff, 1/1.852)
        term6 = tro_main_coeff*pow(1 + term5, 1.852) + ser_coeff
        mser_intermsof_mgv2_coeff = pow(term2/term6, 1/1.852)
        ##Expressing total flowrate as a function as gv2 flowrate
        mgv2_intermsof_miceandmtro_coeff = 1 + mhsb_intermsof_mgv2_coeff + mpfa_intermaof_mgv2_coeff + mser_intermsof_mgv2_coeff        
        
        total_flow = ref_flow 
        gv2_flow_temp = total_flow / mgv2_intermsof_miceandmtro_coeff
        pressure = ice_main_coeff*pow(total_flow, 1.852) +  gv2_coeff*pow(gv2_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['ice_tro_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'ice_tro_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        delp_ice_tro_sys = max(gv2_delp, hsb_delp, pfa_delp, ser_delp)
        ##This is true based on the current split ratio
        ice_tro_sys_coeff = delp_ice_tro_sys / pow(ice_flow + tro_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(ice_tro_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, ice_flow + tro_flow)
        ##Finding the intersection between the pwl pieces and the pump curve at max rpm
        intersect_data = pwl_pieces_pump_int (pwl_table, network_pump_param['ice_tro_branch_pump_delp'])
        ##Finding the maximum electricity 
        ice_tro_max_sys_flow = intersect_data[0]
        ice_tro_max_elect_cons = (network_pump_param['ice_tro_branch_pump_elect'][0] * pow(ice_tro_max_sys_flow, 3)) + (network_pump_param['ice_tro_branch_pump_elect'][1] * pow(ice_tro_max_sys_flow, 2)) + (network_pump_param['ice_tro_branch_pump_elect'][2] * ice_tro_max_sys_flow) + network_pump_param['ice_tro_branch_pump_elect'][3] 


        ##Assuming linear relationship with flowrate 
        if ice_tro_max_sys_flow != 0:
            ice_tro_pump_elect_cons = (ice_tro_max_elect_cons / ice_tro_max_sys_flow) * (ice_flow + tro_flow)
        else:
            ice_tro_pump_elect_cons = 0
        
        return_values['ice_tro_max_flow'] = ice_tro_max_sys_flow
        return_values['ice_tro_delp'] = est_pressure
        return_values['ice_tro_elect_cons'] = ice_tro_pump_elect_cons   

        ##fir network 

        ##Finding a tighter upper bound 
        ##determining the lowest pressure case, this is just a single curve 
        search_bounds = [0, max_flow]                 

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, fir_coeff, network_pump_param['fir_branch_pump_delp'])      
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'fir_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)  
        
        ##Generating the pwl table 
        pwl_table = pwl_generate_table_pressure(fir_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, fir_flow)                    
        ##Finding the intersection between the pwl pieces and the pump curve at max rpm
        intersect_data = pwl_pieces_pump_int (pwl_table, network_pump_param['fir_branch_pump_delp'])
        ##Finding the maximum electricity 
        fir_max_sys_flow = intersect_data[0]
        fir_max_elect_cons = (network_pump_param['fir_branch_pump_elect'][0] * pow(fir_max_sys_flow, 3)) + (network_pump_param['fir_branch_pump_elect'][1] * pow(fir_max_sys_flow, 2)) + (network_pump_param['fir_branch_pump_elect'][2] * fir_max_sys_flow) + network_pump_param['fir_branch_pump_elect'][3]
  
        ##Assuming linear relationship with flowrate 
        if fir_max_sys_flow != 0:
            fir_pump_elect_cons = (fir_max_elect_cons / fir_max_sys_flow) * fir_flow
        else:
            fir_pump_elect_cons = 0
        
        return_values['fir_max_flow'] = fir_max_sys_flow
        return_values['fir_delp'] = est_pressure
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

        ##ice network 
        
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        
        ##Expressing hsb flowrate in terms of gv2 flowrate
        mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
        ##Expressing total flowrate as a function as gv2 flowrate
        mgv2_intermsof_mice_coeff = 1 + mhsb_intermsof_mgv2_coeff
        
        total_flow = ref_flow 
        gv2_flow_temp = total_flow / mgv2_intermsof_mice_coeff
        pressure = ice_main_coeff*pow(total_flow, 1.852) +  gv2_coeff*pow(gv2_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]
        
        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['ice_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'ice_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        delp_ice_sys = max(gv2_delp, hsb_delp)
        ##This is true based on the current split ratio
        ice_sys_coeff = delp_ice_sys / pow(ice_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(ice_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, ice_flow)
        ##Finding the intersection between the pwl pieces and the pump curve at max rpm
        intersect_data = pwl_pieces_pump_int (pwl_table, network_pump_param['ice_branch_pump_delp'])
        ##Finding the maximum electricity 
        ice_max_sys_flow = intersect_data[0]
        ice_max_elect_cons = (network_pump_param['ice_branch_pump_elect'][0] * pow(ice_max_sys_flow, 3)) + (network_pump_param['ice_branch_pump_elect'][1] * pow(ice_max_sys_flow, 2)) + (network_pump_param['ice_branch_pump_elect'][2] * ice_max_sys_flow) + network_pump_param['ice_branch_pump_elect'][3]        

        ##Assuming linear relationship with flowrate 
        if ice_max_sys_flow != 0:
            ice_pump_elect_cons = (ice_max_elect_cons / ice_max_sys_flow) * ice_flow
        else:
            ice_pump_elect_cons = 0
        
        return_values['ice_max_flow'] = ice_max_sys_flow
        return_values['ice_delp'] = est_pressure
        return_values['ice_elect_cons'] = ice_pump_elect_cons

        ##tro and fir network 
        
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        ##Expresing ser flowrate in terms of pfa flowrate 
        mser_intermsof_mpfa_coeff = pow(pfa_coeff / ser_coeff, 1/1.852)
        ##Expressing fir flowrate in terms of pfa flowrate 
        term1 = pow(pfa_coeff/ser_coeff, 1/1.852)
        term2 = tro_main_coeff*pow(1 + term1, 1.852) + pfa_coeff
        mfir_intermsof_mpfa_coeff = pow(term2/fir_coeff, 1/1.852)
        ##Expressing total flowrate as a function of pfa flowrate 
        mtrofir_intermsof_mpfa_coeff = 1 + mser_intermsof_mpfa_coeff + mfir_intermsof_mpfa_coeff      
        
        total_flow = ref_flow 
        pfa_flow_temp = total_flow / mtrofir_intermsof_mpfa_coeff
        pressure = tro_main_coeff*pow(total_flow, 1.852) +  pfa_coeff*pow(pfa_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['tro_fir_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'tro_fir_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        fir_delp = fir_coeff * pow(fir_flow, 1.852)
        delp_tro_fir_sys = max(pfa_delp, ser_delp, fir_delp)
        ##This is true based on the current split ratio
        tro_fir_sys_coeff = delp_tro_fir_sys / pow(tro_flow + fir_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(tro_fir_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, tro_flow + fir_flow)
        ##Finding the intersection between the pwl pieces and the pump curve at max rpm
        intersect_data = pwl_pieces_pump_int (pwl_table, network_pump_param['tro_fir_branch_pump_delp'])
        ##Finding the maximum electricity 
        tro_fir_max_sys_flow = intersect_data[0]
        tro_fir_max_elect_cons = (network_pump_param['tro_fir_branch_pump_elect'][0] * pow(tro_fir_max_sys_flow, 3)) + (network_pump_param['tro_fir_branch_pump_elect'][1] * pow(tro_fir_max_sys_flow, 2)) + (network_pump_param['tro_fir_branch_pump_elect'][2] * tro_fir_max_sys_flow) + network_pump_param['tro_fir_branch_pump_elect'][3] 


        ##Assuming linear relationship with flowrate 
        if tro_fir_max_sys_flow != 0:
            tro_fir_pump_elect_cons = (tro_fir_max_elect_cons / tro_fir_max_sys_flow) * (tro_flow + fir_flow)
        else:
            tro_fir_pump_elect_cons = 0
        
        return_values['tro_fir_max_flow'] = tro_fir_max_sys_flow
        return_values['tro_fir_delp'] = est_pressure
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
        
    ##All networks share pumps 
    elif network_pump_param['nwk_choice'] == 3:   
        
        ##ice, tro and fir network 
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        ##Expresing hsb flowrate in terms of gv2 flowrate
        mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
        ##Expressing pfa flowrate in terms of gv2 flowrate 
        term1 = pow(gv2_coeff/hsb_coeff, 1/1.852)
        term2 = ice_main_coeff*pow(1 + term1, 1.852) + gv2_coeff
        term3 = pow(pfa_coeff/ser_coeff, 1/1.852)
        term4 = tro_main_coeff*pow(1 + term3, 1.852) + pfa_coeff
        mpfa_intermaof_mgv2_coeff = pow(term2/term4, 1/1.852)
        ##Expressing ser flowrate in terms of gv2 flowrate 
        term5 = pow(ser_coeff/pfa_coeff, 1/1.852)
        term6 = tro_main_coeff*pow(1 + term5, 1.852) + ser_coeff
        mser_intermsof_mgv2_coeff = pow(term2/term6, 1/1.852)
        ##Expressing fir flowrate in terms of gv2 flowrate 
        term7 = pow(gv2_coeff/hsb_coeff, 1/1.852)
        term8 = ice_main_coeff*pow(1 + term7, 1.852) + gv2_coeff
        mfir_intermsof_mgv2_coeff = pow(term8/fir_coeff, 1/1.852)
        ##Expressing total flowrate as a function of gv2 flowrate
        micetrofir_intermsof_mgv2_coeff = 1 + mhsb_intermsof_mgv2_coeff + mpfa_intermaof_mgv2_coeff + mser_intermsof_mgv2_coeff + mfir_intermsof_mgv2_coeff
        
        total_flow = ref_flow 
        gv2_flow_temp = total_flow / micetrofir_intermsof_mgv2_coeff
        pressure = ice_main_coeff*pow(total_flow, 1.852) +  gv2_coeff*pow(gv2_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]        

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['ice_tro_fir_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.2
        
        #print(max_config_flow)
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'ice_tro_fir_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        fir_delp = fir_coeff * pow(fir_flow, 1.852)
        delp_ice_tro_fir_sys = max(gv2_delp, hsb_delp, pfa_delp, ser_delp, fir_delp)
        ##This is true based on the current split ratio
        ice_tro_fir_sys_coeff = delp_ice_tro_fir_sys / pow(ice_flow + tro_flow + fir_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(ice_tro_fir_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, ice_flow + tro_flow + fir_flow)
        ##Finding the intersection between the pwl pieces and the pump curve at max rpm
        intersect_data = pwl_pieces_pump_int (pwl_table, network_pump_param['ice_tro_fir_branch_pump_delp'])
        ##Finding the maximum electricity 
        ice_tro_fir_max_sys_flow = intersect_data[0]
        ice_tro_fir_max_elect_cons = (network_pump_param['ice_tro_fir_branch_pump_elect'][0] * pow(ice_tro_fir_max_sys_flow, 3)) + (network_pump_param['ice_tro_fir_branch_pump_elect'][1] * pow(ice_tro_fir_max_sys_flow, 2)) + (network_pump_param['ice_tro_fir_branch_pump_elect'][2] * ice_tro_fir_max_sys_flow) + network_pump_param['ice_tro_fir_branch_pump_elect'][3] 


        ##Assuming linear relationship with flowrate 
        if ice_tro_fir_max_sys_flow != 0:
            ice_tro_fir_pump_elect_cons = (ice_tro_fir_max_elect_cons / ice_tro_fir_max_sys_flow) * (ice_flow + tro_flow + fir_flow)
        else:
            ice_tro_fir_pump_elect_cons = 0
        
        return_values['ice_tro_fir_max_flow'] = ice_tro_fir_max_sys_flow
        return_values['ice_tro_fir_delp'] = est_pressure
        return_values['ice_tro_fir_elect_cons'] = ice_tro_fir_pump_elect_cons   

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

################################################################################################################################################################
################################################################################################################################################################
##Model 3: Regression of pump and network electricity consumption  
def dist_nwk_piecewise_pressure_reg_pumpnwk(consumer_demand, m_total, perc_split, nwk_pump_select, tin_dist_nwk, steps):

    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'      
    import sys 
    sys.path.append(current_path + 'add_on_functions\\')
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
    
    ##steps --- number of linear pieces
    
    return_values = {}
    tighter_flow_upper_bounds = pd.DataFrame(columns = ['Nwk_pump_select', 'Name', 'Value'])
    
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
    
    ##Refercence flow 
    ref_flow = 500                  ##Just need a non-zero flowrate for calculating the pressure coefficients
    max_flow = 3200                 ##for the use with the golden_section search function
    
    ##Checking which network choice
    
    ##All branches served by their own pumps 
    if network_pump_param['nwk_choice'] == 0:

        ##ice network 
        
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        
        ##Expressing hsb flowrate in terms of gv2 flowrate
        mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
        ##Expressing total flowrate as a function as gv2 flowrate
        mgv2_intermsof_mice_coeff = 1 + mhsb_intermsof_mgv2_coeff
        
        total_flow = ref_flow 
        gv2_flow_temp = total_flow / mgv2_intermsof_mice_coeff
        pressure = ice_main_coeff*pow(total_flow, 1.852) +  gv2_coeff*pow(gv2_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]
        
        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['ice_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'ice_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        delp_ice_sys = max(gv2_delp, hsb_delp)
        ##This is true based on the current split ratio
        ice_sys_coeff = delp_ice_sys / pow(ice_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(ice_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, ice_flow)
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['ice_branch_pump_delp'], network_pump_param['ice_branch_pump_elect'], ice_sys_coeff)
        ##Calculating electricity consumption 
        ice_pump_elect_cons = (ret_values[0,0] * ice_flow) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['ice_max_flow'] = ret_values[3,0]
        return_values['ice_delp'] = est_pressure
        return_values['ice_elect_cons'] = ice_pump_elect_cons      

        ##tro network 

        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        
        ##Expressing ser flowrate in terms of pfa flowrate 
        mser_intermsof_mpfa_coeff = pow(pfa_coeff / ser_coeff, 1/1.852)
        ##Expressing total flowrate as a function as pfa flowrate
        mpfa_intermsof_mtro_coeff = 1 + mser_intermsof_mpfa_coeff        
        
        total_flow = ref_flow 
        pfa_flow_temp = total_flow / mpfa_intermsof_mtro_coeff
        pressure = tro_main_coeff*pow(total_flow, 1.852) +  pfa_coeff*pow(pfa_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]        

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['tro_branch_pump_delp'])        

        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1

        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'tro_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)   
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        delp_tro_sys = max(pfa_delp, ser_delp)
        ##This is true based on the current split ratio
        tro_sys_coeff = delp_tro_sys / pow(tro_flow, 1.852)        
        pwl_table = pwl_generate_table_pressure(tro_sys_coeff, 0, max_config_flow, steps)        
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, tro_flow)
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['tro_branch_pump_delp'], network_pump_param['tro_branch_pump_elect'], tro_sys_coeff)
        ##Calculating electricity consumption 
        tro_pump_elect_cons = (ret_values[0,0] * tro_flow) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['tro_max_flow'] = ret_values[3,0]
        return_values['tro_delp'] = est_pressure
        return_values['tro_elect_cons'] = tro_pump_elect_cons                                

        ##fir network 

        ##Finding a tighter upper bound 
        ##determining the lowest pressure case, this is just a single curve 
        search_bounds = [0, max_flow]                 

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, fir_coeff, network_pump_param['fir_branch_pump_delp'])      
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'fir_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)  
        
        ##Generating the pwl table 
        pwl_table = pwl_generate_table_pressure(fir_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, fir_flow)                            
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['fir_branch_pump_delp'], network_pump_param['fir_branch_pump_elect'], fir_coeff)
        ##Calculating electricity consumption 
        fir_pump_elect_cons = (ret_values[0,0] * fir_flow) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['fir_max_flow'] = ret_values[3,0]
        return_values['fir_delp'] = est_pressure
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

    ##ice and tro share pumps, fir is served by own pump
    elif network_pump_param['nwk_choice'] == 1:
        
        ##ice and tro network 
        
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        ##Expressing hsb flowrate in terms of gv2 flowrate
        mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
        ##Expressing pfa flowrate in terms of gv2 flowrate 
        term1 = pow(gv2_coeff/hsb_coeff, 1/1.852)
        term2 = ice_main_coeff*pow(1 + term1, 1.852) + gv2_coeff
        term3 = pow(pfa_coeff/ser_coeff, 1/1.852)
        term4 = tro_main_coeff*pow(1 + term3, 1.852) + pfa_coeff
        mpfa_intermaof_mgv2_coeff = pow(term2/term4, 1/1.852)
        ##Expressing ser flowrate in terms of gv2 flowrate 
        term5 = pow(ser_coeff/pfa_coeff, 1/1.852)
        term6 = tro_main_coeff*pow(1 + term5, 1.852) + ser_coeff
        mser_intermsof_mgv2_coeff = pow(term2/term6, 1/1.852)
        ##Expressing total flowrate as a function as gv2 flowrate
        mgv2_intermsof_miceandmtro_coeff = 1 + mhsb_intermsof_mgv2_coeff + mpfa_intermaof_mgv2_coeff + mser_intermsof_mgv2_coeff        
        
        total_flow = ref_flow 
        gv2_flow_temp = total_flow / mgv2_intermsof_miceandmtro_coeff
        pressure = ice_main_coeff*pow(total_flow, 1.852) +  gv2_coeff*pow(gv2_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['ice_tro_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'ice_tro_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        delp_ice_tro_sys = max(gv2_delp, hsb_delp, pfa_delp, ser_delp)
        ##This is true based on the current split ratio
        ice_tro_sys_coeff = delp_ice_tro_sys / pow(ice_flow + tro_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(ice_tro_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, ice_flow + tro_flow)
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['ice_tro_branch_pump_delp'], network_pump_param['ice_tro_branch_pump_elect'], ice_tro_sys_coeff)
        ##Calculating electricity consumption 
        ice_tro_pump_elect_cons = (ret_values[0,0] * (ice_flow + tro_flow)) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['ice_tro_max_flow'] = ret_values[3,0]
        return_values['ice_tro_delp'] = est_pressure
        return_values['ice_tro_elect_cons'] = ice_tro_pump_elect_cons    

        ##fir network 

        ##Finding a tighter upper bound 
        ##determining the lowest pressure case, this is just a single curve 
        search_bounds = [0, max_flow]                 

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, fir_coeff, network_pump_param['fir_branch_pump_delp'])      
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'fir_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)  
        
        ##Generating the pwl table 
        pwl_table = pwl_generate_table_pressure(fir_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, fir_flow)    
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['fir_branch_pump_delp'], network_pump_param['fir_branch_pump_elect'], fir_coeff)
        ##Calculating electricity consumption 
        fir_pump_elect_cons = (ret_values[0,0] * fir_flow) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['fir_max_flow'] = ret_values[3,0]
        return_values['fir_delp'] = est_pressure
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

        ##ice network 
        
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        
        ##Expressing hsb flowrate in terms of gv2 flowrate
        mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
        ##Expressing total flowrate as a function as gv2 flowrate
        mgv2_intermsof_mice_coeff = 1 + mhsb_intermsof_mgv2_coeff
        
        total_flow = ref_flow 
        gv2_flow_temp = total_flow / mgv2_intermsof_mice_coeff
        pressure = ice_main_coeff*pow(total_flow, 1.852) +  gv2_coeff*pow(gv2_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]
        
        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['ice_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'ice_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        delp_ice_sys = max(gv2_delp, hsb_delp)
        ##This is true based on the current split ratio
        ice_sys_coeff = delp_ice_sys / pow(ice_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(ice_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, ice_flow)
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['ice_branch_pump_delp'], network_pump_param['ice_branch_pump_elect'], ice_sys_coeff)
        ##Calculating electricity consumption 
        ice_pump_elect_cons = (ret_values[0,0] * ice_flow) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['ice_max_flow'] = ret_values[3,0]
        return_values['ice_delp'] = est_pressure
        return_values['ice_elect_cons'] = ice_pump_elect_cons  
                                    
        ##tro and fir network 
        
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        ##Expresing ser flowrate in terms of pfa flowrate 
        mser_intermsof_mpfa_coeff = pow(pfa_coeff / ser_coeff, 1/1.852)
        ##Expressing fir flowrate in terms of pfa flowrate 
        term1 = pow(pfa_coeff/ser_coeff, 1/1.852)
        term2 = tro_main_coeff*pow(1 + term1, 1.852) + pfa_coeff
        mfir_intermsof_mpfa_coeff = pow(term2/fir_coeff, 1/1.852)
        ##Expressing total flowrate as a function of pfa flowrate 
        mtrofir_intermsof_mpfa_coeff = 1 + mser_intermsof_mpfa_coeff + mfir_intermsof_mpfa_coeff      
        
        total_flow = ref_flow 
        pfa_flow_temp = total_flow / mtrofir_intermsof_mpfa_coeff
        pressure = tro_main_coeff*pow(total_flow, 1.852) +  pfa_coeff*pow(pfa_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['tro_fir_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'tro_fir_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        fir_delp = fir_coeff * pow(fir_flow, 1.852)
        delp_tro_fir_sys = max(pfa_delp, ser_delp, fir_delp)
        ##This is true based on the current split ratio
        tro_fir_sys_coeff = delp_tro_fir_sys / pow(tro_flow + fir_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(tro_fir_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, tro_flow + fir_flow)
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['tro_fir_branch_pump_delp'], network_pump_param['tro_fir_branch_pump_elect'], tro_fir_sys_coeff)
        ##Calculating electricity consumption 
        tro_fir_pump_elect_cons = (ret_values[0,0] * (tro_flow + fir_flow)) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['tro_fir_max_flow'] = ret_values[3,0]
        return_values['tro_fir_delp'] = est_pressure
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
        
    ##All networks share pumps 
    elif network_pump_param['nwk_choice'] == 3:         
        
        ##ice, tro and fir network 
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        ##Expresing hsb flowrate in terms of gv2 flowrate
        mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
        ##Expressing pfa flowrate in terms of gv2 flowrate 
        term1 = pow(gv2_coeff/hsb_coeff, 1/1.852)
        term2 = ice_main_coeff*pow(1 + term1, 1.852) + gv2_coeff
        term3 = pow(pfa_coeff/ser_coeff, 1/1.852)
        term4 = tro_main_coeff*pow(1 + term3, 1.852) + pfa_coeff
        mpfa_intermaof_mgv2_coeff = pow(term2/term4, 1/1.852)
        ##Expressing ser flowrate in terms of gv2 flowrate 
        term5 = pow(ser_coeff/pfa_coeff, 1/1.852)
        term6 = tro_main_coeff*pow(1 + term5, 1.852) + ser_coeff
        mser_intermsof_mgv2_coeff = pow(term2/term6, 1/1.852)
        ##Expressing fir flowrate in terms of gv2 flowrate 
        term7 = pow(gv2_coeff/hsb_coeff, 1/1.852)
        term8 = ice_main_coeff*pow(1 + term7, 1.852) + gv2_coeff
        mfir_intermsof_mgv2_coeff = pow(term8/fir_coeff, 1/1.852)
        ##Expressing total flowrate as a function of gv2 flowrate
        micetrofir_intermsof_mgv2_coeff = 1 + mhsb_intermsof_mgv2_coeff + mpfa_intermaof_mgv2_coeff + mser_intermsof_mgv2_coeff + mfir_intermsof_mgv2_coeff
        
        total_flow = ref_flow 
        gv2_flow_temp = total_flow / micetrofir_intermsof_mgv2_coeff
        pressure = ice_main_coeff*pow(total_flow, 1.852) +  gv2_coeff*pow(gv2_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]        

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['ice_tro_fir_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.2
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'ice_tro_fir_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        fir_delp = fir_coeff * pow(fir_flow, 1.852)
        delp_ice_tro_fir_sys = max(gv2_delp, hsb_delp, pfa_delp, ser_delp, fir_delp)
        ##This is true based on the current split ratio
        ice_tro_fir_sys_coeff = delp_ice_tro_fir_sys / pow(ice_flow + tro_flow + fir_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(ice_tro_fir_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, ice_flow + tro_flow + fir_flow)
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['ice_tro_fir_branch_pump_delp'], network_pump_param['ice_tro_fir_branch_pump_elect'], ice_tro_fir_sys_coeff)
        ##Calculating electricity consumption 
        ice_tro_fir_pump_elect_cons = (ret_values[0,0] * (ice_flow + tro_flow + fir_flow)) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['ice_tro_fir_max_flow'] = ret_values[3,0]
        return_values['ice_tro_fir_delp'] = est_pressure
        return_values['ice_tro_fir_elect_cons'] = ice_tro_fir_pump_elect_cons 

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

################################################################################################################################################################
################################################################################################################################################################
##Model 4: Lp relaxation of the temperature mixing 
def dist_nwk_piecewise_pressure_reg_pumpnwk_bilinear_temp(consumer_demand, m_total, perc_split, nwk_pump_select, tin_dist_nwk, steps, tin_ss_max, bilinear_pieces):

    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'      
    import sys 
    sys.path.append(current_path + 'add_on_functions\\')
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
    
    ##steps --- number of linear pieces
    
    return_values = {}
    tighter_flow_upper_bounds = pd.DataFrame(columns = ['Nwk_pump_select', 'Name', 'Value'])
    
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
    
    ##Refercence flow 
    ref_flow = 500                  ##Just need a non-zero flowrate for calculating the pressure coefficients
    max_flow = 3200                 ##for the use with the golden_section search function
    
    ##Checking which network choice
    
    ##All branches served by their own pumps 
    if network_pump_param['nwk_choice'] == 0:

        ##ice network 
        
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        
        ##Expressing hsb flowrate in terms of gv2 flowrate
        mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
        ##Expressing total flowrate as a function as gv2 flowrate
        mgv2_intermsof_mice_coeff = 1 + mhsb_intermsof_mgv2_coeff
        
        total_flow = ref_flow 
        gv2_flow_temp = total_flow / mgv2_intermsof_mice_coeff
        pressure = ice_main_coeff*pow(total_flow, 1.852) +  gv2_coeff*pow(gv2_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]
        
        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['ice_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'ice_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        delp_ice_sys = max(gv2_delp, hsb_delp)
        ##This is true based on the current split ratio
        ice_sys_coeff = delp_ice_sys / pow(ice_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(ice_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, ice_flow)
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['ice_branch_pump_delp'], network_pump_param['ice_branch_pump_elect'], ice_sys_coeff)
        ##Calculating electricity consumption 
        ice_pump_elect_cons = (ret_values[0,0] * ice_flow) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['ice_max_flow'] = ret_values[3,0]
        return_values['ice_delp'] = est_pressure
        return_values['ice_elect_cons'] = ice_pump_elect_cons      

        ##tro network 

        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        
        ##Expressing ser flowrate in terms of pfa flowrate 
        mser_intermsof_mpfa_coeff = pow(pfa_coeff / ser_coeff, 1/1.852)
        ##Expressing total flowrate as a function as pfa flowrate
        mpfa_intermsof_mtro_coeff = 1 + mser_intermsof_mpfa_coeff        
        
        total_flow = ref_flow 
        pfa_flow_temp = total_flow / mpfa_intermsof_mtro_coeff
        pressure = tro_main_coeff*pow(total_flow, 1.852) +  pfa_coeff*pow(pfa_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]        

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['tro_branch_pump_delp'])        

        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1

        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'tro_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)   
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        delp_tro_sys = max(pfa_delp, ser_delp)
        ##This is true based on the current split ratio
        tro_sys_coeff = delp_tro_sys / pow(tro_flow, 1.852)        
        pwl_table = pwl_generate_table_pressure(tro_sys_coeff, 0, max_config_flow, steps)        
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, tro_flow)
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['tro_branch_pump_delp'], network_pump_param['tro_branch_pump_elect'], tro_sys_coeff)
        ##Calculating electricity consumption 
        tro_pump_elect_cons = (ret_values[0,0] * tro_flow) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['tro_max_flow'] = ret_values[3,0]
        return_values['tro_delp'] = est_pressure
        return_values['tro_elect_cons'] = tro_pump_elect_cons                                

        ##fir network 

        ##Finding a tighter upper bound 
        ##determining the lowest pressure case, this is just a single curve 
        search_bounds = [0, max_flow]                 

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, fir_coeff, network_pump_param['fir_branch_pump_delp'])      
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'fir_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)  
        
        ##Generating the pwl table 
        pwl_table = pwl_generate_table_pressure(fir_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, fir_flow)                            
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['fir_branch_pump_delp'], network_pump_param['fir_branch_pump_elect'], fir_coeff)
        ##Calculating electricity consumption 
        fir_pump_elect_cons = (ret_values[0,0] * fir_flow) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['fir_max_flow'] = ret_values[3,0]
        return_values['fir_delp'] = est_pressure
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

    ##ice and tro share pumps, fir is served by own pump
    elif network_pump_param['nwk_choice'] == 1:
        
        ##ice and tro network 
        
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        ##Expressing hsb flowrate in terms of gv2 flowrate
        mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
        ##Expressing pfa flowrate in terms of gv2 flowrate 
        term1 = pow(gv2_coeff/hsb_coeff, 1/1.852)
        term2 = ice_main_coeff*pow(1 + term1, 1.852) + gv2_coeff
        term3 = pow(pfa_coeff/ser_coeff, 1/1.852)
        term4 = tro_main_coeff*pow(1 + term3, 1.852) + pfa_coeff
        mpfa_intermaof_mgv2_coeff = pow(term2/term4, 1/1.852)
        ##Expressing ser flowrate in terms of gv2 flowrate 
        term5 = pow(ser_coeff/pfa_coeff, 1/1.852)
        term6 = tro_main_coeff*pow(1 + term5, 1.852) + ser_coeff
        mser_intermsof_mgv2_coeff = pow(term2/term6, 1/1.852)
        ##Expressing total flowrate as a function as gv2 flowrate
        mgv2_intermsof_miceandmtro_coeff = 1 + mhsb_intermsof_mgv2_coeff + mpfa_intermaof_mgv2_coeff + mser_intermsof_mgv2_coeff        
        
        total_flow = ref_flow 
        gv2_flow_temp = total_flow / mgv2_intermsof_miceandmtro_coeff
        pressure = ice_main_coeff*pow(total_flow, 1.852) +  gv2_coeff*pow(gv2_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['ice_tro_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'ice_tro_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        delp_ice_tro_sys = max(gv2_delp, hsb_delp, pfa_delp, ser_delp)
        ##This is true based on the current split ratio
        ice_tro_sys_coeff = delp_ice_tro_sys / pow(ice_flow + tro_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(ice_tro_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, ice_flow + tro_flow)
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['ice_tro_branch_pump_delp'], network_pump_param['ice_tro_branch_pump_elect'], ice_tro_sys_coeff)
        ##Calculating electricity consumption 
        ice_tro_pump_elect_cons = (ret_values[0,0] * (ice_flow + tro_flow)) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['ice_tro_max_flow'] = ret_values[3,0]
        return_values['ice_tro_delp'] = est_pressure
        return_values['ice_tro_elect_cons'] = ice_tro_pump_elect_cons    

        ##fir network 

        ##Finding a tighter upper bound 
        ##determining the lowest pressure case, this is just a single curve 
        search_bounds = [0, max_flow]                 

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, fir_coeff, network_pump_param['fir_branch_pump_delp'])      
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'fir_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)  
        
        ##Generating the pwl table 
        pwl_table = pwl_generate_table_pressure(fir_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, fir_flow)    
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['fir_branch_pump_delp'], network_pump_param['fir_branch_pump_elect'], fir_coeff)
        ##Calculating electricity consumption 
        fir_pump_elect_cons = (ret_values[0,0] * fir_flow) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['fir_max_flow'] = ret_values[3,0]
        return_values['fir_delp'] = est_pressure
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

        ##ice network 
        
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        
        ##Expressing hsb flowrate in terms of gv2 flowrate
        mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
        ##Expressing total flowrate as a function as gv2 flowrate
        mgv2_intermsof_mice_coeff = 1 + mhsb_intermsof_mgv2_coeff
        
        total_flow = ref_flow 
        gv2_flow_temp = total_flow / mgv2_intermsof_mice_coeff
        pressure = ice_main_coeff*pow(total_flow, 1.852) +  gv2_coeff*pow(gv2_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]
        
        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['ice_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'ice_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        delp_ice_sys = max(gv2_delp, hsb_delp)
        ##This is true based on the current split ratio
        ice_sys_coeff = delp_ice_sys / pow(ice_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(ice_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, ice_flow)
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['ice_branch_pump_delp'], network_pump_param['ice_branch_pump_elect'], ice_sys_coeff)
        ##Calculating electricity consumption 
        ice_pump_elect_cons = (ret_values[0,0] * ice_flow) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['ice_max_flow'] = ret_values[3,0]
        return_values['ice_delp'] = est_pressure
        return_values['ice_elect_cons'] = ice_pump_elect_cons  
                                    
        ##tro and fir network 
        
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        ##Expresing ser flowrate in terms of pfa flowrate 
        mser_intermsof_mpfa_coeff = pow(pfa_coeff / ser_coeff, 1/1.852)
        ##Expressing fir flowrate in terms of pfa flowrate 
        term1 = pow(pfa_coeff/ser_coeff, 1/1.852)
        term2 = tro_main_coeff*pow(1 + term1, 1.852) + pfa_coeff
        mfir_intermsof_mpfa_coeff = pow(term2/fir_coeff, 1/1.852)
        ##Expressing total flowrate as a function of pfa flowrate 
        mtrofir_intermsof_mpfa_coeff = 1 + mser_intermsof_mpfa_coeff + mfir_intermsof_mpfa_coeff      
        
        total_flow = ref_flow 
        pfa_flow_temp = total_flow / mtrofir_intermsof_mpfa_coeff
        pressure = tro_main_coeff*pow(total_flow, 1.852) +  pfa_coeff*pow(pfa_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['tro_fir_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'tro_fir_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        fir_delp = fir_coeff * pow(fir_flow, 1.852)
        delp_tro_fir_sys = max(pfa_delp, ser_delp, fir_delp)
        ##This is true based on the current split ratio
        tro_fir_sys_coeff = delp_tro_fir_sys / pow(tro_flow + fir_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(tro_fir_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, tro_flow + fir_flow)
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['tro_fir_branch_pump_delp'], network_pump_param['tro_fir_branch_pump_elect'], tro_fir_sys_coeff)
        ##Calculating electricity consumption 
        tro_fir_pump_elect_cons = (ret_values[0,0] * (tro_flow + fir_flow)) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['tro_fir_max_flow'] = ret_values[3,0]
        return_values['tro_fir_delp'] = est_pressure
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
        
    ##All networks share pumps 
    elif network_pump_param['nwk_choice'] == 3:         
        
        ##ice, tro and fir network 
        ##Finding a tighter upper bound 
        ##determining the lowest pressure case
        ##Expresing hsb flowrate in terms of gv2 flowrate
        mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
        ##Expressing pfa flowrate in terms of gv2 flowrate 
        term1 = pow(gv2_coeff/hsb_coeff, 1/1.852)
        term2 = ice_main_coeff*pow(1 + term1, 1.852) + gv2_coeff
        term3 = pow(pfa_coeff/ser_coeff, 1/1.852)
        term4 = tro_main_coeff*pow(1 + term3, 1.852) + pfa_coeff
        mpfa_intermaof_mgv2_coeff = pow(term2/term4, 1/1.852)
        ##Expressing ser flowrate in terms of gv2 flowrate 
        term5 = pow(ser_coeff/pfa_coeff, 1/1.852)
        term6 = tro_main_coeff*pow(1 + term5, 1.852) + ser_coeff
        mser_intermsof_mgv2_coeff = pow(term2/term6, 1/1.852)
        ##Expressing fir flowrate in terms of gv2 flowrate 
        term7 = pow(gv2_coeff/hsb_coeff, 1/1.852)
        term8 = ice_main_coeff*pow(1 + term7, 1.852) + gv2_coeff
        mfir_intermsof_mgv2_coeff = pow(term8/fir_coeff, 1/1.852)
        ##Expressing total flowrate as a function of gv2 flowrate
        micetrofir_intermsof_mgv2_coeff = 1 + mhsb_intermsof_mgv2_coeff + mpfa_intermaof_mgv2_coeff + mser_intermsof_mgv2_coeff + mfir_intermsof_mgv2_coeff
        
        total_flow = ref_flow 
        gv2_flow_temp = total_flow / micetrofir_intermsof_mgv2_coeff
        pressure = ice_main_coeff*pow(total_flow, 1.852) +  gv2_coeff*pow(gv2_flow_temp, 1.852)
        temp_coeff = pressure / pow(total_flow, 1.852)
        search_bounds = [0, max_flow]        

        ##Now find the intersection between this derived system curve and the selected pump curve,
        ##The reason for this is to determine a tighter upper bound for the piecewise linearization of the pressure curve
        max_config_flow = golden_section_dist(pump_sys_int_dist, search_bounds, temp_coeff, network_pump_param['ice_tro_fir_branch_pump_delp'])
        
        ##Add 10 percent overhead to the maximum configuration flow
        max_config_flow = max_config_flow * 1.1
        
        ##Storing values for other usage
        tbf_data = [nwk_pump_select, 'ice_tro_fir_nwk', max_config_flow]
        tbf_df = pd.DataFrame(data = [tbf_data], columns = ['Nwk_pump_select', 'Name', 'Value'])
        tighter_flow_upper_bounds = tighter_flow_upper_bounds.append(tbf_df, ignore_index = True)
        
        ##Generating the pwl table 
        ##Determining the composite system curve parameters
        gv2_delp = (gv2_coeff * pow(gv2_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        hsb_delp = (hsb_coeff * pow(hsb_flow, 1.852)) + (ice_main_coeff * pow(ice_flow, 1.852))
        pfa_delp = (pfa_coeff * pow(pfa_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        ser_delp = (ser_coeff * pow(ser_flow, 1.852)) + (tro_main_coeff * pow(tro_flow, 1.852))
        fir_delp = fir_coeff * pow(fir_flow, 1.852)
        delp_ice_tro_fir_sys = max(gv2_delp, hsb_delp, pfa_delp, ser_delp, fir_delp)
        ##This is true based on the current split ratio
        ice_tro_fir_sys_coeff = delp_ice_tro_fir_sys / pow(ice_flow + tro_flow + fir_flow, 1.852)
        pwl_table = pwl_generate_table_pressure(ice_tro_fir_sys_coeff, 0, max_config_flow, steps)
        ##Searching the generated table to find estimated value of pressure drop
        est_pressure = search_pwl_table_for_values(pwl_table, ice_flow + tro_flow + fir_flow)
        ##Determining the electricity consumption using curve regression method, the coefficient needs to be the lowest pressure drop case
        ret_values = dist_pump_nwk_regress (network_pump_param['ice_tro_fir_branch_pump_delp'], network_pump_param['ice_tro_fir_branch_pump_elect'], ice_tro_fir_sys_coeff)
        ##Calculating electricity consumption 
        ice_tro_fir_pump_elect_cons = (ret_values[0,0] * (ice_flow + tro_flow + fir_flow)) + (ret_values[1,0] * est_pressure) + ret_values[2,0]
        
        return_values['ice_tro_fir_max_flow'] = ret_values[3,0]
        return_values['ice_tro_fir_delp'] = est_pressure
        return_values['ice_tro_fir_elect_cons'] = ice_tro_fir_pump_elect_cons 

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
    
    ##Determining the bounds of independent variables 
    m_perc_min = 0
    m_perc_max = 1
    tin_min = 273.15 + 1
    tin_max = tin_ss_max
    
    ##Generating the bilinear look up table 
    u_table, v_table = gen_bilinear_pieces (m_perc_min, m_perc_max, tin_min, tin_max, bilinear_pieces)
    ##Getting the estimated values 
    est_bilin_gv2 = search_bilin_table_for_values (u_table, v_table, perc_split[0], tin_dist_nwk)
    est_bilin_hsb = search_bilin_table_for_values (u_table, v_table, perc_split[1], tin_dist_nwk)    
    est_bilin_pfa = search_bilin_table_for_values (u_table, v_table, perc_split[2], tin_dist_nwk)
    est_bilin_ser = search_bilin_table_for_values (u_table, v_table, perc_split[3], tin_dist_nwk)
    est_bilin_fir = search_bilin_table_for_values (u_table, v_table, perc_split[4], tin_dist_nwk)
    ##Finding the constant values
    m_total_kgs = (m_total * 998.2) / 3600
    gv2_cst_val = consumer_demand[0] / (m_total_kgs * 4.2)
    hsb_cst_val = consumer_demand[1] / (m_total_kgs * 4.2)    
    pfa_cst_val = consumer_demand[2] / (m_total_kgs * 4.2)    
    ser_cst_val = consumer_demand[3] / (m_total_kgs * 4.2)
    fir_cst_val = consumer_demand[4] / (m_total_kgs * 4.2)
    ##Computing the bilinear estimated temperatures 
    est_tout_gv2_perc = est_bilin_gv2 + gv2_cst_val
    est_tout_hsb_perc = est_bilin_hsb + hsb_cst_val
    est_tout_pfa_perc = est_bilin_pfa + pfa_cst_val
    est_tout_ser_perc = est_bilin_ser + ser_cst_val
    est_tout_fir_perc = est_bilin_fir + fir_cst_val
    ##Computing the combined temperature out of the distribution network 
    tout_dist_nwk = est_tout_gv2_perc + est_tout_hsb_perc + est_tout_pfa_perc + est_tout_ser_perc + est_tout_fir_perc
    
    return_values['gv2_tout'] = est_tout_gv2_perc / perc_split[0]
    return_values['hsb_tout'] = est_tout_hsb_perc / perc_split[1]
    return_values['pfa_tout'] = est_tout_pfa_perc / perc_split[2]
    return_values['ser_tout'] = est_tout_ser_perc / perc_split[3]
    return_values['fir_tout'] = est_tout_fir_perc / perc_split[4] 

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
    
    return_values['tout_dist_nwk'] = tout_dist_nwk
    data_temp = ['tout_dist_nwk', return_values['tout_dist_nwk'], 'K']
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])
    return_values_df = return_values_df.append(data_temp_df, ignore_index = True)       
    
    return return_values, return_values_df
   
################################################################################################################################################################
################################################################################################################################################################
##Add-on functions

##Function to calculate the deviation between the pump and system curves, this function is to be used  
def pump_sys_int_dist (sys_coeff, pump_coeffs, flow):
    ##sys_coeff --- the single coefficient of the system curve 
    ##pump_coeffs[0] --- x2 coefficient 
    ##pump_coeffs[1] --- x coefficient
    ##pump_coeffs[2] --- constant term 
    ##flow --- the flowrate which the intersection point may be 
    
    sys_curve_value = sys_coeff*pow(flow, 1.852)
    pump_curve_value = (pump_coeffs[0] * pow(flow, 2)) + (pump_coeffs[1] * flow) + pump_coeffs[2]
    ret_value = abs(pump_curve_value - sys_curve_value)
    ##print(sys_curve_value)
    ##print(pump_curve_value)
    
    return ret_value
    
##Function to determine the upper and lower bounds of each piecewise linear pieces
def pwl_generate_table_pressure (sys_coeff, lb, ub, steps):
    import pandas as pd    
    step_size = (ub - lb) / steps 
    ref_table = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int'])
    
    for i in range (0, steps):
        lb_temp = (i * step_size) + lb
        ub_temp = ((i + 1) * step_size) + lb
        f_lb = sys_coeff * pow(lb_temp, 1.852)
        f_ub = sys_coeff * pow(ub_temp, 1.852)
        grad_temp = (f_ub - f_lb) / (ub_temp - lb_temp)
        int_temp = f_ub - (grad_temp * ub_temp)
        
        data_temp = [lb_temp, ub_temp, grad_temp, int_temp]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['lb', 'ub', 'grad', 'int'])
        ref_table = ref_table.append(temp_df, ignore_index = True)
    
    return ref_table

##Function to search through the pwl tables and return the estimated value
def search_pwl_table_for_values (ref_table, var_value):    
    dim_ref_table = ref_table.shape 
    
    for i in range (0, dim_ref_table[0]):
        if (var_value >= ref_table['lb'][i]) and (var_value <= ref_table['ub'][i]):
            ret_value = (ref_table['grad'][i] * var_value) + ref_table['int'][i]
            break
    
    return ret_value
    
##Function to find the intersection point between pwl pieces and pump curves 
def pwl_pieces_pump_int (ref_table, pump_curve):
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'      
    import sys 
    sys.path.append(current_path + 'add_on_functions\\')
    from solve_quad_simul_eqns import solve_quad_simul_eqns
    
    dim_ref_table = ref_table.shape
    ##Finding the intersection points of each piecewise linear 
    for i in range (0, dim_ref_table[0]):
        sys_curve = [0, ref_table['grad'][i], ref_table['int'][i]]
        int_flow, int_press = solve_quad_simul_eqns(pump_curve, sys_curve)
        if (int_flow >= ref_table['lb'][i]) and (int_flow <= ref_table['ub'][i]):
            return_data = [int_flow, int_press]
            break
    return return_data
    
##Function to determine the regression the relationship between flow, pressure and elect cons for a given configuration 
def dist_pump_nwk_regress (pump_coeff_delp, pump_coeff_elect, nwk_coeff):

    ##pump_coeff_delp[0] --- x2 coefficient
    ##pump_coeff_delp[1] --- x coefficient
    ##pump_coeff_delp[2] --- cst term
    
    ##pump_coeff_elect[0] --- x3 coefficient
    ##pump_coeff_elect[1] --- x2 coefficient
    ##pump_coeff_elect[2] --- x coefficient
    ##pump_coeff_elect[3] --- cst term

    ##nwk_coeff --- specific to the parallel branch 
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'      
    import sys 
    sys.path.append(current_path + 'add_on_functions\\')
    from golden_section import golden_section_evap_cond_regress
    import numpy as np
    from sklearn import linear_model 
    import matplotlib.pyplot as plt 

    ##Network parameters 
    dist_nwk_A_val = nwk_coeff
    ##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case
    func_bounds = [0, 3200]
    config_max_flow = golden_section_evap_cond_regress(pump_sys_int_dist, func_bounds, dist_nwk_A_val, pump_coeff_delp)
    ##The corresponding electricity consumption at the maximum flowrate and rpm is 
    config_max_elect = pump_coeff_elect[0]*pow(config_max_flow, 3) + pump_coeff_elect[1]*pow(config_max_flow, 2) + pump_coeff_elect[2]*config_max_flow + pump_coeff_elect[3]
    ##From here onwards, variable speed of the pump will be assumed to linearly correlate with electrical consumption 
    ##We want to express E = A1m + A2p + cst, hence regression analysis is needed 
    ##To do that, we take 20 points for each of the flowrate interval for different pressure drops and electricity consumptions 
    delp_interval = 20 
    flowrate_interval = 50
    flowrate_step = config_max_flow / flowrate_interval 
    ##Initiate a matrix to hold all the values 
    ##Column 1 will be flowrate 
    ##Column 2 will be pressure drop 
    ##Column 3 will be electricity consumed 
    value_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
    value_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))

    for i in range (0, flowrate_interval+1):
        ##current flowrate 
        c_fr = i * flowrate_step 
        ##minimum pressure drop comes from the system curve 
        min_p = dist_nwk_A_val*pow(c_fr, 1.852)
        ##maximum pressure drop comes from the pump curve 
        max_p = pump_coeff_delp[0]*pow(c_fr, 2) + pump_coeff_delp[1]*c_fr + pump_coeff_delp[2]
        ##minimum electricity consumption comes from the linear assumption curve 
        min_e = c_fr * (config_max_elect / config_max_flow)
        ##maximum electricity consumption comes from the electricity curve 
        max_e = pump_coeff_elect[0]*pow(c_fr, 3) + pump_coeff_elect[1]*pow(c_fr, 2) + pump_coeff_elect[2]*c_fr + pump_coeff_elect[3]
        ##recording the maximum and minimums 
        temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
        temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)

        for j in range (0, delp_interval):
            value_table_X[i*delp_interval+j, 0] = c_fr
            value_table_X[i*delp_interval+j, 1] = temp_pressure_rec[j]
            value_table_Y[i*delp_interval+j, 0] = temp_elec_rec[j]
    
    ##Performing regression analysis
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(value_table_X, value_table_Y)
    result = clf.score(value_table_X, value_table_Y, sample_weight=None)
    lin_coeff = clf.coef_
    int_lin = clf.intercept_  

    ##Evaluating the electricity consumption using linear combination model 
    calc_Y = np.zeros(((delp_interval*(flowrate_interval+1) ,1)))
    for i in range (0, delp_interval*(flowrate_interval+1)):
        calc_Y[i,0] = lin_coeff[0,0]*value_table_X[i,0] + lin_coeff[0,1]*value_table_X[i,1] + int_lin

    ##Plotting the pressure drop and flowrate area
    ##plt.plot(value_table_X[:, 0], value_table_X[:, 1], 'o')
    ##plt.xlabel('Flowrate m3/h')
    ##plt.ylabel('Pressure mH2O')
    ##plt.show()
    ##Plotting the electricity consumption and flowrate area
    ##plt.plot(value_table_X[:, 0], value_table_Y[:, 0], 'o')
    ##plt.xlabel('Flowrate m3/h')
    ##plt.ylabel('Elect kWh')
    ##plt.show()
    ##Plotting actual values and predicted values 
    ##plt.plot(calc_Y, value_table_Y, 'o')
    ##plt.xlabel('Regression Values')
    ##plt.ylabel('Calculated Values')
    ##plt.show()
    ##plt.plot(value_table_X[:, 0], calc_Y, 'o')
    ##plt.xlabel('Flowrate m3/h')
    ##plt.ylabel('Regression Values (Elect kWh)')
    ##plt.show()
    
    ##Assembling the return values 
    dist_pump_m_coeff = lin_coeff[0,0]
    dist_pump_p_coeff = lin_coeff[0,1]
    dist_pump_cst = int_lin
    dist_pump_max_flow = config_max_flow
    dist_pump_regress_r2 = result
    
    ret_values = np.zeros((5,1))
    ret_values[0,0] = dist_pump_m_coeff
    ret_values[1,0] = dist_pump_p_coeff
    ret_values[2,0] = dist_pump_cst
    ret_values[3,0] = dist_pump_max_flow
    ret_values[4,0] = dist_pump_regress_r2    

    return ret_values
    
##A function to generate a lookup table of bilinear pieces 
def gen_bilinear_pieces (x_min, x_max, y_min, y_max, bilinear_pieces):
    import pandas as pd 
    u_table = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int'])
    v_table = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int']) 
    
    ##u_bounds 
    u_overall_min = x_min + y_min 
    u_overall_max = x_max + y_max
    ##y_bounds 
    v_overall_min = x_min - y_max
    v_overall_max = x_max - y_min 
    ##step_increment 
    u_step = (u_overall_max - u_overall_min) / bilinear_pieces
    v_step = (v_overall_max - v_overall_min) / bilinear_pieces

    for i in range (0, bilinear_pieces):
        ##Handling u values first 
        u_min = (i * u_step) + u_overall_min
        u_max = ((i + 1) * u_step) + u_overall_min
        fu_min = 0.25 * pow(u_min, 2)
        fu_max = 0.25 * pow(u_max, 2)
        u_grad = (fu_max - fu_min) / (u_max - u_min)
        u_int = fu_max - (u_grad * u_max)
        u_data = [u_min, u_max, u_grad, u_int]
        u_df = pd.DataFrame(data = [u_data], columns = ['lb', 'ub', 'grad', 'int'])
        u_table = u_table.append(u_df, ignore_index = True)
        ##Handling v values next 
        v_min = (i * v_step) + v_overall_min
        v_max = ((i + 1) * v_step) + v_overall_min
        fv_min = 0.25 * pow(v_min, 2)
        fv_max = 0.25 * pow(v_max, 2)
        v_grad = (fv_max - fv_min) / (v_max - v_min)
        v_int = fv_max - (v_grad * v_max)
        v_data = [v_min, v_max, v_grad, v_int]
        v_df = pd.DataFrame(data = [v_data], columns = ['lb', 'ub', 'grad', 'int'])
        v_table = v_table.append(v_df, ignore_index = True)        
        
    return u_table, v_table 
    
##A function to determine the estimated values of using bilinear pieces 
def search_bilin_table_for_values (u_table, v_table, x_actual, y_actual):
    
    ##Computing the actual values 
    u_actual = x_actual + y_actual 
    v_actual = x_actual - y_actual 
    ##Computing the number of iterations 
    dim_u_table = u_table.shape 
    dim_v_table = v_table.shape 
    
    for i in range (0, dim_u_table[0]):
        if (u_actual >= u_table['lb'][i]) and (u_actual <= u_table['ub'][i]):
            fu_calc = (u_actual * u_table['grad'][i]) + u_table['int'][i]
            break
    for i in range (0, dim_v_table[0]):
         if (v_actual >= v_table['lb'][i]) and (v_actual <= v_table['ub'][i]):
            fv_calc = (v_actual * v_table['grad'][i]) + v_table['int'][i]
            break       
        
    bilin_est = fu_calc - fv_calc

    return bilin_est
    

