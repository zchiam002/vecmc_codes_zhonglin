##This function runs the saved model for the actor critic advantage model 
def a2c_run_saved_model (env, action_tf_var, action_placeholder, state_placeholder, saved_model_directory, saved_data_directory):
    
    ##env                           --- the environment 
    ##action_tf_var                 --- the output of tensor of the actor_advantage_network 
    ##action_placeholder            --- a placeholder for the action 
    ##state_placeholder             --- a placeholder for the state 
    ##saved_model_directory         --- the directory at which the model to be evaluated is saved 
    ##saved_data_directory          --- the directory at which the validation statistic is saved 
  
        
    import tensorflow as tf 
    import numpy as np
    import pandas as pd 
    
    ##Initializing tensorflow session 
    with tf.Session() as sess:   
        
            ##Restoring the previous model 
            saver = tf.train.Saver()
            saver.restore(sess, saved_model_directory)
            print('#########################################################')
            print('Validating trained model... ... ...')
            print('#########################################################')   
                  
            ##Importing all states which are to be evaluated 
            all_states = env.get_validation_states()
            
            ##Determining the dimensions of the validation states 
            dim_all_states = all_states.shape
            
            ##Initializing arrays to collect output and reward values
            return_dataframe = pd.DataFrame(columns = ['gv2_demand', 'hsb_demand', 'pfa_demand', 'ser_demand', 'T_WB', 'v0', 'v1', 'obj_func'])
            
            for i in range (0, dim_all_states[0]):
                curr_state = np.array([all_states[i, :]])
                ##Taking an action according to the actor neural network 
                action = sess.run(action_tf_var, feed_dict={state_placeholder: curr_state})   
                ##Evaluating the action 
                objective_function, actual_action, actual_state = env.evaluate_reward_real (np.squeeze(curr_state, axis = 0), np.squeeze(action, axis = 0))
                
                ##Appending the return Dataframes
                temp_data = [actual_state[0], actual_state[1], actual_state[2], actual_state[3], actual_state[4], actual_action[0], actual_action[1], objective_function]
                temp_df = pd.DataFrame(data = [temp_data], columns = ['gv2_demand', 'hsb_demand', 'pfa_demand', 'ser_demand', 'T_WB', 'v0', 'v1', 'obj_func'])
                return_dataframe = return_dataframe.append(temp_df, ignore_index = True)
                
                print('Progress... ' + str(i) + ' of ' + str(dim_all_states[0]) + '...')
            ##Saving the validation statistic 
            return_dataframe.to_csv(saved_data_directory + 'vali_output.csv')
    
    return 