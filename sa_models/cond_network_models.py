##This script contains all the condensation network models, the input and output of all the models should be the same 
##The entire model is built based on 

##Condenser side 

##Model 1: Original condenser network model 
##Model 2: Piecewise linearization of pressure drop 
##Model 3: Regression of pump and network electricity consumption
##Model 4: Lp relaxation of temperature mixing 


################################################################################################################################################
################################################################################################################################################
################################################################################################################################################

def cond_nwk_org (chiller_input, num_cooling_towers):

    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'  
    import sys
    sys.path.append(current_path + 'add_on_functions\\')
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
    
################################################################################################################################################

def cond_nwk_piecewise_pressure (chiller_input, num_cooling_towers, steps):

    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'      
    import sys 
    sys.path.append(current_path + 'add_on_functions\\')
    from solve_quad_simul_eqns import solve_quad_simul_eqns
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
    
    ##steps --- number of piecewise pieces
    
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
    ch1_cond_nwk_flow_limit = 590
    ch2_cond_nwk_flow_limit = 1840    
    ch3_cond_nwk_flow_limit = 1840
    
    ##Determine the stepsize for flowrates for each system
    ch1_cond_nwk_flow_limit_step = ch1_cond_nwk_flow_limit / steps
    ch2_cond_nwk_flow_limit_step = ch2_cond_nwk_flow_limit / steps    
    ch3_cond_nwk_flow_limit_step = ch3_cond_nwk_flow_limit / steps
    
    ##Pressure drop calcualtion for the common network  
    total_cond_nwk_flow = chiller_input['Value'][0] + chiller_input['Value'][2] + chiller_input['Value'][4]
    delp_common_nwk = common_nwk_coeff * pow(total_cond_nwk_flow, 1.852)
    
    ##Setting up the reference table for piecewise pressure drop
    piecewise_pressure = pd.DataFrame(columns = ['ch1_flow_lb', 'ch1_flow_ub', 'ch1_grad', 'ch1_int', 
                                                 'ch2_flow_lb', 'ch2_flow_ub', 'ch2_grad', 'ch2_int', 
                                                 'ch3_flow_lb', 'ch3_flow_ub', 'ch3_grad', 'ch3_int'])
    
    for i in range (0, steps):
        ##Calculation for chiller 1 cond network 
        ch1_flow_lb = i * ch1_cond_nwk_flow_limit_step
        ch1_flow_ub = (i + 1) * ch1_cond_nwk_flow_limit_step
        ##If the total flowrate in the network is kept a constant, the relationship between the original pressure curve 
        ##and the new one is just a vertical offset
        ch1_press_lb = (ch1_nwk_coeff * pow(ch1_flow_lb, 1.852)) + delp_common_nwk
        ch1_press_ub = (ch1_nwk_coeff * pow(ch1_flow_ub, 1.852)) + delp_common_nwk
        ch1_grad = (ch1_press_ub - ch1_press_lb) / (ch1_flow_ub - ch1_flow_lb)
        ch1_int = ch1_press_ub - (ch1_grad * ch1_flow_ub)
        
        ##Calculation for chiller 2 cond network 
        ch2_flow_lb = i * ch2_cond_nwk_flow_limit_step
        ch2_flow_ub = (i + 1) * ch2_cond_nwk_flow_limit_step
        ##If the total flowrate in the network is kept a constant, the relationship between the original pressure curve 
        ##and the new one is just a vertical offset
        ch2_press_lb = (ch2_nwk_coeff * pow(ch2_flow_lb, 1.852)) + delp_common_nwk
        ch2_press_ub = (ch2_nwk_coeff * pow(ch2_flow_ub, 1.852)) + delp_common_nwk
        ch2_grad = (ch2_press_ub - ch2_press_lb) / (ch2_flow_ub - ch2_flow_lb)
        ch2_int = ch2_press_ub - (ch2_grad * ch2_flow_ub)
        
        ##Calculation for chiller 3 cond network 
        ch3_flow_lb = i * ch3_cond_nwk_flow_limit_step
        ch3_flow_ub = (i + 1) * ch3_cond_nwk_flow_limit_step
        ##If the total flowrate in the network is kept a constant, the relationship between the original pressure curve 
        ##and the new one is just a vertical offset
        ch3_press_lb = (ch3_nwk_coeff * pow(ch3_flow_lb, 1.852)) + delp_common_nwk
        ch3_press_ub = (ch3_nwk_coeff * pow(ch3_flow_ub, 1.852)) + delp_common_nwk
        ch3_grad = (ch3_press_ub - ch3_press_lb) / (ch3_flow_ub - ch3_flow_lb)
        ch3_int = ch3_press_ub - (ch3_grad * ch3_flow_ub)    
        
        ##Assembling data and placing it in the dataframe 
        temp_data = [ch1_flow_lb, ch1_flow_ub, ch1_grad, ch1_int, ch2_flow_lb, ch2_flow_ub, ch2_grad, ch2_int, ch3_flow_lb,
                     ch3_flow_ub, ch3_grad, ch3_int]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['ch1_flow_lb', 'ch1_flow_ub', 'ch1_grad', 'ch1_int', 
                                                              'ch2_flow_lb', 'ch2_flow_ub', 'ch2_grad', 'ch2_int', 
                                                              'ch3_flow_lb', 'ch3_flow_ub', 'ch3_grad', 'ch3_int'])
        piecewise_pressure = piecewise_pressure.append(temp_df, ignore_index = True)
    
    ##Checking which step the flowrate falls in and the right bounds
    check_ch1 = 0
    check_ch2 = 0
    check_ch3 = 0
    
    for i in range (0, steps):
        if check_ch1 == 0:
            if (chiller_input['Value'][0] >= piecewise_pressure['ch1_flow_lb'][i]) and (chiller_input['Value'][0] <= piecewise_pressure['ch1_flow_ub'][i]):
                ch1_press_pw = (piecewise_pressure['ch1_grad'][i] * chiller_input['Value'][0]) + piecewise_pressure['ch1_int'][i]
                check_ch1 = 1
        if check_ch2 == 0:
            if (chiller_input['Value'][2] >= piecewise_pressure['ch2_flow_lb'][i]) and (chiller_input['Value'][2] <= piecewise_pressure['ch2_flow_ub'][i]):
                ch2_press_pw = (piecewise_pressure['ch2_grad'][i] * chiller_input['Value'][2]) + piecewise_pressure['ch2_int'][i]
                check_ch2 = 1
        if check_ch3 == 0:
            if (chiller_input['Value'][4] >= piecewise_pressure['ch3_flow_lb'][i]) and (chiller_input['Value'][4] <= piecewise_pressure['ch3_flow_ub'][i]):
                ch3_press_pw = (piecewise_pressure['ch3_grad'][i] * chiller_input['Value'][4]) + piecewise_pressure['ch3_int'][i]
                check_ch3 = 1
        if (check_ch1 != 0) and (check_ch2 != 0) and (check_ch3 != 0):
            break

    return_values['Chiller1_cond_pump_delp'] = ch1_press_pw
    return_values['Chiller2_cond_pump_delp'] = ch2_press_pw
    return_values['Chiller3_cond_pump_delp'] = ch3_press_pw

    ##Finding the intersection points of each piecewise linear 
    
    check_ch1 = 0
    check_ch2 = 0
    check_ch3 = 0
    
    for i in range (0, steps):
        if check_ch1 == 0:
            sys_curve = [0, piecewise_pressure['ch1_grad'][i], piecewise_pressure['ch1_int'][i]]
            int_flow, int_press = solve_quad_simul_eqns(cond_pump_1_delp, sys_curve)
            if (int_flow >= piecewise_pressure['ch1_flow_lb'][i]) and (int_flow <= piecewise_pressure['ch1_flow_ub'][i]):
                max_elect = (cond_pump_1_elect[0] * pow(int_flow, 3)) + (cond_pump_1_elect[1] * pow(int_flow, 2)) + (cond_pump_1_elect[2] * int_flow) + cond_pump_1_elect[3]
                ch1_pwl_int_data = [int_flow, int_press, max_elect]
                check_ch1 = 1
        if check_ch2 == 0:
            sys_curve = [0, piecewise_pressure['ch2_grad'][i], piecewise_pressure['ch2_int'][i]]
            int_flow, int_press = solve_quad_simul_eqns(cond_pump_2_delp, sys_curve)
            if (int_flow >= piecewise_pressure['ch2_flow_lb'][i]) and (int_flow <= piecewise_pressure['ch2_flow_ub'][i]):
                max_elect = (cond_pump_2_elect[0] * pow(int_flow, 3)) + (cond_pump_2_elect[1] * pow(int_flow, 2)) + (cond_pump_2_elect[2] * int_flow) + cond_pump_2_elect[3]
                ch2_pwl_int_data = [int_flow, int_press, max_elect]
                check_ch2 = 1
        if check_ch3 == 0:
            sys_curve = [0, piecewise_pressure['ch3_grad'][i], piecewise_pressure['ch3_int'][i]]
            int_flow, int_press = solve_quad_simul_eqns(cond_pump_3_delp, sys_curve)
            if (int_flow >= piecewise_pressure['ch3_flow_lb'][i]) and (int_flow <= piecewise_pressure['ch3_flow_ub'][i]):
                max_elect = (cond_pump_3_elect[0] * pow(int_flow, 3)) + (cond_pump_3_elect[1] * pow(int_flow, 2)) + (cond_pump_3_elect[2] * int_flow) + cond_pump_3_elect[3]
                ch3_pwl_int_data = [int_flow, int_press, max_elect]
                check_ch3 = 1
        if (check_ch1 != 0) and (check_ch2 != 0) and (check_ch3 != 0):
            break
    
    return_values['Chiller1_cond_pump_max_flow'] = ch1_pwl_int_data[0]    
    return_values['Chiller2_cond_pump_max_flow'] = ch2_pwl_int_data[0]     
    return_values['Chiller3_cond_pump_max_flow'] = ch3_pwl_int_data[0] 

    ##Finding the corresponding electricity consumption of each pump
    ch1_cond_pump_elect_cons = (ch1_pwl_int_data[2] / ch1_pwl_int_data[0]) * chiller_input['Value'][0]
    ch2_cond_pump_elect_cons = (ch2_pwl_int_data[2] / ch2_pwl_int_data[0]) * chiller_input['Value'][2]
    ch3_cond_pump_elect_cons = (ch3_pwl_int_data[2] / ch3_pwl_int_data[0]) * chiller_input['Value'][4]
    
    return_values['Chiller1_cond_pump_elect_cons'] = ch1_cond_pump_elect_cons 
    return_values['Chiller2_cond_pump_elect_cons'] = ch2_cond_pump_elect_cons 
    return_values['Chiller3_cond_pump_elect_cons'] = ch3_cond_pump_elect_cons   

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

