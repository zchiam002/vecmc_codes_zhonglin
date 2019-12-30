##This is a temporary interface for converting the master decision variables into inputs for the slave optimization 

def slave_test_script(obj_weights, curr_run, thread_num, process_method):
    
    from datetime import datetime
    startTime = datetime.now()
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level\\auxillary')
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\load_only_storage_milp_master_level_models\\')
    sys.path.append('C:\\Optimization_zlc\\slave_level_models\\load_only_storage_milp_slave_convex\\')
    from models.cvx_prog_run import cvx_prog_run
    from input_data_process import extract_temp
    from input_data_process import extract_demand
    from input_data_process import extract_elect_tariff
    from convert_mdv_to_slave_param import convert_mdv_to_slave_param_v3
    import pandas as pd
    
    ##obj_weights --- the associated weights to each of the objective functions 
    ##curr_run --- the current itertaion number
    ##thread_num --- id for parallel processing
    ##process_method --- serial or parallel, affects the printing
    
    ###########################################################################
    ###########################DEFINING PARAMETERS#############################
    ###########################################################################
    
    thread_number = thread_num   ##Arbiturary number, not useful for serial processing 
    piecewise_steps = 4
    bilinear_pieces = 20
    
    ###########################################################################
    #########################INPUT DATA PROCESSING#############################
    ###########################################################################
    
    ##DEMAND DATA 
    
    ##Location for the demand data 
        ##Processing high load data
    demand_file_loc = 'C:\\Optimization_zlc\\input_data\\load_only_storage_milp_input_data\\high_load\\high_demand.csv'
        ##Importing them into dataFrames 
    demand = extract_demand(demand_file_loc)
    dim_demand = demand.shape
        ##The number of time steps is dependent on this 
    time_steps = dim_demand[0]

    ##WEATHER DATA 
    
    ##Getting information for condenser inlet temperature 
    temp_loc = 'C:\\Optimization_zlc\\input_data\\load_only_storage_milp_input_data\\high_load\\high_demand_weather.csv'
    temp_wb = pd.read_csv(temp_loc)
    
    ##ELECTRICITY TARIFF DATA 
    
    hourly_elect_tariff_loc = 'C:\\Optimization_zlc\\input_data\\load_only_storage_milp_input_data\\electricity_tariff\\highest_tariff.csv'
    hourly_elect_tariff_data = pd.read_csv(hourly_elect_tariff_loc)
    
    ##Artificial data
    pricing_structure_loc = 'C:\\Optimization_zlc\\input_data\\load_only_storage_milp_input_data\\electricity_tariff\\pricing_structure_fake.csv'
    pricing_structure_data = pd.read_csv(pricing_structure_loc)
    
    hourly_price = extract_elect_tariff (pricing_structure_data, hourly_elect_tariff_data)
    
    ###########################################################################
    ######################MASTER DECISION VARIABLES############################
    ###########################################################################
    
    master_dv = []
    
    ###########################################################################
    ###########PREPARING LOCAL VARIABLES FOR THE MILP FORMULATION##############
    ###########################################################################
    
    ##Saving the data into column defined time-step
    convert_mdv_to_slave_param_v3 (thread_number, master_dv, demand, temp_wb, hourly_price, piecewise_steps, time_steps)
    
    ##Determining the weights for the objective function
#    o1 = 0.9
#    o2 = 1 - o1
#    obj_weights = [o1, o2]
    
    ###########################################################################
    ##########################CHOOSING THE SOLVER##############################
    ###########################################################################    
    
    ##glpk or gurobi
    solver_choice = 'gurobi'

    ###########################################################################
    ##################CALLING THE MAIN FILE FOR MODELS#########################
    ###########################################################################
   
    obj_value, results, results_y, ind_obj_value, obj_func_table_dict = cvx_prog_run(thread_number, bilinear_pieces, solver_choice, time_steps, obj_weights)
    
    if process_method == 'serial':    
        print('Current iteration : ' + str(curr_run))
        print('Weighted objective function value: ', obj_value)
        print('Objective function value info:', ind_obj_value)

    ##Saving the results to csv format
    results.to_csv('C:\\Optimization_zlc\\control_center\\load_only_storage_milp\\results_store\\results_output_run_' + str(curr_run) + '.csv')
    results_y.to_csv('C:\\Optimization_zlc\\control_center\\load_only_storage_milp\\results_store\\results_y_output_run_' + str(curr_run) + '.csv')    
    ind_obj_value.to_csv('C:\\Optimization_zlc\\control_center\\load_only_storage_milp\\results_store\\ind_obj_value_run_' + str(curr_run) + '.csv')
    obj_func_table_dict['power'].to_csv('C:\\Optimization_zlc\\control_center\\load_only_storage_milp\\results_store\\obj1_power_table_output_' + str(curr_run) + '.csv')
    obj_func_table_dict['operation_cost'].to_csv('C:\\Optimization_zlc\\control_center\\load_only_storage_milp\\results_store\\obj2_operation_cost_table_output_' + str(curr_run) + '.csv')    

    if process_method == 'serial':  
        print('Current runtime: ', datetime.now() - startTime) 
    
    return ind_obj_value, obj_value

