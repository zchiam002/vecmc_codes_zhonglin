##This function creates the policy gradient network 
    ##It inputs the state 
    ##Outputs 2 values per output variable  
        ##mu    --- the mean of a gaussian distribution 
        ##sigma --- the standard deviation of a gaussian distribution 
    ##Since we want an action sampled from a continuous action space, this is the way to represent the probabilistic function 
    ##After which, the sampled action and the normal distribution function will be returned
##Note that it is important to configure the following:
##  activation function 
##  initiation function 

def policy_gradient_function (state_placeholder, hidden_layer_neurons, output_dimension, env_action_ub_lb):
    
    ##state_placeholder         --- the tensorflow placeholder of the input to this neural network 
    ##hidden_layer_neurons      --- an array determining the number of hidden layers and their respective number of neurons 
    ##output_layer_nuerons      --- the number of output neurons 
    ##env_action_ub_lb          --- the dictionary of upper and lower bounds for clipping the outputs

    import tensorflow as tf 

    ##Determining the number of hidden layers 
    num_hidden_layers = len(hidden_layer_neurons)    

    with tf.variable_scope('policy_gradient_network'):
        
        ##Initializing function for the weights ##ADJUSTABLE WEIGHTS INITIALIZATION##
        init_weights_fcn = tf.contrib.layers.variance_scaling_initializer()
        
        ##Initializing a dictionary to hold the layers 
        layers = {}
        
        ##First hidden layer
        layers['0'] = tf.layers.dense(state_placeholder, hidden_layer_neurons[0], None, init_weights_fcn)              ##ADJUSTABLE ACTIVATION FUNCTION##

        for i in range (1, num_hidden_layers):
            layers[str(i)] = tf.layers.dense(layers[str(i - 1)], hidden_layer_neurons[i], tf.nn.elu, init_weights_fcn)      ##ADJUSTABLE ACTIVATION FUNCTION## 

        ##Output layer for the first action 
            ##The output layer for the mean of the gaussian distribution 
        mu = tf.layers.dense(layers[str(num_hidden_layers - 1)], output_dimension, None, init_weights_fcn)                  ##ADJUSTABLE ACTIVATION FUNCTION##
            ##The output layer for the sigma of the gaussian distribution 
        sigma = tf.layers.dense(layers[str(num_hidden_layers - 1)], output_dimension, None, init_weights_fcn)               ##ADJUSTABLE ACTIVATION FUNCTION##
            ##The standard deviation should not be 0
        sigma = tf.nn.softmax(sigma) + 1e-5                                                                                 ##ADJUSTABLE SCALE##         
            ##Creating a normal distribution based on the above parameters 
        norm_dist = tf.contrib.distributions.Normal(mu, sigma)
        ##Placing the output value in the proper form 
        action_tf_var = tf.squeeze(norm_dist.sample(1), axis=0)
        ##Clipping the values of the output
        action_tf_var = tf.clip_by_value(action_tf_var, env_action_ub_lb['lb'], env_action_ub_lb['ub'])        

    return action_tf_var, norm_dist 

