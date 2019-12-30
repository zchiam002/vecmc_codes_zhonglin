##This function processes the variable values into readable form

def process_readable_form ():
    
    import pandas as pd 
    
    general_folder_loc = 'C:\\Optimization_zlc\\control_center\\single_chiller_single_demand_run\\ga_results_current_store\\'
    dedicated_folder_name = 'test_run' + '\\'
    result_file_name = 'best_performing_all.csv'
    
    result_file = pd.read_csv(general_folder_loc + dedicated_folder_name + result_file_name)
    dim_result_file = result_file.shape
    
    ##Determining the number of time-steps 
    time_steps = 2
    ##Determning the number of pwl pieces 
    pwl_pieces = 4
    ##Total number of variables in 1 time-step 
    slave_var_number = 26
    num_mdv = 4
    total_num_var = slave_var_number + num_mdv
    
    mdv_names = ['chiller_evap_return_temp', 'chiller_cond_entry_temp', 'total_evap_nwk_flowrate', 'total_cond_nwk_flowrate']
    ##Consolidate the pwl units 
    slave_names = ['sp1_temp_t_inout', 'sp2_temp_t_inout', 'ch1_evap_m_perc', 'ch1_evap_t_out', 'gv2_ss_m_perc', 'gv2_ss_t_in', 'cp_nwk_m_perc', 'cp_nwk_tinout']
    
    ##Initiating a dataframe to hold the return values 
    return_values = pd.DataFrame(columns = 'time_step' + mdv_names + slave_names + 'obj_value')
    
    for i in range (0, dim_result_file[0]):
        for j in range (0, time_steps):
            ##Determining lower bounds 
            lb = {}
            lb['sp1_temp_t_inout'] = 273.15
            lb['sp2_temp_t_inout'] = 273.15
            lb['ch1_evap_m_perc'] = 0
            lb['ch1_evap_t_out'] = 274.15
            lb['gv2_ss_m_perc'] = 0
            lb['gv2_ss_t_in'] = 274.15
            lb['cp_nwk_m_perc'] = 0
            lb['cp_nwk_tinout'] = 
            ##Determine upper bounds 
            ub = {}
            ub['sp1_temp_t_inout'] = 273.15 + 30
            ub['sp2_temp_t_inout'] = 273.15 + 30
            ub['ch1_evap_m_perc'] = 
            ub['ch1_evap_t_out'] = 
            ub['gv2_ss_m_perc'] = 
            ub['gv2_ss_t_in'] = 
            ub['cp_nwk_m_perc'] = 
            ub['cp_nwk_tinout'] =             
    
    
    return 




#########################################################################################################################################################################
##Running the extraction algorithm  
if __name__ == '__main__':
    process_readable_form ()
