##This function trains the two neural networks with offline traces before the online training begins 
def a2c_offline_trace_training (env, action_tf_var, action_placeholder, training_op_actor, loss_actor, state_placeholder, last_layer, loss_critic, training_op_critic, 
                                training_episodes, target_placeholder, delta_placeholder, model_save_path, critic_input_placeholder, batch_size, offline_trace_full_dir):
    
    ##env                           --- the environment 
    ##action_tf_var                 --- the output of tensor of the actor_advantage_network 
    ##action_placeholder            --- a placeholder for the action 
    ##training_op_actor             --- training function for the actor_advantage neural network 
    ##loss_actor                    --- loss placeholder for the actor_advantage neural network 
    ##state_placeholder             --- a placeholder for the state
    ##last_layer                    --- the last layer of the critic network 
    ##loss_critic                   --- loss placeholder for the critic neural network 
    ##training_op_critic            --- training function for the critic neural network 
    ##training_episodes             --- number of training episodes
    ##target_placeholder            --- the total reward placeholder
    ##delta_placeholder             --- error placeholder for training the actor network
    ##model_save_path               --- the save path for the trained model
    ##critic_input_placeholder      --- the placeholder for the input into the critic network
    ##bath_size                     --- the number of instances to train concurrently
    ##offline_trace_full_dir        --- the directory of the offline traces to pretrain the neural networks

    import tensorflow as tf 
    import numpy as np 
    import pandas as pd 
    import random 
    
    ##Importing the necessary data 
    offline_trace = pd.read_csv(offline_trace_full_dir)
    
    ##Checking the data to see if it is compatible with the batch size 
    dim_offline_trace = offline_trace.shape 
    
    extra_data_needed = dim_offline_trace[0] % batch_size 
    
    if extra_data_needed > 0:
        ##Randomly duplicating the traces of data 
        for i in range (0, extra_data_needed):
            rand = random.randint(0, dim_offline_trace[0])
            
            temp_data = [offline_trace['T_evap_in'][rand], offline_trace['evap_flow'][rand], offline_trace['ss_gv2_demand'][rand], offline_trace['ss_hsb_demand'][rand], 
                         offline_trace['ss_pfa_demand'][rand], offline_trace['ss_ser_demand'][rand], offline_trace['T_WB'][rand], offline_trace['return_obj'][rand], 
                         offline_trace['temp_error'][rand]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['T_evap_in', 'evap_flow', 'ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'T_WB', 
                                                                  'return_obj', 'temp_error'])
            
            offline_trace = offline_trace.append(temp_df, ignore_index = True)
            
    ##Determining the number of training epochs
    dim_offline_trace = offline_trace.shape
    num_epoch = int(dim_offline_trace[0] / batch_size)
    
    ##Starting the training process
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
    
        print('###############################################################')
        print('              Starting offline training... ... ...')
        print('###############################################################')    
    
        ##Tracking number of the dataframe 
        track = 0
        
        for i in range (0, num_epoch):
            
            ##Preparing the traces in mini batches for training 
            ##First trace 
            state = np.array([[offline_trace['ss_gv2_demand'][track], offline_trace['ss_hsb_demand'][track], offline_trace['ss_pfa_demand'][track], 
                               offline_trace['ss_ser_demand'][track], offline_trace['T_WB'][track]]])
            
            action = np.array([[offline_trace['T_evap_in'][track], offline_trace['evap_flow'][track]]])
            
            critic_input = np.array([[offline_trace['ss_gv2_demand'][track], offline_trace['ss_hsb_demand'][track], offline_trace['ss_pfa_demand'][track], 
                                      offline_trace['ss_ser_demand'][track], offline_trace['T_WB'][track], offline_trace['T_evap_in'][track], 
                                      offline_trace['evap_flow'][track]]])
            
            ##Getting an output from the critic 
            predicted_values = sess.run(last_layer, feed_dict = {critic_input_placeholder: critic_input})  
            ##Calculating the critic error
            env_output_values = np.array([[offline_trace['return_obj'][track], offline_trace['temp_error'][track]]])
            critic_error = env_output_values - predicted_values
            
            ##Calculating the q_value 
            qv0 = predicted_values[0,1] + predicted_values[0,0]                     ##Temperature affects both error and objective function
            qv1 = predicted_values[0,0]                                             ##Flowrate just affects the objective function
            q_value = 100 * np.array([[qv0, qv1]]) 
            
            ##Updating the track number
            track = track + 1
            
            ##Remaining traces
            for j in range (1, batch_size):
                state1 = np.array([[offline_trace['ss_gv2_demand'][track], offline_trace['ss_hsb_demand'][track], offline_trace['ss_pfa_demand'][track], 
                                    offline_trace['ss_ser_demand'][track], offline_trace['T_WB'][track]]])
                
                action1 = np.array([[offline_trace['T_evap_in'][track], offline_trace['evap_flow'][track]]])                
                
                critic_input1 = np.array([[offline_trace['ss_gv2_demand'][track], offline_trace['ss_hsb_demand'][track], offline_trace['ss_pfa_demand'][track], 
                                           offline_trace['ss_ser_demand'][track], offline_trace['T_WB'][track], offline_trace['T_evap_in'][track], 
                                           offline_trace['evap_flow'][track]]])  
                
                ##Getting an output from the critic 
                predicted_values = sess.run(last_layer, feed_dict = {critic_input_placeholder: critic_input1})
                ##Calculating the critic error
                env_output_values1 = np.array([[offline_trace['return_obj'][track], offline_trace['temp_error'][track]]])                
                critic_error1 = env_output_values1 - predicted_values                
            
                ##Calculating the q_value 
                qv0 = predicted_values[0,1] + predicted_values[0,0]                     ##Temperature affects both error and objective function
                qv1 = predicted_values[0,0]                                             ##Flowrate just affects the objective function
                q_value1 = 100 * np.array([[qv0, qv1]]) 
                
                ##Concatenating the essential numpy arrays
                state = np.concatenate((state, state1), axis = 0)
                action = np.concatenate((action, action1), axis = 0)
                critic_input = np.concatenate((critic_input, critic_input1), axis = 0)
                critic_error = np.concatenate((critic_error, critic_error1), axis = 0)
                env_output_values = np.concatenate((env_output_values, env_output_values1), axis = 0)
                q_value = np.concatenate((q_value, q_value1), axis = 0)
                
                ##Updating the track number
                track = track + 1
                
            ##Updating the Actor by minimizing loss (Actor training)
            _, loss_actor_val  = sess.run([training_op_actor, loss_actor], feed_dict={action_placeholder: action, state_placeholder: state, 
                                          delta_placeholder: q_value})
            ##Updating the Critic by minimizing loss (Critic training)
            _, loss_critic_val  = sess.run([training_op_critic, loss_critic], feed_dict={critic_input_placeholder: critic_input, target_placeholder: env_output_values})  
            
        #Saving the pre-trained model 
        saver = tf.train.Saver()
        save_path = saver.save(sess, model_save_path)                
        print('###############################################################')
        print('               Pretrained Model Saved... ... ...')
        print('###############################################################')         
            
    return 