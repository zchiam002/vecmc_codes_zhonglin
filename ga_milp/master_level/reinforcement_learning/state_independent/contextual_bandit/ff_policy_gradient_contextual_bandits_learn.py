##Function to train the neural network 
def ff_policy_gradient_contextual_bandits_learn(self):

    import numpy as np
    
    curr_reward = self.reward
    corrected_reward = ff_policy_gradient_contextual_bandits_convert_rewards_error(self.reward)    

    state = np.array([self.state])
    state = state[:, np.newaxis]
    
    action = np.transpose(self.action)
    
    
    ##Training the nework
    self.sess.run(self.train_op, feed_dict={self.X: state,
                                            self.Y: action,
                                            self.rewards_tensor: [corrected_reward]})

    ##Reset the data after each iteration
    self.state, self.action, self.reward  = 0, 0, 0

    return curr_reward

##A function to convert the reward into a error value for the neural network to minimize
def ff_policy_gradient_contextual_bandits_convert_rewards_error(reward):
    
    ##reward --- the bigger the better, however in a neural network, the natural thing to do is to minimize error 
    
    reward = reward * -1
    
    return reward