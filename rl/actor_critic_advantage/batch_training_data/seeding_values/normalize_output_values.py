##This function normalizes the output data of the pre training traces 
def normalize_output_values ():

    import os 
    current_directory = os.path.dirname(__file__)[:-84] + '//'    
    import sys 
    sys.path.append(current_directory + 'control_center//chiller_optimization_dist_nwk_a2c//')
    from a2c_env_custom import a2c_env_custom
    import pandas as pd
    
    ##Importing the environment 
    env = a2c_env_custom()
    
    ##Loading the pretraining batches
    pretrain_trace = pd.read_csv(current_directory + 'control_center//chiller_optimization_dist_nwk_a2c//batch_training_data//seeding_values//cleansed_norm.csv')
    
    dim_pretrain_trace = pretrain_trace.shape
    
    new_df = pd.DataFrame(columns = ['T_evap_in', 'evap_flow', 'ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand',	 'ss_ser_demand',	 'T_WB', 'return_obj', 'temp_error'])
    
    for i in range (0, dim_pretrain_trace[0]):
        
        ret_obj = pretrain_trace['return_obj'][i]
        tem_err = pretrain_trace['temp_error'][i]
        
        ret_obj_norm = (ret_obj - env.model_output_lb[0]) / (env.model_output_ub[0] - env.model_output_lb[0])
        ret_obj_norm = (ret_obj_norm * (env.model_output_norm_ub[0] - env.model_output_norm_lb[0])) + env.model_output_norm_lb[0]
        
        tem_err_norm = (tem_err - env.model_output_lb[1]) / (env.model_output_ub[1] - env.model_output_lb[1])
        tem_err_norm = (tem_err_norm * (env.model_output_norm_ub[1] - env.model_output_norm_lb[1])) + env.model_output_norm_lb[1]
        
        temp_data = [pretrain_trace['T_evap_in'][i], pretrain_trace['evap_flow'][i], pretrain_trace['ss_gv2_demand'][i], pretrain_trace['ss_hsb_demand'][i], 
                     pretrain_trace['ss_pfa_demand'][i], pretrain_trace['ss_ser_demand'][i], pretrain_trace['T_WB'][i], ret_obj_norm,
                     tem_err_norm]
        
        temp_df = pd.DataFrame(data = [temp_data], columns = ['T_evap_in', 'evap_flow', 'ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand',	 
                                                              'ss_ser_demand',	 'T_WB', 'return_obj', 'temp_error'])
        
        new_df = new_df.append(temp_df, ignore_index = True)
        
    
    ##Saving the new dataframe 
    new_df.to_csv(current_directory + 'control_center//chiller_optimization_dist_nwk_a2c//batch_training_data//seeding_values//cleansed_norm_op.csv')
    
    return 

##########################################################################################################################################################################################
##########################################################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    normalize_output_values ()