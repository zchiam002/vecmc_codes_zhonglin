##This script contains ancillary functions 

##This function connects to the problem and solves it using the k-sliding window technique 
def evaluate_problem (sliding_window_size):
    
    ##sliding_window_size           --- the current sliding window size
    
    from minimum_hamiltonian_path import minimum_hamiltonian_path
    
    ##Running the problem 
    total_distance, stop_order = minimum_hamiltonian_path(sliding_window_size)
        
    ##Assembling the return data 
    ret_data = [total_distance, stop_order]
    
    return ret_data







