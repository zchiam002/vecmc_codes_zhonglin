##This function determines the input state 
##Given the number of states, it ignores the bounds, returns a value ranging from 0-1

def rl_gen_input_state (self, hyperparameters):
    
    from random import uniform 
    import numpy as np
    
    ##hyperparameters --- a dictionary of hyperparameters
    ##self -- an object containing the neural network and other important parameters
    
    ##Determining the number of state inputs, i.e. the number of input neurons 
    num_states = self.n_x
    
    ##Generating an array to hold the generated states
    states = np.zeros((1, num_states))
    
    for i in range (0, num_states):
        rand = uniform(0,1)
        states[0,i] = round(rand)
    
    ##Appending the object 
    self.curr_state = states
    
    ##Determine the current iteration in the batch 
    curr_iter_in_batch = self.iter_in_batch
    ##Appending the generated states 
    for i in range (0, num_states):
        self.state[curr_iter_in_batch, i] = states[i]
    
    return