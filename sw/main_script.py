##This is the main script for funning the k-sliding window algorithm

def run_k_sliding_window ():

    import os
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'    
    import sys 
    sys.path.append(current_path + 'working_folder\\')
    import pandas as pd 
    
    from ancillaries import run_inroute_algo
    from ancillaries import run_sliding_window_inroute_algo
    from generate_straight_line_matrix import generate_sl_dist_matrix
    
    ##Importing the relevant files 
    
    ##This is for the 70 stops
    # stop_info = pd.read_csv(current_path + 'input_data\\stop_info.csv', parse_dates = ['TimeWindowStart', 'TimeWindowEnd'], dayfirst = False)
    # del stop_info['Unnamed: 0']
    # time_matrix = pd.read_csv(current_path + 'input_data\\time_matrix.csv')
    # del time_matrix['Unnamed: 0']
    # distance_matrix = pd.read_csv(current_path + 'input_data\\distance_matrix.csv')
    # del distance_matrix['Unnamed: 0']
    # home_info = pd.read_csv(current_path + 'input_data\\home_info_0.csv')
    # del home_info['Unnamed: 0']            
    # sl_dist_matrix = generate_sl_dist_matrix(stop_info, home_info) 
    # sl_dist_matrix.to_csv(current_path + 'input_data\\sl_distance_matrix.csv')
    # sl_dist_matrix = pd.read_csv(current_path + 'input_data\\sl_distance_matrix.csv')
    # del sl_dist_matrix['Unnamed: 0']
    
    ##This is for s0 dataset
    # stop_info = pd.read_csv(current_path + 'input_data\\stop_info_s0.csv', parse_dates = ['TimeWindowStart', 'TimeWindowEnd'], dayfirst = False)
    # del stop_info['Unnamed: 0']
    # time_matrix = pd.read_csv(current_path + 'input_data\\time_matrix_s0.csv')
    # del time_matrix['Unnamed: 0']
    # distance_matrix = pd.read_csv(current_path + 'input_data\\distance_matrix_s0.csv')
    # del distance_matrix['Unnamed: 0']    
    # home_info = pd.read_csv(current_path + 'input_data\\home_info_0.csv')
    # del home_info['Unnamed: 0']   
    # sl_dist_matrix = generate_sl_dist_matrix(stop_info, home_info) 
    # sl_dist_matrix.to_csv(current_path + 'input_data\\sl_distance_matrix_s0.csv')
    # sl_dist_matrix = pd.read_csv(current_path + 'input_data\\sl_distance_matrix_s0.csv')
    # del sl_dist_matrix['Unnamed: 0']

    # #This is for s1 dataset
    # stop_info = pd.read_csv(current_path + 'input_data\\stop_info_s1.csv', parse_dates = ['TimeWindowStart', 'TimeWindowEnd'], dayfirst = False)
    # del stop_info['Unnamed: 0']
    # time_matrix = pd.read_csv(current_path + 'input_data\\time_matrix_s1.csv')
    # del time_matrix['Unnamed: 0']
    # distance_matrix = pd.read_csv(current_path + 'input_data\\distance_matrix_s1.csv')
    # del distance_matrix['Unnamed: 0']    
    # home_info = pd.read_csv(current_path + 'input_data\\home_info_s1.csv')
    # del home_info['Unnamed: 0']   
    # sl_dist_matrix = generate_sl_dist_matrix(stop_info, home_info) 
    # sl_dist_matrix.to_csv(current_path + 'input_data\\sl_distance_matrix_s1.csv')
    # sl_dist_matrix = pd.read_csv(current_path + 'input_data\\sl_distance_matrix_s1.csv')
    # del sl_dist_matrix['Unnamed: 0']

    #This is for s2 dataset
    stop_info = pd.read_csv(current_path + 'input_data\\stop_info_s2.csv', parse_dates = ['TimeWindowStart', 'TimeWindowEnd'], dayfirst = False)
    del stop_info['Unnamed: 0']
    time_matrix = pd.read_csv(current_path + 'input_data\\time_matrix_s2.csv')
    del time_matrix['Unnamed: 0']
    distance_matrix = pd.read_csv(current_path + 'input_data\\distance_matrix_s2.csv')
    del distance_matrix['Unnamed: 0']    
    home_info = pd.read_csv(current_path + 'input_data\\home_info_s2.csv')
    del home_info['Unnamed: 0']   
    sl_dist_matrix = generate_sl_dist_matrix(stop_info, home_info) 
    sl_dist_matrix.to_csv(current_path + 'input_data\\sl_distance_matrix_s2.csv')
    sl_dist_matrix = pd.read_csv(current_path + 'input_data\\sl_distance_matrix_s2.csv')
    del sl_dist_matrix['Unnamed: 0']
    
    ##This is for the p0 dataset 
    # stop_info = pd.read_csv(current_path + 'input_data\\stop_info_p0.csv', parse_dates = ['TimeWindowStart', 'TimeWindowEnd'], dayfirst = False)
    # del stop_info['Unnamed: 0']
    # time_matrix = pd.read_csv(current_path + 'input_data\\time_matrix_p0.csv')
    # del time_matrix['Unnamed: 0']
    # distance_matrix = pd.read_csv(current_path + 'input_data\\distance_matrix_p0.csv')
    # del distance_matrix['Unnamed: 0']      
    # home_info = pd.read_csv(current_path + 'input_data\\home_info_p0.csv')
    # del home_info['Unnamed: 0']             
    # sl_dist_matrix = generate_sl_dist_matrix(stop_info, home_info) 
    # sl_dist_matrix.to_csv(current_path + 'input_data\\sl_distance_matrix_p0.csv')
    # sl_dist_matrix = pd.read_csv(current_path + 'input_data\\sl_distance_matrix_p0.csv')
    # del sl_dist_matrix['Unnamed: 0']    
    
    ##Determining the size of the sliding window 
    k_sw = 3
    
    ##Reformatting the information 
    home_loc = [home_info['lat'][0], home_info['lon'][0]]
    
    ##Running the inroute algorithm 
    run_inroute_algo (home_loc, stop_info, sl_dist_matrix, sl_dist_matrix)
    
    ##Running the sliding window inroute algorithm 
    results = pd.DataFrame(columns = ['valid', 'total_stops', 'early_stops', 'late_stops', 'total_time', 'total_distance', 'running_time', 'sws'])
    for i in range (1, 10):
        k_sw = i
        results = run_sliding_window_inroute_algo (home_loc, stop_info, sl_dist_matrix, sl_dist_matrix, k_sw, results)
    
    ##Saving the results 
    results.to_csv(current_path + 'results\\results_sw_all.csv')
    
    return 

#######################################################################################################################################################
#######################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    run_k_sliding_window ()
