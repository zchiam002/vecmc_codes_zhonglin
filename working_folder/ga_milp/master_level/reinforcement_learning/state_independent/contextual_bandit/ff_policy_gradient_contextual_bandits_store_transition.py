##A function which stores the transition information pertaining to the states, actions and the corresponding reward
def ff_policy_gradient_contextual_bandits_store_transition(self, state, action, reward):
    
    ##state --- the current state of the environment 
    ##action --- the current actions taken 
    ##reward --- the corresponding reward function 
    
    self.state = state
    self.reward = reward
    self.action = action    
    
    return