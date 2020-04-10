##This script functions as the main script for all the standalone models used
def run_standalone_models ():
    
    from chiller_model_main import run_chiller_model_main
    from evap_network_model_main import run_evaporator_network_model_main 
    
    ##Running the chiller models
    run_chiller_model_main()
    
    ##Running the evaporator network models
    run_evaporator_network_model_main()
    return 

###############################################################################################################################################################################
###############################################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    run_standalone_models()