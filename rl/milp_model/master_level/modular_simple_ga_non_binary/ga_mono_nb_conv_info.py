##This function converts the list of variable information  

def ga_mono_nb_conv_info (variable_list):
    
    import pandas as pd
    
    ##variable_list --- the list of variables and their corresponding properties 
    
    dim_variable_list = variable_list.shape 
    
    ##Initializing a return variable list, with information about the binary conversion process
        ##Interval --- the number of discrete steps between the upper bound and lower bound based on the precision
    ret_var_list = pd.DataFrame(columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Interval', 'Dec_prec'])

    
    for i in range (0, dim_variable_list[0]):
        
        if variable_list['Type'][i] == 'continuous':
            ##Rounding the upper and lower bounds to the predefined number of decimal places 
            round_lower_bound = round(variable_list['Lower_bound'][i], variable_list['Dec_prec'][i])
            round_upper_bound = round(variable_list['Upper_bound'][i], variable_list['Dec_prec'][i])
            ##Finding the number of discrete steps between the upper and lower bounds based on the predefined precision 
            discrete_steps = int((round_upper_bound * pow(10, variable_list['Dec_prec'][i])) - (round_lower_bound * pow(10, variable_list['Dec_prec'][i])))
            
            temp_data = [variable_list['Name'][i], variable_list['Type'][i], round_lower_bound, round_upper_bound,
                         discrete_steps, variable_list['Dec_prec'][i]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Interval', 'Dec_prec'])
            ret_var_list = ret_var_list.append(temp_df, ignore_index = True)
    
            
        elif variable_list['Type'][i] == 'binary':
            ##Establishing the lower and upper bounds for the variable
            lower_bound = 0 
            upper_bound = 1
            ##Finding the number of discrete steps between the upper and lower bounds 
            discrete_steps = int(upper_bound - lower_bound) 
            
            temp_data = [variable_list['Name'][i], variable_list['Type'][i], lower_bound, upper_bound, discrete_steps, variable_list['Dec_prec'][i]]
 
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Interval', 'Dec_prec'])
            ret_var_list = ret_var_list.append(temp_df, ignore_index = True)            

        elif variable_list['Type'][i] == 'discrete':
            ##Finding the discrete steps which should already been predefined 
            discrete_steps = int(variable_list['Steps'][i])
            
            temp_data = [variable_list['Name'][i], variable_list['Type'][i], variable_list['Lower_bound'][i], variable_list['Upper_bound'][i],
                         discrete_steps, variable_list['Dec_prec'][i]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Interval', 'Dec_prec'])
            ret_var_list = ret_var_list.append(temp_df, ignore_index = True)
            
    return ret_var_list