###############################################################################################################################################################

def cond_nwk_piecewise_pressure_reg_pumpnwk (chiller_input, num_cooling_towers, steps):
        
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
    
    ##steps --- the number of piecewise steps 
    
    return_values = {}
    
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
    ch1_cond_nwk_flow_limit = 590
    ch2_cond_nwk_flow_limit = 1840    
    ch3_cond_nwk_flow_limit = 1840
    
    ##Determine the stepsize for flowrates for each system
    ch1_cond_nwk_flow_limit_step = ch1_cond_nwk_flow_limit / steps
    ch2_cond_nwk_flow_limit_step = ch2_cond_nwk_flow_limit / steps    
    ch3_cond_nwk_flow_limit_step = ch3_cond_nwk_flow_limit / steps
    
    ##Pressure drop calcualtion for the common network  
    total_cond_nwk_flow = chiller_input['Value'][0] + chiller_input['Value'][2] + chiller_input['Value'][4]
    delp_common_nwk = common_nwk_coeff * pow(total_cond_nwk_flow, 1.852)
    
    ##Setting up the reference table for piecewise pressure drop
    piecewise_pressure = pd.DataFrame(columns = ['ch1_flow_lb', 'ch1_flow_ub', 'ch1_grad', 'ch1_int', 
                                                 'ch2_flow_lb', 'ch2_flow_ub', 'ch2_grad', 'ch2_int', 
                                                 'ch3_flow_lb', 'ch3_flow_ub', 'ch3_grad', 'ch3_int'])
    
    for i in range (0, steps):
        ##Calculation for chiller 1 evap network 
        ch1_flow_lb = i * ch1_cond_nwk_flow_limit_step
        ch1_flow_ub = (i + 1) * ch1_cond_nwk_flow_limit_step
        ##If the total flowrate in the network is kept a constant, the relationship between the original pressure curve 
        ##and the new one is just a vertical offset
        ch1_press_lb = (ch1_nwk_coeff * pow(ch1_flow_lb, 1.852)) + delp_common_nwk
        ch1_press_ub = (ch1_nwk_coeff * pow(ch1_flow_ub, 1.852)) + delp_common_nwk
        ch1_grad = (ch1_press_ub - ch1_press_lb) / (ch1_flow_ub - ch1_flow_lb)
        ch1_int = ch1_press_ub - (ch1_grad * ch1_flow_ub)
        
        ##Calculation for chiller 2 evap network 
        ch2_flow_lb = i * ch2_cond_nwk_flow_limit_step
        ch2_flow_ub = (i + 1) * ch2_cond_nwk_flow_limit_step
        ##If the total flowrate in the network is kept a constant, the relationship between the original pressure curve 
        ##and the new one is just a vertical offset
        ch2_press_lb = (ch2_nwk_coeff * pow(ch2_flow_lb, 1.852)) + delp_common_nwk
        ch2_press_ub = (ch2_nwk_coeff * pow(ch2_flow_ub, 1.852)) + delp_common_nwk
        ch2_grad = (ch2_press_ub - ch2_press_lb) / (ch2_flow_ub - ch2_flow_lb)
        ch2_int = ch2_press_ub - (ch2_grad * ch2_flow_ub)
        
        ##Calculation for chiller 3 evap network 
        ch3_flow_lb = i * ch3_cond_nwk_flow_limit_step
        ch3_flow_ub = (i + 1) * ch3_cond_nwk_flow_limit_step
        ##If the total flowrate in the network is kept a constant, the relationship between the original pressure curve 
        ##and the new one is just a vertical offset
        ch3_press_lb = (ch3_nwk_coeff * pow(ch3_flow_lb, 1.852)) + delp_common_nwk
        ch3_press_ub = (ch3_nwk_coeff * pow(ch3_flow_ub, 1.852)) + delp_common_nwk
        ch3_grad = (ch3_press_ub - ch3_press_lb) / (ch3_flow_ub - ch3_flow_lb)
        ch3_int = ch3_press_ub - (ch3_grad * ch3_flow_ub)    
        
        ##Assembling data and placing it in the dataframe 
        temp_data = [ch1_flow_lb, ch1_flow_ub, ch1_grad, ch1_int, ch2_flow_lb, ch2_flow_ub, ch2_grad, ch2_int, ch3_flow_lb,
                     ch3_flow_ub, ch3_grad, ch3_int]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['ch1_flow_lb', 'ch1_flow_ub', 'ch1_grad', 'ch1_int', 
                                                              'ch2_flow_lb', 'ch2_flow_ub', 'ch2_grad', 'ch2_int', 
                                                              'ch3_flow_lb', 'ch3_flow_ub', 'ch3_grad', 'ch3_int'])
        piecewise_pressure = piecewise_pressure.append(temp_df, ignore_index = True)
    
    ##Checking which step the flowrate falls in and the right bounds
    check_ch1 = 0
    check_ch2 = 0
    check_ch3 = 0
    
    for i in range (0, steps):
        if check_ch1 == 0:
            if (chiller_input['Value'][0] >= piecewise_pressure['ch1_flow_lb'][i]) and (chiller_input['Value'][0] <= piecewise_pressure['ch1_flow_ub'][i]):
                ch1_press_pw = (piecewise_pressure['ch1_grad'][i] * chiller_input['Value'][0]) + piecewise_pressure['ch1_int'][i]
                check_ch1 = 1
        if check_ch2 == 0:
            if (chiller_input['Value'][2] >= piecewise_pressure['ch2_flow_lb'][i]) and (chiller_input['Value'][2] <= piecewise_pressure['ch2_flow_ub'][i]):
                ch2_press_pw = (piecewise_pressure['ch2_grad'][i] * chiller_input['Value'][2]) + piecewise_pressure['ch2_int'][i]
                check_ch2 = 1
        if check_ch3 == 0:
            if (chiller_input['Value'][4] >= piecewise_pressure['ch3_flow_lb'][i]) and (chiller_input['Value'][4] <= piecewise_pressure['ch3_flow_ub'][i]):
                ch3_press_pw = (piecewise_pressure['ch3_grad'][i] * chiller_input['Value'][4]) + piecewise_pressure['ch3_int'][i]
                check_ch3 = 1
        if (check_ch1 != 0) and (check_ch2 != 0) and (check_ch3 != 0):
            break

    return_values['Chiller1_cond_pump_delp'] = ch1_press_pw
    return_values['Chiller2_cond_pump_delp'] = ch2_press_pw
    return_values['Chiller3_cond_pump_delp'] = ch3_press_pw

    ##Using the regression model to determine the electricity consumption 
    ch1_ret_values = cond_pump_nwk_regress(cond_pump_1_delp, cond_pump_1_elect, ch1_cond_nwk_flow_limit, ch1_nwk_coeff, common_nwk_coeff)
    ch2_ret_values = cond_pump_nwk_regress(cond_pump_2_delp, cond_pump_2_elect, ch2_cond_nwk_flow_limit, ch2_nwk_coeff, common_nwk_coeff)    
    ch3_ret_values = cond_pump_nwk_regress(cond_pump_3_delp, cond_pump_3_elect, ch3_cond_nwk_flow_limit, ch3_nwk_coeff, common_nwk_coeff)
    
    return_values['Chiller1_cond_pump_max_flow'] = ch1_ret_values[3,0]  
    return_values['Chiller2_cond_pump_max_flow'] = ch2_ret_values[3,0]     
    return_values['Chiller3_cond_pump_max_flow'] = ch3_ret_values[3,0]    
    
    ch1_elect_cons = ch1_ret_values[0,0]*chiller_input['Value'][0] + ch1_ret_values[1,0]*ch1_press_pw + ch1_ret_values[2,0]
    ch2_elect_cons = ch2_ret_values[0,0]*chiller_input['Value'][2] + ch2_ret_values[1,0]*ch2_press_pw + ch2_ret_values[2,0]
    ch3_elect_cons = ch3_ret_values[0,0]*chiller_input['Value'][4] + ch3_ret_values[1,0]*ch3_press_pw + ch3_ret_values[2,0]       

    return_values['Chiller1_cond_pump_elect_cons'] = ch1_elect_cons 
    return_values['Chiller2_cond_pump_elect_cons'] = ch2_elect_cons 
    return_values['Chiller3_cond_pump_elect_cons'] = ch3_elect_cons     

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
    
