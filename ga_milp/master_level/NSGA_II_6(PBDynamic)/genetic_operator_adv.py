##This script contains functions to perform the crossover process
import numpy as np 
import copy 
from random import uniform
import math
from evaluate_objective import evaluate_objective 
from multiprocessing import Pool,cpu_count

def cross_mutation(parent_pool,mutation_prob,input_v,bin_info_variable_list,parents_array,split,dim_variable_list):
    ##parent_pool --- the selected chromosomes for crossover purposes, by standard convention 
        ##last column --- fitness value 
        ##2nd last column --- objective function 
    ##crossover duty --- the number of child chromosomes needed 
    
    dim_parent_pool = parent_pool.shape
    ##Determine the total number of combinations possible 
    total_binary_len = dim_parent_pool[1] - input_v['M'] - 2
    ##Initialize an array containing a list of parents

    ##Performing the crossover 

        ##Copying the array for manipulations
    if uniform(0,1) < 0.9:
        parents_array_copied = copy.copy(parents_array)
        
        ##Selecting parent 1 
        parent1_index = np.random.choice(parents_array_copied)
        ##Removing parent 1 index from the choices 
        parents_array_copied.remove(parents_array_copied[parent1_index])
        ##Selecting parent 2
        parent2_index = np.random.choice(parents_array_copied)
        
        ##Selecting the crossover point 
        crossover_point = np.random.choice(split)
        
        ##Copying the parents array 
        parent1 = parent_pool[parent1_index, :(- input_v['M'] - 2)]
        parent2 = parent_pool[parent2_index, :(- input_v['M'] - 2)]
        
        ##Forming the child arrays 
        child_p1 = parent1[0:crossover_point]
        child_p2 = parent2[crossover_point:total_binary_len]

        child2_p1 = parent2[0:crossover_point]
        child2_p2 = parent1[crossover_point:total_binary_len]
        
        child_1 = np.append(child_p1, child_p2)
        child_2 = np.append(child2_p1, child2_p2)
        
        dec_child_1 = conv_from_binary (bin_info_variable_list, np.ndarray.flatten(child_1), dim_variable_list[0])
        dec_child_2 = conv_from_binary (bin_info_variable_list,np.ndarray.flatten(child_2), dim_variable_list[0])
        
#            input_v['xAll'] = np.concatenate((input_v['xAll'] , [dec_child_1]), axis=0)
        x11 = [dec_child_1.copy(),dec_child_2.copy()]
        child_1_obj = evaluate_objective(dec_child_1, input_v,1)
#            input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_1_obj), axis=0)
        
 #           input_v['xAll'] = np.concatenate((input_v['xAll'] ,[dec_child_2]), axis=0)
        child_2_obj = evaluate_objective(dec_child_2, input_v,1)
  #          input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_2_obj), axis=0)
        xobj11 = [child_1_obj.copy(),child_2_obj.copy()]
        child_1_obj = np.ndarray.flatten(child_1_obj)
        for k in range(0, len(child_1_obj)):
            dec_child_1.append(child_1_obj[k])
        
        child_2_obj = np.ndarray.flatten(child_2_obj)
        for k in range(0, len(child_2_obj)):
            dec_child_2.append(child_2_obj[k])
            
        ##Set the crossover flag. When corssover is performaed two children are generated, conversely, when mutation is
        ##only performed only after the children are generated 
        was_crossover = 1
        was_mutation = 0

 
        ##Empty columns for the fitness values and the objective function
        #child_1 = np.append(child_1, [0, 0, 0])        
        #child_2 = np.append(child_2, [0, 0, 0])
        
    else:
        #combined_pool = parent_pool

        ##Determining the total number of bits
        bit_len = total_binary_len                  ##The last 2 columns are for the objective function and the fitness respectively 
        mutation_perc = uniform(0,1)
        if mutation_perc <0.5 :
            mutation_perc = 0.5
        bits_to_mutate = math.ceil(mutation_perc * bit_len)
        
        ##Making a copy of the combined_pool
        child_3 = np.copy(parent_pool)
        row = np.random.choice(range(dim_parent_pool[0]))
        columns = np.random.choice(range(dim_parent_pool[1] - input_v['M'] - 2), bits_to_mutate, p = mutation_prob)
        
        
        for ik in range (0, bits_to_mutate):
        
           #column = np.random.choice(range(dim_combined_pool[1] - 3), p = mutation_prob)
           if int(child_3[row, columns[ik]]) == 0:
               child_3[row, columns[ik]] = 1
           else:
               child_3[row, columns[ik]] = 0
               
        dec_child_3 = conv_from_binary (bin_info_variable_list, np.ndarray.flatten(child_3), dim_variable_list[0])

        #input_v['xAll'] = np.concatenate((input_v['xAll'] ,[dec_child_3]), axis=0)
        x11 = [dec_child_3.copy()]
        child_3_obj = evaluate_objective(dec_child_3, input_v,1)
        #input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_3_obj), axis=0)
        xobj11 = [child_3_obj.copy()]
        child_3_obj = np.ndarray.flatten(child_3_obj)
        for k in range(0, len(child_3_obj)):
            dec_child_3.append(child_3_obj[k])
        
        ##Set the mutation flag 
        was_mutation = 1
        was_crossover = 0 
               
    if was_crossover == 1:
        return ([dec_child_1,dec_child_2],x11,xobj11)
        was_crossover = 0
    elif was_mutation == 1:
        return ([dec_child_3],x11,xobj11)
  

