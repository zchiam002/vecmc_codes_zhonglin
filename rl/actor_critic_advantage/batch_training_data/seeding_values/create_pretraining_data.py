##This function creates the seeding values for the neural network 
def create_pretraining_data ():
    
    import os 
    current_directory = os.path.dirname(__file__)[:-84] + '//'
    import sys 
    import pandas as pd
    
    ##Import seeding values for all 3 load scenarios  
    seeding_values = pd.read_csv(current_directory + 'control_center//chiller_optimization_dist_nwk_a2c//batch_training_data//seeding_values//seeding_values.csv')
    
    ##Importing the environment
    sys.path.append(current_directory + 'control_center//chiller_optimization_dist_nwk_a2c//')
    from a2c_env_custom import a2c_env_custom 
    from a2c_env_custom import one_run_slave
    
    env = a2c_env_custom()
    
    dim_seeding_values = seeding_values.shape 
    
    ##Setting up a new dataframe to store the return values
    new_df = pd.DataFrame(columns = ['T_evap_in', 'evap_flow', 'ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'T_WB', 'return_obj', 'temp_error'])
    new_df_norm = pd.DataFrame(columns = ['T_evap_in', 'evap_flow', 'ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'T_WB', 'return_obj', 'temp_error'])
    
    for i in range (0, dim_seeding_values[0]):
        ##Preparing the state
        state = [seeding_values['ss_gv2_demand'][i], seeding_values['ss_hsb_demand'][i], seeding_values['ss_pfa_demand'][i], seeding_values['ss_ser_demand'][i],
                 seeding_values['T_WB'][i]]
        ##Preparing the action 
        action = [seeding_values['T_evap_in'][i], seeding_values['evap_flow'][i]]
        
        return_obj, temp_error = one_run_slave(action, state, iteration = 10001001)
        
        new_data = [seeding_values['T_evap_in'][i], seeding_values['evap_flow'][i], seeding_values['ss_gv2_demand'][i], seeding_values['ss_hsb_demand'][i], 
                    seeding_values['ss_pfa_demand'][i], seeding_values['ss_ser_demand'][i], seeding_values['T_WB'][i], return_obj, temp_error]
        
        temp_df = pd.DataFrame(data = [new_data], columns = ['T_evap_in', 'evap_flow', 'ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'T_WB', 
                               'return_obj', 'temp_error'])
        
        new_df = new_df.append(temp_df, ignore_index = True)

        ##Normalizing the state 
        state_norm = []
        for j in range (0, len(state)):
            t0 = (state[j] - env.state_lb[j]) / (env.state_ub[j] - env.state_lb[j])
            t0 = (t0 * (env.state_space_norm_high - env.state_space_norm_low)) + env.state_space_norm_low
            state_norm.append(t0)
            
        ##Normalizing the action 
        action_norm = []
        for j in range (0, len(action)):
            t1 = (action[j] - env.action_space_lb[j]) / (env.action_space_ub[j] - env.action_space_lb[j])
            t1 = (t1 * (env.action_space_norm_high - env.action_space_norm_low)) + env.action_space_norm_low
            action_norm.append(t1)
        
        ##Appending the new dataframe 
        new_data = [action_norm[0], action_norm[1], state_norm[0], state_norm[1], state_norm[2], state_norm[3], state_norm[4], return_obj, temp_error]
        temp_df = pd.DataFrame(data = [new_data], columns = ['T_evap_in', 'evap_flow', 'ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'T_WB', 
                               'return_obj', 'temp_error'])                
                
        new_df_norm = new_df_norm.append(temp_df, ignore_index = True)    

        print('Progress... ...' + str(i) + ' of ' + str(dim_seeding_values[0]) + ' completed...')
        
        
    ##Saving the prepared seeding values 
    new_df.to_csv(current_directory + 'control_center//chiller_optimization_dist_nwk_a2c//batch_training_data//seeding_values//fully_prepared.csv')
    new_df_norm.to_csv(current_directory + 'control_center//chiller_optimization_dist_nwk_a2c//batch_training_data//seeding_values//fully_prepared_norm.csv')    
        
    
    print('ALL DONE!')        
    
    return 

################################################################################################################################################################################
################################################################################################################################################################################
##Running the script
if __name__ == '__main__':
    create_pretraining_data()