#########################################################################################################################################################################
##Auxillary functions

##Serial implementation    
def run_serial (iterations, max_weight, num_obj_funcs, objective_function_list, process_method):  
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import time
    
    ##iterations --- the required number of iterations 
    ##max_weight --- the maximum weight value of the objective function 
    ##num_obj_funcs --- the number of objective functions 
    ##objective_function_list --- the list of objective function names
    
    ##Calculating the step size
    weight_step = max_weight/iterations
    
    ##Creating a dataframe to store the final results 
    final_data_store_columns = []
    
    for i in range (0, num_obj_funcs):
        final_data_store_columns.append(objective_function_list[i] + '_Value')
        final_data_store_columns.append(objective_function_list[i] + '_Weight')    

    final_data_store_columns.append('Rep_obj_value')
    final_data_store = pd.DataFrame(columns = final_data_store_columns)
    
    ##Setting up the dynamic graph 
    x_gen = []
    y_gen = []
    plt.show()
    axes = plt.gca()
    
    ##Artificial thread number 
    thread_num = 10020123213
    
    
    for i in range (0, (iterations + 1)):
        o1 = i * weight_step 
        o2 = 1 - o1
        obj_weights = [o1, o2]
        ind_obj_value, obj_value = slave_test_script(obj_weights, i, thread_num, process_method)
        
        temp_data = []
        for j in range (0, num_obj_funcs):
            temp_data.append(ind_obj_value['Value'][j])
            temp_data.append(ind_obj_value['Weight'][j]) 
        temp_data.append(obj_value)         
        temp_df = pd.DataFrame(data = [temp_data], columns = final_data_store_columns)
        final_data_store = final_data_store.append(temp_df, ignore_index = True)
        
        ##Dynamic plotting
        x_gen.append(ind_obj_value['Value'][0])
        y_gen.append(ind_obj_value['Value'][1])
        ##Dynamic axes
        axes.clear()
        line, = axes.plot(x_gen, y_gen, 'b*')
        plt.title('Multi-Objective Pareto Frontier')
        plt.xlabel('Power (kWh)')
        plt.ylabel('Operation Cost (\u20ac)')            
        axes.set_xlim(0.9 * min(x_gen), 1.1 * max(x_gen))
        axes.set_ylim(0.9 * min(y_gen), 1.1 * max(y_gen))    
        line.set_xdata(x_gen)
        line.set_ydata(y_gen)
        curr_msg = 'Current iteration: \n' + str(i) + ' of ' + str(iterations)
        plt.text(0.7, 0.9, curr_msg, horizontalalignment='center', verticalalignment='center', transform = axes.transAxes)
        plt.draw()
        plt.pause(1e-17)
        time.sleep(0.1)
    
    plt.show()
    
    return final_data_store

##Parallel implementation 
def run_parallel (iterations, max_weight, num_cores, num_obj_funcs, objective_function_list):
    
    import pandas as pd
    import matplotlib.pyplot as plt
    import multiprocessing as mp
    import numpy as np
    
    ##Processing input data into a location accessible by all cores
    num_calc_list = prep_run_parallel (iterations, max_weight, num_obj_funcs)
    
    ##Creating a dataframe to store the final results 
    final_data_store_columns = []
    
    for i in range (0, num_obj_funcs):
        final_data_store_columns.append(objective_function_list[i] + '_Value')
        final_data_store_columns.append(objective_function_list[i] + '_Weight')    
    final_data_store_columns.append('Rep_obj_value')
    final_data_store = pd.DataFrame(columns = final_data_store_columns)
    
    ##Determining the number of cores to be used
    if (num_cores < mp.cpu_count()) and (num_cores >= 1):    
        p = mp.Pool(num_cores)
        ret_values = p.map(execute_parallel_ind_run, num_calc_list)
        p.close()
        p.join()
    
        ret_values = np.array(ret_values)   
        
    else:
        p = mp.Pool()
        ret_values = p.map(execute_parallel_ind_run, num_calc_list)
        p.close()
        p.join()
    
        ret_values = np.array(ret_values)    
        
    print(ret_values)
    
    
    ##Assembling the computed data into a dataframe 
    
    for i in range (0, iterations):
        current_column = 0
        temp_data = []
        for j in range (0, num_obj_funcs):
            temp_data.append(ret_values[i, current_column])
            current_column = current_column + 1
            temp_data.append(ret_values[i, current_column])
            current_column = current_column + 1
            
        temp_data.append(ret_values[i, current_column])
            
        temp_df = pd.DataFrame(data = [temp_data], columns = final_data_store_columns)
        final_data_store = final_data_store.append(temp_df, ignore_index = True)
        
    ##Plotting the data 
    
    fig = plt.figure()
    
    plt.scatter(final_data_store[objective_function_list[0] + '_Value'], final_data_store[objective_function_list[1] + '_Value'])
    
    plt.title('Multi-Objective Pareto Frontier')
    plt.xlabel('Power (kWh)')
    plt.ylabel('Operation Cost (\u20ac)') 
    
    plt.show()
        
    return final_data_store 

