##This script contains ancillary functions 

##This function runs the inroute algorithm with sliding window
def run_sliding_window_inroute_algo (home_loc, stop_info, time_matrix, distance_matrix, k_sw, results):
    
    ##home_loc          --- the home coordinates in an array 
    ##stop_info         --- information about the stops 
    ##time_matrix       --- the time matrix 
    ##distance_matrix   --- the distance matrix 
    ##results           --- a dataframe to hold the results
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
    import pandas as pd 
    from datetime import datetime
    
    from sliding_window_inroute_algo import sliding_window_inroute_algorithm
    
    ##Some parameters
    scoring_criteria = 'driving_time'
    sla_buffer = 0
    check_sla = 'no'
    
    startTime = datetime.now()   
    ##Running the inroute algorithm with sliding window   
    stop_order, stop_coordinates, stop_start_time, stop_end_time, idle_time, total_time, valid = sliding_window_inroute_algorithm(home_loc, stop_info, time_matrix, scoring_criteria, 
                                                                                                                                  sla_buffer, check_sla, k_sw)
    running_time = datetime.now() - startTime
    
    ##Converting the results into the readable format 
    ret_df, ret_df_1 = store_inroute_algo_df (stop_order, stop_coordinates, stop_start_time, stop_end_time, idle_time, total_time, valid, distance_matrix)
    
    ##Saving the results
    ret_df.to_csv(current_path + 'results\\sliding_window_inroute_solution_' + str(k_sw) + '.csv')
    ret_df_1.to_csv(current_path + 'results\\sliding_window_inroute_results_' + str(k_sw) + '.csv')   
    
    ##Plotting and saving the final route 
    plot_final_route ('sliding_window_inroute_final_route_plot_' + str(k_sw) + '', ret_df, home_loc)   
    
    ##Placing the running time data into a dataframe 
    running_time_df = pd.DataFrame(data = [[running_time]], columns = ['Running time'])
    running_time_df.to_csv(current_path + 'results\\sliding_window_inroute_running_time_' + str(k_sw) + '.csv')
    
    ##Appending the results dataframe 
    temp_data = list(ret_df_1.values[0, :]) + [running_time, k_sw]
    results = results.append(pd.DataFrame(data = [temp_data], columns = results.columns), ignore_index = True)
    
    return results

###############################################################################################################################################################################
###############################################################################################################################################################################
##This function runs the inroute algorithm for the given dataset 
def run_inroute_algo (home_loc, stop_info, time_matrix, distance_matrix):
    
    ##home_loc          --- the home coordinates in an array 
    ##stop_info         --- information about the stops 
    ##time_matrix       --- the time matrix 
    ##distance_matrix   --- the distance matrix 
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'
    current_path_basic = os.path.dirname(os.path.abspath(__file__))[:-25] + '\\' 
    import sys 
    sys.path.append(current_path_basic + 'inroute_algo\\')
    import pandas as pd 
    from datetime import datetime
    
    from inroute_algo import inroute_algo
    
    ##Some parameters
    scoring_criteria = 'driving_time'
    sla_buffer = 0
    check_sla = 'no'
    
    running_times = []
    startTime = datetime.now()   
    ##Running the inroute algorithm    
    stop_order, stop_coordinates, stop_start_time, stop_end_time, idle_time, total_time, valid = inroute_algo(home_loc, stop_info, time_matrix, scoring_criteria, sla_buffer, check_sla)
    running_times.append([datetime.now() - startTime])
    
    ##Converting the results into the readable format 
    ret_df, ret_df_1 = store_inroute_algo_df (stop_order, stop_coordinates, stop_start_time, stop_end_time, idle_time, total_time, valid, distance_matrix)
    
    ##Saving the results

    ret_df.to_csv(current_path + 'results\\inroute_solution.csv')
    ret_df_1.to_csv(current_path + 'results\\inroute_results.csv')   
    
    ##Plotting and saving the final route 
    plot_final_route ('inroute_final_route_plot', ret_df, home_loc)   
    
    ##Placing the running time data into a dataframe 
    running_time_df = pd.DataFrame(data = running_times, columns = ['Running time'])
    running_time_df.to_csv(current_path + 'results\\inroute_running_time.csv')
    
    return 
