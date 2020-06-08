##This script contains ancillary functions required to run the sliding window inroute algorithm

##This function evaluates the score to check if the difference is smaller than a threshold, we select the stop which finishes more quickly 
def check_score_similarity_choose_quicker_task (brute_force_df, stop_data):
    
    ##score             --- a dataframe holding the values which have be scored against
    ##to_score          --- other scoring mechanism, which is to be used with the criteria 'time_window_priority'
    ##stop_data         --- includes the processing time etc
    
    import pandas as pd 
    
    ##Determining the scoring threshold 
    scoring_threshold = 0.001
    max_threshold = scoring_threshold * brute_force_df.shape[0]
    ##Determining the current best row id             
    best_time = brute_force_df['total_route_time'][0]   
    ##Extracting all the times which also fall within the threshold 
    extracted_score = brute_force_df[abs(brute_force_df['total_route_time'] - best_time) < max_threshold].copy() 
    
    ##Based on this score, we want to extract the processing time which is at the minimum
    processing_time_df = pd.DataFrame(columns = ['stop_idx', 'time_spent_at_loc'])
    
    for i in range (0, extracted_score.shape[0]):
        curr_index = list(extracted_score.index)[i]
        curr_first_stop = extracted_score[0][curr_index]
        curr_processing_time = stop_data['time_spent_at_loc'][int(curr_first_stop) - 1]
        
        processing_time_df = processing_time_df.append(pd.DataFrame(data = [[curr_index, curr_processing_time]], columns = processing_time_df.columns), ignore_index = True)
        
    ##Finding the best index based on the processing time 
    best_row_index = list(processing_time_df['time_spent_at_loc'][:]).index(min(processing_time_df['time_spent_at_loc']))
    best_stop_order = brute_force_df.values[best_row_index][: len(brute_force_df.values[best_row_index]) - 1]     
            
    return best_stop_order
###############################################################################################################################################################################
###############################################################################################################################################################################
##This function takes in the scoring mechanism and chooses the k-best scores before forming a route with them 
def evaluate_k_best_routes (score, to_score, stop_data, k_sw, curr_base_stop, eval_matrix, check_sla, curr_time):
    
    ##score             --- a dataframe holding the values which have be scored against
    ##to_score          --- other scoring mechanism, which is to be used with the criteria 'time_window_priority'
    ##stop_data         --- includes the processing time etc
    ##k_sw              --- the slize of the sliding window
    ##curr_base_stop    --- the base stop to compute from (stop id )
    ##eval_matrix       --- the matrix used for evaluating the objective function 
    ##check_sla         --- on whether there is a need to include the sla waiting penalty if the driver arrives earlier 
    ##curr_time         --- the current time in the route 
    
    from itertools import permutations 
    
    ##Extracting the index of the best score     
    if len(to_score) == 0:                                                  ##In this scenario we use the score mechanism to determine the route 
        ##Sorting the score based on the smallest values first 
        sorted_score = score.sort_values().reset_index()            
    else:
        ##Sorting the score based on the smallest values first              ##Else we use another mechanism to determine the route 
        sorted_score = to_score.sort_values().reset_index()                            

    ##Selecting the top scoring candidates to build the route 
    top_scoring_indices = list(sorted_score['index'][:k_sw])            
    ##Creating a matrix of all possible combinations of the seleted indices
    all_permutation_list = list(permutations(top_scoring_indices))                
    ##Solving the small scale travelling salesman problem in brute force 
    brute_force_df = brute_force_small_scale_tsp (curr_base_stop, eval_matrix, stop_data, all_permutation_list, check_sla, curr_time, k_sw)
                
    return brute_force_df

