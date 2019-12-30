##This function initializes the chromosomes. Each chromosome has the followith at this stage
##      *set of decision variables 
##      *objective function values 
##where,
##N - Population size
##M - Number of objective functions
##V - Number of decision variables
##min_range - A vector of decimal values which indicate the minimum value
##for each decision variable.
##max_range - Vector of maximum possible values for decision variables.

def initialize_variables(input_v,activate_parallel,num_cores,bin_info_variable_list):
    from evaluate_objective import evaluate_objective 
    from random import uniform
    import numpy as np
    from multiprocessing import Pool,cpu_count

    #import copy
    import random
    #from multiprocessing import Pool,cpu_count
    N = input_v['population']
    M = input_v['M']
    V = input_v['V']

    mini = input_v['min_range']
    maxi = input_v['max_range']

    K = M + V
    my_list = []

    ##Initialize each chromosome 
    f_obj = np.zeros((N,M))             ##To only contain objective function values 
    f_x = np.zeros((N,V))               ##To contain only variables
    
    num_calcs = N
    dim_variable_list = bin_info_variable_list.shape
    total_bin_str_len = sum(bin_info_variable_list['Bits'][:])
    
    ##The last row will host the objective function value
    ret_values_bin = np.zeros((num_calcs, total_bin_str_len))
    #ret_values_dec = np.zeros((num_calcs, dim_variable_list[0]))
    
    
    ##The total number of possible combinations based on string length 
    total_comb = pow(2, total_bin_str_len)
    
    ##Generating random integer numbers between 0, total_comb - 1, as many times as required
    ##This function ensures no duplicates
    if total_bin_str_len <= 64:
        random_num_list = random.sample(range(total_comb), num_calcs)
    ##Too many integers to handle, it is difficult for the program
    else:
        random_num_list = []
        for i in range (0, num_calcs):
            temp_select = int((random.uniform(0,1)) * total_comb)
            random_num_list.append(temp_select)
    
    ##Converting to the corresponding binary string 
    my_list = []
    if activate_parallel == 'yes':
        #evaluate_objective.counter = 1
        for i in range(0, num_calcs):
            bin_temp_str = "{0:b}".format(random_num_list[i])
            ##Determining the length of the string 
            len_bin_temp_str = len(bin_temp_str)
            ##Finding the number of 0s preceeding the real values 
            preceding_zeros = total_bin_str_len - len_bin_temp_str
            
            ##Filling up the return array
            
            ##Filling up the zeros first
            current_index = 0
            for j in range (0, preceding_zeros):
                ret_values_bin[i, j] = 0
                current_index = current_index + 1
                
            ##Filling up the values of the strings
            for k in range (0, len_bin_temp_str):
                ret_values_bin[i, current_index] = int(bin_temp_str[k])
                current_index = current_index + 1
                
            ##Now that the strings are filled with binary, it is time to process the values as input values (decimal)
                ##To do that it is important to know the length of the string 
            
            ##Setting up a temporary array to deal with the function 
            bin_and_empty_obj_func = ret_values_bin[i, :] 
            
            ##Converting the randomly chosen binary values to decimal         
            dec_values = conv_from_binary (bin_info_variable_list, bin_and_empty_obj_func, dim_variable_list[0])
            
            f_x[i,:] = dec_values
            my_list.append((f_x[i,:],input_v,1))
            
            ##For ease of computation and handling data the chromosome also has the value of the objective
            ##function concatenated at the end. The elements V + 1 to K has the objective function values.
            ##The function evaluate_objective takes one chromosome at a time, infact only the decision variables 
            ##are passed to the function along with information about the number of objective functions which are 
            ##processed and returns the value for the objective functions. These values are now stored at the end 
            ##of the chromosome itself.
        #print(*my_list)
        if (num_cores < cpu_count()) and (num_cores >= 1):
            
            p = Pool(num_cores)
            
        else:
            p = Pool()
        
        results = p.starmap(evaluate_objective, my_list)
        p.close()
        p.join()
        for i in range (0,N):
          f_obj[i,:] = results[i]  
            
        input_v['objAll'] = f_obj
        input_v['xAll'] = f_x
        input_v['xAll_binary'] = ret_values_bin
    
        f_all = np.concatenate((f_x, f_obj), axis=1) 
        return f_all, input_v

    else:
        #evaluate_objective.counter = 0 #series unique
        for i in range(0, num_calcs):
            bin_temp_str = "{0:b}".format(random_num_list[i])
            ##Determining the length of the string 
            len_bin_temp_str = len(bin_temp_str)
            ##Finding the number of 0s preceeding the real values 
            preceding_zeros = total_bin_str_len - len_bin_temp_str
            
            ##Filling up the return array
            
            ##Filling up the zeros first
            current_index = 0
            for j in range (0, preceding_zeros):
                ret_values_bin[i, j] = 0
                current_index = current_index + 1
                
            ##Filling up the values of the strings
            for k in range (0, len_bin_temp_str):
                ret_values_bin[i, current_index] = int(bin_temp_str[k])
                current_index = current_index + 1
                
            ##Now that the strings are filled with binary, it is time to process the values as input values (decimal)
                ##To do that it is important to know the length of the string 
            
            ##Setting up a temporary array to deal with the function 
            bin_and_empty_obj_func = ret_values_bin[i, :] 
            
            ##Converting the randomly chosen binary values to decimal         
            dec_values = conv_from_binary (bin_info_variable_list, bin_and_empty_obj_func, dim_variable_list[0])
            
            f_x[i,:] = dec_values
            f_obj[i,:] = evaluate_objective(f_x[i,:], input_v,0)
            number = i + 1
            display_message = 'Initializing population ' + str(number) + ' of ' + str(N)
            print(display_message)
            
        input_v['objAll'] = f_obj
        input_v['xAll'] = f_x
        input_v['xAll_binary'] = ret_values_bin
    
        f_all = np.concatenate((f_x, f_obj), axis=1) 
        return f_all, input_v


