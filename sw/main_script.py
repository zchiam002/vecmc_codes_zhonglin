##This is the main script for funning the k-sliding window algorithm
def run_k_sliding_window ():

    import os
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'         
    import pandas as pd 
    from evaluate_problem import evaluate_problem 
    
    ##Determining the sizes of the sliding windows 
    k_sw_min = 1
    k_sw_max = 5            ##This needs to correspond to the maximum size of the problem (variables, time-steps, etc)
    
    ##Creating a dataframe to hold thre return values 
    ret_values = pd.DataFrame(columns = ['sliding_window_size', 'variables', 'objective_function'])
    
    ##Running the sliding window inroute algorithm 
    for i in range (k_sw_min, k_sw_max):
        ##Evaluating the problem 
        ret_data = evaluate_problem (i)
        ##Appending the dataframe 
        ret_values = ret_values.append(pd.DataFrame(data = [[i, ret_data[1], ret_data[0]]], columns = ['sliding_window_size', 'variables', 'objective_function']), ignore_index = True)
        
    ##Saving the results 
    ret_values.to_csv(current_path + 'results//results.csv')
    
    return 

#######################################################################################################################################################
#######################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    run_k_sliding_window ()