###############################################################################################################################################################################
###############################################################################################################################################################################
##This function solves the travelling sales man problem using brute force 
def brute_force_small_scale_tsp (curr_base_stop, eval_matrix, stop_data, all_permutation_list, check_sla, curr_time, k_sw):
    
    ##curr_base_stop            --- the base stop to compute from (stop id )
    ##eval_matrix               --- the matrix used for evaluating the objective function 
    ##stop_data                 --- includes the processing time etc
    ##all_permutation_list      --- all the permutations for which the city order could undertake 
    ##check_sla                 --- on whether there is a need to include the sla waiting penalty if the driver arrives earlier   
    ##curr_time                 --- the current time on the global route scale
    ##k_sw                      --- the slize of the sliding window
    
    import pandas as pd 
    from datetime import timedelta 
    
    ##Initializing a list to hold the return results
    return_data = []
    
    ##Iterating all possible combinations 
    for i in range (0, len(all_permutation_list)):
        ##Extracting the current stop combination 
        curr_combi = list(all_permutation_list[i])
        ##Building the route 
        curr_total_route_time = 0
        prev_stop = curr_base_stop
        ##Looping through the stops
        for j in range (0, len(curr_combi)):
            curr_driving_time = eval_matrix[str(int(prev_stop))][int(curr_combi[j])]                ##in seconds
            curr_processing_time = stop_data['time_spent_at_loc'][int(curr_combi[j]) - 1] * 60      ##in seconds
            curr_total_route_time = curr_total_route_time + curr_driving_time + curr_processing_time
            if (check_sla == 'yes') and (curr_time != None):
                curr_sla_start = stop_data['TimeWindowStart'][int(curr_combi[j]) - 1]
                if curr_time < curr_sla_start:
                    idle_time = (curr_sla_start - curr_time).seconds
                    curr_total_route_time = curr_total_route_time + idle_time
            ##Updating the previous stop
            prev_stop = int(curr_combi[j])
        ##Appending the return list 
        return_data.append(curr_combi + [curr_total_route_time])
    
    ##Placing the data into a dataframe 
    ret_data_columns = list(range(k_sw)) + ['total_route_time']
    ret_dataframe = pd.DataFrame(data = return_data, columns = ret_data_columns)
    
    ##Sorting the dataframe 
    ret_dataframe.sort_values(by = ['total_route_time'], inplace = True)
    ret_dataframe.reset_index(inplace = True)
    del ret_dataframe['index']
    
    return ret_dataframe

###############################################################################################################################################################################
###############################################################################################################################################################################
##This function evaluates the score based on a formula for determining the time window priority 
def eval_score_time_window_priority (curr_stop, unassigned_stops, eval_matrix, stop_data, iteration, curr_end_time):
    
    ##curr_stop             --- the current stop to be referenced from 
    ##unassigned_stops      --- the stops which have yet to be assigned
    ##eval_matrix           --- the matrix for which the criteria is to be evaluated 
    ##stop_data             --- a dataframe containing information about the stops
    ##iteration             --- the current iteration, i.e., which stop are we trying to add right now

    import pandas as pd 
    from datetime import timedelta  
    
    ##Some parameters 
    scaling_factor = 0.15
    
    ##Extracting the relevant driving time data from the eval_matrix
    score = eval_matrix[str(curr_stop)][unassigned_stops]
    
    ##The objective is to choose the stop which SLA ends more quickly using a formula
        ##Generating a list of relevant indices to extract information from 
    indices_to_check = [i - 1 for i in unassigned_stops]
        ##Finding the list of starting SLA
    start_SLA = stop_data['TimeWindowStart'][indices_to_check]
        ##Finding the list of ending SLA
    end_SLA = stop_data['TimeWindowEnd'][indices_to_check]
    
    ##Assembling the list of time to evaluate   
        ##If it is the first stop we need to find the latest possible starting time (i.e. the time the driver departs the deport)
    if iteration == 0:
        curr_end_time = determine_latest_start_time (start_SLA, score)
    
    ##Now we need to append the score dataframe
    new_score = []
    for i in unassigned_stops:
        ##Determining the time at which the driver will arrive at the stop, which may be earlier than the SLA
        time_to_test = curr_end_time + timedelta(seconds = int(score[i]))
        ##Determining the amount of idle time
        if time_to_test < start_SLA[i-1]:
            curr_idle_time = (start_SLA[i-1] - time_to_test).seconds
        else:
            curr_idle_time = 0
        ##Determining the difference between the end of the SLA window and when the driver just left the previous stop
        second_duration = (end_SLA[i-1] - curr_end_time).seconds
        
        ##Appending the time according to the formula 
        time_to_append = int(score[i]) + curr_idle_time + (scaling_factor * second_duration)
        
        new_score.append(time_to_append)
        
    ##Placing the new data into a dataframe
    new_score_df = pd.Series(data = new_score, index = list(score.index))            
    
    return new_score_df, score 

