##This function converts the list of variable information  

def nsga_ii_para_imple_conv_info (input_v):
    
    ##input_v['population']                     ---     population
    ##input_v['generations']                    ---     generations
    ##input_v['num_obj_func']                   ---     num_obj_func    
    ##input_v['selection_choice_data']          ---     selection_choice_data
    ##input_v['crossover_perc']                 ---     crossover_perc
    ##input_v['mutation_distribution_index']    ---     mutation_distribution_index
    ##input_v['mutation_perc']                  ---     mutation_perc
    ##input_v['crossover_distribution_index']   ---     crossover_distribution_index    
    ##input_v['variable_list']                  ---     variable_list
    ##input_v['initial_variable_values']        ---     initial_variable_values
    ##input_v['parallel_process']               ---     parallel_process
    ##input_v['obj_func_plot']                  ---     obj_func_plot
    ##input_v['cores_used']                     ---     cores_used      
    ##input_v['objAll']                         ---     []
    ##input_v['xAll']                           ---     []
    ##input_v['M']                              ---     number of objective functions
    ##input_v['V']                              ---     number of decision variables      
    
    import pandas as pd
    
    ##variable_list --- the list of variables and their corresponding properties 
    
    dim_variable_list = input_v['variable_list'].shape 
    
    ##Initializing a return variable list, with information about the binary conversion process
        ##Interval --- the number of discrete steps between the upper bound and lower bound based on the precision
    ret_var_list = pd.DataFrame(columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Interval', 'Dec_prec'])

    
    for i in range (0, dim_variable_list[0]):
        
        if input_v['variable_list']['Type'][i] == 'continuous':
            ##Rounding the upper and lower bounds to the predefined number of decimal places 
            round_lower_bound = round(input_v['variable_list']['Lower_bound'][i], input_v['variable_list']['Dec_prec'][i])
            round_upper_bound = round(input_v['variable_list']['Upper_bound'][i], input_v['variable_list']['Dec_prec'][i])
            ##Finding the number of discrete steps between the upper and lower bounds based on the predefined precision 
            discrete_steps = (round_upper_bound * pow(10, input_v['variable_list']['Dec_prec'][i])) - (round_lower_bound * pow(10, input_v['variable_list']['Dec_prec'][i]))
            
            temp_data = [input_v['variable_list']['Name'][i], input_v['variable_list']['Type'][i], round_lower_bound, round_upper_bound,
                         discrete_steps, input_v['variable_list']['Dec_prec'][i]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Interval', 'Dec_prec'])
            ret_var_list = ret_var_list.append(temp_df, ignore_index = True)
    
            
        elif input_v['variable_list']['Type'][i] == 'binary':
            ##Establishing the lower and upper bounds for the variable
            lower_bound = 0 
            upper_bound = 1
            ##Finding the number of discrete steps between the upper and lower bounds 
            discrete_steps = upper_bound - lower_bound 
            
            temp_data = [input_v['variable_list']['Name'][i], input_v['variable_list']['Type'][i], lower_bound, upper_bound, discrete_steps, input_v['variable_list']['Dec_prec'][i]]
 
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Interval', 'Dec_prec'])
            ret_var_list = ret_var_list.append(temp_df, ignore_index = True)            

        elif input_v['variable_list']['Type'][i] == 'discrete':
            ##Finding the discrete steps which should already been predefined 
            discrete_steps = input_v['variable_list']['Steps'][i]
            
            temp_data = [input_v['variable_list']['Name'][i], input_v['variable_list']['Type'][i], input_v['variable_list']['Lower_bound'][i], 
                         input_v['variable_list']['Upper_bound'][i], discrete_steps, input_v['variable_list']['Dec_prec'][i]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Interval', 'Dec_prec'])
            ret_var_list = ret_var_list.append(temp_df, ignore_index = True)
            
    return ret_var_list