###############################################################################################################################################################

def cond_nwk_piecewise_pressure_reg_pumpnwk_bilinear_temp (chiller_input, num_cooling_towers, steps, tcond_in, bilinear_pieces):

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
    
    ##steps --- number of piecewise pieces
    ##tcond_in --- the temperature inlet to the condenser of the chillers, which is the same for all
    ##bilinear_pieces --- the number of bilinear pieces for temperature calculations 
    
    return_values = {}
    
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
    ch1_cond_nwk_flow_limit = 590
    ch2_cond_nwk_flow_limit = 1840    
    ch3_cond_nwk_flow_limit = 1840
    
    ##Determine the stepsize for flowrates for each system
    ch1_cond_nwk_flow_limit_step = ch1_cond_nwk_flow_limit / steps
    ch2_cond_nwk_flow_limit_step = ch2_cond_nwk_flow_limit / steps    
    ch3_cond_nwk_flow_limit_step = ch3_cond_nwk_flow_limit / steps
    
    ##Pressure drop calcualtion for the common network  
    total_cond_nwk_flow = chiller_input['Value'][0] + chiller_input['Value'][2] + chiller_input['Value'][4]
    delp_common_nwk = common_nwk_coeff * pow(total_cond_nwk_flow, 1.852)
    
    ##Setting up the reference table for piecewise pressure drop
    piecewise_pressure = pd.DataFrame(columns = ['ch1_flow_lb', 'ch1_flow_ub', 'ch1_grad', 'ch1_int', 
                                                 'ch2_flow_lb', 'ch2_flow_ub', 'ch2_grad', 'ch2_int', 
                                                 'ch3_flow_lb', 'ch3_flow_ub', 'ch3_grad', 'ch3_int'])
    
    for i in range (0, steps):
        ##Calculation for chiller 1 cond network 
        ch1_flow_lb = i * ch1_cond_nwk_flow_limit_step
        ch1_flow_ub = (i + 1) * ch1_cond_nwk_flow_limit_step
        ##If the total flowrate in the network is kept a constant, the relationship between the original pressure curve 
        ##and the new one is just a vertical offset
        ch1_press_lb = (ch1_nwk_coeff * pow(ch1_flow_lb, 1.852)) + delp_common_nwk
        ch1_press_ub = (ch1_nwk_coeff * pow(ch1_flow_ub, 1.852)) + delp_common_nwk
        ch1_grad = (ch1_press_ub - ch1_press_lb) / (ch1_flow_ub - ch1_flow_lb)
        ch1_int = ch1_press_ub - (ch1_grad * ch1_flow_ub)
        
        ##Calculation for chiller 2 cond network 
        ch2_flow_lb = i * ch2_cond_nwk_flow_limit_step
        ch2_flow_ub = (i + 1) * ch2_cond_nwk_flow_limit_step
        ##If the total flowrate in the network is kept a constant, the relationship between the original pressure curve 
        ##and the new one is just a vertical offset
        ch2_press_lb = (ch2_nwk_coeff * pow(ch2_flow_lb, 1.852)) + delp_common_nwk
        ch2_press_ub = (ch2_nwk_coeff * pow(ch2_flow_ub, 1.852)) + delp_common_nwk
        ch2_grad = (ch2_press_ub - ch2_press_lb) / (ch2_flow_ub - ch2_flow_lb)
        ch2_int = ch2_press_ub - (ch2_grad * ch2_flow_ub)
        
        ##Calculation for chiller 3 cond network 
        ch3_flow_lb = i * ch3_cond_nwk_flow_limit_step
        ch3_flow_ub = (i + 1) * ch3_cond_nwk_flow_limit_step
        ##If the total flowrate in the network is kept a constant, the relationship between the original pressure curve 
        ##and the new one is just a vertical offset
        ch3_press_lb = (ch3_nwk_coeff * pow(ch3_flow_lb, 1.852)) + delp_common_nwk
        ch3_press_ub = (ch3_nwk_coeff * pow(ch3_flow_ub, 1.852)) + delp_common_nwk
        ch3_grad = (ch3_press_ub - ch3_press_lb) / (ch3_flow_ub - ch3_flow_lb)
        ch3_int = ch3_press_ub - (ch3_grad * ch3_flow_ub)    
        
        ##Assembling data and placing it in the dataframe 
        temp_data = [ch1_flow_lb, ch1_flow_ub, ch1_grad, ch1_int, ch2_flow_lb, ch2_flow_ub, ch2_grad, ch2_int, ch3_flow_lb,
                     ch3_flow_ub, ch3_grad, ch3_int]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['ch1_flow_lb', 'ch1_flow_ub', 'ch1_grad', 'ch1_int', 
                                                              'ch2_flow_lb', 'ch2_flow_ub', 'ch2_grad', 'ch2_int', 
                                                              'ch3_flow_lb', 'ch3_flow_ub', 'ch3_grad', 'ch3_int'])
        piecewise_pressure = piecewise_pressure.append(temp_df, ignore_index = True)
    
    ##Checking which step the flowrate falls in and the right bounds
    check_ch1 = 0
    check_ch2 = 0
    check_ch3 = 0
    
    for i in range (0, steps):
        if check_ch1 == 0:
            if (chiller_input['Value'][0] >= piecewise_pressure['ch1_flow_lb'][i]) and (chiller_input['Value'][0] <= piecewise_pressure['ch1_flow_ub'][i]):
                ch1_press_pw = (piecewise_pressure['ch1_grad'][i] * chiller_input['Value'][0]) + piecewise_pressure['ch1_int'][i]
                check_ch1 = 1
        if check_ch2 == 0:
            if (chiller_input['Value'][2] >= piecewise_pressure['ch2_flow_lb'][i]) and (chiller_input['Value'][2] <= piecewise_pressure['ch2_flow_ub'][i]):
                ch2_press_pw = (piecewise_pressure['ch2_grad'][i] * chiller_input['Value'][2]) + piecewise_pressure['ch2_int'][i]
                check_ch2 = 1
        if check_ch3 == 0:
            if (chiller_input['Value'][4] >= piecewise_pressure['ch3_flow_lb'][i]) and (chiller_input['Value'][4] <= piecewise_pressure['ch3_flow_ub'][i]):
                ch3_press_pw = (piecewise_pressure['ch3_grad'][i] * chiller_input['Value'][4]) + piecewise_pressure['ch3_int'][i]
                check_ch3 = 1
        if (check_ch1 != 0) and (check_ch2 != 0) and (check_ch3 != 0):
            break

        
    return_values['Chiller1_cond_pump_delp'] = ch1_press_pw
    return_values['Chiller2_cond_pump_delp'] = ch2_press_pw
    return_values['Chiller3_cond_pump_delp'] = ch3_press_pw

    ##Using the regression model to determine the electricity consumption 
    ch1_ret_values = cond_pump_nwk_regress(cond_pump_1_delp, cond_pump_1_elect, ch1_cond_nwk_flow_limit, ch1_nwk_coeff, common_nwk_coeff)
    ch2_ret_values = cond_pump_nwk_regress(cond_pump_2_delp, cond_pump_2_elect, ch2_cond_nwk_flow_limit, ch2_nwk_coeff, common_nwk_coeff)    
    ch3_ret_values = cond_pump_nwk_regress(cond_pump_3_delp, cond_pump_3_elect, ch3_cond_nwk_flow_limit, ch3_nwk_coeff, common_nwk_coeff)
    
    return_values['Chiller1_cond_pump_max_flow'] = ch1_ret_values[3,0]  
    return_values['Chiller2_cond_pump_max_flow'] = ch2_ret_values[3,0]     
    return_values['Chiller3_cond_pump_max_flow'] = ch3_ret_values[3,0]    
    
    ch1_elect_cons = ch1_ret_values[0,0]*chiller_input['Value'][0] + ch1_ret_values[1,0]*ch1_press_pw + ch1_ret_values[2,0]
    ch2_elect_cons = ch2_ret_values[0,0]*chiller_input['Value'][2] + ch2_ret_values[1,0]*ch2_press_pw + ch2_ret_values[2,0]
    ch3_elect_cons = ch3_ret_values[0,0]*chiller_input['Value'][4] + ch2_ret_values[1,0]*ch3_press_pw + ch3_ret_values[2,0]       

    return_values['Chiller1_cond_pump_elect_cons'] = ch1_elect_cons 
    return_values['Chiller2_cond_pump_elect_cons'] = ch2_elect_cons 
    return_values['Chiller3_cond_pump_elect_cons'] = ch3_elect_cons  

    ##Bilinear estimation of the outlet temperature 
    total_cond_nwk_flow = chiller_input['Value'][0] + chiller_input['Value'][2] + chiller_input['Value'][4]
    if total_cond_nwk_flow != 0:
        ch1_cond_perc = chiller_input['Value'][0] / total_cond_nwk_flow
        ch2_cond_perc = chiller_input['Value'][2] / total_cond_nwk_flow
        ch3_cond_perc = chiller_input['Value'][4] / total_cond_nwk_flow

    m_perc_min = 0
    m_perc_max = 1
    tcond_out_min = 273.15 + 1
    tcond_out_max = tcond_in                ##It is reasonable to do this because all the chillers have the same condenser inlet temperature
    
    u_min_overall = m_perc_min + tcond_out_min
    u_max_overall = m_perc_max + tcond_out_max
    v_min_overall = m_perc_min - tcond_out_max
    v_max_overall = m_perc_max - tcond_out_min
    
    u_step = (u_max_overall - u_min_overall) / bilinear_pieces
    v_step = (v_max_overall - v_min_overall) / bilinear_pieces
    
    u_values = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int'])
    v_values = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int'])
    
    for i in range (0, bilinear_pieces):
        ##Handling u values first 
        u1 = (i * u_step) + u_min_overall
        u2 = ((i+1) * u_step) + u_min_overall
        f_u1 = 0.25 * pow(u1, 2)
        f_u2 = 0.25 * pow(u2, 2)
        u_grad = (f_u2 - f_u1) / (u2 - u1)
        u_int = f_u2 - (u2 * u_grad)
        bilin_data = [u1, u2, u_grad, u_int]
        bilin_pieces_list_temp = pd.DataFrame(data = [bilin_data], columns = ['lb', 'ub', 'grad', 'int'])
        u_values = u_values.append(bilin_pieces_list_temp, ignore_index = True)

        ##Handling v values next
        v1 = (i * v_step) + v_min_overall
        v2 = ((i+1) * v_step) + v_min_overall
        f_v1 = 0.25 * pow(v1, 2)
        f_v2 = 0.25 * pow(v2, 2)
        v_grad = (f_v2 - f_v1) / (v2 - v1)
        v_int = f_v2 - (v2 * v_grad)          
        bilin_data = [v1, v2, v_grad, v_int]
        bilin_pieces_list_temp = pd.DataFrame(data = [bilin_data], columns = ['lb', 'ub', 'grad', 'int'])        
        v_values = v_values.append(bilin_pieces_list_temp, ignore_index = True)
    
    ##Here, we need to compare the actual values of u and v, using the correct ones to predict resultant temperature output
    ##The bilinearization only takes place at the chiller level, the sum is what we are interested in.
    ##As all chillers are subjected to the same set of u and vs, we can establish them individually 
    
    ch1_u_actual = ch1_cond_perc + chiller_input['Value'][1]
    ch2_u_actual = ch2_cond_perc + chiller_input['Value'][3]
    ch3_u_actual = ch3_cond_perc + chiller_input['Value'][5]
    
    ch1_v_actual = ch1_cond_perc - chiller_input['Value'][1]
    ch2_v_actual = ch2_cond_perc - chiller_input['Value'][3]
    ch3_v_actual = ch3_cond_perc - chiller_input['Value'][5]
    
    check_ch1_u = 0
    check_ch2_u = 0
    check_ch3_u = 0
    check_ch1_v = 0
    check_ch2_v = 0
    check_ch3_v = 0

    for i in range (0, bilinear_pieces):
        ##Checking for chiller 1 values
        if check_ch1_u == 0:
            if (ch1_u_actual >= u_values['lb'][i]) and (ch1_u_actual <= u_values['ub'][i]):
                check_ch1_u = 1
                ch1_fu_value = (u_values['grad'][i] * ch1_u_actual) + u_values['int'][i]
        if check_ch1_v == 0:
            if (ch1_v_actual >= v_values['lb'][i]) and (ch1_v_actual <= v_values['ub'][i]):
                check_ch1_v = 1
                ch1_fv_value = (v_values['grad'][i] * ch1_v_actual) + v_values['int'][i]            
        ##Checking for chiller 2 values
        if check_ch2_u == 0:
            if (ch2_u_actual >= u_values['lb'][i]) and (ch2_u_actual <= u_values['ub'][i]):
                check_ch2_u = 1
                ch2_fu_value = (u_values['grad'][i] * ch2_u_actual) + u_values['int'][i]
        if check_ch2_v == 0:
            if (ch2_v_actual >= v_values['lb'][i]) and (ch2_v_actual <= v_values['ub'][i]):
                check_ch2_v = 1
                ch2_fv_value = (v_values['grad'][i] * ch2_v_actual) + v_values['int'][i]        
        ##Checking for chiller 3 values
        if check_ch3_u == 0:
            if (ch3_u_actual >= u_values['lb'][i]) and (ch3_u_actual <= u_values['ub'][i]):
                check_ch3_u = 1
                ch3_fu_value = (u_values['grad'][i] * ch3_u_actual) + u_values['int'][i]
        if check_ch3_v == 0:
            if (ch3_v_actual >= v_values['lb'][i]) and (ch3_v_actual <= v_values['ub'][i]):
                check_ch3_v = 1
                ch3_fv_value = (v_values['grad'][i] * ch3_v_actual) + v_values['int'][i]
        ##Checking if it is time to break the loop
        if (check_ch1_u != 0) and (check_ch2_u != 0) and (check_ch3_u != 0) and (check_ch1_v != 0) and (check_ch2_v != 0) and (check_ch3_v != 0):
            break
    
    ##Calculating the real values 
    ch1_est_out = ch1_fu_value - ch1_fv_value
    ch2_est_out = ch2_fu_value - ch2_fv_value
    ch3_est_out = ch3_fu_value - ch3_fv_value
    
    tout_cond_nwk = ch1_est_out + ch2_est_out + ch3_est_out
    
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
    
