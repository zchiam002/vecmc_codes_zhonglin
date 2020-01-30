##This script contains auxillary scripts to preprocess the data, i.e. pretrain the neural network 

##This function samples the state input space and normalizes the data and returns a scaler  
def state_normalization (env, sample_size):
    
    ##env           --- the environment to be samples from 
    ##sample_size   --- the number of iterations    
    
    import numpy as np
    import sklearn
    import sklearn.preprocessing    
    
    state_space_samples = np.array([env.observation_space.sample() for x in range (sample_size)])
    scaler = sklearn.preprocessing.StandardScaler()
    scaler.fit(state_space_samples)
    
    return scaler

##This function scales takes in a state and a scaler, returning the scaled data 
def scale_state (state, scaler):
    
    ##state         --- the current state 
    ##scaler        --- the scaler to scale the data
    
    scaled = scaler.transform([state])  ##Requires the inpt shape=(X,) 
                                        ##Required to return the proper shape 
    return scaled
