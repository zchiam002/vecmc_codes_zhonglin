##This function contains the evaluate objective function for the reinforcement learner

def rl_evaluate_objective (self, actual_state_values, actual_action_values):
    
    ##actual_state_values --- un-normalized form of the input state values
    ##actual_action_values --- un-normalized form of the output action values
    
    ##Evaluating the reward 
    reward = contextual_bandit(actual_state_values, actual_action_values)
    
    ##Appending the object 
    self.curr_reward = [reward]
    
    print('State', actual_state_values)
    print('Action', actual_action_values)
    print('Reward', reward)
    
    return reward

################################################################################################################################################################################
################################################################################################################################################################################
################################################################################################################################################################################
    
##An auxillary test function for optimization
def test_function_Rastrigin (actual_state_values, actual_action_values):
    
    import math
    
    ##actual_state_values --- an array of actual state values
    ##actual_action_values --- an array of actual action values 
    
    ##The main feature of this test function is that when a state is 
        ##0, the larger the values, the better
        ##1, the smaller the values, the better 
    ##The equations used in this test function - Rastrigin function https://en.wikipedia.org/wiki/Rastrigin_function
        ##f(x) = A*n + sum(x_i^2 - A*cos(2*pi*x_i))
        
###############################################################################################    
    ##REMINDER: The conditions in the function state_independent_setup needs to be fulfiled. 
###############################################################################################
    if actual_state_values[0] == 0:
        ##Under this state, the function is directly computed 
        
        ##First determine the number of actions 
        num_actions = len(actual_action_values)
        
        ##Computing the function
        ret_value = 10 * num_actions 
        
        for i in range (0, num_actions):
            ret_value = ret_value + (pow(actual_action_values[i], 2) - (10 * math.cos(2 * 3.142 * actual_action_values[i])))
    
    elif actual_state_values[0] == 1:
        ##Under this state, the function is computed using the only the positive values, reversed from max to min
        
        ##Fist determine the number of actions 
        num_actions = len(actual_action_values)
        
        ##Making sure that it is all positive 
        neg = 0
        for i in range (0, num_actions):
            if actual_action_values[i] < 0:
                neg = 1
                ret_value = 30
                break
        
        ##If it is all positive 
        if neg == 0:
            
            ##Reverse the values
            rev_actions = []
            for i in range (0, num_actions):
                difference = 5.12 - actual_action_values[i]
                rev_actions.append(5.12 - difference)
                
            ##Computing the function 
            ret_value = 10 * num_actions 
            
            for i in range (0, num_actions):
                ret_value = ret_value + (pow(rev_actions[i], 2) - (10 * math.cos(2 * 3.142 * rev_actions[i])))
    
    #print('State', actual_state_values)    
    #print('Action', actual_action_values)
    #print('Obj_funct', ret_value)
        
    return ret_value

##The classic stateless multi-arm bandit problem 
def contextual_bandit (actual_state_values, actual_action_values):
    
    import numpy as np 
    
    bandits = np.array([[0.2,0,-0.0,-5],[0.1,-5,1,0.25],[-5,5,5,5]])
    
    selected_bandit = bandits[int(actual_state_values[0]), int(actual_action_values[0])]
    
    random_generator = np.random.randn(1)

    if random_generator > selected_bandit:
        #return a positive reward.
        return 0
    else:
        #return a negative reward.
        return 1    
    

