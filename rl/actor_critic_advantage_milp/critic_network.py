##This function creates the critic network
    ##Inputs the state placeholder 
    ##Outputs the value placeholder for the value function 
##Note that it is important to configure the following:
##  activation function 
##  initiation function 

def critic_network_function (input_placeholder, hidden_layer_neurons, output_dimension, model_output_bounds):
    
    ##input_placeholder         --- the tensorflow placeholder of the input to this neural network 
    ##hidden_layer_neurons      --- an array determining the number of hidden layers and their respective number of neurons 
    ##output_layer_nuerons      --- the number of output neurons 
    ##model_output_bounds       --- the bounds of the critic network 
    
    import tensorflow as tf 
    
    ##Determining the number of hidden layers 
    num_hidden_layers = len(hidden_layer_neurons)
    
    with tf.variable_scope('critic_network'):
        
        ##Initializing function for the weights ##ADJUSTABLE WEIGHTS INITIALIZATION##
        init_weights_fcn = tf.contrib.layers.variance_scaling_initializer()

        ##Initializing a dictionary to hold the layers 
        layers = {}
        
        ##First hidden layer
        layers['0'] = tf.layers.dense(input_placeholder, hidden_layer_neurons[0], tf.nn.elu, init_weights_fcn)   ##ADJUSTABLE ACTIVATION FUNCTION##
        
        for i in range (1, num_hidden_layers):
            layers[str(i)] = tf.layers.dense(layers[str(i-1)], hidden_layer_neurons[i], tf.nn.elu, init_weights_fcn)      ##ADJUSTABLE ACTIVATION FUNCTION##
        
        ##The second last layer --- outputs the predicted objective function and the temperature error 
        last_layer = tf.layers.dense(layers[str(num_hidden_layers-1)], output_dimension, None, init_weights_fcn)
        ##Clipping the outputs of the critic network
        last_layer = tf.clip_by_value(last_layer, model_output_bounds['lb'], model_output_bounds['ub'])

        
    return last_layer