###############################################################################################################################################################
##Additional functions 
def cond_pump_nwk_regress (pump_coeff_delp, pump_coeff_elect, max_flow, nwk_coeff, common_nwk_coeff):
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'  
    import sys 
    sys.path.append(current_path + 'add_on_functions\\')
    from golden_section import golden_section_evap_cond_regress
    import numpy as np
    from sklearn import linear_model 
    import matplotlib.pyplot as plt 
    
    ##pump_coeff_delp[0] --- x2 coefficient
    ##pump_coeff_delp[1] --- x coefficient
    ##pump_coeff_delp[2] --- cst term
    
    ##pump_coeff_elect[0] --- x3 coefficient
    ##pump_coeff_elect[1] --- x2 coefficient
    ##pump_coeff_elect[2] --- x coefficient
    ##pump_coeff_elect[3] --- cst term
    
    ##max_flow --- maximum flow for the configuration (requires precalculation)
    ##nwk_coeff --- specific to the parallel branch 
    ##common_nwk_coeff --- the shared branch

    ##Network parameters 
    cond_nwk_A_val = nwk_coeff + common_nwk_coeff
    ##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case 
    func_bounds = [0, 3200]
    config_max_flow = golden_section_evap_cond_regress(pump_sys_int_evap_cond_regress, func_bounds, cond_nwk_A_val, pump_coeff_delp)
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
        min_p = cond_nwk_A_val*pow(c_fr, 1.852)
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
    cond_pump_m_coeff = lin_coeff[0,0]
    cond_pump_p_coeff = lin_coeff[0,1]
    cond_pump_cst = int_lin
    cond_pump_max_flow = config_max_flow
    cond_pump_regress_r2 = result
    
    ret_values = np.zeros((5,1))
    ret_values[0,0] = cond_pump_m_coeff
    ret_values[1,0] = cond_pump_p_coeff
    ret_values[2,0] = cond_pump_cst
    ret_values[3,0] = cond_pump_max_flow
    ret_values[4,0] = cond_pump_regress_r2    

    return ret_values
    
