##This is the main function which runs the mono-objective Genetic Algorithm 
def run_mono_ga_nb ():
    
    import os
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'            ##Incase of the need to use relative directory
    import sys 
    sys.path.append(current_path + '')
    from ga_mono_simple_setup_nb import ga_mono_simple_setup_nb
    
    ##Running the GA
    ga_mono_simple_setup_nb()
    
    
    return 

#########################################################################################################################################################################
#########################################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    run_mono_ga_nb ()