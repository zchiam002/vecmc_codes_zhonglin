##This is the main function to activate the actor_critic_advantage algorithm 
def main_a2c_function ():
    
    import os
    current_directory = os.path.dirname(__file__) + '//'
    import tensorflow as tf 
    from a2c_environment import a2c_environment     
    from actor_advantage_network import actor_advantage_function
    from critic_network import critic_network_function
    from preprocessing_module import state_normalization  
    from a2c_offline_trace_training import a2c_offline_trace_training
    from a2c_training_loop import a2c_training_loop
    from a2c_resume_training_saved_model import a2c_resume_training_saved_model
    from a2c_run_saved_model import a2c_run_saved_model
    
    ##Importing the environment 
    env = a2c_environment()
    
    ##Parameters 
    actor_input_dim = env.num_states
    actor_output_dim = env.num_actions
    actor_hidden_layers = [4000, 4000, 4000, 4000, 1000]
    actor_lr = 0.0001
    actor_output_bounds = {}
    actor_output_bounds['lb'] = env.action_space_norm_low
    actor_output_bounds['ub'] = env.action_space_norm_high
    
    model_output_bounds = {}
    model_output_bounds['lb'] = env.model_output_norm_lb
    model_output_bounds['ub'] = env.model_output_norm_ub    
    
    critic_input_dim = actor_input_dim + actor_output_dim
    critic_output_dim = 2
    critic_hidden_layers = [5000, 5000, 4000, 4000, 1000]
    critic_lr = 0.00001
    
    training_episodes = 3
    exploration_epsilon = 0.05
    batch_size = 1
    
    ##Offline trace information 
    offline_trace_folder = current_directory + 'batch_training_data\\'
    offline_trace_save_file_name = 'cleansed_norm_op.csv'
    offline_trace_full_dir = offline_trace_folder + offline_trace_save_file_name
    
    
    ##The save path for the a2c model
    save_folder_directory = current_directory + 'saved_model\\'
    save_file_name = 'a2c_trained.ckpt'
    save_dir = save_folder_directory + save_file_name
    resume_training_count = 0
    
    ##Defining the required placeholders
    state_placeholder = tf.placeholder(tf.float32, [None, actor_input_dim])
    action_placeholder = tf.placeholder(tf.float32, [None, actor_output_dim])
    critic_input_placeholder = tf.placeholder(tf.float32, [None, critic_input_dim])
    delta_placeholder = tf.placeholder(tf.float32, [None, actor_output_dim])
    target_placeholder = tf.placeholder(tf.float32, [None, critic_output_dim])   
    
    ##Getting the tensors from the associated networks
    action_tf_var, norm_dist = actor_advantage_function (state_placeholder, actor_hidden_layers, actor_output_dim, actor_output_bounds)
    last_layer = critic_network_function(critic_input_placeholder, critic_hidden_layers, critic_output_dim, model_output_bounds)
    
    ##Defining the loss function for the actor 
    loss_actor = tf.reduce_mean(-tf.log(norm_dist.prob(action_placeholder) + 1e-5) * delta_placeholder) 
    training_op_actor = tf.train.AdamOptimizer(actor_lr, name='actor_optimizer').minimize(loss_actor)    
    
    ##Defining the loss function for the critic 
    loss_critic = tf.reduce_mean(100 * tf.squared_difference(tf.squeeze(last_layer), target_placeholder))
    training_op_critic = tf.train.AdamOptimizer(critic_lr, name='critic_optimizer').minimize(loss_critic)    

#############################################################################################################################################################################
    ##Pretraining the neural networks with offline traces
    a2c_offline_trace_training (env, action_tf_var, action_placeholder, training_op_actor, loss_actor, state_placeholder, last_layer, loss_critic, training_op_critic, 
                                training_episodes, target_placeholder, delta_placeholder, save_dir, critic_input_placeholder, batch_size, offline_trace_full_dir)

#############################################################################################################################################################################    
    ##Training the networks (online, fresh)
    a2c_training_loop (env, action_tf_var, action_placeholder, training_op_actor, loss_actor, state_placeholder, last_layer, loss_critic, 
                       training_op_critic, training_episodes, target_placeholder, delta_placeholder, save_dir, exploration_epsilon, critic_input_placeholder, batch_size)

#############################################################################################################################################################################    
    ##Resmue training the network 
#    a2c_resume_training_saved_model (env, action_tf_var, action_placeholder, training_op_actor, loss_actor, state_placeholder, last_layer, loss_critic, training_op_critic, 
#                                     training_episodes, target_placeholder, delta_placeholder, save_dir, exploration_epsilon, critic_input_placeholder, save_file_name, 
#                                     resume_training_count, save_folder_directory, batch_size)
#############################################################################################################################################################################
    ##Validating the trained neural network 
    trained_model_directory = current_directory + 'saved_model//'
    trained_model_save_file_name = './a2c_trained.ckpt'
    trained_model_save_dir = trained_model_directory + trained_model_save_file_name
    
    vali_saved_dir = current_directory + 'validation_data//'
    
    a2c_run_saved_model (env, action_tf_var, action_placeholder, state_placeholder, trained_model_save_dir, vali_saved_dir)
        
    return 

################################################################################################################################################################################
################################################################################################################################################################################
##Running the script

if __name__ == '__main__':
    main_a2c_function ()
