##This script is designed to run the GA multiple times 
def run_ga_multiple_times ():
    
    import pandas as pd 
    import numpy as np 
    from ga_mono_simple_setup_nb import ga_mono_simple_setup_nb
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__))[:-62] + '\\'
    import time 
    
    ##Determining the number of time-steps 
    starting_time_step = 0
    ending_time_step = 24   ##Excluding 
    
    ##Determining the load_type 
    load_type = 'high'
    
    for i in range (starting_time_step, ending_time_step):
        ##Creating an empty dataframe to be stored 
        curr_ts = pd.DataFrame(data = [i], columns = ['Current_time_step'])
            ##Saving the dataframe 
        save_path = current_path + 'control_center\\manu_revision_chiller_only_with_dist_nwk_slave\\temp_working_dir\\'
        save_name = save_path + 'curr_ts.csv'
        curr_ts.to_csv(save_name)
        
        ##Waiting for 30 seconds
        time.sleep(30)
        
        ##Running the genetic algorithm 
        ga_mono_simple_setup_nb()
        
        ##Wait for 30 seconds 
        time.sleep(30)
        
        ##Extracting the output files 
            ##File locations
        result_file_location = current_path + 'master_level\\modular_simple_ga_non_binary\\ga_mono_results\\'
        file_1_dir = result_file_location + 'all_eval_pop.csv'
        file_2_dir = result_file_location + 'best_agent_movement.csv'
        file_3_dir = result_file_location + 'best_obj_per_gen.csv'
        
        file_1 = np.genfromtxt(file_1_dir, delimiter = ',')
        file_2 = np.genfromtxt(file_2_dir, delimiter = ',')
        file_3 = np.genfromtxt(file_3_dir, delimiter = ',')

        ##Saving in the appropriate locations 
        save_file_location = current_path + 'control_center\\manu_revision_chiller_only_with_dist_nwk_slave\\ga_results_current_store\\' + load_type + '_load\\'
        ##Creating an empty folder in the designated location 
        new_dir = save_file_location + 'ts_' + str(i) + '\\'
        os.mkdir(new_dir)
        ##Saving the files
        np.savetxt(new_dir + 'all_eval_pop.csv', file_1, delimiter = ',')                
        np.savetxt(new_dir + 'best_agent_movement.csv', file_2, delimiter = ',') 
        np.savetxt(new_dir + 'best_obj_per_gen.csv', file_3, delimiter = ',')         
        
    return 

#######################################################################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    
    run_ga_multiple_times ()
