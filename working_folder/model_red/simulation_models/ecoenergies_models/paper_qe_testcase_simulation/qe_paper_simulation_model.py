##This is a simulation case scenario of the following:
    ##3 chillers, consolidated demand and the common pipe
    ##
    
def input_control ():
    
    import numpy as np 
    import pandas as pd 
    
    ##Variables 
    variables = {}
    variables['piecewise_steps'] = 4
    variables['bilinear_pieces'] = 20
    variables['twb_approach_limit'] = 5
    variables['chilled_water_setpoint'] = 5
    variables['gv2_dt_target'] = 1.5
    variables['hsb_dt_target'] = 6.5
    variables['pfa_dt_target'] = 3
    variables['ser_dt_target'] = 3
    
    load_type = 'high'
    
    ##Loading demand 
    demand_loc = 'C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\'+ load_type +'_load\\' + load_type + '_demand.csv'
    demand_day = pd.read_csv(demand_loc)
    ##Loading weather data 
    weather_loc = 'C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\' + load_type + '_load\\' + load_type +'_demand_weather.csv'
    weather_day = pd.read_csv(weather_loc)
    
    ##Result location 
    result_loc_store = 'C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\paper_qe_testcase_simulation\\results\\'
    
    ##Running simulation 
    running_simulation (variables, demand_day, weather_day, result_loc_store)
    
    return


#######################################################################################################################################################
##Supporting functions 

def running_simulation (variables, demand_day, weather_day, result_loc_store):
    
    import numpy as np 
    import pandas as pd 
    
    ##Saving the parameters 
    save_parameters (variables, result_loc_store)
    
    ##Determining the required flowrate and the target delta t required on the chiller side and which chillers are operational 
    flow_dt_info, chiller_on_off = determine_dt_flow_chiller (variables, demand_day, result_loc_store)
    
    ##Preparing the initial values for the optimization 
    prepare_seeding_values (flow_dt_info, variables, result_loc_store)
    
    ##Determining the electricity consumption of the chiller and the cop
    determine_chiller_operation (variables, demand_day, weather_day, flow_dt_info, chiller_on_off, result_loc_store)
    
    ##Determining the electricity consumption of the evaporator and condenser pumps
        ##Determine the pressure drop in each evaporator network 
        ##Determine the corresponding pump electricity consumption 
        
    ##Determine the electicity consumption of the distribution pumps 
        ##Determine the pressure drop in the condenser network 
        ##Determine the corresponding pump electicity consumption 

    ##Do a rough estimation of the cooling tower electricity consumption        
    
    
    
    return 

#########################################################################################################################################################################
##Additional functions 

##This function prepares the seeding values for the optimization case 
def prepare_seeding_values (flow_dt_info, variables, result_loc_store):
    
    import numpy as np 
    import pandas as pd 

    ch1_cond_flow = 407
    ch2_cond_flow = 1476
    ch3_cond_flow = 1476 
    
    cond_flow_combi = [ch1_cond_flow, ch2_cond_flow, ch1_cond_flow+ch2_cond_flow, ch2_cond_flow+ch3_cond_flow, ch1_cond_flow+ch2_cond_flow+ch3_cond_flow]
    
    dim_flow_dt_info = flow_dt_info.shape  
    
    ##Initiating a return dataframe 
    seeding_values = pd.DataFrame(columns = ['evap_flow', 'T_evap_in', 'cond_flow'])
    
    for i in range (0, dim_flow_dt_info[0]):
        ##Determining the total evaporator flowrate 
        evap_flow_total = flow_dt_info['gv2_req_flow'][i] + flow_dt_info['hsb_req_flow'][i] + flow_dt_info['pfa_req_flow'][i] + flow_dt_info['ser_req_flow'][i] + flow_dt_info['cp_flow'][i]
        ##Determining the chiller return temperature 
        chil_ret_temp = flow_dt_info['req_dt_evap'][i] + variables['chilled_water_setpoint'] + 273.15
        ##Determining the condenser flow number code
        for j in range (0, len(cond_flow_combi)):
            if flow_dt_info['req_cond_flow'][i] <= cond_flow_combi[j] + 1:
                cond_flow_total = j
                break
            
        ##Adding buffers
        evap_flow_total = evap_flow_total + 2
        chil_ret_temp = chil_ret_temp + 2
        
        temp_data = [evap_flow_total, chil_ret_temp, cond_flow_total]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['evap_flow', 'T_evap_in', 'cond_flow'])
        seeding_values = seeding_values.append(temp_df, ignore_index = True)
    
    seeding_values.to_csv(result_loc_store + 'seeding_values.csv')
    
    return 

