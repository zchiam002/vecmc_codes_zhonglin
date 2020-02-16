##This function creates the a simple forward feed policy gradient neural network, based on continuous input states and actions 

class state_independent_object:
    
    ##Initialization of all the variables 
    def __init__(self, hyperparameters):
        
        import os
        os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
        import numpy as np
        
        ##hyperparameters --- a dictionary of hyperparameters which is used to define the class
        
        ##Determining the training batch size 
        batch_size = hyperparameters['Training_batch_size']
        self.batch_size = batch_size
        ##Determining the number of epoch per batch 
        epoch_per_batch = hyperparameters['Epoch_per_batch']
        self.epoch_per_batch = epoch_per_batch
        
        ##Number of states in the environment
        self.n_x = hyperparameters['Number_of_states']
        ##Number of actions in the environment 
        self.n_y = hyperparameters['Number_of_actions']
        ##Initialize the variables for storing the states, actions and rewards
        self.state = np.zeros((batch_size, self.n_x))
        self.action = np.zeros((batch_size, self.n_y))
        self.reward = np.zeros((batch_size, 1))
        
        ##The current iteration in a given batch 
        self.iter_in_batch = 0
        
        ##Define a function called build_network for building the neural network
        from si_s_build_agent import si_s_build_agent
        self.si_s_build_agent = si_s_build_agent(hyperparameters)
        
        return
