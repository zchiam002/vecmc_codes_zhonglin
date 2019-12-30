##This function takes in the neural network object and updates it serially 

def si_s_update_network (self):
    
    import numpy as np
    
    ##self -- an object containing the neural network and other important parameter
    
    ##Determining the size of the training batch 
    batch_size = self.batch_size
    
    ##Generating a set of pseudo optimal values based on the reward function
        #
    ave_reward_holder = []
    
    for i in range (0, batch_size):
        ##Divide up the error amongst the output values equally
        ave_reward_holder.append(pow((self.reward[i,0] / self.n_y),0.5))
    
    pseudo_optimal_action_values = np.zeros((batch_size, self.n_y))
        
    for i in range (0, batch_size):
        for j in range (0, self.n_x):
            pseudo_optimal_action_values[i,j] = self.action[i,j] + ave_reward_holder[i]
    
    ##Appending the pseudo optimal values to the object
    self.pseudo_optimal_action = pseudo_optimal_action_values
    
    ##Training the network 
    hist = self.si_s_build_agent.fit(self.state, self.pseudo_optimal_action, epochs = self.epoch_per_batch, batch_size = self.batch_size) #verbose = 0)
    
    ##Calculating the average loss over all epochs in a batch 
    total_losses_over_epoch = sum(hist.history['loss'])
    ave_loss = total_losses_over_epoch / batch_size
        
    ##Appending the losses in the object 
    self.ave_loss_epoch = ave_loss
        
    return 