##This function determines corresponding outputs based on current chiller operation 
def determine_chiller_operation (variables, demand_day, weather_day, flow_dt_info, chiller_on_off, result_loc_store):
    
    import numpy as np 
    import pandas as pd 
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from chiller_models import chiller_gnu_stepwise_cop_lprelax
    
    
    ##Chiller 1 settings 
    ch1_Tout_evap = variables['chilled_water_setpoint']
    ch1_Qe_max = 2000
    ch1_mevap = 218.3903135
    ch1_mcond = 407
    
    ##Chiller 2 settings 
    ch2_Tout_evap = variables['chilled_water_setpoint']
    ch2_mevap1 = 820.4531779 / 2
    ch2_mevap2 = 820.4531779
    ch2_mcond = 1476
    ch2_Qe_max = 7330 
    
    ##Chiller 3 settings 
    ch3_Tout_evap = variables['chilled_water_setpoint']
    ch3_mevap1 = 820.4531779 / 2
    ch3_mevap2 = 820.4531779
    ch3_mcond = 1180
    ch3_Qe_max = 7330
    
    ##Chiller 1 coefficients
    ch1_b0 = 0.123020043325872
    ch1_b1 = 1044.79734873891
    ch1_b2 = 0.0204660495029597
    ch1_qc_coeff = 1.09866273284186
    
    ##Chiller 2 coefficients 
    ch2_b0 = 1.35049420632748
    ch2_b1 = -134.853705222833
    ch2_b2 = 0.00430128306723068
    ch2_qc_coeff = 1.10348067074030
    
    ##Chiller 3 coefficients 
    ch3_b0 = 1.35049420632748
    ch3_b1 = -134.853705222833
    ch3_b2 = 0.00430128306723068
    ch3_qc_coeff = 1.10348067074030
    
    ##Determine input demand time steps 
    dim_demand_day = demand_day.shape
    time_steps = dim_demand_day[0]
    bilinear_pieces = variables['bilinear_pieces']
    piecewise_steps = variables['piecewise_steps']
    

    ##Initializing a dataframe to hold the return results
    consolidated_results_ch1 = pd.DataFrame(columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
    consolidated_results_ch2a = pd.DataFrame(columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
    consolidated_results_ch2b = pd.DataFrame(columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
    consolidated_results_ch3a = pd.DataFrame(columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
    consolidated_results_ch3b = pd.DataFrame(columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])

    for i in range (0, time_steps):
        
        print('time_step', i)
        current_demand = demand_day['ss_gv2_demand'][i] + demand_day['ss_hsb_demand'][i] + demand_day['ss_pfa_demand'][i] + demand_day['ss_ser_demand'][i]
        req_flow_evap = flow_dt_info['gv2_req_flow'][i] + flow_dt_info['hsb_req_flow'][i] + flow_dt_info['pfa_req_flow'][i] + flow_dt_info['ser_req_flow'][i] + flow_dt_info['cp_flow'][i] 
        total_cond_nwk_flow = flow_dt_info['req_cond_flow'][i]
        cond_tin = weather_day['T_WB'][i] + variables['twb_approach_limit']
        
        t_wb = weather_day['T_WB'][i]
        
        ##Determine chiller operation 
            ##Chiller 1 operation 
        if chiller_on_off['ch1'][i] == 1:
            reg_cst_c1 = [ch1_b0, ch1_b1, ch1_b2]
            qc_coeff_c1 = ch1_qc_coeff 
            Tin_cond_c1 = cond_tin 
            Tout_evap_c1 = ch1_Tout_evap
            mevap_c1 = ch1_mevap
            mcond_c1 = ch1_mcond
            Qe_max_c1 = ch1_Qe_max
            mevap_t_c1 = req_flow_evap
            mcond_t_c1 = total_cond_nwk_flow            
        
            ##Calculating the return temperature to the chillers 
            Tin_evap_c1 = flow_dt_info['req_dt_evap'][i] + Tout_evap_c1
            return_values, return_values_df = chiller_gnu_stepwise_cop_lprelax (reg_cst_c1, qc_coeff_c1, Tin_evap_c1, Tout_evap_c1, Tin_cond_c1, mevap_c1, mcond_c1, Qe_max_c1, piecewise_steps, bilinear_pieces, mevap_t_c1, mcond_t_c1, t_wb)
           
            temp_data = [current_demand, req_flow_evap, Tin_evap_c1, return_values_df['Value'][0], return_values_df['Value'][1], return_values_df['Value'][2], return_values_df['Value'][3], return_values_df['Value'][4]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results_ch1 = consolidated_results_ch1.append(temp_df, ignore_index = True)
        else:
            temp_data = [current_demand, req_flow_evap, 0, 0, 0, 0, 0, 0]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results_ch1 = consolidated_results_ch1.append(temp_df, ignore_index = True)
            
            ##Chiller 2a operation
        if chiller_on_off['ch2a'][i] == 1:
            reg_cst_c2a = [ch2_b0, ch2_b1, ch2_b2]
            qc_coeff_c2a = ch2_qc_coeff 
            Tin_cond_c2a = cond_tin 
            Tout_evap_c2a = ch2_Tout_evap
            mevap_c2a = ch2_mevap1
            mcond_c2a = ch2_mcond
            Qe_max_c2a = ch2_Qe_max
            mevap_t_c2a = req_flow_evap
            mcond_t_c2a = total_cond_nwk_flow            
        
            ##Calculating the return temperature to the chillers 
            Tin_evap_c2a = flow_dt_info['req_dt_evap'][i] + Tout_evap_c2a
            return_values, return_values_df = chiller_gnu_stepwise_cop_lprelax (reg_cst_c2a, qc_coeff_c2a, Tin_evap_c2a, Tout_evap_c2a, Tin_cond_c2a, mevap_c2a, mcond_c2a, Qe_max_c2a, piecewise_steps, bilinear_pieces, mevap_t_c2a, mcond_t_c2a, t_wb)
           
            temp_data = [current_demand, req_flow_evap, Tin_evap_c2a, return_values_df['Value'][0], return_values_df['Value'][1], return_values_df['Value'][2], return_values_df['Value'][3], return_values_df['Value'][4]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results_ch2a = consolidated_results_ch2a.append(temp_df, ignore_index = True)
        else:
            temp_data = [current_demand, req_flow_evap, 0, 0, 0, 0, 0, 0]        
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results_ch2a = consolidated_results_ch2a.append(temp_df, ignore_index = True)        
        
            ##Chiller 2b operation
        if chiller_on_off['ch2b'][i] == 1:
            reg_cst_c2b = [ch2_b0, ch2_b1, ch2_b2]
            qc_coeff_c2b = ch2_qc_coeff 
            Tin_cond_c2b = cond_tin 
            Tout_evap_c2b = ch2_Tout_evap
            mevap_c2b = ch2_mevap2
            mcond_c2b = ch2_mcond
            Qe_max_c2b = ch2_Qe_max
            mevap_t_c2b = req_flow_evap
            mcond_t_c2b = total_cond_nwk_flow            
        
            ##Calculating the return temperature to the chillers 
            Tin_evap_c2b = flow_dt_info['req_dt_evap'][i] + Tout_evap_c2b
            return_values, return_values_df = chiller_gnu_stepwise_cop_lprelax (reg_cst_c2b, qc_coeff_c2b, Tin_evap_c2b, Tout_evap_c2b, Tin_cond_c2b, mevap_c2b, mcond_c2b, Qe_max_c2b, piecewise_steps, bilinear_pieces, mevap_t_c2b, mcond_t_c2b, t_wb)
           
            temp_data = [current_demand, req_flow_evap, Tin_evap_c2b, return_values_df['Value'][0], return_values_df['Value'][1], return_values_df['Value'][2], return_values_df['Value'][3], return_values_df['Value'][4]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results_ch2b = consolidated_results_ch2b.append(temp_df, ignore_index = True)
        else:
            temp_data = [current_demand, req_flow_evap, 0, 0, 0, 0, 0, 0]        
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results_ch2b = consolidated_results_ch2b.append(temp_df, ignore_index = True)          
        
            ##Chiller 3a operation
        if chiller_on_off['ch3a'][i] == 1:
            reg_cst_c3a = [ch3_b0, ch3_b1, ch3_b2]
            qc_coeff_c3a = ch3_qc_coeff 
            Tin_cond_c3a = cond_tin 
            Tout_evap_c3a = ch3_Tout_evap
            mevap_c3a = ch3_mevap1
            mcond_c3a = ch3_mcond
            Qe_max_c3a = ch3_Qe_max
            mevap_t_c3a = req_flow_evap
            mcond_t_c3a = total_cond_nwk_flow            
        
            ##Calculating the return temperature to the chillers 
            Tin_evap_c3a = flow_dt_info['req_dt_evap'][i] + Tout_evap_c3a
            return_values, return_values_df = chiller_gnu_stepwise_cop_lprelax (reg_cst_c3a, qc_coeff_c3a, Tin_evap_c3a, Tout_evap_c3a, Tin_cond_c3a, mevap_c3a, mcond_c3a, Qe_max_c3a, piecewise_steps, bilinear_pieces, mevap_t_c3a, mcond_t_c3a, t_wb)
           
            temp_data = [current_demand, req_flow_evap, Tin_evap_c3a, return_values_df['Value'][0], return_values_df['Value'][1], return_values_df['Value'][2], return_values_df['Value'][3], return_values_df['Value'][4]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results_ch3a = consolidated_results_ch3a.append(temp_df, ignore_index = True)
        else:
            temp_data = [current_demand, req_flow_evap, 0, 0, 0, 0, 0, 0]        
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results_ch3a = consolidated_results_ch3a.append(temp_df, ignore_index = True)           
        
            ##Chiller 3b operation
        if chiller_on_off['ch3b'][i] == 1:
            reg_cst_c3b = [ch3_b0, ch3_b1, ch3_b2]
            qc_coeff_c3b = ch3_qc_coeff 
            Tin_cond_c3b = cond_tin 
            Tout_evap_c3b = ch3_Tout_evap
            mevap_c3b = ch3_mevap2
            mcond_c3b = ch3_mcond
            Qe_max_c3b = ch3_Qe_max
            mevap_t_c3b = req_flow_evap
            mcond_t_c3b = total_cond_nwk_flow            
        
            ##Calculating the return temperature to the chillers 
            Tin_evap_c3b = flow_dt_info['req_dt_evap'][i] + Tout_evap_c3b
            return_values, return_values_df = chiller_gnu_stepwise_cop_lprelax (reg_cst_c3b, qc_coeff_c3b, Tin_evap_c3b, Tout_evap_c3b, Tin_cond_c3b, mevap_c3b, mcond_c3b, Qe_max_c3b, piecewise_steps, bilinear_pieces, mevap_t_c3b, mcond_t_c3b, t_wb)
           
            temp_data = [current_demand, req_flow_evap, Tin_evap_c3b, return_values_df['Value'][0], return_values_df['Value'][1], return_values_df['Value'][2], return_values_df['Value'][3], return_values_df['Value'][4]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results_ch3b = consolidated_results_ch3b.append(temp_df, ignore_index = True)
        else:
            temp_data = [current_demand, req_flow_evap, 0, 0, 0, 0, 0, 0]        
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results_ch3b = consolidated_results_ch3b.append(temp_df, ignore_index = True)          
        
    
    consolidated_results_ch1.to_csv(result_loc_store + 'consolidated_results_ch1.csv')    
    consolidated_results_ch2a.to_csv(result_loc_store + 'consolidated_results_ch2a.csv')  
    consolidated_results_ch2b.to_csv(result_loc_store + 'consolidated_results_ch2b.csv')  
    consolidated_results_ch3a.to_csv(result_loc_store + 'consolidated_results_ch3a.csv')  
    consolidated_results_ch3b.to_csv(result_loc_store + 'consolidated_results_ch3b.csv')  
                    
    return 

##This function determines the required flowrate and target delta t required on the chiller side 
def determine_dt_flow_chiller (variables, demand_day, result_loc_store):
    
    import numpy as np 
    import pandas as pd 
    
    dim_demand_day = demand_day.shape 
    
    ch1_evap_flow = 218.3903135
    ch2_evap_flow_1 = 820.4531779 / 2
    ch2_evap_flow_2 = 820.4531779
    ch3_evap_flow_1 = 820.4531779 / 2
    ch3_evap_flow_2 = 820.4531779
    
    ch1_cond_flow = 407
    ch2_cond_flow = 1476
    ch3_cond_flow = 1476
    
    ##Options for evap flow
    discrete_evap_flow = []
    discrete_evap_flow.append(ch1_evap_flow)
    discrete_evap_flow.append(ch2_evap_flow_1)   
    discrete_evap_flow.append(ch1_evap_flow + ch2_evap_flow_1)      
    discrete_evap_flow.append(ch2_evap_flow_2) 
    discrete_evap_flow.append(ch2_evap_flow_2 + ch1_evap_flow)   
    discrete_evap_flow.append(ch2_evap_flow_2 + ch3_evap_flow_1)    
    discrete_evap_flow.append(ch2_evap_flow_2 + ch3_evap_flow_1 + ch1_evap_flow) 
    discrete_evap_flow.append(ch2_evap_flow_2 + ch3_evap_flow_2)   
    discrete_evap_flow.append(ch2_evap_flow_2 + ch3_evap_flow_2 + ch1_evap_flow)   
    
    ##Initializing a dataframe to hold the return data 
    flow_dt_info = pd.DataFrame(columns = ['gv2_req_flow', 'hsb_req_flow', 'pfa_req_flow', 'ser_req_flow', 'cp_flow', 'req_dt_evap', 'req_cond_flow'])
    chiller_on_off = pd.DataFrame(columns = ['ch1', 'ch2a', 'ch2b', 'ch3a', 'ch3b'])
    
    
    ##Using the demand to estimate the required evaporator flow
    for i in range(0, dim_demand_day[0]):
        gv2_req_flow = (demand_day['ss_gv2_demand'][i] / (4.2 * variables['gv2_dt_target'])) * (3600 / 998.2)
        hsb_req_flow = (demand_day['ss_hsb_demand'][i] / (4.2 * variables['hsb_dt_target'])) * (3600 / 998.2)        
        pfa_req_flow = (demand_day['ss_pfa_demand'][i] / (4.2 * variables['pfa_dt_target'])) * (3600 / 998.2)       
        ser_req_flow = (demand_day['ss_ser_demand'][i] / (4.2 * variables['ser_dt_target'])) * (3600 / 998.2)
        
        total_demand_req_flow = gv2_req_flow + hsb_req_flow + pfa_req_flow + ser_req_flow
    
        ##Determining the discrete flow which the system will operate at 
        for j in range (0, len(discrete_evap_flow)):
            if total_demand_req_flow <= discrete_evap_flow[j]:
                total_evap_flow = discrete_evap_flow[j]
                key = j
                cp_flow = total_evap_flow - total_demand_req_flow
                break
    
        ##Determining the target dt on the evaporator side of the system 
        total_demand = demand_day['ss_gv2_demand'][i] + demand_day['ss_hsb_demand'][i] + demand_day['ss_pfa_demand'][i] + demand_day['ss_ser_demand'][i]
        total_flow_in_kg_s = total_evap_flow * 998.2 / 3600
        req_dt_evap = total_demand / (total_flow_in_kg_s * 4.2)
        
        ##Determining the discrete flow on the condenser side of the system 
            ##Finding key 
            
        total_cond_flow = 0
            ##Checking if chiller 1 is on
        if key in [0, 2, 4, 6, 8]:
            total_cond_flow = total_cond_flow + ch1_cond_flow 
            ##Checking if chiller 2 is on 
        if key > 0:
            total_cond_flow = total_cond_flow + ch2_cond_flow 
            ##Checking if chiller 3 is on 
        if key > 4:
            total_cond_flow = total_cond_flow + ch3_cond_flow             
        
        temp_data = [gv2_req_flow, hsb_req_flow, pfa_req_flow, ser_req_flow, cp_flow, req_dt_evap, total_cond_flow]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['gv2_req_flow', 'hsb_req_flow', 'pfa_req_flow', 'ser_req_flow', 'cp_flow', 'req_dt_evap', 'req_cond_flow'])
        flow_dt_info = flow_dt_info.append(temp_df, ignore_index = True)
    
        ##Determining the chiller on-off
        temp_data_ch = [0,0,0,0,0]
            ##Checking if chiller 1 is on
        if key in [0, 2, 4, 6, 8]:
            temp_data_ch[0] = 1 
            ##Checking if chiller 2a is on 
        if key in [1, 2]:
            temp_data_ch[1] = 1
            ##Checking if chiller 2b is on 
        if key > 2:
            temp_data_ch[2] = 1 
            ##Checking if chiller 3a is on 
        if key in [5, 6]:
            temp_data_ch[3] = 1
            ##Checking if chiller 3b is on 
        if key > 6:
            temp_data_ch[4] = 1    
        
        temp_df_ch = pd.DataFrame(data = [temp_data_ch], columns = ['ch1', 'ch2a', 'ch2b', 'ch3a', 'ch3b'])
        chiller_on_off = chiller_on_off.append(temp_df_ch, ignore_index = True)
    
    chiller_on_off.to_csv(result_loc_store + 'chiller_on_off.csv')   
    flow_dt_info.to_csv(result_loc_store + 'flow_dt_info.csv')

    return flow_dt_info, chiller_on_off

##This function saves the parameters as a csv file 
def save_parameters (variables, result_loc_store):
    
    import pandas as pd 
    import numpy as np
    
    ##Initialize a return dataframe
    parameters = pd.DataFrame(columns = ['Name', 'Value'])
    
    
    temp_data = ['chilled_water_setpoint', variables['chilled_water_setpoint']]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)
    
    
    temp_data = ['gv2_dt_target', variables['gv2_dt_target']]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)
    temp_data = ['hsb_dt_target', variables['hsb_dt_target']]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)
    temp_data = ['pfa_dt_target', variables['pfa_dt_target']]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)
    temp_data = ['ser_dt_target', variables['ser_dt_target']]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)    
    temp_data = ['piecewise_steps', variables['piecewise_steps']]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)
    temp_data = ['bilinear_pieces', variables['bilinear_pieces']]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)    
    temp_data = ['twb_approach_limit', variables['twb_approach_limit']]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)     
    
    parameters.to_csv(result_loc_store + 'parameters.csv')
    
    return 

#########################################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    input_control()




