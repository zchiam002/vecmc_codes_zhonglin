##A function for creating the neural network 
def ff_policy_gradient_contextual_bandits_build_network(self, hyperparameters):
    
    import os
    os.environ["TF_CPP_MIN_LOG_LEVEL"]="3"
    import tensorflow as tf
    
    #Placeholders for input x, and output y
    self.X = tf.placeholder(tf.float32, shape=(self.n_x, None), name="X")           ##The states of the environment 
    self.Y = tf.placeholder(tf.float32, shape=(self.n_y, None), name="Y")           ##The actions of the agent 
    
    #Placeholders for the reward 
    self.rewards_tensor = tf.placeholder(tf.float32, [None, ], name="actions_value")
    
    ##Building a N hidden layer neural network 
    num_layers = hyperparameters['Hidden_layers']
    
        ##Number of neurons in each hidden layer 
    neurons_layer = []
    for i in range (0, num_layers):
        temp_name = 'Hidden_layer_' + str(i) + '_neurons'
        neurons_layer.append(hyperparameters[temp_name])
    
    ##Initialize weights and bias value using tensorflow's tf.contrib.layers.xavier_initializer
        ##Dictionaries to hold values
    weights = {}
    bias = {}
    
    for i in range (0, num_layers):
        temp_name_w = 'W' + str(i)
        temp_name_b = 'b' + str(i)
        
        if i == 0:
            weights[temp_name_w] = tf.get_variable(temp_name_w, [neurons_layer[i], self.n_x], initializer = tf.contrib.layers.xavier_initializer(seed=1))
        else:
            weights[temp_name_w] = tf.get_variable(temp_name_w, [neurons_layer[i], neurons_layer[i-1]], initializer = tf.contrib.layers.xavier_initializer(seed=1))
            
        bias[temp_name_b] = tf.get_variable(temp_name_b, [neurons_layer[i], 1], initializer = tf.contrib.layers.xavier_initializer(seed=1))
    
        ##Dealing with the final layer 
    i = num_layers
    temp_name_w = 'W' + str(i)
    temp_name_b = 'b' + str(i)        
    weights[temp_name_w] = tf.get_variable(temp_name_w, [self.n_y, neurons_layer[i-1]], initializer = tf.contrib.layers.xavier_initializer(seed=1))
    bias[temp_name_b] = tf.get_variable(temp_name_b, [self.n_y, 1], initializer = tf.contrib.layers.xavier_initializer(seed=1))        
    
    ##Now the forward propagation is performed 
        ##Dictionaries to hold values 
    z_function = {}
    a_function = {}
    
    for i in range (0, num_layers):
        temp_name_z = 'Z' + str(i)
        temp_name_a = 'A' + str(i)
        temp_name_w = 'W' + str(i)
        temp_name_b = 'b' + str(i)            
        
        if i == 0:
            z_function[temp_name_z] = tf.add(tf.matmul(weights[temp_name_w],self.X), bias[temp_name_b])
        else:
            temp_name_a_minus_1 = 'A' + str(i-1)
            z_function[temp_name_z] = tf.add(tf.matmul(weights[temp_name_w],a_function[temp_name_a_minus_1]), bias[temp_name_b])                
        if hyperparameters['Hidden_layer_activation_function'] == 'relu':
                a_function[temp_name_a] = tf.nn.relu(z_function[temp_name_z])
    
        ##Dealing with the output layer, num_layers only account for the number of hidden layers. Since it starts from 0, the output layer is indexed by the num_layers 
    i = num_layers
    temp_name_z = 'Z' + str(i)
    temp_name_a = 'A' + str(i)
    temp_name_w = 'W' + str(i)
    temp_name_b = 'b' + str(i)         
    temp_name_a_minus_1 = 'A' + str(i-1)
        
    z_function[temp_name_z] = tf.add(tf.matmul(weights[temp_name_w], a_function[temp_name_a_minus_1]), bias[temp_name_b])
    if hyperparameters['Output_layer_activation_function'] == 'softmax':        
        a_function[temp_name_a] = tf.nn.softmax(z_function[temp_name_z])
        logits = tf.transpose(z_function[temp_name_z])
        labels = tf.transpose(self.Y)
        self.outputs = tf.nn.softmax(logits, name=temp_name_a)
        
        
    elif hyperparameters['Output_layer_activation_function'] == 'none':
        a_function[temp_name_a] = 'none'
        
    
    ##Define loss function
    if hyperparameters['Loss_function'] == 'softmax_cross_entropy_with_logits':
        neg_log_prob = tf.nn.softmax_cross_entropy_with_logits(logits = logits, labels=labels)
    
    ##Define the reward guided loss
    if hyperparameters['Reward_guided_loss'] == 'reduce_mean':        
        loss = tf.reduce_mean(neg_log_prob * self.rewards_tensor)
        
    ##Define the optimizer for minimizeing the loss
    if hyperparameters['NN_optimizer'] == 'adam_optimizer':
        self.train_op = tf.train.AdamOptimizer(self.lr).minimize(loss)
        
    return