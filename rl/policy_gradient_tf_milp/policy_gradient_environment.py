##This script deals with the environment which the agent gets to interact with 
def policy_gradient_environment ():
    
    import os 
    current_directory = os.path.dirname(__file__)[:-70] + '//'  
    import sys
    sys.path.append(current_directory + 'control_center//chiller_optimization_dist_nwk_pg//')
    from pg_env_custom import pg_env_custom

    env = pg_env_custom()
    
    return env

################################################################################################################################################################################
################################################################################################################################################################################

