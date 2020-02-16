##This function employs a version of the policy gradient method with disregard for the state 

def si_calculate_rewards (curr_reward):
    
    ##curr_reward --- an array of reward from the current trial
    
    ##Since it is a minimization function, let the and state independent, there is no need to treat the input value. 
    ##i.e. if the objective function is large, the corresponding error is large also
    
    
    return curr_reward