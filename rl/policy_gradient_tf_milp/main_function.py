##This is the main function to activate the policy_gradient algorithm 
def main_pg_function ():
    
    import os
    current_directory = os.path.dirname(__file__)[:-70] + '//'
    import sys 
    import tensorflow as tf 
    sys.path.append(current_directory + 'master_level\\reinforcement_learning_algorithm\\policy_gradient_tf_milp\\')
    from policy_gradient_environment import policy_gradient_environment     
    from policy_gradient_network import policy_gradient_function
    from preprocessing_module import state_normalization  
    from policy_gradient_offline_trace_training import pg_offline_trace_training
    from policy_gradient_training_loop import pg_training_loop
    from policy_gradient_resume_training_saved_model import pg_resume_training_saved_model
    
    ##Importing the environment 
    env = policy_gradient_environment()
    
    ##Parameters 
    pg_input_dim = env.num_states
    pg_output_dim = env.num_actions
    pg_hidden_layers = [400, 250, 100]
    pg_lr = 0.001
    pg_output_bounds = {}
    pg_output_bounds['lb'] = env.action_space_norm_low
    pg_output_bounds['ub'] = env.action_space_norm_high
    
    model_output_bounds = {}
    model_output_bounds['lb'] = env.model_output_norm_lb
    model_output_bounds['ub'] = env.model_output_norm_ub    
    
    training_episodes = 1000000
    exploration_epsilon = 0.05
    batch_size = 1
    
    ##Offline trace information 
    offline_trace_folder = current_directory + 'control_center\\chiller_optimization_dist_nwk_pg\\batch_training_data\\seeding_values\\'
    offline_trace_save_file_name = 'cleansed_norm_op.csv'
    offline_trace_full_dir = offline_trace_folder + offline_trace_save_file_name
    
    
    ##The save path for the a2c model
    save_folder_directory = current_directory + 'master_level\\reinforcement_learning_algorithm\\policy_gradient_tf_milp\\saved_model\\'
    save_file_name = 'pg_trained.ckpt'
    save_dir = save_folder_directory + save_file_name
    resume_training_count = 0
    
    ##Defining the required placeholders
    state_placeholder = tf.placeholder(tf.float32, [None, pg_input_dim])
    action_placeholder = tf.placeholder(tf.float32, [None, pg_output_dim])
    delta_placeholder = tf.placeholder(tf.float32, [None, pg_output_dim]) 
    
    ##Getting the tensors from the associated networks
    action_tf_var, norm_dist = policy_gradient_function (state_placeholder, pg_hidden_layers, pg_output_dim, pg_output_bounds)
    
    ##Defining the loss function for the policy 
    loss_policy = tf.reduce_mean(-tf.log(norm_dist.prob(action_placeholder) + 1e-5) * delta_placeholder) 
    training_op_policy = tf.train.AdamOptimizer(pg_lr, name='actor_optimizer').minimize(loss_policy)     

#############################################################################################################################################################################
    ##Pretraining the neural networks with offline traces
#    pg_offline_trace_training (env, action_tf_var, action_placeholder, training_op_policy, loss_policy, state_placeholder, training_episodes, delta_placeholder, save_dir, 
#                               batch_size, offline_trace_full_dir)

#############################################################################################################################################################################    
    ##Training the networks (online, fresh)
    pg_training_loop (env, action_tf_var, action_placeholder, training_op_policy, loss_policy, state_placeholder, training_episodes, delta_placeholder, save_dir, 
                      exploration_epsilon,batch_size)

#############################################################################################################################################################################    
    ##Resmue training the network 
#    pg_resume_training_saved_model (env, action_tf_var, action_placeholder, training_op_policy, loss_policy, state_placeholder, training_episodes, delta_placeholder, save_dir, 
#                                    exploration_epsilon, save_file_name, resume_training_count, save_folder_directory, batch_size)
    
    
    
    return 

################################################################################################################################################################################
################################################################################################################################################################################
##Running the script

if __name__ == '__main__':
    main_pg_function ()