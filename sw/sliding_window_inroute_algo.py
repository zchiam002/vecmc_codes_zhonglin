##This is the sliding window version of the inroute algorithm 
def sliding_window_inroute_algorithm (home_stop, stop_data, eval_matrix, scoring_criteria, sla_buffer, check_sla, k_sw):
    
    ##home_stop             --- the an array containing the coordinates of the home stop
    ##stop_data             --- a dataframe containing the information about the stop, such as the required processing time and SLA, etc 
    ##eval_matrix           --- a dataframe containing the socring contributor (e.g distance)
    ##scoring_criteria      --- a string to lead to the correct socring mechanism 
    ##sla_buffer            --- the number of miniytes in which the time window can be preceeded or exceeded 
    ##check_sla             --- whether to add idle time, respect sla
    ##k_sw                  --- the slize of the sliding window
    
    from datetime import timedelta 
    from sliding_window_inroute_algo_anc import eval_total_time_spent_at_location
    from sliding_window_inroute_algo_anc import evaluate_k_best_routes    
    from sliding_window_inroute_algo_anc import check_score_similarity_choose_quicker_task
    from sliding_window_inroute_algo_anc import eval_score_driving_time
    from sliding_window_inroute_algo_anc import eval_score_fastest_arrival
    from sliding_window_inroute_algo_anc import eval_score_time_window_priority
    
    ##Determining the total number of stops
    total_stops = stop_data.shape[0]
    ##Determining the number of iterations required for the given window size 
    req_iter = total_stops - k_sw + 1
    ##Determining the number of stops to add to the route 
    num_stops_to_add = stop_data.shape[0]
    ##Initiating an array to hold the stop order, and relevant details
    stop_order = []
    stop_coordinates = []
    stop_start_time = []
    stop_end_time = []
    idle_time = []
    ##Initiating an array to hold the unassigned stops
    unassigned_stops = list(range(1, stop_data.shape[0] + 1))
    ##A check to determine if the allocation is feasible  
    valid = True
    ##Finding the cumulative time spent at a location
    stop_data['time_spent_at_loc'] = stop_data['ParkingTime'] + stop_data['LocationTime'] + stop_data['ProcessingTime'] + stop_data['UnparkingTime']    
    ##An arbiturary starting time to evalaute the first stop
    curr_time = None
    ##A tracker for adding the total time elasped
    total_time = 0

    ##Running the algorithm 
    for i in range (0, req_iter):
        ##Determining the current stop
        if i == 0:
            curr_stop = 0                                                                                       ##For the first iteration, the current stop will be the home stop
        else:
            curr_stop = stop_order[len(stop_order) - 1]                                                         ##Else it will be the last added stop
    
        ##Determining the processing time required for each of the stops
        unassigned_time_spent_loc = eval_total_time_spent_at_location(unassigned_stops, stop_data)
        
        ##Evaluate the score
            ##An arbiturary array to ensure compatibility with the 'evaluate_k_best_routes' function
        to_score = []
        
        if scoring_criteria == 'driving_time':
            score = eval_score_driving_time (curr_stop, unassigned_stops, eval_matrix)
        elif scoring_criteria == 'fastest_arrival':
            score = eval_score_fastest_arrival (curr_stop, unassigned_stops, eval_matrix, stop_data, i, curr_time)
        elif scoring_criteria == 'time_window_priority':
            to_score, score = eval_score_time_window_priority (curr_stop, unassigned_stops, eval_matrix, stop_data, i, curr_time)   
    
        ##Evaluating the k-best routes generate by the current window 
        brute_force_df = evaluate_k_best_routes(score, to_score, stop_data, k_sw, curr_stop, eval_matrix, check_sla, curr_time)
        ##Selecting the most appropriate city order
        best_stop_order = check_score_similarity_choose_quicker_task (brute_force_df, stop_data)
        print(best_stop_order)
        ##Determining the best stop id 
        best_stop_id = int(best_stop_order[0])
        
        ##Performing checks if the stop will arrive within the SLA
            ##Score is in seconds, basically the driving time 
        curr_driving_time = int(score[best_stop_id])
        total_time = total_time + score[best_stop_id]
            ##Time spent at location is in minutes, lets call this the processing time 
        curr_processing_time = int(unassigned_time_spent_loc[best_stop_id - 1])                                 ##The index of the stop_data dataframe does not include the home location, hence -1
    
        ##Only for the first iteration: to initialize some variables 
        if i == 0:
            curr_time = stop_data['TimeWindowStart'][best_stop_id - 1]                                          ##The time where the driver will reach the first stop
            initial_time = stop_data['TimeWindowStart'][best_stop_id - 1]
            initial_driving_time = int(curr_driving_time)
        else:
            curr_time = curr_time + timedelta(seconds = int(curr_driving_time))                                 ##The driver needs to travel to reach the next stop
        
        ##Preparing for comparison with SLA parameters 
        curr_sla_start = stop_data['TimeWindowStart'][best_stop_id - 1] - timedelta(minutes = sla_buffer)       ##Adding buffers to the SLAs
        curr_sla_end = stop_data['TimeWindowEnd'][best_stop_id - 1] + timedelta(minutes = sla_buffer)                  

        ##Performing checks for SLA compliances, only 3 scenarios can happen 
            ##If too early 
        if curr_time < curr_sla_start:
            curr_idle_time = (curr_sla_start - curr_time).seconds                                               ##If the driver arrived too early we want to add the idle time
            idle_time.append(curr_idle_time)
            if check_sla == 'yes':
                curr_time = curr_time + timedelta(seconds = curr_idle_time)
                total_time = total_time + curr_idle_time
            ##If within the SLA window 
        elif (curr_time >= curr_sla_start) and (curr_time <= curr_sla_end):
            curr_idle_time = timedelta(seconds = 0).seconds
            idle_time.append(curr_idle_time)
            ##If it is later than the SLA window 
        else:                      
            curr_idle_time = (curr_time - curr_sla_end).seconds
            idle_time.append(-curr_idle_time)
            valid = False
        
        ##Appending the relevant information 
        stop_order.append(best_stop_id)
        stop_coordinates.append([stop_data['Latitude'][best_stop_id - 1], stop_data['Longitude'][best_stop_id - 1]])
        stop_start_time.append(curr_time)
        stop_end_time.append(curr_time + timedelta(minutes = int(curr_processing_time)))
        
        ##Updating the current time 
        curr_time = curr_time + timedelta(minutes = int(curr_processing_time))
        total_time = total_time + (60 * curr_processing_time)
        
        ##We also need to delete elements from the unassigned array 
        list_index_to_del = unassigned_stops.index(best_stop_id)
        del unassigned_stops[list_index_to_del]        

    ##We still need to append the final stops
    for i in range (1, len(best_stop_order)):
        ##Determining the best stop id 
        best_stop_id = int(best_stop_order[i])   
        
        ##Performing checks if the stop will arrive within the SLA
            ##Score is in seconds, basically the driving time 
        curr_driving_time = int(score[best_stop_id])
        total_time = total_time + score[best_stop_id]
            ##Time spent at location is in minutes, lets call this the processing time 
        curr_processing_time = int(unassigned_time_spent_loc[best_stop_id - 1])                                 ##The index of the stop_data dataframe does not include the home location, hence -1
            ##Appending the driving time
        curr_time = curr_time + timedelta(seconds = int(curr_driving_time))

        ##Preparing for comparison with SLA parameters 
        curr_sla_start = stop_data['TimeWindowStart'][best_stop_id - 1] - timedelta(minutes = sla_buffer)       ##Adding buffers to the SLAs
        curr_sla_end = stop_data['TimeWindowEnd'][best_stop_id - 1] + timedelta(minutes = sla_buffer)                  

        ##Performing checks for SLA compliances, only 3 scenarios can happen 
            ##If too early 
        if curr_time < curr_sla_start:
            curr_idle_time = (curr_sla_start - curr_time).seconds                                               ##If the driver arrived too early we want to add the idle time
            idle_time.append(curr_idle_time)
            if check_sla == 'yes':
                curr_time = curr_time + timedelta(seconds = curr_idle_time)
                total_time = total_time + curr_idle_time
            ##If within the SLA window 
        elif (curr_time >= curr_sla_start) and (curr_time <= curr_sla_end):
            curr_idle_time = timedelta(seconds = 0).seconds
            idle_time.append(curr_idle_time)
            ##If it is later than the SLA window 
        else:                      
            curr_idle_time = (curr_time - curr_sla_end).seconds
            idle_time.append(-curr_idle_time)
            valid = False
        
        ##Appending the relevant information 
        stop_order.append(best_stop_id)
        stop_coordinates.append([stop_data['Latitude'][best_stop_id - 1], stop_data['Longitude'][best_stop_id - 1]])
        stop_start_time.append(curr_time)
        stop_end_time.append(curr_time + timedelta(minutes = int(curr_processing_time)))
        
        ##Updating the current time 
        curr_time = curr_time + timedelta(minutes = int(curr_processing_time))
        total_time = total_time + (60 * curr_processing_time)

    return stop_order, stop_coordinates, stop_start_time, stop_end_time, idle_time, total_time, valid