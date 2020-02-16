##This script contains the ancillaries for the milp_run_script.py



####################################################################################################################################################################
####################################################################################################################################################################
##This function writes the parameters for the milp solver 
def mrs_write_slave_param (cooling_load_data, weather_condition, ga_inputs, piecewise_linear_steps, parallel_thread_number): 
        
    ##cooling_load_data                 --- the associated cooling load data 
    ##weather_condition                 --- the associated weather condition
    ##ga_inputs                         --- inputs from the genetic algorithm
    ##piecewise_linear_steps            --- the number of pieces used to linearize the models 
    ##parallel_thread_number            --- the unique parallel processing number used to access files
    
    import os 
    current_path = os.path.dirname(__file__) + '//'
    from mrs_manual_edit import mrs_manual_edit_milp_param
    
    ##The csv location to store parameters for parallel processing 
    csv_save_loc = current_path+ 'milp_conversion_handlers\\master_values\\'
    csv_save_name = 'ga_milp_var_list_' + str(parallel_thread_number) + '.csv'
    csv_final_save_name = csv_save_loc + csv_save_name
    
    ##Checking if there are similar files with the same name, and removing it, if there are
    exist_result = os.path.exists(csv_final_save_name)
    if exist_result == True:
        os.remove(csv_final_save_name)      
    
    ##Placing the important values into a dataframe 
    milp_param = mrs_manual_edit_milp_param(cooling_load_data, weather_condition, ga_inputs, piecewise_linear_steps)
    milp_param.to_csv(csv_final_save_name)

    return 

####################################################################################################################################################################
####################################################################################################################################################################
##This function imports the relevant files needed to run the milp 
def mrs_import_relevant_files (cooling_load_data_loc, weather_condition_loc, ga_inputs_loc):
    
    ##cooling_load_data_loc         --- directory of the file containing the cooling loads
    ##weather_condition_loc         --- directory of the file containing the weather condition 
    ##ga_inputs_loc                 --- directory of the file containing inputs from the genetic algorithm, (if it is used)
    
    import pandas as pd 
    
    ##Importing the files 
    cooling_load_data = pd.read_csv(cooling_load_data_loc)
    weather_condition = pd.read_csv(weather_condition_loc)
    ga_inputs = pd.read_csv(ga_inputs_loc)
    
    return cooling_load_data, weather_condition, ga_inputs