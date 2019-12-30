##This function creates the a simple forward feed policy gradient neural network, based on continuous input states and actions 

class ff_policy_gradient_contextual_bandits:
    
    ##Initialization of all the variables 
    def __init__(self, hyperparameters):
        
        import os
        os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
        import tensorflow as tf
        import numpy as np
        
        ##hyperparameters --- a dictionary of hyperparameters which is used to define the class
        
        ##Number of states in the environment
        self.n_x = hyperparameters['Number_of_states']
        ##Number of actions in the environment 
        self.n_y = hyperparameters['Number_of_actions']
        ##Learning rate of the network 
        self.lr = hyperparameters['Learning_rate']
        ##Initialize the variables for storing the states, actions and rewards
        self.state = 0
        self.action = 0
        self.reward = 0
        ##Define a function called build_network for building the neural network
        from ff_policy_gradient_contextual_bandits_build_network import ff_policy_gradient_contextual_bandits_build_network
        self.ff_policy_gradient_contextual_bandits_build_network = ff_policy_gradient_contextual_bandits_build_network(self, hyperparameters)
        ##A list for storing the loss function 
        self.loss_history = []
        ##Initialize tensorflow session 
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())                     
        
        return

    