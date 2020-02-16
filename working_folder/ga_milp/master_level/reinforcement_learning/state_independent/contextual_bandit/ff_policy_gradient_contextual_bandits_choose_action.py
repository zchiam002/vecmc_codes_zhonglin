##A function choose_action for choosing the action given the state 
def ff_policy_gradient_contextual_bandits_choose_action(self, state, hyperparameters):
    
    import numpy as np 
    import random 
    
    ##state --- the current environmental state 
    ##hyperparameters --- the hyperparameters of the setup
    
    ##Reshape the state
    state = np.array([state])
    state = state[:, np.newaxis]
    
    ##Run forward propagation to get the outputs 
    nn_outputs = self.sess.run(self.outputs, feed_dict = {self.X: state})
    
    ##Select an action based based on probability 
    epsilon = hyperparameters['Epsilon']
    selected_prob = random.uniform(0,1)
    
    ##Exploration problem 
    if selected_prob <= epsilon:
        random_action_array = []
        for i in range (0, self.n_y):
            temp_name_lb = 'Action_' + str(i) + '_lb'
            temp_name_ub = 'Action_' + str(i) + '_ub'
            random_action = random.uniform(hyperparameters[temp_name_lb], hyperparameters[temp_name_ub])
            random_action_array.append(random_action)
        selected_action = random_action_array  
        print('Random_action_taken')
        print(selected_action)
        print('End')
    ##Exploitation problem 
    else:
        selected_action = nn_outputs
    
    return selected_action