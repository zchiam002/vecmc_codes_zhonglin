##This is a rough script for generating the straight line distance matrix for a given set of stop info and home coordinates
def generate_sl_dist_matrix (stop_info, home_loc):
    
    ##stop_info             --- a dataframe containing the information about the stops 
    ##home_loc              --- a dataframe containing information about the home coordinates 
    
    import os 
    current_path_basic = os.path.dirname(os.path.abspath(__file__))[:-49] + '\\'
    import sys 
    sys.path.append(current_path_basic + 'algo_lab\\route_calculator\\')
    from distance_matrix import distance_matrix_straight_line
    
    ##Arranging the coordinates into the correct format 
    coordinates = [[home_loc['lat'][0], home_loc['lon'][0]]]
    
    for i in range (0, stop_info.shape[0]):
        coordinates.append([stop_info['Latitude'][i], stop_info['Longitude'][i]])
    
    dist_df = distance_matrix_straight_line(coordinates)
    
    return dist_df
###############################################################################################################################################################################
###############################################################################################################################################################################
##Running the script 
if __name__ == '__main__':

    import os 
    current_path_basic = os.path.dirname(os.path.abspath(__file__))[:-49] + '\\'
    import pandas as pd     
    
    stop_info = pd.read_csv(current_path_basic + 'algo_lab\\sliding_window_heuristic\\input_data\\stop_info_s0.csv')
    del stop_info['Unnamed: 0']
    home_loc = pd.read_csv(current_path_basic + 'algo_lab\\sliding_window_heuristic\\input_data\\home_info_0.csv')
    del home_loc['Unnamed: 0']    
    
    dist_df = generate_sl_dist_matrix (stop_info, home_loc)
    
    print(dist_df)