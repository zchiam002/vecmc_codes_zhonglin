##This is a simulation case scenario of the following:
    ##3 chillers, consolidated demand and the common pipe
    ##
    
def input_control ():
    
    import numpy as np 
    import pandas as pd 
    
    ##Variables 
    piecewise_steps = 4
    bilinear_pieces = 20
    twb_limit = 15
    chilled_water_setpoint = 5
    network_dt_target = 4
        
    ##Loading demand 
    demand_loc = 'C:\\Optimization_zlc\\input_data\\3_chiller_1_demand_12ts_3_period_input_data\\high_load\\high_demand.csv'
    demand_day = pd.read_csv(demand_loc)

    ##Running simulation 
    running_simulation (chilled_water_setpoint, demand_day, network_dt_target, piecewise_steps, bilinear_pieces, twb_limit)
    
    return


#######################################################################################################################################################
##Supporting functions 

def running_simulation (chilled_water_setpoint, demand_day, network_dt_target, piecewise_steps, bilinear_pieces, twb_limit):
    
    import numpy as np 
    import pandas as pd 
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from chiller_models import chiller_gnu_stepwise_cop_lprelax
    
    
    ##Chiller 1 settings 
    ch1_Tout_evap = chilled_water_setpoint
    ch1_Tin_cond = 25
    ch1_mevap = 200
    ch1_mcond = 330
    ch1_Qe_max = 2000
    ch1_mevap_t = 218.3903135
    ch1_mcond_t = 561.0120813
    
    ##Chiller 2 settings 
    ch2_Tout_evap = chilled_water_setpoint
    ch2_Tin_cond = 25
    ch2_mevap1 = 450
    ch2_mevap2 = 800
    ch2_mcond = 1180
    ch2_Qe_max = 7330
    ch2_mevap_t = 820.4531779
    ch2_mcond_t = 1829.472166    
    
    ##Chiller 3 settings 
    ch3_Tout_evap = chilled_water_setpoint
    ch3_Tin_cond = 25
    ch3_mevap1 = 450
    ch3_mevap2 = 800
    ch3_mcond = 1180
    ch3_Qe_max = 7330
    ch3_mevap_t = 820.4531779
    ch3_mcond_t = 1829.472166   
    
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
    
    parameters = pd.DataFrame(columns = ['Name', 'Value'])
    temp_data = ['chilled_water_setpoint', chilled_water_setpoint]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)
    temp_data = ['network_dt_target', network_dt_target]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)
    temp_data = ['piecewise_steps', piecewise_steps]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)
    temp_data = ['bilinear_pieces', bilinear_pieces]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)    
    temp_data = ['twb_limit', 25]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)     
    temp_data = ['ch1_mevap', ch1_mevap]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True) 
    temp_data = ['ch2_mevap1', ch2_mevap1]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)
    temp_data = ['ch2_mevap2', ch2_mevap2]
    temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Value'])
    parameters = parameters.append(temp_df, ignore_index = True)
    
    parameters.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\simulation_cases\\results\\parameters.csv')
    
    consolidated_results = pd.DataFrame(columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
    
    for i in range (0, time_steps):
        current_demand = demand_day['ss_gv2_demand'][i] + demand_day['ss_hsb_demand'][i] + demand_day['ss_pfa_demand'][i] + demand_day['ss_ser_demand'][i] + demand_day['ss_fir_demand'][i]
        req_flow = (current_demand / (4.2 * network_dt_target)) /998.2 * 3600
        
        print('time_step', i)
        print('demand', current_demand)
        print('required flow', req_flow)
        
        ##Choice 1 use chiller 1 only 
        if req_flow <= ch1_mevap:
            reg_cst_c1 = [ch1_b0, ch1_b1, ch1_b2]
            qc_coeff_c1 = ch1_qc_coeff 
            Tin_cond_c1 = ch1_Tin_cond 
            Tout_evap_c1 = ch1_Tout_evap
            mevap_c1 = ch1_mevap
            mcond_c1 = ch1_mcond
            Qe_max_c1 = ch1_Qe_max
            mevap_t_c1 = ch1_mevap_t
            mcond_t_c1 = ch1_mcond_t
            
            ##Calculating the return temperature to the chillers 
            cp_flow = ch1_mevap - req_flow 
            Tin_evap_c1 = ((req_flow/mevap_c1)*(Tout_evap_c1 + network_dt_target)) + ((cp_flow/mevap_c1)*(Tout_evap_c1))
            print('ret_temp', Tin_evap_c1)
            return_values, return_values_df = chiller_gnu_stepwise_cop_lprelax (reg_cst_c1, qc_coeff_c1, Tin_evap_c1, Tout_evap_c1, Tin_cond_c1, mevap_c1, mcond_c1, Qe_max_c1, piecewise_steps, bilinear_pieces, mevap_t_c1, mcond_t_c1, twb_limit)
           
            temp_data = [current_demand, req_flow, Tin_evap_c1, return_values_df['Value'][0], return_values_df['Value'][1], return_values_df['Value'][2], return_values_df['Value'][3], return_values_df['Value'][4]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results = consolidated_results.append(temp_df, ignore_index = True)
            
            
        #Choice 2a use chiller 2 or 3 only for flow 1         
        elif (req_flow <= ch2_mevap1) and (req_flow > ch1_mevap):
            reg_cst_c2a = [ch2_b0, ch2_b1, ch2_b2]
            qc_coeff_c2a = ch2_qc_coeff 
            Tin_cond_c2a = ch2_Tin_cond 
            Tout_evap_c2a = ch2_Tout_evap
            mevap_c2a = ch2_mevap1
            mcond_c2a = ch2_mcond
            Qe_max_c2a = ch2_Qe_max
            mevap_t_c2a = ch2_mevap_t
            mcond_t_c2a = ch2_mcond_t
            
            ##Calculating the return temperature to the chillers 
            cp_flow = ch2_mevap1 - req_flow 
            Tin_evap_c2a = ((req_flow/mevap_c2a)*(Tout_evap_c2a + network_dt_target)) + ((cp_flow/mevap_c2a)*(Tout_evap_c2a))
            print('ret_temp', Tin_evap_c2a)
            return_values, return_values_df = chiller_gnu_stepwise_cop_lprelax (reg_cst_c2a, qc_coeff_c2a, Tin_evap_c2a, Tout_evap_c2a, Tin_cond_c2a, mevap_c2a, mcond_c2a, Qe_max_c2a, piecewise_steps, bilinear_pieces, mevap_t_c2a, mcond_t_c2a, twb_limit)            

            temp_data = [current_demand, req_flow, Tin_evap_c2a, return_values_df['Value'][0], return_values_df['Value'][1], return_values_df['Value'][2], return_values_df['Value'][3], return_values_df['Value'][4]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results = consolidated_results.append(temp_df, ignore_index = True)

        ##Choice 2b use chiller 2 or 3 only for higher flow 2            
        elif (req_flow <= ch2_mevap2) and (req_flow > ch2_mevap1):
            reg_cst_c2b = [ch2_b0, ch2_b1, ch2_b2]
            qc_coeff_c2b = ch2_qc_coeff 
            Tin_cond_c2b = ch2_Tin_cond 
            Tout_evap_c2b = ch2_Tout_evap
            mevap_c2b = ch2_mevap2
            mcond_c2b = ch2_mcond
            Qe_max_c2b = ch2_Qe_max
            mevap_t_c2b = ch2_mevap_t
            mcond_t_c2b = ch2_mcond_t
            
            ##Calculating the return temperature to the chillers 
            cp_flow = ch2_mevap2 - req_flow 
            Tin_evap_c2b = ((req_flow/mevap_c2b)*(Tout_evap_c2b + network_dt_target)) + ((cp_flow/mevap_c2b)*(Tout_evap_c2b))
            print('ret_temp', Tin_evap_c2b)
            return_values, return_values_df = chiller_gnu_stepwise_cop_lprelax (reg_cst_c2b, qc_coeff_c2b, Tin_evap_c2b, Tout_evap_c2b, Tin_cond_c2b, mevap_c2b, mcond_c2b, Qe_max_c2b, piecewise_steps, bilinear_pieces, mevap_t_c2b, mcond_t_c2b, twb_limit)                        

            temp_data = [current_demand, req_flow, Tin_evap_c2b, return_values_df['Value'][0], return_values_df['Value'][1], return_values_df['Value'][2], return_values_df['Value'][3], return_values_df['Value'][4]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Total_demand', 'Required_flow', 'Ret_temp', 'Elect_cons', 'COP', 'Cooling_load', 'Tout_cond', 'Heat_rejected'])
            consolidated_results = consolidated_results.append(temp_df, ignore_index = True)
        
        ##Choice 3 use chiller 1 and 2 only         
        ##Choice 4 use chiller 2 and 3 only 
        ##Choice 5 use chiller 1, 2 and 3
        
        
    
    consolidated_results.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\simulation_cases\\results\\consolidated_results.csv')
    
    
    
    
    
    
    
    
    return 


#########################################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    input_control()