#    for i in range (0, N):
        ##Initialize the decision variables based on the minimum and the maximum possible values.
        ##V is the number of decision variables. A random number is picked between the minimum and 
        ##maximum possible values for each decision variable.
            
 #       for j in range (0, V):
  #          f_x[i,j] = mini[j] + ((maxi[j] - mini[j])*uniform(0,1))
        
        ##For ease of computation and handling data the chromosome also has the value of the objective
        ##function concatenated at the end. The elements V + 1 to K has the objective function values.
        ##The function evaluate_objective takes one chromosome at a time, infact only the decision variables 
        ##are passed to the function along with information about the number of objective functions which are 
        ##processed and returns the value for the objective functions. These values are now stored at the end 
        ##of the chromosome itself.
        
   #     f_obj[i,:] = evaluate_objective(f_x[i,:], input_v)
    #    number = i + 1
     #   display_message = 'Initializing population ' + str(number) + ' of ' + str(N)
      #  print(display_message)

     
 #   input_v['objAll'] = f_obj
  #  input_v['xAll'] = f_x

   # f_all = np.concatenate((f_x, f_obj), axis=1)       
    
    #return f_all, input_v


##Defining a function to convert the binary string into values for the evaluate function 
def conv_from_binary (bin_info_variable_list, bin_and_empty_obj_func, num_var):
    
    ##bin_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes
    ##bin_and_empty_obj_func --- a array with a binary string and an empty column for the objective function 
    ##num_var --- the number of variables 
    
    ##Creating a temporary array to hold the return values
    ret_dec_vals = []
    
    ##Determining the values variables
    current_position = 0
    for i in range (0, num_var):
        
        if bin_info_variable_list['Type'][i] == 'continuous':
            lb_bits = current_position
            ub_bits = current_position + bin_info_variable_list['Bits'][i]
            
            ##Initialize an empty string to hold the values 
            string_bits = ''
            string_ul = ''              ##The upperlimit on the strings 
            
            for j in range (lb_bits, ub_bits):
                string_bits = string_bits + str(int(bin_and_empty_obj_func[j]))
                string_ul = string_ul + str(1)
                
            ##Converting the strings to decimal 
            temp_value = int(string_bits, 2)
            max_value = int(string_ul, 2) 
            ##The ratio of the max and min  
            temp_upper_bound = float(bin_info_variable_list['Upper_bound'][i])            
            temp_lower_bound = float(bin_info_variable_list['Lower_bound'][i])           
            dec_value = ((temp_value / (max_value-1)) * (temp_upper_bound - temp_lower_bound)) + temp_lower_bound
            ##Appending the final return list 
            ret_dec_vals.append(dec_value)
            ##Updating the current_value
            current_position = ub_bits
    
        elif bin_info_variable_list['Type'][i] == 'binary':
            ret_dec_vals.append(bin_and_empty_obj_func[current_position])
            current_position = current_position + 1
            
        elif bin_info_variable_list['Type'][i] == 'discrete':
            
            ##Establishing the number of bins
            num_bins = int(bin_info_variable_list['Steps'][i])
            ##Establishing the bin size 
            bin_sz = float(bin_info_variable_list['Bin_sz'][i])
            
            ##Determining the value of the binary choice 
            lb_bits = current_position 
            ub_bits = current_position + bin_info_variable_list['Bits'][i]

            ##Initialize an empty string to hold the values 
            string_bits = ''
            
            for j in range (lb_bits, ub_bits):
                string_bits = string_bits + str(int(bin_and_empty_obj_func[j]))
                
            ##Converting the strings to decimal 
            temp_value = int(string_bits, 2)     
            
            ##Establishing which bin the number is allocated to 
            for j in range (0, num_bins):
                bin_lb = j * bin_sz
                bin_ub = (j + 1) * bin_sz
                if (temp_value >= bin_lb) and (temp_value <= bin_ub):
                    allocated_bin = j
                    break
                
            temp_upper_bound = float(bin_info_variable_list['Upper_bound'][i])            
            temp_lower_bound = float(bin_info_variable_list['Lower_bound'][i])   
                
            dec_value = ((allocated_bin / (num_bins-1)) * (temp_upper_bound - temp_lower_bound)) + temp_lower_bound

            ret_dec_vals.append(dec_value)
            ##Updating the current_value
            current_position = ub_bits 
            
    return ret_dec_vals
##Copyright (c) 2009, Aravind Seshadri
##All rights reserved.

##Redistribution and use in source and binary forms, with or without  modification, are permitted provided that the following 
##conditions are met:

##   * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
##   * Mohit - Binary conversion(A diffeent one sugggested)See the optimization framework on the thesis
##   * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer 
##     in the documentation and/or other materials provided with the distribution
##     
##THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT 
##NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
##THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
##(INCLUDING, Mohit Gupta BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
##HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
##ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.