##Function to calculate the deviation between the pump and system curves, this function is to be used  
def pump_sys_int_evap_cond (sys_coeff, pump_coeffs, sys_offset, flow):
    ##sys_coeff --- the single coefficient of the system curve 
    ##pump_coeffs[0] --- x2 coefficient 
    ##pump_coeffs[1] --- x coefficient
    ##pump_coeffs[2] --- constant term 
    ##flow --- the flowrate which the intersection point may be 
    
    sys_curve_value = (sys_coeff*pow(flow, 1.852)) + sys_offset
    pump_curve_value = (pump_coeffs[0] * pow(flow, 2)) + (pump_coeffs[1] * flow) + pump_coeffs[2]
    ret_value = abs(pump_curve_value - sys_curve_value)
    ##print(sys_curve_value)
    ##print(pump_curve_value)
    #print(sys_curve_value, pump_curve_value, ret_value)
    
    return ret_value
    
def pump_sys_int_evap_cond_regress (sys_coeff, pump_coeffs, flow):
    ##sys_coeff --- the single coefficient of the system curve 
    ##pump_coeffs[0] --- x2 coefficient 
    ##pump_coeffs[1] --- x coefficient
    ##pump_coeffs[2] --- constant term 
    ##flow --- the flowrate which the intersection point may be 
    
    sys_curve_value = (sys_coeff*pow(flow, 1.852))
    pump_curve_value = (pump_coeffs[0] * pow(flow, 2)) + (pump_coeffs[1] * flow) + pump_coeffs[2]
    ret_value = abs(pump_curve_value - sys_curve_value)
    ##print(sys_curve_value)
    ##print(pump_curve_value)
    #print(sys_curve_value, pump_curve_value, ret_value)
    
    return ret_value