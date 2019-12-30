##This function evaluates the objective of the related problem 
##This is also ths script which the problem definition should be placed.

def ff_policy_gradient_contextual_bandits_evaluate_objective (action, state, iteration_number):
     
    ##action --- an array of actions 
    ##state --- the input state of the environment 
    
    objective_value = contextual_bandit(action, state)
    
    return objective_value

def contextual_bandit (action, state):
    
    import numpy as np 
    
    ##action --- an array of 4 actions to be taken 
    ##state --- the given state of the problem 
    
    ##Predefined bandits
    bandits = np.zeros((3,4))
    r1 = [0.2, 0, -0.0, -5]
    r2 = [0.1, -5, 1, 0.25]
    r3 = [-5, 5, 5, 5]

    for i in range (0, 3):
        for j in range (0, 4):
            if i == 0:
                bandits[i,j] = r1[j]
            if i == 1:
                bandits[i,j] = r2[j]
            if i == 2:
                bandits[i,j] = r3[j]                
    
    ##Checking which state the and executing the appropriate action
    for i in range (0, len(bandits)):
        if state == i:
            
            ##Calculating the reward
            reward = 0
            for j in range (0, len(action)):
                print(bandits[i,j])
                print(action[0,j])

                reward = reward + (bandits[i,j] * action[0,j])

            
            break
    
    return reward

