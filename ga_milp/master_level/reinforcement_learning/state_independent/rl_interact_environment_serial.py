##This function interacts with the environment in series

def rl_interact_environment_serial (self, hyperparameters, curr_action):
    
    ##hyperparameters --- a dictionary of hyperparameters
    ##self -- an object containing the neural network and other important parameters
    ##curr_action --- the current set of actions
    
    ##Randomly generated number to indicate the thread and subsequent set of folders, could be critical to the extraction of results 
    iteration_number = 100131
    
    ##Determining the actual state values 
    actual_state_values = define_variable_value_by_type(self, hyperparameters, self.curr_state, 'state')
    
    ##Determining the actual action values 
    actual_action_values = define_variable_value_by_type(self, hyperparameters, curr_action, 'action')
    
    ##Importing the relevant function to compute the reward
    from rl_evaluate_objective import rl_evaluate_objective 
    
    ##The value of the state is also needed for the the computation of the reward
    reward = rl_evaluate_objective(self, actual_state_values, actual_action_values)
    
    ##Determining the current iteration in the given batch 
    curr_iter_in_batch = self.iter_in_batch
    ##Appending the rewards
    self.reward[curr_iter_in_batch, 0] = reward
    
    return reward

##############################################################################################################################################################################
##############################################################################################################################################################################
##############################################################################################################################################################################

##Auxillary functions
    
##This function determines the type of variable and returns the actual value     
def define_variable_value_by_type (self, hyperparameters, curr_state_action, state_or_action):
    
    ##hyperparameters --- a dictionary of hyperparameters
    ##curr_state_action --- the current set of actions
    ##state_or_action --- a string to indicate if it is a state or action 
    
    ##Checking if it is a state or an action
    if state_or_action == 'action':
        ##Convert the set of numbers from their normalized form to the original form 
        act_lb = hyperparameters['Action_lower_bound']
        act_ub = hyperparameters['Action_upper_bound']
        
        ##The number of actions 
        num_actions = self.n_y
    
        ##An array to store the actual action values
        return_values = []
        
        ##Determine the variable type 
        var_type =  hyperparameters['Action_output_type']
        
        if var_type == 'Continuous':
            for i in range (0, num_actions):
                actual_action_value = (curr_state_action[0,i] * (act_ub[i] - act_lb[i])) + act_lb[i]
                return_values.append(actual_action_value)
        elif var_type == 'Discrete':
            for i in range (0, num_actions):
                actual_action_value = (curr_state_action[0,i] * (act_ub[i] - act_lb[i])) + act_lb[i]
                return_values.append(round(actual_action_value))
        elif var_type == 'Binary':
            for i in range (0, num_actions):
                actual_action_value = curr_state_action[0,i]
                return_values.append(round(actual_action_value))
        
    elif state_or_action == 'state':
        ##Convert the set of numbers from their normalized form to the original form 
        sta_lb = hyperparameters['State_lower_bound']
        sta_ub = hyperparameters['State_upper_bound']
        
        ##The number of states 
        num_states = self.n_x
        
        ##An array to store the actual state values 
        return_values = []
        
        ##Determine the variable type 
        var_type =  hyperparameters['State_output_type']        

        if var_type == 'Continuous':
            for i in range (0, num_states):
                actual_action_value = (curr_state_action[0,i] * (sta_ub[i] - sta_lb[i])) + sta_lb[i]
                return_values.append(actual_action_value)
        elif var_type == 'Discrete':
            for i in range (0, num_states):
                actual_action_value = (curr_state_action[0,i] * (sta_ub[i] - sta_lb[i])) + sta_lb[i]
                return_values.append(round(actual_action_value))
        elif var_type == 'Binary':
            for i in range (0, num_states):
                actual_action_value = curr_state_action[0,i]
                return_values.append(round(actual_action_value))        
    
    return return_values
    