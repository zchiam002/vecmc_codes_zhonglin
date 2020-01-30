##This script resumes the training of the trained model 
def pg_resume_training_saved_model (env, action_tf_var, action_placeholder, training_op_policy, loss_policy, state_placeholder, training_episodes, delta_placeholder, 
                                    save_directory, exploration_epsilon, save_file_name, resume_training_count, save_folder_directory, batch_size):
    
    ##env                           --- the environment 
    ##action_tf_var                 --- the output of tensor of the policy gradient
    ##action_placeholder            --- a placeholder for the action 
    ##training_op_policy             --- training function for the policy gradient neural network 
    ##loss_policy                    --- loss placeholder for the policy gradient neural network 
    ##state_placeholder             --- a placeholder for the state 
    ##training_episodes             --- number of training episodes
    ##delta_placeholder             --- error placeholder for training the policy gradient network
    ##save_directory                --- the save path for the trained model
    ##exploration_epsilon           --- the chance of taking a random action     
    ##save_file_name                --- the file name for the trained model 
    ##resume_training_count         --- the resume_training iteration
    ##save_folder_directory         --- the directory for the saved models 
    ##batch_size                    --- the number of instances to train concurrently   
    
    import tensorflow as tf 
    import numpy as np
    import os
    current_directory = os.path.dirname(__file__)[:-70] + '//'
    import sys
    sys.path.append(current_directory + 'master_level\\reinforcement_learning_algorithm\\policy_gradient_tf_milp\\')
    from preprocessing_module import scale_state
    from policy_gradient_backup_before_resume import pg_backup_before_resume
    import pandas as pd
    import matplotlib.pyplot as plt 
    import time
    import statistics    

    ##Before resuming the training, it is of utmost importance to backup the starting files before writing over it 
    proceed = pg_backup_before_resume (save_file_name, resume_training_count, save_folder_directory)

    ##For the dynamic graphs 
    fig = plt.figure(figsize = (14, 7))
    
    reward_history = []
    reward_error_history = []
    policy_loss_history = []
    iteration = []

    if proceed == 1:
        with tf.Session() as sess:
            
            ##Restoring the previous model 
            saver = tf.train.Saver()
            saver.restore(sess, save_directory)
            print('#########################################################')
            print('Resuming training from previously stored model... ... ...')
            print('#########################################################')
    
            for i in range(0, training_episodes):
                
                ##Mini batch averages
                mini_batch_reward_history = []
                mini_batch_reward_error_history = []
                
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
 
                ##Assembling the outputs into a an array 
                env_output_values = np.array([[reward, reward_error]])
                
                ##Reflecting the objective function as error to the policy network 
                qv0 = env_output_values[0,1] + env_output_values[0,0]                       ##Temperature affects both error and objective function
                qv1 = env_output_values[0,0]                                                ##Flowrate just affects the objective function
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
                    
                    ##Assembling the outputs into a an array 
                    env_output_values1 = np.array([[reward, reward_error]])
                    
                    ##Reflecting the objective function as error to the policy network 
                    qv0 = env_output_values1[0,1] + env_output_values1[0,0]                         ##Temperature affects both error and objective function
                    qv1 = env_output_values1[0,0]                                                   ##Flowrate just affects the objective function
                    q_value1 = 100 * np.array([[qv0, qv1]])                
                
                    ##Concatenating the essential numpy arrays
                    state = np.concatenate((state, state1), axis = 0)
                    action = np.concatenate((action, action1), axis = 0)
                    env_output_values = np.concatenate((env_output_values, env_output_values1), axis = 0)
                    q_value = np.concatenate((q_value, q_value1), axis = 0)            

                    print(str(j + 1) + ' of ' + str(batch_size))
                
                ##Updating the Policy by minimizing loss (Policy training)
                _, loss_policy_val  = sess.run([training_op_policy, loss_policy], feed_dict={action_placeholder: action, state_placeholder: state, 
                                              delta_placeholder: q_value})  
             
                
                ##Printing values
                print('Iteration', i)
                print('Reward_mean', statistics.mean(mini_batch_reward_history))
                print('Reward_error_mean', statistics.mean(mini_batch_reward_error_history))
                print('Policy_loss', loss_policy_val)
                
                ##Ploting graphs 
                reward_history.append(statistics.mean(mini_batch_reward_history))
                reward_error_history.append(statistics.mean(mini_batch_reward_error_history))
                policy_loss_history.append(loss_policy_val)
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
                
                ##policy_loss_history plot
                ax3 = fig.add_subplot(223) 
                ax3.clear()
                line, = ax3.plot(iteration, policy_loss_history, 'b-', linewidth=0.5)
                plt.xlabel('Iteration')
                plt.ylabel('Policy_loss')            
                ax3.set_xlim(0, i + 1)
                ax3.set_ylim(min(policy_loss_history), max(policy_loss_history))    
                line.set_xdata(iteration)
                line.set_ydata(policy_loss_history) 
                
                plt.draw()    
                plt.pause(1e-17)
                time.sleep(0.1)             
                
                ##Saving the networks after every 20 iterations 
                if i%50 == 0:
                    saver = tf.train.Saver()
                    save_path = saver.save(sess, save_directory)     
                    
                    ##Saving the loss statistics
                    loss_stats = pd.DataFrame(columns = ['Policy_loss'])
                    for l in range (0, len(policy_loss_history)):
                        temp_data = [policy_loss_history[l]]
                        temp_temp_df = pd.DataFrame(data = [temp_data], columns = ['Policy_loss'])
                        loss_stats = loss_stats.append(temp_temp_df, ignore_index = True)
                    loss_stats.to_csv(current_directory + 'master_level//reinforcement_learning_algorithm//policy_gradient_tf_milp//saved_model//loss_statistics//loss_stats.csv')
                    
                    print('###############################################################')
                    print('                 Model Saved... ... ...')
                    print('###############################################################')    
    plt.show()   
    
    return 