##This function takes in the parameters and master decison variable and writes them in a slave readable form 

##This function writes the parameters for the slave solver 
def convert_mdv_to_slave_param_v2 (thread_number, var, demand, weather_and_ct_coeff, piecewise_steps):
    
    ##thread_number --- the thread number for coding output files
    ##var --- variable values from the master decision 
    ##demand --- the demand of the substations
    ##weather_and_ct_coeff --- the weather and the cooling tower coefficients 
    ##piecewise_steps --- the number of piecewise_steps 
    
    import os
    current_directory = os.path.dirname(__file__)[:-86] + '//'    
    import sys 
    sys.path.append(current_directory + 'milp_model//master_level_models//chiller_optimization_dist_nwk_a2c_master_level_models//prep_functions//')
    import os.path
    from prepare_slave_param_csv_vtest2 import prepare_slave_param_csv_vtest2    #Needs modification  
    
    ##The final csv location 
    csv_save_loc = current_directory + 'milp_model//slave_convex_handlers\\master_values\\'
    csv_save_name = 'master_slave_var_list_' + str(thread_number) + '.csv'
    csv_final_save = csv_save_loc + csv_save_name

    ##Checking if there are similar files with the same name, and removing if there is     
    exist_result = os.path.exists(csv_final_save)
    if exist_result == True:
        os.remove(csv_final_save)   

    ##Putting the values into a dataframe
    mdv_slave_param = prepare_slave_param_csv_vtest2(var, demand, weather_and_ct_coeff, piecewise_steps)

    mdv_slave_param.to_csv(csv_final_save)
    
    return 
