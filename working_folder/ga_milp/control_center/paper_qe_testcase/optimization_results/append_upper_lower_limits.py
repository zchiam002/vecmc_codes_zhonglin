##This function appends the lower and upper limited of the variables used in the the optimization program 

def append_lower_upper_limits (dt, time_step):
    
    import numpy as np 
    import pandas as pd
    
    ##Determining the master decisiob variable values 
    mdv_file_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\ga_results_current_store\\' + dt + '_load\\ts_' + str(time_step) + '\\' + 'best_agent_movement.csv'
    
    ##Extract the master decision variables 
    mdv_list = np.genfromtxt(mdv_file_loc, delimiter=',')
    extracted_values_t_ret = mdv_list[30, 0]
    extracted_values_evap_flow = mdv_list[30, 1]
    extracted_values_cond_flow = mdv_list[30, 2]
    
    mdv_used = [extracted_values_t_ret, extracted_values_evap_flow, extracted_values_cond_flow]
        
    ##Determining the wet bulb temperature required 
    wet_bulb_temp_loc = 'C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\' + dt + '_load\\' + dt + '_demand_weather.csv'
    wet_bulb_temp_data = pd.read_csv(wet_bulb_temp_loc)
    
    req_wet_bulb_temp = wet_bulb_temp_data['T_WB'][time_step] + 273.15
    
    ##Determining the total condenser flowrate 
    total_cond_flow = determine_total_cond_flow (mdv_used[2])
    
    ##Loading the list of variables 
    var_list_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\optimization_results\\opti_' + dt + '\\cleansed_varlist_only_' + dt + '.csv'
    var_list_namelist = pd.read_csv(var_list_loc)
    
    ##Create var_name list 
    dim_var_list_namelist = var_list_namelist.shape 
    var_list_all = []
    upper_limit = []
    lower_limit = []
    
    for i in range (0, dim_var_list_namelist[0]):
        var_list_all.append(var_list_namelist['Name'][i])
    
    ##Handling the evaportor limits of chillers first 
    for i in range (0, 3):
        upper_limit.append(mdv_used[1])
        upper_limit.append(mdv_used[0])
        
        lower_limit.append(0)
        lower_limit.append(274.15)
        
    ##Handling the limits of distribution pumps next 
    for i in range (0, 14):
        upper_limit.append('-')
        lower_limit.append('-')       

    ##Handling ch_c_f_c_4nc_m_perc
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0)       
        
    ##Handling ch_e_f_c_4nc_m_perc
    upper_limit.append(mdv_used[1])  
    lower_limit.append(0)  
        
    ##Handling ch_evap_ret_4nc_t_in
    upper_limit.append(mdv_used[0])  
    lower_limit.append(0)  
        
    ##Determining the condenser limits of chillers 
    upper_limit.append(407) 
    upper_limit.append(req_wet_bulb_temp + 5 + 7)
    lower_limit.append(0) 
    lower_limit.append(req_wet_bulb_temp + 5)     

    upper_limit.append(1476) 
    upper_limit.append(req_wet_bulb_temp + 5 + 7)
    lower_limit.append(0) 
    lower_limit.append(req_wet_bulb_temp + 5)     

    upper_limit.append(1476) 
    upper_limit.append(req_wet_bulb_temp + 5 + 7)
    lower_limit.append(0) 
    lower_limit.append(req_wet_bulb_temp + 5)   
    
    ##Handling cp_nwk_4nc
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0) 
    
    upper_limit.append(273.15 + 30)    
    lower_limit.append(273.15)

    ##Handling gv2_ss_4nc
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0) 
    
    upper_limit.append(273.15 + 5)    
    lower_limit.append(273.15 + 1)

    ##Handling hsb_ss_4nc
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0) 
    
    upper_limit.append(273.15 + 5)    
    lower_limit.append(273.15 + 1)   

    ##Handling para_nwk_con_4nc_delp
    upper_limit.append('-')
    lower_limit.append('-')    
        
    ##Handling pfa_ss_4nc
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0) 
    
    upper_limit.append(273.15 + 5)    
    lower_limit.append(273.15 + 1) 

    ##Handling ser_ss_4nc
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0) 
    
    upper_limit.append(273.15 + 5)    
    lower_limit.append(273.15 + 1)   

    ##Handling sp1_temp_4nc
    upper_limit.append(273.15 + 30)    
    lower_limit.append(273.15)
        
    ##Handling sp2_temp_4nc 
    upper_limit.append(273.15 + 30)    
    lower_limit.append(273.15)

    ##Handling ch1_cnwk_4nc
    upper_limit.append(total_cond_flow)    
    lower_limit.append(0)
        
    ##Handling ch1_cp_4nc
    upper_limit.append('-')
    lower_limit.append('-')     
    upper_limit.append('-')
    lower_limit.append('-')  

    ##Handling ch1_enwk_4nc 
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0)          
        
    ##Handling ch1_ep_4nc
    upper_limit.append('-')
    lower_limit.append('-')     
    upper_limit.append('-')
    lower_limit.append('-')      
        
    ##Handling ch2_cnwk_4nc
    upper_limit.append(total_cond_flow)    
    lower_limit.append(0)
        
    ##Handling ch2_cp_4nc
    upper_limit.append('-')
    lower_limit.append('-')     
    upper_limit.append('-')
    lower_limit.append('-')  

    ##Handling ch2_enwk_4nc 
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0) 
        
    ##Handling ch2_ep_4nc
    upper_limit.append('-')
    lower_limit.append('-')     
    upper_limit.append('-')
    lower_limit.append('-') 
        
    ##Handling ch3_cnwk_4nc
    upper_limit.append(total_cond_flow)    
    lower_limit.append(0)
        
    ##Handling ch3_cp_4nc
    upper_limit.append('-')
    lower_limit.append('-')     
    upper_limit.append('-')
    lower_limit.append('-')  
        
    ##Handling ch3_enwk_4nc 
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0)
        
    ##Handling ch3_ep_4nc
    upper_limit.append('-')
    lower_limit.append('-')     
    upper_limit.append('-')
    lower_limit.append('-') 
        
    ##Handling gv2_nwk_4nc 
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0)
    
    ##Handling hsb_nwk_4nc 
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0)
    
    ##Handling ice_nwk_4nc 
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0)
    
    ##Handling pfa_nwk_4nc 
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0)
        
    ##Handling ser_nwk_4nc
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0)
        
    ##Handling tro_nwk_4nc
    upper_limit.append(mdv_used[1])    
    lower_limit.append(0)
    
    ##Handling obj_func 
    upper_limit.append('-')
    lower_limit.append('-') 
    
    num_iterations = len(var_list_all)
    
    return_data_frame = pd.DataFrame(columns = ['Var_name', 'lower_limit', 'upper_limit'])
    for i in range (0, num_iterations):
        temp_data = [var_list_all[i], lower_limit[i], upper_limit[i]]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Var_name', 'lower_limit', 'upper_limit'])
        return_data_frame = return_data_frame.append(temp_df, ignore_index = True)
    
    save_file_loc = 'C:\\Optimization_zlc\\control_center\\paper_qe_testcase\\optimization_results\\opti_' + dt + '\\limits' + str(time_step) + '.csv'
    return_data_frame.to_csv(save_file_loc)
    
    return 

##To determine the total condenser flowrate 

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
############################################################################################################################################################

if __name__ == '__main__':
    
    ##The upper and lower limits differ for each time step 
    dt = 'high'
    
    for i in range (0, 24):
        append_lower_upper_limits (dt, i)