###############################################################################################################################################################################
###############################################################################################################################################################################
##This function evaluates the score to determine which the SLA window to choose, based on which one starts first 
def eval_score_fastest_arrival (curr_stop, unassigned_stops, eval_matrix, stop_data, iteration, curr_end_time):
    
    ##curr_stop             --- the current stop to be referenced from 
    ##unassigned_stops      --- the stops which have yet to be assigned
    ##eval_matrix           --- the matrix for which the criteria is to be evaluated 
    ##stop_data             --- a dataframe containing information about the stops
    ##iteration             --- the current iteration, i.e., which stop are we trying to add right now
    
    import pandas as pd 
    import numpy as np
    from datetime import timedelta  

    ##Extracting the relevant driving time data from the eval_matrix
    score = eval_matrix[str(curr_stop)][unassigned_stops]
    
    ##The objective is to choose the earlier SLAs
        ##Generating a list of relevant indices to extract information from 
    indices_to_check = [i - 1 for i in unassigned_stops]
        ##Finding the list of starting SLA
    start_SLA = stop_data['TimeWindowStart'][indices_to_check]
    
    ##Assembling the list of travelling times
        ##If it is the first stop we need to find the latest possible starting time (i.e. the time the driver departs the deport)
    if iteration == 0:
        curr_end_time = determine_latest_start_time (start_SLA, score)
    
    ##Now we need to append the score dataframe
    new_score = [0] * len(unassigned_stops)
    for i in range(0, len(unassigned_stops)):
        curr_unassigned_stop = unassigned_stops[i]
        time_to_test = curr_end_time + timedelta(seconds = int(score[curr_unassigned_stop]))
        if time_to_test < start_SLA[curr_unassigned_stop-1]:
            curr_idle_time = (start_SLA[curr_unassigned_stop-1] - time_to_test).seconds
            new_score[i] = score[curr_unassigned_stop] + curr_idle_time
        else:
            new_score[i] = score[curr_unassigned_stop]
    
    ##Placing the new data into a dataframe
    new_score_df = pd.Series(data = new_score, index = list(score.index))
        
    return new_score_df

###############################################################################################################################################################################
###############################################################################################################################################################################
##This function determines the latest start time for which the driver should leave the deport, only used for the first iteration 
def determine_latest_start_time (start_SLA, score):
    
    ##start_SLA         --- a dataframe containing the list of start SLAs for the stops to be evaluated 
    ##score             --- the datafrme containing the travelling distance to the for the stops to be evaluated
    
    import pandas as pd 
    from datetime import timedelta
    
    ##Finding the list of earliest SLAs
    earliest_SLA = min(start_SLA)
    list_earliest_SLA = start_SLA[start_SLA == earliest_SLA].copy()
    ##Creating a list of possible times in which the driver could leave the deport
    list_possible_starts = []

    for i in list(list_earliest_SLA.index):
        list_possible_starts.append([list_earliest_SLA[i] - timedelta(seconds = int(score[i + 1]))])
    
    possible_starts_df = pd.DataFrame(data = list_possible_starts)       
    ##Finding the latest possible starting time
    latest_possible_start_time = max(possible_starts_df[0])     
    
    return latest_possible_start_time

###############################################################################################################################################################################
###############################################################################################################################################################################
##This function evaluates the score by driving time  
def eval_score_driving_time (curr_stop, unassigned_stops, eval_matrix):
    
    ##curr_stop             --- the current stop to be referenced from 
    ##unassigned_stops      --- the stops which have yet to be assigned
    ##eval_matrix           --- the matrix for which the criteria is to be evaluated 
    
    ##Extracting the relevant driving time data from the eval_matrix 
    score = eval_matrix[str(curr_stop)][unassigned_stops]
   
    return score

###############################################################################################################################################################################
###############################################################################################################################################################################
##This function evaluates the total time required to be spent at the location 
def eval_total_time_spent_at_location (unassigned_stops, stop_data):
    
    ##unassigned_stops      --- the stops which have yet to be assigned
    ##stop_data             --- a dataframe containing information about the stops

    ##Decrease all values in the list by 1 
    new_unassigned = [i -1 for i in unassigned_stops]
    unassigned_time_spent_loc = stop_data.loc[new_unassigned, 'time_spent_at_loc']
    
    return unassigned_time_spent_loc