###############################################################################################################################################################################
###############################################################################################################################################################################
##This function stores the results of the inroute algorithm into a dataframe 
def store_inroute_algo_df (stop_order, stop_coordinates, stop_start_time, stop_end_time, idle_time, total_time, valid, distance_matrix):
    
    ##stop_order                    --- the order in which the cities should be visited
    ##stop_coordinates              --- the corresponding coordinates of the cities
    ##stop_start_time               --- the time in which the driver reaches the city 
    ##stop_end_time                 --- the time which the driver leaves the city 
    ##idle_time                     --- the time which the driver waits for the SLA to begin/ too late 
    ##total_time                    --- the total computed time of the trip
    ##valid                         --- if all the SLAs are not violated, it is considered to be True
    ##distance_matrix               --- the distance matrix to compute the stop to stop distance and the total distance travelled 
    
    import pandas as pd 
    
    ##Initialzing a dataframe to hold the values 
    ret_df = pd.DataFrame(columns = ['stop_order', 'lat', 'lon', 'op_win_start', 'op_win_end', 'idle_time_mins'])
    
    for i in range (0, len(stop_order)):
        temp_data = []
        temp_data.append(stop_order[i])
        temp_data.append(stop_coordinates[i][0])
        temp_data.append(stop_coordinates[i][1])
        temp_data.append(stop_start_time[i])
        temp_data.append(stop_end_time[i])
        temp_data.append(idle_time[i])
        
        ret_df = ret_df.append(pd.DataFrame(data = [temp_data], columns = ret_df.columns), ignore_index = True)
        
    ##Computing the total distance 
    total_distance = compute_total_distance (stop_order, distance_matrix)
    
    ##Computing the number of stops which are deemed late 
    late_stops = 0
    early_stops = 0
    for i in range (0, len(idle_time)):
        if idle_time[i] > 0:
            early_stops = early_stops + 1
        elif idle_time[i] < 0:
            late_stops = late_stops + 1
    
    ##Initializing another dataframe to hold the values
    data = [valid, len(stop_order), early_stops, late_stops, total_time, total_distance]
    
    ret_df_1 = pd.DataFrame(data = [data], columns = ['valid', 'total_stops', 'early_stops', 'late_stops', 'total_time', 'total_distance'])
    
    return ret_df, ret_df_1

###############################################################################################################################################################################
###############################################################################################################################################################################
##This function plots the reccommended route by the inroute algorithm
def plot_final_route (save_file_name, solution_file, home_coordinates):
    
    ##save_file_name            --- the file name to save the data
    ##solution_file             --- the solution file after the optimization is solved 
    ##home_coordinates          --- the home coordinates 

    import os
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'     
    import matplotlib.pyplot as plt 
    
    ##Creating the x and y axes to plot 
    x = [home_coordinates[1]]
    y = [home_coordinates[0]]
    
    x_stops = []
    y_stops = []
    
    for i in range (0, solution_file.shape[0]):
        x.append(solution_file['lon'][i])
        y.append(solution_file['lat'][i])
        
        x_stops.append(solution_file['lon'][i])
        y_stops.append(solution_file['lat'][i])

    
    fig = plt.figure()
    plt.plot(x, y, 'b-')
    plt.plot([home_coordinates[1]], [home_coordinates[0]], 'g*')
    plt.plot(x_stops, y_stops, 'r*')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    
    plt.savefig(current_path + 'results\\' + save_file_name + '.png', dpi = 1000)
    
    plt.close()
    
    return 

###############################################################################################################################################################################
###############################################################################################################################################################################
##This function intakes the distance matrix and the stop order, after which it comutes the total distance which has to be travelled 
def compute_total_distance (stop_order, distance_matrix):
    
    ##stop_order                    --- the order in which the cities should be visited  
    ##distance_matrix               --- the distance matrix to compute the stop to stop distance and the total distance travelled 
    
    total_distance = 0
    prev_stop = 0
    
    for i in range (0, len(stop_order)):
        total_distance = total_distance + distance_matrix[str(prev_stop)][stop_order[i]]
        prev_stop = stop_order[i]

    return total_distance