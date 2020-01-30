##This script deals with the environment which the agent gets to interact with 
def a2c_environment ():
    
    import os 
    current_directory = os.path.dirname(__file__)[:-74] + '//'  
    import sys
    sys.path.append(current_directory + 'control_center//chiller_optimization_dist_nwk_a2c//')
    from a2c_env_custom import a2c_env_custom

    env = a2c_env_custom()
    
    return env

################################################################################################################################################################################
################################################################################################################################################################################


    