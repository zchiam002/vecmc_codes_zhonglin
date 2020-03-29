##This script contains the ancillaries for the milp_run_script.py

##This function calculates the return temperature from the MILP solver and computes the difference with the expected return temperature
def mrs_check_temperature_diff (obj_value, results, cooling_load_data, ga_inputs, all_dataframes):
    
    ##obj_value                                             --- the value of the objective function 
    ##results                                               --- a dataframe documenting the values of the continuous decision variables 
    ##cooling_load_data                                     --- a dataframe containing all the cooling load values
    ##ga_inputs                                             --- the inputs from the genetic algorithm
    
    ##all_dataframes                                        --- a dictionary of compiled dataframes from the models 
    ##all_dataframes['utilitylist_bilinear']                --- list of bilinear utilities 
    ##all_dataframes['processlist_bilinear']                --- list of bilinear processes
    ##all_dataframes['streams_bilinear']                    --- list of bilinear streams 
    ##all_dataframes['cons_eqns_terms_bilinear']            --- list of bilinear cons_eqns_terms
    ##all_dataframes['utilitylist_linear']                  --- linear utility list 
    ##all_dataframes['processlist_linear']                  --- linear process list 
    ##all_dataframes['streams_linear']                      --- linear streams list 
    ##all_dataframes['cons_eqns_terms_linear']              --- linear cons_eqns_terms 
    ##all_dataframes['cons_eqns_all']                       --- all cons_eqns  
    ##all_dataframes['layerslist']                          --- layerslist
    ##all_dataframes['utilitylist']                         --- utilitylist
    ##all_dataframes['processlist']                         --- processlist
    ##all_dataframes['streams']                             --- streams
    ##all_dataframes['cons_eqns']                           --- cons_eqns
    ##all_dataframes['cons_eqns_terms']                     --- cons_eqns_terms

    import os 
    current_path = os.path.dirname(__file__) + '//'
    import pandas as pd 
    
    ##Identifiers  
    temp_id = 't'                                           ##Identifier for temperature-related variables 
    flow_id = 'm_perc'                                      ##Identifier for flow-related variable 
    
    values_to_extract_per_model = 2                         ##The number of optimal values to extract per model 
    
    ##Extracting the values from the ga_input file 
    tin_evap = ga_inputs['tin_evap'][0]                     ##The expected return temperature 
    evap_flow = ga_inputs['evap_flow'][0]                   ##The expected total flow rate through the evaporator network 
    
    ##Determining the names of the models listed as processes
    sub_station_names = list(cooling_load_data.columns)
    ##Appending the common pipe name 
    common_pipe_name = ['cp_nwk']
    ##Creating a dictionary to store the relevant variable names for each of the required models 
    req_model_var_names = {}
    for i in sub_station_names:
        req_model_var_names[i] = []
        for j in range (0, all_dataframes['utilitylist'].shape[0]):
            if all_dataframes['utilitylist']['Name'][j] == i:
                req_model_var_names[i].append(i + '_' + all_dataframes['utilitylist']['Variable1'][j])
                req_model_var_names[i].append(i + '_' + all_dataframes['utilitylist']['Variable2'][j])
                break
        
    ##If the flowrate is 0, then it does not make any sense to continue the calculations 
    if evap_flow > 0:
        flow = evap_flow * 998.2 / 3600
        exit_cst_values = {}
        for i in sub_station_names:
            exit_cst_values[i] = cooling_load_data[i][0] / (flow * 4.2)
    
        ##Extracting the optimum values 
        opti_values = {}
        for i in sub_station_names:
            opti_values[i] = {}
            curr_values_to_extract = values_to_extract_per_model
            for j in range (0, results.shape[0]):
                if i in results['Name'][j]:
                    if temp_id in results['Name'][j]:
                        opti_values[i][temp_id] = results['Values'][j]
                        curr_values_to_extract = curr_values_to_extract - 1
                    elif flow_id in results['Name'][j]:
                        opti_values[i][flow_id] = results['Values'][j]
                        curr_values_to_extract = curr_values_to_extract - 1 
                elif curr_values_to_extract == 0:
                    break 
        
        for i in common_pipe_name:
            opti_values[i] = {}
            curr_values_to_extract = values_to_extract_per_model
            for j in range (0, results.shape[0]):
                if i in results['Name'][j]:
                    if temp_id in results['Name'][j]:
                        opti_values[i][temp_id] = results['Values'][j]
                        curr_values_to_extract = curr_values_to_extract - 1
                    elif flow_id in results['Name'][j]:
                        opti_values[i][flow_id] = results['Values'][j]
                        curr_values_to_extract = curr_values_to_extract - 1 
                elif curr_values_to_extract == 0:
                    break     
        
        ##Calculating the outlet temperature for the substation and the common pipe 
        ss_tinmax = pd.read_csv(current_path + 'model_param//\model_param.csv')['Value'][0]
                        
        opti_values_real_tout = {}
        calculated_return_temperature = 0 
        
        for i in list(opti_values.keys()):
            if i in sub_station_names:
                opti_values_real_tout[i] = (274.15 * opti_values[i][flow_id]) + ((ss_tinmax - 273.15 - 1) * opti_values[i][flow_id] * opti_values[i][temp_id]) + exit_cst_values[i]
                calculated_return_temperature = calculated_return_temperature + opti_values_real_tout[i]
            elif i in common_pipe_name:
                opti_values_real_tout[i] = (273.15 * opti_values[i][flow_id]) + (30 * opti_values[i][flow_id] * opti_values[i][temp_id])
                calculated_return_temperature = calculated_return_temperature + opti_values_real_tout[i]
    
        ##Calculating the difference with the expected return temperature
        diff = abs(calculated_return_temperature - tin_evap)
        
    else:
        calculated_return_temperature = 'na'
        diff = 'na'
    
    return calculated_return_temperature, diff 

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
    del cooling_load_data['Unnamed: 0']
    weather_condition = pd.read_csv(weather_condition_loc)
    del weather_condition['Unnamed: 0']
    ga_inputs = pd.read_csv(ga_inputs_loc)
    
    return cooling_load_data, weather_condition, ga_inputs