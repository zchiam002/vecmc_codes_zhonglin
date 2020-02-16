##This is the setup page for the contextual bandit problem 

def state_independent_setup ():
    
    ##Defining the input hyperparameters 
    
    hyperparameters = {}
    
    hyperparameters['Asynchronous'] = 'no'                                          ##Parallel or serial implementation
    hyperparameters['Dynamic_graph'] = 'yes'                                        ##Function to dynamically plot the loss function 
    
    ##NOTE: When using the test function (Rastigin function), following hyperparameters must be observed:
        ##State:
        ##hyperparameters['Number_of_states'] = 1 
        ##hyperparameters['State_lower_bound'] = [0]
        ##hyperparameters['State_upper_bound'] = [1]
        ##hyperparameters['State_output_type'] = 'Continuous'        
        ##Action:
        ##hyperparameters['Number_of_actions'] = anything
        ##hyperparameters['Action_lower_bound'] = [-5.12, ..., ...,]
        ##hyperparameters['Action_upper_bound'] = [5.12, ..., ...,]
        ##hyperparameters['Action_output_type'] = 'Continuous' 
        
    hyperparameters['Training_episodes'] = 1000
    hyperparameters['Training_batch_size'] = 1
    hyperparameters['Epoch_per_batch'] = 1
    
    
    hyperparameters['Number_of_states'] = 1                                         ##The number of neurons allocated for the input layer 
    hyperparameters['State_lower_bound'] = [0]
    hyperparameters['State_upper_bound'] = [2]
    hyperparameters['State_output_type'] = 'Discrete'                               ##Only 3 types 1. Continuous, 2. Binary, 3. Discrete
    
    hyperparameters['Number_of_actions'] = 1                                        ##The number of neurons allocated for the output layer   
    hyperparameters['Action_lower_bound'] = [0]
    hyperparameters['Action_upper_bound'] = [3]
    hyperparameters['Action_output_type'] = 'Discrete'                              ##Only 3 types 1. Continuous, 2. Binary, 3. Discrete
    
    ##Agent Neural Network
    hyperparameters['Hidden_layers'] = 3
    hl_n = []
    for i in range (0, hyperparameters['Hidden_layers']):
        hl_n.append(10)

    hyperparameters['Hidden_layer_activation_function'] = 'sigmoid'
    hyperparameters['Output_layer_activation_function'] = 'sigmoid'
    
    ##Hidden layer neurons 
    
        ##Appending the dictionary 
    for i in range (0, hyperparameters['Hidden_layers']):
        hyperparameters['Hidden_layer_' + str(i) + '_neurons'] = hl_n[i]
        
    hyperparameters['Loss_function'] = 'mean_squared_error'                         ##For more loss functions: https://keras.io/losses/
    
    ##Defining the input parameters of the neural network training algorithm
    from keras.optimizers import Adam 
    #from keras.optimizers import SGD
    hyperparameters['Learning_rate'] = 0.001    
    hyperparameters['NN_optimizer'] = Adam(lr = hyperparameters['Learning_rate'])   ##Direct input of the optimizer arguments. For more information: https://keras.io/optimizers/
    

    #hyperparameters['NN_optimizer'] = SGD(lr=hyperparameters['Learning_rate'], decay=1e-6, momentum=0.9, nesterov=True)
    
    
    ##Exploration probability - take a random value other than from the neural network 
    hyperparameters['Epsilon'] = 0.01
    
    ##Path to save the model 
    hyperparameters['Filename'] = 'rastigin_test_0'
    
    ##Running the reinforcement learner 
    state_independent_run(hyperparameters)
    
    return 

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

##A function for running the reinforcement learner 
def state_independent_run (hyperparameters):

    import numpy as np
    import matplotlib.pyplot as plt
    import time
    
    ##hyperparameters --- the dictionary of hyperparameters which is used to define the reinforcement learning problem 
    
    ##Setting up the dynamic graph if required
    if hyperparameters['Dynamic_graph'] == 'yes':
        x_gen = []
        y_gen = []
        plt.show()
        axes = plt.gca()
    
    
    ##Creating the object, with an empty neural network    
    from state_independent_object import state_independent_object  
    si_rl_object = state_independent_object(hyperparameters)
    
    ##Training the network proper 
    num_episodes = hyperparameters['Training_episodes']
    batch_size = hyperparameters['Training_batch_size']
    
    ##Import state function 
    from rl_gen_input_state import rl_gen_input_state
    ##Import the choose action function 
    from rl_choose_action import rl_choose_action 
    ##Import the function to enable interaction with the environment 
    from rl_interact_environment_serial import rl_interact_environment_serial 
    ##Import the function to calculate rewards 
    from si_calculate_rewards import si_calculate_rewards
    ##Import the function to update the network 
    from si_s_update_network import si_s_update_network 
    
    ##Training the model 
    for i in range (0, num_episodes):
        
        ##Iteration based on the batch size 
        for j in range (0, batch_size):

            ##Appending the current iteration in the given batch 
            si_rl_object.iter_in_batch = j
            
            ##Generate a state 
            rl_gen_input_state(si_rl_object, hyperparameters)
    
            ##Choose an action 
            curr_action = rl_choose_action(si_rl_object, hyperparameters)
            print('Curr action', curr_action)
            ##Performing an action on the environment 
            reward = rl_interact_environment_serial(si_rl_object, hyperparameters, curr_action)
            
            ##Invoking the reward function 
            reward = si_calculate_rewards(reward)
        
        ##Updating the network 
        si_s_update_network(si_rl_object)    
        
        ##Printing the newly predicted values by performing the same action on the environment 
        for j in range (0, batch_size):
            reward = rl_interact_environment_serial (si_rl_object, hyperparameters, curr_action)
        #print(si_rl_object.reward)
        #print(si_rl_object.action)
        
        ##Plotting the graph 
        if hyperparameters['Dynamic_graph'] == 'yes':
            x_gen.append(i)
            y_gen.append(si_rl_object.ave_loss_epoch)
            ##Dynamic axes
            axes.clear()
            line, = axes.plot(x_gen, y_gen, 'b.')
            plt.title('Neural network loss history')
            plt.xlabel('Episodes')
            plt.ylabel('Agent neural network loss')            
            axes.set_xlim(0, i + 1)
            axes.set_ylim(0.9 * min(y_gen), 1.1 * max(y_gen))    
            line.set_xdata(x_gen)
            line.set_ydata(y_gen)
            plt.draw()
            plt.pause(1e-17)
            time.sleep(0.1)
    
    if hyperparameters['Dynamic_graph'] == 'yes':
        plt.show()
        
    ##Saving the agent model 
    import os 
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname +  '//saved_models//' + hyperparameters['Filename'] + '.h5')
    si_rl_object.si_s_build_agent.save(filename)
        
    ##Reset the state, reward and action holders
    si_rl_object.state = np.zeros((batch_size, si_rl_object.n_x))
    si_rl_object.action = np.zeros((batch_size, si_rl_object.n_y))
    si_rl_object.reward = np.zeros((batch_size, 1))
        
    
    
    
    
    return 

###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################




###############################################################################################################################################################################
###############################################################################################################################################################################
###############################################################################################################################################################################

##Testing the script 
if __name__ == '__main__':
     state_independent_setup ()