##A function to prepare the data for parallel implementation 
def prep_run_parallel (iterations, max_weight, num_obj_funcs):

    import pandas as pd 
    
    ##Calculating the step size
    weight_step = max_weight/iterations
    
    ##Determining a file to hold the input values for parallel processing
    file_loc = 'C:\\Optimization_zlc\\control_center\\load_only_storage_milp\\parallel_processing_working_folder\\input_data.csv'
    ##Initiating a dataframe 
    input_data_columns = []
    
    for i in range (0, num_obj_funcs):
        header = 'obj_weight_' + str(i)
        input_data_columns.append(header)
    
    input_data_columns.append('curr_run')
    input_data_columns.append('thread_num') 
    
    ##Initializing an empty dataframe for holding all input values for the iterations 
    input_data = pd.DataFrame(columns = input_data_columns) 
    
    ##Assuming 2 objective functions only
    for i in range (0, (iterations + 1)):
        o1 = i * weight_step 
        o2 = 1 - o1
        
        temp_data = [o1, o2, i, i+10000]
        temp_df = pd.DataFrame(data = [temp_data], columns = input_data_columns)
        input_data = input_data.append(temp_df, ignore_index = True)
        
    input_data.to_csv(file_loc)
    
    ##Preparing a list as input to the processing function 
    num_calc_list = []
    for i in range (0, (iterations + 1)):
        num_calc_list.append(i)
    
    return num_calc_list

##A function to execute the parallel implementation 
def execute_parallel_ind_run (id_number):
    
    import pandas as pd 
    
    ##id_number --- important for extracting the right input data 
    
    process_method = 'parallel'
    
    ##First, extract the relevant information 
    input_data_loc = 'C:\\Optimization_zlc\\control_center\\load_only_storage_milp\\parallel_processing_working_folder\\input_data.csv'
    input_data = pd.read_csv(input_data_loc)
    
    obj_weights = [input_data['obj_weight_0'][id_number], input_data['obj_weight_1'][id_number]]
    curr_run = input_data['curr_run'][id_number]
    thread_num = input_data['thread_num'][id_number]
    
    ind_obj_value, obj_value = slave_test_script(obj_weights, curr_run, thread_num, process_method)
    
    ##For parallel processing, the return values are only possible in the form of an array 
    
    dim_ind_obj_value = ind_obj_value.shape
    
    ret_values_arr = []
    
    for i in range (0, dim_ind_obj_value[0]):
        ret_values_arr.append(ind_obj_value['Value'][i])    
        ret_values_arr.append(ind_obj_value['Weight'][i])    

    ret_values_arr.append(obj_value)        
        
    return ret_values_arr
    

#############################################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    
    iterations = 2
    max_weight = 1
    num_obj_funcs = 2                                                           ##The number of objective functions
    objective_function_list = ['power', 'operation_cost']
    
    ##Determining computation method - serial or parallel 
    process_method = 'serial'                 
    num_cores = 8
    
    if process_method == 'serial':
        final_data_store = run_serial (iterations, max_weight, num_obj_funcs, objective_function_list, process_method)
        print(final_data_store)
        final_data_store.to_csv('C:\\Optimization_zlc\\control_center\\load_only_storage_milp\\moo_results.csv')
        
        
    elif process_method == 'parallel':
        run_parallel (iterations, max_weight, num_cores, num_obj_funcs, objective_function_list)
        print(final_data_store)
        final_data_store.to_csv('C:\\Optimization_zlc\\control_center\\load_only_storage_milp\\moo_results.csv')