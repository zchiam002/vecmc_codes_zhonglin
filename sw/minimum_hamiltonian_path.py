##This function contains the minimium hamiltonian path problem 
def minimum_hamiltonian_path (sliding_window_size):
    
    ##sliding_window_size               --- the size of the sliding window

    import os
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'       
    import pandas as pd 
    from itertools import permutations 
    
    ##Importing the relevant datasets
        ##The stops to traverse
    stop_info = pd.read_csv(current_path + 'input_data\\stop_info_s2.csv')
    del stop_info['Unnamed: 0']
        ##The starting stop 
    home_info = pd.read_csv(current_path + 'input_data\\home_info_s2.csv')
    del home_info['Unnamed: 0']
        ##The straight-line distance matrix 
    sl_dist_matrix = pd.read_csv(current_path + 'input_data\\sl_distance_matrix_s2.csv')
    del sl_dist_matrix['Unnamed: 0']
    
    ##Determining total iterations to run 
    total_stops = stop_info.shape[0]
    ##Determining the number of iterations required for the given window size 
    req_iter = total_stops - sliding_window_size + 1     
    ##An array to track the stop order 
    stop_order = [] 
    ##A variable to track the total distance travelled 
    total_distance = 0
    ##Initiating an array to hold the unassigned stops
    unassigned_stops = list(range(1, stop_info.shape[0] + 1)) 
    ##A tracker of the previous stop 
    prev_stop = 0                                                               ##0 is indicative of the home stop 
    
    ##Running the algorithm 
    for i in range (0, req_iter):
        ##Ranking the next best stops according in the unassigned list 
        score = eval_score_driving_time (prev_stop, unassigned_stops, sl_dist_matrix)        
        ##Sorting the stops in the correct order 
        score_sorted = score.sort_values().reset_index()
        ##Selecting the top scoring candidates to build the route 
        top_scoring_indices = list(score_sorted['index'][0: sliding_window_size])
        ##Iterating through all possible permutations of the top scoing indices
        all_permutation_list = list(permutations(top_scoring_indices)) 
        ##Brute forcing the list of stops 
        ret_dataframe = brute_force_small_scale_tsp (prev_stop, sl_dist_matrix, stop_info, all_permutation_list, sliding_window_size)
        ##Finding the next best stop to the list 
        next_best_stop = ret_dataframe[0][0]
        ##Adding the distance to the total distance tracker       
        total_distance = total_distance + sl_dist_matrix[str(prev_stop)][next_best_stop]
        ##Appending the next best stop to the list 
        stop_order.append(next_best_stop)
        ##We also need to delete elements from the unassigned array 
        list_index_to_del = unassigned_stops.index(next_best_stop)
        del unassigned_stops[list_index_to_del]  
        ##Updating the previous stop 
        prev_stop = next_best_stop 

    ##We still need to append the final stops
    best_stop_order = ret_dataframe.values[0, :sliding_window_size]
    for i in range (1, len(best_stop_order)):
        ##Determining the best stop id 
        next_best_stop = int(best_stop_order[i])
        ##Appending the next stop data 
        stop_order.append(next_best_stop)
        ##Appending the total distance 
        total_distance = total_distance + sl_dist_matrix[str(prev_stop)][next_best_stop]
        ##Updating the previous stop 
        prev_stop = next_best_stop
       
    return total_distance, stop_order

#######################################################################################################################################################
#######################################################################################################################################################
##This function solves the travelling sales man problem using brute force 
def brute_force_small_scale_tsp (curr_base_stop, eval_matrix, stop_data, all_permutation_list, k_sw):
    
    ##curr_base_stop            --- the base stop to compute from (stop id )
    ##eval_matrix               --- the matrix used for evaluating the objective function 
    ##stop_data                 --- includes the processing time etc
    ##all_permutation_list      --- all the permutations for which the city order could undertake 
    ##k_sw                      --- the slize of the sliding window
    
    import pandas as pd 
    
    ##Initializing a list to hold the return results
    return_data = []
    
    ##Iterating all possible combinations 
    for i in range (0, len(all_permutation_list)):
        ##Extracting the current stop combination 
        curr_combi = list(all_permutation_list[i])
        ##Building the route 
        curr_total_route_distance = 0
        prev_stop = curr_base_stop
        ##Looping through the stops
        for j in range (0, len(curr_combi)):
            ##Updating the total distance 
            curr_total_route_distance = curr_total_route_distance + eval_matrix[str(prev_stop)][int(curr_combi[j])] 
            ##Updating the previous stop
            prev_stop = int(curr_combi[j])
        ##Appending the return list 
        return_data.append(curr_combi + [curr_total_route_distance])
    
    ##Placing the data into a dataframe 
    ret_data_columns = list(range(k_sw)) + ['total_route_distance']
    ret_dataframe = pd.DataFrame(data = return_data, columns = ret_data_columns)
    
    ##Sorting the dataframe 
    ret_dataframe.sort_values(by = ['total_route_distance'], inplace = True)
    ret_dataframe.reset_index(inplace = True)
    del ret_dataframe['index']
    
    return ret_dataframe

#######################################################################################################################################################
#######################################################################################################################################################
##This function evaluates the score by driving time  
def eval_score_driving_time (curr_stop, unassigned_stops, eval_matrix):
    
    ##curr_stop             --- the current stop to be referenced from 
    ##unassigned_stops      --- the stops which have yet to be assigned
    ##eval_matrix           --- the matrix for which the criteria is to be evaluated 
    
    ##Extracting the relevant driving time data from the eval_matrix 
    score = eval_matrix[str(curr_stop)][unassigned_stops]
   
    return score