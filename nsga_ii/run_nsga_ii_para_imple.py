##This is the main function which runs the mono-objective Genetic Algorithm 
def run_nsga_ii_para_imple ():
    
    import os
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'            ##Incase of the need to use relative directory
    import sys 
    sys.path.append(current_path + '')
    from nsga_ii_para_imple_simple_setup import nsga_ii_para_imple_simple_setup
    
    ##Running NGSA-II
    nsga_ii_para_imple_simple_setup()
    
    
    return 

#########################################################################################################################################################################
#########################################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    run_nsga_ii_para_imple ()