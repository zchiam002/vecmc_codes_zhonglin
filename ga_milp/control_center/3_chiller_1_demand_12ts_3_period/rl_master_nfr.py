##Reinforcement Learner Master-level 

def rl_master_nfr ():
    
    ##Setting the hyper parameters for Reinforcement Learning
    
    policy_nwk_layers = 
    policy_nwk_neurons = 
    
    policy_batch_size = 
    
    training_iterations = 
    discount_factor = 
    learning_rate = 
    
    
    
    
    ##Defining 
    
    return 

###################################################################################################################################################################################
##Additional functions

##This function defines the action which the agent can take to interact with the environment
def action_def (time_steps):
    
    import pandas as pd 
    import numpy as np
    
    #time_steps --- the number of time steps for the associated problem 
    
    ##Initializing the variable_list dataframe 
    variable_list = pd.DataFrame(columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps'])
    
    for i in range (0, time_steps):
        
        variable = {}
        variable['Name'] = 'chiller_evap_return_temp_time_step_' + str(i)
        variable['Type'] = 'continuous'
        variable['Lower_bound'] = 275.16
        variable['Upper_bound'] = 288.15
        variable['Bin_dec_prec'] = 2
        variable['Steps'] = '-'
        
        temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Bin_dec_prec'], variable['Steps']]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps'])
        variable_list = variable_list.append(temp_df, ignore_index = True)  
        
        variable = {}
        variable['Name'] = 'total_evap_nwk_flowrate_time_step_' + str(i) 
        variable['Type'] = 'continuous'
        variable['Lower_bound'] = 0.01
        variable['Upper_bound'] = 1860.00
        variable['Bin_dec_prec'] = 2
        variable['Steps'] = '-'
        
        temp_data = [variable['Name'], variable['Type'], variable['Lower_bound'], variable['Upper_bound'], variable['Bin_dec_prec'], variable['Steps']]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps'])
        variable_list = variable_list.append(temp_df, ignore_index = True)
        
        ##Initial variables
        
        ##The number of seeds
        num_seeds = 1
        num_variables = 2 * time_steps
        initial_variable_values = np.zeros((num_seeds, num_variables))
        
        initial_variable_values[0,:] = [2.86E+02, 1.29E+02]



    return variable_list, initial_variable_values
