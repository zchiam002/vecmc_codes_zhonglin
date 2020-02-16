##This is the main script for running the reinforcement learner for the partial problem: contextual bandits 
##For now, this setup can only deal with continuous variables 
##Always remember that the default objective of this program is to minimiz

def contextual_bandits_rl_setup ():
    
    ##Defining the input hyperparameters 
    
    hyperparameters = {}
    
    hyperparameters['Training_episodes'] = 1000
    hyperparameters['Number_of_states'] = 1                                     ##This means the number of neurons allocated for the input layer 
    hyperparameters['Number_of_actions'] = 4
    act_lb = [0, 0, 0, 0]
    act_ub = [100, 100, 100, 100]
    
    ##Agent NN
    hyperparameters['Hidden_layers'] = 4
    hl_n = [10, 10, 10, 10]


    hyperparameters['Hidden_layer_activation_function'] = 'relu'
    hyperparameters['Output_layer_activation_function'] = 'softmax'
    
    ##Hidden layer neurons 
    
        ##Appending the dictionary 
    for i in range (0, hyperparameters['Hidden_layers']):
        hyperparameters['Hidden_layer_' + str(i) + '_neurons'] = hl_n[i]
        

    hyperparameters['Loss_function'] = 'softmax_cross_entropy_with_logits'
    hyperparameters['Reward_guided_loss'] = 'reduce_mean'
    
    ##Defining the input parameters of the neural network training algorithm
    hyperparameters['Learning_rate'] = 0.01    
    hyperparameters['NN_optimizer'] = 'adam_optimizer'
    
    hyperparameters['Epsilon'] = 0.05
    
    ##Appending the action bounds
    for i in range (0, hyperparameters['Number_of_actions']):
        hyperparameters['Action_' + str(i) + '_lb'] = act_lb[i]
        hyperparameters['Action_' + str(i) + '_ub'] = act_ub[i] 
    
    contextual_bandits_rl_run(hyperparameters)
    
    return

###################################################################################################################################################################################
##Running the reinforcement learner 
def contextual_bandits_rl_run(hyperparameters):
    
    from ff_policy_gradient_contextual_bandits import ff_policy_gradient_contextual_bandits
    from ff_policy_gradient_contextual_bandits_choose_action import ff_policy_gradient_contextual_bandits_choose_action
    from ff_policy_gradient_contextual_bandits_evaluate_objective import ff_policy_gradient_contextual_bandits_evaluate_objective
    from ff_policy_gradient_contextual_bandits_store_transition import ff_policy_gradient_contextual_bandits_store_transition
    from ff_policy_gradient_contextual_bandits_learn import ff_policy_gradient_contextual_bandits_learn
    
    ##hyperparameters --- the dictionary of hyperparameters which is used to define the reinforcement learning problem 
    
    run_cbrl = ff_policy_gradient_contextual_bandits(hyperparameters)
    
    for i in range (0, hyperparameters['Training_episodes']):
        
        ##Generate a state 
        state = contextual_bandits_rl_state_input ()
        
        ##Choose an action based on the given state 
        
        action = ff_policy_gradient_contextual_bandits_choose_action(run_cbrl, state, hyperparameters)
        
        ##Perform an action in the environment and receive a reward
        reward = ff_policy_gradient_contextual_bandits_evaluate_objective(action, state, i)
        
        ##Storing the information 
        ff_policy_gradient_contextual_bandits_store_transition(run_cbrl, state, action, reward)
        
        ##This is an online learning algorithm, hence the network is updated and after every iteration
        curr_reward = ff_policy_gradient_contextual_bandits_learn(run_cbrl)
        
        ##Printing the results 
        print(curr_reward)
        
    
    return 

###################################################################################################################################################################################
##Additional functions
    
##This function delivers a random state to the reinforcement learner 
def contextual_bandits_rl_state_input ():
    
    from random import randint
    
    selected_state = randint(0,2)
    
    return selected_state

####################################################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    contextual_bandits_rl_setup()