##This function builds the model required for state-independent learning
##Serial implementation 

def si_s_build_agent (hyperparameters):
    
    from keras.models import Sequential 
    from keras.layers import Dense, Activation, Dropout
    
    ##hyperparameters --- a dictionary of hyperparameters 
    
    ##Creating the model 
    model = Sequential()
    
    ##Defining the input layer 
    input_layer_input_neurons = hyperparameters['Number_of_states']
    input_layer_output_neurons = hyperparameters['Hidden_layer_0_neurons']
    a_f = hyperparameters['Hidden_layer_activation_function']
    
    model.add(Dense(input_layer_output_neurons, input_dim=input_layer_input_neurons, activation = a_f))
    ##To prevent overfitting, sometimes the layers do not need to be fully connected
    model.add(Dropout(0.5))
    
    ##Defining the hidden layers
    num_hidden_layers = hyperparameters['Hidden_layers']

    
    for i in range(0, num_hidden_layers):
        curr_layer_neurons = hyperparameters['Hidden_layer_' + str(i) + '_neurons']
        model.add(Dense(curr_layer_neurons, activation = a_f))
        ##To prevent overfitting, sometimes the layers do not need to be fully connected
        model.add(Dropout(0.5))       
        
    ##Defining the output layer
    output_layer_output_neurons = hyperparameters['Number_of_actions']
    ol_af = hyperparameters['Output_layer_activation_function']
    
    model.add(Dense(output_layer_output_neurons, activation = ol_af))    

    ##Compiling the model 
    lf = hyperparameters['Loss_function']
    opti = hyperparameters['NN_optimizer']
    
    model.compile(optimizer = opti, loss = lf)
        
    return model

###############################################################################################################################################################################

##Testing the function 
if __name__ == '__main__':
    si_s_build_agent()