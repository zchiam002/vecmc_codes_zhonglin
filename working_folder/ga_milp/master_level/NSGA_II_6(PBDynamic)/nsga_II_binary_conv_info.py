##This function converts the list of gets information about the binary conversion needed 

def nsga_II_binary_conv_info (variable_list):
    
    import pandas as pd
    import math 
    
    ##variable_list --- the list of variables and their corresponding properties 
    
    dim_variable_list = variable_list.shape 
    
    ##Initializing a return variable list, with information about the binary conversion process
    ret_var_list = pd.DataFrame(columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps', 'Bits', 'Bin_sz'])

    
    for i in range (0, dim_variable_list[0]):
        
        if variable_list['Type'][i] == 'continuous':
            ##Getting an estimate of the lower bound when converted to whole numbers 
            lb_est = variable_list['Lower_bound'][i] * pow(10, variable_list['Bin_dec_prec'][i])
            ##Getting an estimate of the upper bound when converted to whole numbers 
            ul_est = variable_list['Upper_bound'][i] * pow(10, variable_list['Bin_dec_prec'][i])
            ##Normalization of the difference to base 0
            norm_est = ul_est - lb_est 
            ##Finding the closest binary power to make the exact binary approximation 
            closest_pow = math.log10(norm_est) / math.log10(2)
            ##Rounding the closest_pow up to the nearest integer, this will be the number of bits required
            closest_pow_int = math.ceil(closest_pow)
            
            temp_data = [variable_list['Name'][i], variable_list['Type'][i], variable_list['Lower_bound'][i], variable_list['Upper_bound'][i],
                         variable_list['Bin_dec_prec'][i], variable_list['Steps'][i], closest_pow_int, '-']
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps', 'Bits', 'Bin_sz'])
            ret_var_list = ret_var_list.append(temp_df, ignore_index = True)
            
        elif variable_list['Type'][i] == 'binary':
            ##This is straight forward, we only need 1 bit for this 
            closest_pow_int = 1
            
            temp_data = [variable_list['Name'][i], variable_list['Type'][i], variable_list['Lower_bound'][i], variable_list['Upper_bound'][i],
                         variable_list['Bin_dec_prec'][i], variable_list['Steps'][i], closest_pow_int, '-']
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps', 'Bits', 'Bin_sz'])
            ret_var_list = ret_var_list.append(temp_df, ignore_index = True)

        elif variable_list['Type'][i] == 'discrete':
            ##Getting an estimate for the upper bound of binary power on steps when converted to the nearest whole number 
            closest_pow = math.log10(variable_list['Steps'][i]) / math.log10(2)
            closest_pow_int = math.ceil(closest_pow)
            ##Forming the bin sizes
            bin_sz = (pow(2, closest_pow_int) - 1) / variable_list['Steps'][i]
            
            temp_data = [variable_list['Name'][i], variable_list['Type'][i], variable_list['Lower_bound'][i], variable_list['Upper_bound'][i],
                         variable_list['Bin_dec_prec'][i], variable_list['Steps'][i], closest_pow_int, bin_sz]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Name', 'Type', 'Lower_bound', 'Upper_bound', 'Bin_dec_prec','Steps', 'Bits', 'Bin_sz'])
            ret_var_list = ret_var_list.append(temp_df, ignore_index = True)      
    
    return ret_var_list