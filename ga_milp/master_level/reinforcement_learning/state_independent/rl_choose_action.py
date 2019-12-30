##This function chooses an action for the agent to take - it can either come from the neural network or a randomly chosen action with a give probability

def rl_choose_action (self, hyperparameters):
    
    from random import uniform 
    import numpy as np 
    
    ##Determining the current set of input values (states)
    curr_state = self.curr_state
    
    ##Determining the probability of choosing from the network or doing otherwise
    explore_prob = hyperparameters['Epsilon']
    ##Randomly generating a number 
    rand_gen = uniform(0,1)
    
    ##Taking values from the neural network 
    if rand_gen > explore_prob:
        actions = self.si_s_build_agent.predict(curr_state)
    ##Generating random values 
    else:
        ##The number of expected actions
        num_expected_actions = self.n_y
        ##An array to store output values
        actions = np.zeros((1, num_expected_actions))
        
        for i in range (0, num_expected_actions):
            rand_action = uniform(0,1)
            actions[0,i] = rand_action
            
    ##Determining the current iteration in the batch 
    curr_iter_in_batch = self.iter_in_batch
    ##Appending the chosen actions
    for i in range (0, self.n_y):    
        self.action[curr_iter_in_batch, i] = actions[0,i]
    
    return actions