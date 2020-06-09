##This function runs the training loop for the actor critic advantage 
def a2c_training_loop (env, action_tf_var, action_placeholder, training_op_actor, loss_actor, state_placeholder, last_layer, loss_critic, 
                       training_op_critic, training_episodes, target_placeholder, delta_placeholder, model_save_path, exploration_epsilon, critic_input_placeholder,
                       batch_size):
        
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
    ##exploration_epsilon           --- the chance of taking a random action 
    ##critic_input_placeholder      --- the placeholder for the input into the critic network
    ##batch_size                    --- the number of instances to train concurrently
    
    import os
    import tensorflow as tf 
    import numpy as np
    import pandas as pd
#    from preprocessing_module import scale_state
    import matplotlib.pyplot as plt
    import time
    import statistics
    import shutil
    from shutil import copyfile
     
    ##For the dynamic graphs 
    fig = plt.figure(figsize = (14, 7))
    
    reward_history = []
    reward_error_history = []
    actor_loss_history = []
    critic_loss_history = []
    iteration = []
    save_count = 0
    
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        
        print('###############################################################')
        print('                 Starting training... ... ...')
        print('###############################################################')
              
        for i in range(0, training_episodes):
            
            ##Mini batch averages
            mini_batch_reward_history = []
            mini_batch_reward_error_history = []

            ##Last error 
            last_error0 = 10000000
            last_error1 = 10000000
            
            ##Get a random state from the environment 
            state = env.get_random_state()
            ##Generating a random number 
            rand_num = np.random.uniform(0,1)
            ##Take a random action 
            if rand_num < exploration_epsilon:
                action = env.take_random_action()
            ##Sample action according to current policy
            else:
                action = sess.run(action_tf_var, feed_dict={state_placeholder: state})          
            ##Get reward from from the chosen action
            reward, reward_error = env.evaluate_reward(np.squeeze(state, axis = 0), np.squeeze(action, axis=0))

            mini_batch_reward_history.append(reward)
            mini_batch_reward_error_history.append(reward_error)
        
            ##Preparing critic input, both state and actions  
            critic_input = []
            for j in range (0, env.num_states):
                critic_input.append(np.squeeze(state)[j])
            for j in range (0, env.num_actions):
                critic_input.append(np.squeeze(action)[j])
    
            critic_input = np.array([critic_input])
            
            ##Output from the second last layer of the critic network 
            predicted_values = sess.run(last_layer, feed_dict = {critic_input_placeholder: critic_input}) 
            
            ##Calculating the error between the real objectives and the predicted values 
                ##Assembling the outputs into a an array 
            env_output_values = np.array([[reward, reward_error]])
            critic_error = env_output_values - predicted_values 
            
            ##Reflecting the objective function as error to the actor network 
            qv0 = (predicted_values[0,1] + predicted_values[0,0]) - (env_output_values[0,1] + env_output_values[0,0])    ##Temperature affects both error and objective function
            qv1 = predicted_values[0,0] - env_output_values[0,0]                                                         ##Flowrate just affects the objective function
            q_value = 100 * np.array([[qv0, qv1]]) 

            print('1 of ' + str(batch_size))
            
            ##To assemble the remaining members of the mini-batch 
            for j in range (1, batch_size):
                ##Get a random state from the environment 
                state1 = env.get_random_state()
                ##Generating a random number 
                rand_num = np.random.uniform(0,1)
                ##Take a random action 
                if rand_num < exploration_epsilon:
                    action1 = env.take_random_action()
                ##Sample action according to current policy
                else:
                    action1 = sess.run(action_tf_var, feed_dict={state_placeholder: state1})          
                ##Get reward from from the chosen action
                reward, reward_error = env.evaluate_reward(np.squeeze(state1, axis = 0), np.squeeze(action1, axis=0))

                mini_batch_reward_history.append(reward)
                mini_batch_reward_error_history.append(reward_error)
            
                #Preparing critic input, both state and actions  
                critic_input1 = []
                for k in range (0, env.num_states):
                    critic_input1.append(np.squeeze(state1)[k])
                for k in range (0, env.num_actions):
                    critic_input1.append(np.squeeze(action1)[k])
        
                critic_input1 = np.array([critic_input1])
                
                ##Output from the second last layer of the critic network 
                predicted_values = sess.run(last_layer, feed_dict = {critic_input_placeholder: critic_input1}) 
                
                ##Calculating the error between the real objectives and the predicted values 
                    ##Assembling the outputs into a an array 
                env_output_values1 = np.array([[reward, reward_error]])
                critic_error1 = env_output_values1 - predicted_values 
                
                ##Reflecting the objective function as error to the actor network 
                qv0 = (predicted_values[0,1] + predicted_values[0,0]) - (env_output_values[0,1] + env_output_values[0,0])    ##Temperature affects both error and objective function
                qv1 = predicted_values[0,0] - env_output_values[0,0]                                                         ##Flowrate just affects the objective function
                q_value1 = 100 * np.array([[qv0, qv1]])               
            
                ##Concatenating the essential numpy arrays
                state = np.concatenate((state, state1), axis = 0)
                action = np.concatenate((action, action1), axis = 0)
                critic_input = np.concatenate((critic_input, critic_input1), axis = 0)
                critic_error = np.concatenate((critic_error, critic_error1), axis = 0)
                env_output_values = np.concatenate((env_output_values, env_output_values1), axis = 0)
                q_value = np.concatenate((q_value, q_value1), axis = 0)            

                print(str(j + 1) + ' of ' + str(batch_size))

            if (statistics.mean(mini_batch_reward_history) < last_error0) and (statistics.mean(mini_batch_reward_error_history) < last_error1):   
                ##Updating the Actor by minimizing loss (Actor training)
                _, loss_actor_val  = sess.run([training_op_actor, loss_actor], feed_dict={action_placeholder: action, state_placeholder: state, 
                                              delta_placeholder: q_value})
                ##Updating the Critic by minimizing loss (Critic training)
                _, loss_critic_val  = sess.run([training_op_critic, loss_critic], feed_dict={critic_input_placeholder: critic_input, target_placeholder: env_output_values})   
                
                ##Printing values
                print('Iteration', i)
                print('Reward_mean', statistics.mean(mini_batch_reward_history))
                print('Reward_error_mean', statistics.mean(mini_batch_reward_error_history))
                print('Actor_loss', loss_actor_val)
                print('Critic_loss', loss_critic_val)
                
                ##Ploting graphs 
                reward_history.append(statistics.mean(mini_batch_reward_history))
                reward_error_history.append(statistics.mean(mini_batch_reward_error_history))
                actor_loss_history.append(loss_actor_val)
                critic_loss_history.append(loss_critic_val)
                iteration.append(i)
                
                ##Rewards_history plot
                ax1 = fig.add_subplot(221)
                ax1.clear()
                line, = ax1.plot(iteration, reward_history, 'b-', linewidth=0.5)
                plt.xlabel('Iteration')
                plt.ylabel('Rewards')            
                ax1.set_xlim(0, i + 1)
                ax1.set_ylim(min(reward_history), max(reward_history))    
                line.set_xdata(iteration)
                line.set_ydata(reward_history)
                
                ##Reward_error_history plot
                ax2 = fig.add_subplot(222)
                ax2.clear()
                line, = ax2.plot(iteration, reward_error_history, 'b-', linewidth=0.5)
                plt.xlabel('Iteration')
                plt.ylabel('Reward_error')            
                ax2.set_xlim(0, i + 1)
                ax2.set_ylim(min(reward_error_history), max(reward_error_history))    
                line.set_xdata(iteration)
                line.set_ydata(reward_error_history)               
                
                ##Actor_loss_history plot
                ax3 = fig.add_subplot(223) 
                ax3.clear()
                line, = ax3.plot(iteration, actor_loss_history, 'b-', linewidth=0.5)
                plt.xlabel('Iteration')
                plt.ylabel('Actor_loss')            
                ax3.set_xlim(0, i + 1)
                ax3.set_ylim(min(actor_loss_history), max(actor_loss_history))    
                line.set_xdata(iteration)
                line.set_ydata(actor_loss_history) 
                
                ##Critic_loss_history plot
                ax4 = fig.add_subplot(224)
                ax4.clear()
                line, = ax4.plot(iteration, critic_loss_history, 'b-', linewidth=0.5)
                plt.xlabel('Iteration')
                plt.ylabel('Critic_loss')            
                ax4.set_xlim(0, i + 1)
                ax4.set_ylim(min(critic_loss_history), max(critic_loss_history))    
                line.set_xdata(iteration)
                line.set_ydata(critic_loss_history)            
                
                plt.draw()    
                plt.pause(1e-17)
                time.sleep(0.1)         
                
            else:
                print('Bad sample... ...')    
                
            ##Saving the networks after every 100 iterations 
            if i%100 == 0:
                
                saver = tf.train.Saver()
                save_path = saver.save(sess, model_save_path)     

                folder_save_dir = model_save_path[:-len('a2c_trained.ckpt')]
                new_folder_name = 'save_iteration_' + str(i) + '\\'
                sub_folder_path = folder_save_dir + new_folder_name  

                ##First check if the sub folder directory exists, if it does, delete it 
                sub_folder_path = folder_save_dir + new_folder_name 
                if os.path.exists(sub_folder_path):
                    shutil.rmtree(sub_folder_path)                    
                ##Now, create the sub folder directory for storing the lp format script for the specific thread
                if not os.path.exists(sub_folder_path):
                    os.makedirs(sub_folder_path) 

                ##The names and fully directory of the files to be copied 
                file_0 = 'a2c_trained.ckpt' + '.data-00000-of-00001'
                file_1 = 'a2c_trained.ckpt' + '.index'
                file_2 = 'a2c_trained.ckpt' + '.meta'
                file_3 = 'checkpoint'
                
                file_0_curr_dir =  folder_save_dir + file_0
                file_1_curr_dir =  folder_save_dir + file_1
                file_2_curr_dir =  folder_save_dir + file_2
                file_3_curr_dir =  folder_save_dir + file_3
                
                file_0_new_dir =   sub_folder_path + file_0  
                file_1_new_dir =   sub_folder_path + file_1  
                file_2_new_dir =   sub_folder_path + file_2  
                file_3_new_dir =   sub_folder_path + file_3

                copyfile(file_0_curr_dir, file_0_new_dir)
                copyfile(file_1_curr_dir, file_1_new_dir)
                copyfile(file_2_curr_dir, file_2_new_dir)
                copyfile(file_3_curr_dir, file_3_new_dir)

                ##Saving the loss statistics
                loss_stats = pd.DataFrame(columns = ['Actor_loss', 'Critic_loss'])

                for l in range (0, len(actor_loss_history)):
                    temp_data = [actor_loss_history[l], critic_loss_history[l]]
                    temp_temp_df = pd.DataFrame(data = [temp_data], columns = ['Actor_loss', 'Critic_loss'])
                    loss_stats = loss_stats.append(temp_temp_df, ignore_index = True)
                loss_stats.to_csv(sub_folder_path + 'loss_stats.csv')
                
                print('###############################################################')
                print('                 Model Saved... ... ...')
                print('###############################################################')    
    plt.show()   
    
 
    
                        
    return 