def genetic_operator_adv(parent_pool,mutation_prob,input_v,bin_info_variable_list,activate_parallel,num_cores):
    ##parent_pool --- the selected chromosomes for crossover purposes, by standard convention 
        ##last column --- fitness value 
        ##2nd last column --- objective function 
    ##crossover duty --- the number of child chromosomes needed 
    
    dim_parent_pool = parent_pool.shape
    ##Determine the total number of combinations possible 
    total_binary_len = dim_parent_pool[1] - input_v['M'] - 2
    ##Initialize an array containing a list of parents
    parents_array = []
    for i in range (0, dim_parent_pool[0]):
        parents_array.append(i)
    ##Initialize an array for the possible split points 
    split = []
    for i in range (1, total_binary_len - 1):
        split.append(i)
    dim_variable_list = bin_info_variable_list.shape

    ##Performing the crossover 
    if activate_parallel == 'yes':
       # for i in range (0, dim_parent_pool[0]):
            ##Copying the array for manipulations
        if uniform(0,1) < 0.9:
            parents_array_copied = copy.copy(parents_array)
            
            ##Selecting parent 1 
            parent1_index = np.random.choice(parents_array_copied)
            ##Removing parent 1 index from the choices 
            parents_array_copied.remove(parents_array_copied[parent1_index])
            ##Selecting parent 2
            parent2_index = np.random.choice(parents_array_copied)
            
            ##Selecting the crossover point 
            crossover_point = np.random.choice(split)
            
            ##Copying the parents array 
            parent1 = parent_pool[parent1_index, :(- input_v['M'] - 2)]
            parent2 = parent_pool[parent2_index, :(- input_v['M'] - 2)]
            
            ##Forming the child arrays 
            child_p1 = parent1[0:crossover_point]
            child_p2 = parent2[crossover_point:total_binary_len]

            child2_p1 = parent2[0:crossover_point]
            child2_p2 = parent1[crossover_point:total_binary_len]
            
            child_1 = np.append(child_p1, child_p2)
            child_2 = np.append(child2_p1, child2_p2)
            
            dec_child_1 = conv_from_binary (bin_info_variable_list, np.ndarray.flatten(child_1), dim_variable_list[0])
            dec_child_2 = conv_from_binary (bin_info_variable_list,np.ndarray.flatten(child_2), dim_variable_list[0])
            
            input_v['xAll'] = np.concatenate((input_v['xAll'] , [dec_child_1]), axis=0)
            child_1_obj = evaluate_objective(dec_child_1, input_v,1)
            input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_1_obj), axis=0)
            
            input_v['xAll'] = np.concatenate((input_v['xAll'] ,[dec_child_2]), axis=0)
            child_2_obj = evaluate_objective(dec_child_2, input_v,1)
            input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_2_obj), axis=0)
            
            child_1_obj = np.ndarray.flatten(child_1_obj)
            for k in range(0, len(child_1_obj)):
                dec_child_1.append(child_1_obj[k])
            
            child_2_obj = np.ndarray.flatten(child_2_obj)
            for k in range(0, len(child_2_obj)):
                dec_child_2.append(child_2_obj[k])
                
            ##Set the crossover flag. When corssover is performaed two children are generated, conversely, when mutation is
            ##only performed only after the children are generated 
            was_crossover = 1
            was_mutation = 0
            
            ##Empty columns for the fitness values and the objective function
            #child_1 = np.append(child_1, [0, 0, 0])        
            #child_2 = np.append(child_2, [0, 0, 0])
            
        else:
            #combined_pool = parent_pool
    
            ##Determining the total number of bits 
            bit_len = total_binary_len                  ##The last 2 columns are for the objective function and the fitness respectively 
            mutation_perc = uniform(0,1)
            if mutation_perc <0.5 :
                mutation_perc = 0.5
            bits_to_mutate = math.ceil(mutation_perc * bit_len)
            
            ##Making a copy of the combined_pool
            child_3 = np.copy(parent_pool)
            row = np.random.choice(range(dim_parent_pool[0]))
            columns = np.random.choice(range(dim_parent_pool[1] - input_v['M'] - 2), bits_to_mutate, p = mutation_prob)
            
            
            for ik in range (0, bits_to_mutate):
            
               #column = np.random.choice(range(dim_combined_pool[1] - 3), p = mutation_prob)
               if int(child_3[row, columns[ik]]) == 0:
                   child_3[row, columns[ik]] = 1
               else:
                   child_3[row, columns[ik]] = 0
                   
            dec_child_3 = conv_from_binary (bin_info_variable_list, np.ndarray.flatten(child_3), dim_variable_list[0])
            input_v['xAll'] = np.concatenate((input_v['xAll'] ,[dec_child_3]), axis=0)
            child_3_obj = evaluate_objective(dec_child_3, input_v,1)
            input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_3_obj), axis=0)
    
            child_3_obj = np.ndarray.flatten(child_3_obj)
            for k in range(0, len(child_3_obj)):
                dec_child_3.append(child_3_obj[k])
            
            ##Set the mutation flag 
            was_mutation = 1
            was_crossover = 0 
                   

        if was_crossover == 1:
            child_ret = np.concatenate(([dec_child_1], [dec_child_2]), axis=0)
            was_crossover = 0
        elif was_mutation == 1:
            child_ret = np.array([dec_child_3])
            was_mutation = 0

        if (num_cores < cpu_count()) and (num_cores >= 1):
            
            p = Pool(num_cores)
            
        else:
            p = Pool()
        
        my_list = [(parent_pool,mutation_prob,input_v,bin_info_variable_list,parents_array,split,dim_variable_list)]*(dim_parent_pool[0]-1)

        result = p.starmap(cross_mutation, my_list)
        p.close()
        p.join()
        result1, result2,result3 = zip(*result)  

        flat_result1 = [item for sublist in result1 for item in sublist]
        child_ret = np.concatenate((flat_result1,child_ret),axis = 0)
        flat_result2 = [item for sublist in result2 for item in sublist]
        flat_result3 = [item for sublist in result3 for item in sublist]
        flat_result33 = [item for sublist in flat_result3 for item in sublist]
        input_v['xAll'] = np.concatenate((input_v['xAll'],flat_result2),axis = 0)
        input_v['objAll'] = np.concatenate((input_v['objAll'],flat_result33),axis = 0)

        #print(result)
        #print('\n\n\n\n\n')
        #print(flat_result2)
        #for w in range(0,len(flat_result3)):
            #print(flat_result2[w])
            #input_v['xAll'] = np.concatenate((input_v['xAll'] ,[flat_result2[w]]),axis = 0)
         #   input_v['objAll'] = np.concatenate((input_v['objAll'] ,flat_result3[w]),axis = 0)
      
      # print('after')
        
        return child_ret, input_v
    else:
        for i in range (0, dim_parent_pool[0]):
            ##Copying the array for manipulations
            if uniform(0,1) < 0.9:
                parents_array_copied = copy.copy(parents_array)
                
                ##Selecting parent 1 
                parent1_index = np.random.choice(parents_array_copied)
                ##Removing parent 1 index from the choices 
                parents_array_copied.remove(parents_array_copied[parent1_index])
                ##Selecting parent 2
                parent2_index = np.random.choice(parents_array_copied)
                
                ##Selecting the crossover point 
                crossover_point = np.random.choice(split)
                
                ##Copying the parents array 
                parent1 = parent_pool[parent1_index, :(- input_v['M'] - 2)]
                parent2 = parent_pool[parent2_index, :(- input_v['M'] - 2)]
                
                ##Forming the child arrays 
                child_p1 = parent1[0:crossover_point]
                child_p2 = parent2[crossover_point:total_binary_len]
    
                child2_p1 = parent2[0:crossover_point]
                child2_p2 = parent1[crossover_point:total_binary_len]
                
                child_1 = np.append(child_p1, child_p2)
                child_2 = np.append(child2_p1, child2_p2)
                
                dec_child_1 = conv_from_binary (bin_info_variable_list, np.ndarray.flatten(child_1), dim_variable_list[0])
                dec_child_2 = conv_from_binary (bin_info_variable_list,np.ndarray.flatten(child_2), dim_variable_list[0])
                
                input_v['xAll'] = np.concatenate((input_v['xAll'] , [dec_child_1]), axis=0)
                child_1_obj = evaluate_objective(dec_child_1, input_v,0)
                input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_1_obj), axis=0)
                
                input_v['xAll'] = np.concatenate((input_v['xAll'] ,[dec_child_2]), axis=0)
                child_2_obj = evaluate_objective(dec_child_2, input_v,0)
                input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_2_obj), axis=0)
                
                child_1_obj = np.ndarray.flatten(child_1_obj)
                for k in range(0, len(child_1_obj)):
                    dec_child_1.append(child_1_obj[k])
                
                child_2_obj = np.ndarray.flatten(child_2_obj)
                for k in range(0, len(child_2_obj)):
                    dec_child_2.append(child_2_obj[k])
                    
                ##Set the crossover flag. When corssover is performaed two children are generated, conversely, when mutation is
                ##only performed only after the children are generated 
                was_crossover = 1
                was_mutation = 0
        
     
                ##Empty columns for the fitness values and the objective function
                #child_1 = np.append(child_1, [0, 0, 0])        
                #child_2 = np.append(child_2, [0, 0, 0])
                
            else:
                #combined_pool = parent_pool
        
                ##Determining the total number of bits 
                bit_len = total_binary_len                  ##The last 2 columns are for the objective function and the fitness respectively 
                mutation_perc = uniform(0,1)
                if mutation_perc <0.5 :
                    mutation_perc = 0.5
                bits_to_mutate = math.ceil(mutation_perc * bit_len)
                
                ##Making a copy of the combined_pool
                child_3 = np.copy(parent_pool)
                row = np.random.choice(range(dim_parent_pool[0]))
                columns = np.random.choice(range(dim_parent_pool[1] - input_v['M'] - 2), bits_to_mutate, p = mutation_prob)
                
                
                for ik in range (0, bits_to_mutate):
                
                   #column = np.random.choice(range(dim_combined_pool[1] - 3), p = mutation_prob)
                   if int(child_3[row, columns[ik]]) == 0:
                       child_3[row, columns[ik]] = 1
                   else:
                       child_3[row, columns[ik]] = 0
                       
                dec_child_3 = conv_from_binary (bin_info_variable_list, np.ndarray.flatten(child_3), dim_variable_list[0])
    
                input_v['xAll'] = np.concatenate((input_v['xAll'] ,[dec_child_3]), axis=0)
                child_3_obj = evaluate_objective(dec_child_3, input_v,0)
                input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_3_obj), axis=0)
        
                child_3_obj = np.ndarray.flatten(child_3_obj)
                for k in range(0, len(child_3_obj)):
                    dec_child_3.append(child_3_obj[k])
                
                ##Set the mutation flag 
                was_mutation = 1
                was_crossover = 0 
                   
            if i == 0:
                if was_crossover == 1:
                    child_ret = np.concatenate(([dec_child_1], [dec_child_2]), axis=0)
                    was_crossover = 0
                elif was_mutation == 1:
                    child_ret = np.array([dec_child_3])
                    was_mutation = 0
            else:
                if was_crossover == 1:
                    child_ret = np.concatenate((child_ret, [dec_child_1]), axis=0)
                    child_ret = np.concatenate((child_ret, [dec_child_2]), axis=0)
                    was_crossover = 0
                elif was_mutation == 1:
                    child_ret = np.concatenate((child_ret, [dec_child_3]), axis=0)
      
    
        return child_ret,input_v

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
