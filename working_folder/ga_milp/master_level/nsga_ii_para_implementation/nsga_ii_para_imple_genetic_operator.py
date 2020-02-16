##This function is utilized to produce offsprings from parent chromosomes. 
##The genetic operators corssover and mutation which are carried out with slight modifications from the original design. 
##For more information read the document enclosed. 

def nsga_ii_para_imple_genetic_operator(parent_chromosome, input_v):
    
    ##parent_chromosome     ---     the sorted population 
    
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
    ##input_v['variable_list_conv_info']        ---     a dataframe of the intervals based on each variable type 
    
    import numpy as np

    M = input_v['M']
    V = input_v['V'] 
    mu = input_v['crossover_distribution_index']
    mum = input_v['mutation_distribution_index'] 
    

    
    ##Checking for parallel processing 
    if input_v['parallel_process']  == 'no':
        iteration_num = 10001
        ##Determining limits for each variable and storing them in a list 
        l_limit, u_limit = create_variable_upper_lower_limits (input_v)
        
        child, input_v = serial_genetic_operator (parent_chromosome, M, V, mu, mum, l_limit, u_limit, input_v, iteration_num, input_v['variable_list_conv_info'],
                                                  input_v['mutation_perc'])
        
    else:
        ##Preparing the associated data for parallel pool processing 
        iter_list = prepare_para_process_input_genetic_operator (parent_chromosome, M, V, mu, mum, input_v['variable_list_conv_info'], input_v['mutation_perc'])
        
        import multiprocessing as mp 
        ##Determining the number of cores to be used 
        if (input_v['cores_used'] < mp.cpu_count()) and (input_v['cores_used'] >= 1):
    
            p = mp.Pool(input_v['cores_used'])
            ret_values_all = p.map(para_calc_indiv_genetic_operator, iter_list)
            p.close()
            p.join()
        
            ret_values_all = np.array(ret_values_all)    
    
        else:
            p = mp.Pool()
            ret_values_all = p.map(para_calc_indiv_genetic_operator, iter_list)
            p.close()
            p.join()
        
            ret_values_all = np.array(ret_values_all)  
            
        ##Post processing of all the outputs from parallel pools 
        child, input_v = post_process_para_indv_go (ret_values_all, V, M, input_v)
    
    return child, input_v

##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##Auxillary functions 
    
##This function processes the individual worker job for each parallel core 
def para_calc_indiv_genetic_operator (iteration):
    
    ##iteration     ---     the specific number to unlock information
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__))[:-40] + '\\'
    import sys
    sys.path.append(current_path + 'master_level\\nsga_ii_para_implementation\\auxillary_functions\\')
    from auxillary_functions_nsga_ii_para_imple import identical_array
    from nsga_ii_para_imple_evaluate_objective import nsga_ii_para_imple_evaluate_objective 
    import numpy as np
    from random import uniform
    
    ##First is to unpack all the important parameter values 
    parent_chromosome, M, V, mu, mum, variable_list_conv_info, mutation_perc, l_limit, u_limit = unpack_information_for_para_indiv ()   
    
    ##Running only one iteration 

    ##Determining the population size
    dim_parent_chromosome = parent_chromosome.shape
    N = dim_parent_chromosome[0]
    
    ##Flags wsed to set if crossover and mutation were actually performed 
    was_crossover = 0
    was_mutation = 0    

    ##With ~90% probability perform crossover 
    if uniform(0,1) < (1 - mutation_perc):
        ##Initialize the children to be null vectors 
        child_1 = []
        child_2 = []
        ##Select the first parent 
        parent_1 = int(round(((N-1)*uniform(0,1))))
        parent_2 = int(round(((N-1)*uniform(0,1))))
        
        ##Make sure that both parents are not the same 
        while identical_array(parent_chromosome[parent_1,:], parent_chromosome[parent_2,:]) == 1:
            parent_2 = int(round(((N-1)*uniform(0,1))))

        ##Get the chromosome information fro each randomly selected parents 
        parent_1 = parent_chromosome[parent_1]
        parent_2 = parent_chromosome[parent_2]
        
        ##Perform crossover for each decision variable in the chromosome
        u = []
        bq = []
        for j in range (0, V):
            ##SBX (Simulated Binary Crossover)
            ##For more information about SBX refer to the encolsed pdf file.
            ##Generate a random number 
            u.append(uniform(0,1))
            
            if u[j] <= 0.5:
                bq.append(pow((2*u[j]),(1/(mu + 1))))
            else:
                bq.append(pow((1/(2*(1-u[j]))),(1/(mu + 1))))
            
            ##Generate the jth element of the first child 
            child_1.append(0.5*(((1 + bq[j])*parent_1[j]) + ((1 - bq[j])*parent_2[j])))
            ##Generate the jth element of the second child 
            child_2.append(0.5*(((1 - bq[j])*parent_1[j]) + ((1 + bq[j])*parent_2[j])))
            ##Make sure that the generated element is within the specified decision space else set it to the appropriate 
            ##extrema
            if child_1[j] > u_limit[j]:
                child_1[j] = u_limit[j]

            elif child_1[j] < l_limit[j]:
                child_1[j] = l_limit[j]

            if child_2[j] > u_limit[j]:
                child_2[j] = u_limit[j]

            elif child_2[j] < l_limit[j]:
                child_2[j] = l_limit[j]

        ##Evaluate the objective function for the offsprings and as before concatenate the offspring chromosome with 
        ##objective value
        
        ##Fixing the variables according to predefined types and decimal points 
        child_1 = fix_variable_type_genetic_operator_serial(variable_list_conv_info, child_1)
        child_2 = fix_variable_type_genetic_operator_serial(variable_list_conv_info, child_1)
        
        child_1_obj = nsga_ii_para_imple_evaluate_objective(child_1, M, iteration)

        child_2_obj = nsga_ii_para_imple_evaluate_objective(child_2, M, iteration)
                
        ##Appending the objective functions at the end of the children
        child_1_obj = np.ndarray.flatten(child_1_obj)
        for k in range(0, len(child_1_obj)):
            child_1.append(child_1_obj[k])
        
        child_2_obj = np.ndarray.flatten(child_2_obj)
        for k in range(0, len(child_2_obj)):
            child_2.append(child_2_obj[k])
            
        ##Set the crossover flag. When corssover is performaed two children are generated, conversely, when mutation is
        ##only performed only after the children are generated 
        was_crossover = 1
        was_mutation = 0
    
    ##With ~10% probability perform mutation. Mutation is based on polynomial mutation 
    else:
        ##Select the parent at random 
        parent_3 = int(round(((N-1)*uniform(0,1))))
        
        ##Get the chromosome information for the randomly selected parent
        child_3 = []
        for j in range (0, V):
            child_3.append(parent_chromosome[parent_3, j])
        ##Perform mutation on each element of the selected parent 
        
        r = []
        delta = []
        for j in range (0, V):
            r.append(uniform(0,1))
            if r[j] < 0.5:
                delta.append((pow((2*r[j]), (1/(mum+1)))) - 1)
            else:
                delta.append(1 - (pow((2*(1 - r[j])), (1/(mum+1)))))
       
            ##Generate the corresponding child element 
            child_3[j] = child_3[j] + delta[j]
            
            ##Make sure that the generated element is withing the decision space 
            if child_3[j] > u_limit[j]:
                child_3[j] = u_limit[j]
            elif child_3[j] < l_limit[j]:
                child_3[j] = l_limit[j]
        
        ##Evaluate the objective function for the offspring and as before concatenate the offspring chromosome with objective 
        ##value 
        
        ##Fixing the variables according to predefined types and decimal points 
        child_3 = fix_variable_type_genetic_operator_serial(variable_list_conv_info, child_3) 
        
        child_3_obj = nsga_ii_para_imple_evaluate_objective(child_3, M, iteration)

        child_3_obj = np.ndarray.flatten(child_3_obj)
        for k in range(0, len(child_3_obj)):
            child_3.append(child_3_obj[k])
        
        ##Set the mutation flag 
        was_mutation = 1
        was_crossover = 0
    
    ##Keep proper count and appropriately fill the child variable with all the generated children for the particular generation 
    
    ##It is meant to store the return values in the form of variables, objective_functions, variables, objective_functions, mutation/crossover
    ##If the final values is 1, it had undergone mutation, else it underwent crossover.
    ##In the event that it had undergone mutation, the trailing values will be 0
    ret_child = []
    
    if was_crossover == 1:
        for ii in range(0, len(child_1)):
            ret_child.append(child_1[ii])
        for ii in range(0, len(child_2)):
            ret_child.append(child_2[ii])
        ##Appending the final column with information whether it had undergone crossover or mutation 
        ret_child.append(0)

    elif was_mutation == 1:
        for ii in range (0, len(child_3)):
            ret_child.append(child_3[ii])
        for ii in range (0, len(child_3)):
            ret_child.append(0)
        ##Appending the final column with information wether it had undergone crossover or mutation 
        ret_child.append(1)
            
    return ret_child
    

##This function processes the genetic operator function serially 
def serial_genetic_operator (parent_chromosome, M, V, mu, mum, l_limit, u_limit, input_v, iteration_num, variable_list_conv_info, mutation_perc):
    
    ##parent_chromosome         ---     the set of selected chromosomes.
    ##M                         ---     number of objective functions
    ##V                         ---     number of decision varaiables
    ##mu                        ---     distribution index for crossover (read the enlcosed pdf file)
    ##mum                       ---     distribution index for mutation (read the enclosed pdf file)
    ##l_limit                   ---     a vector of lower limit for the corresponding decsion variables
    ##u_limit                   ---     a vector of upper limit for the corresponding decsion variables
    ##iteration_num             ---     a number just to make the file unique 
    ##variable_list_cov_info    ---     a dataframe of the intervals based on each variable type 
    ##mutation_perc             ---     percentage of the time the variables undergo mutation

    ##The genetic operation is performed only on the decision variables, that is the first V elements in the chromosome vector. 
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__))[:-40] + '\\'
    import sys
    sys.path.append(current_path + 'master_level\\nsga_ii_para_implementation\\auxillary_functions\\')
    from auxillary_functions_nsga_ii_para_imple import identical_array
    from nsga_ii_para_imple_evaluate_objective import nsga_ii_para_imple_evaluate_objective 
    import numpy as np
    from random import uniform
    
    ##Determining the population size
    dim_parent_chromosome = parent_chromosome.shape
    N = dim_parent_chromosome[0]
    
    ##Flags wsed to set if crossover and mutation were actually performed 
    was_crossover = 0
    was_mutation = 0
    
    for i in range (0, N):
        ##With ~90% probability perform crossover 
        if uniform(0,1) < (1 - mutation_perc):
            ##Initialize the children to be null vectors 
            child_1 = []
            child_2 = []
            ##Select the first parent 
            parent_1 = int(round((N-1)*uniform(0,1)))
            parent_2 = int(round((N-1)*uniform(0,1)))
            
            ##Make sure that both parents are not the same 
            while identical_array(parent_chromosome[parent_1,:], parent_chromosome[parent_2,:]) == 1:
                parent_2 = int(round((N-1)*uniform(0,1)))

            
            ##Get the chromosome information fro each randomly selected parents 
            parent_1 = parent_chromosome[parent_1]
            parent_2 = parent_chromosome[parent_2]
            
            ##Perform crossover for each decision variable in the chromosome
            u = []
            bq = []
            for j in range (0, V):
                ##SBX (Simulated Binary Crossover)
                ##For more information about SBX refer to the encolsed pdf file.
                ##Generate a random number 
                u.append(uniform(0,1))
                
                if u[j] <= 0.5:
                    bq.append(pow((2*u[j]),(1/(mu + 1))))
                else:
                    bq.append(pow((1/(2*(1-u[j]))),(1/(mu + 1))))
                
                ##Generate the jth element of the first child 
                child_1.append(0.5*(((1 + bq[j])*parent_1[j]) + ((1 - bq[j])*parent_2[j])))
                ##Generate the jth element of the second child 
                child_2.append(0.5*(((1 - bq[j])*parent_1[j]) + ((1 + bq[j])*parent_2[j])))
                ##Make sure that the generated element is within the specified decision space else set it to the appropriate 
                ##extrema
                if child_1[j] > u_limit[j]:
                    child_1[j] = u_limit[j]

                elif child_1[j] < l_limit[j]:
                    child_1[j] = l_limit[j]
    
                if child_2[j] > u_limit[j]:
                    child_2[j] = u_limit[j]

                elif child_2[j] < l_limit[j]:
                    child_2[j] = l_limit[j]

            ##Evaluate the objective function for the offsprings and as before concatenate the offspring chromosome with 
            ##objective value
            
            ##Fixing the variables according to predefined types and decimal points 
            child_1 = fix_variable_type_genetic_operator_serial(variable_list_conv_info, child_1)
            child_2 = fix_variable_type_genetic_operator_serial(variable_list_conv_info, child_1)
            
            input_v['xAll'] = np.concatenate((input_v['xAll'] , [child_1]), axis=0)
            child_1_obj = nsga_ii_para_imple_evaluate_objective(child_1, M, iteration_num)
            input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_1_obj), axis=0)
            
            input_v['xAll'] = np.concatenate((input_v['xAll'] ,[child_2]), axis=0)
            child_2_obj = nsga_ii_para_imple_evaluate_objective(child_2, M, iteration_num)
            input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_2_obj), axis=0)
            
            child_1_obj = np.ndarray.flatten(child_1_obj)
            for k in range(0, len(child_1_obj)):
                child_1.append(child_1_obj[k])
            
            child_2_obj = np.ndarray.flatten(child_2_obj)
            for k in range(0, len(child_2_obj)):
                child_2.append(child_2_obj[k])
                
            ##Set the crossover flag. When corssover is performaed two children are generated, conversely, when mutation is
            ##only performed only after the children are generated 
            was_crossover = 1
            was_mutation = 0
        
        ##With ~10% probability perform mutation. Mutation is based on polynomial mutation 
        else:
            ##Select the parent at random 
            parent_3 = int(round((N-1)*uniform(0,1)))
            
            ##Get the chromosome information for the randomly selected parent
            child_3 = []
            for j in range (0, V):
                child_3.append(parent_chromosome[parent_3, j])
            ##Perform mutation on each element of the selected parent 
            
            r = []
            delta = []
            for j in range (0, V):
                r.append(uniform(0,1))
                if r[j] < 0.5:
                    delta.append((pow((2*r[j]), (1/(mum+1)))) - 1)
                else:
                    delta.append(1 - (pow((2*(1 - r[j])), (1/(mum+1)))))
           
                ##Generate the corresponding child element 
                child_3[j] = child_3[j] + delta[j]
                
                ##Make sure that the generated element is withing the decision space 
                if child_3[j] > u_limit[j]:
                    child_3[j] = u_limit[j]
                elif child_3[j] < l_limit[j]:
                    child_3[j] = l_limit[j]
            
            ##Evaluate the objective function for the offspring and as before concatenate the offspring chromosome with objective 
            ##value 
            
            ##Fixing the variables according to predefined types and decimal points 
            child_3 = fix_variable_type_genetic_operator_serial(variable_list_conv_info, child_3) 
            
            input_v['xAll'] = np.concatenate((input_v['xAll'] ,[child_3]), axis=0)
            child_3_obj = nsga_ii_para_imple_evaluate_objective(child_3, M, iteration_num)
            input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_3_obj), axis=0)

            child_3_obj = np.ndarray.flatten(child_3_obj)
            for k in range(0, len(child_3_obj)):
                child_3.append(child_3_obj[k])
            
            ##Set the mutation flag 
            was_mutation = 1
            was_crossover = 0
        
        ##Keep proper count and appropriately fill the child variable with all the generated children for the particular generation 
        if i == 0:
            if was_crossover == 1:
                child = np.concatenate(([child_1], [child_2]), axis=0)
                was_crossover = 0
            elif was_mutation == 1:
                child = [child_3]
                was_mutation = 0
        else:
            if was_crossover == 1:
                child = np.concatenate((child, [child_1]), axis=0)
                child = np.concatenate((child, [child_2]), axis=0)
                was_crossover = 0
            elif was_mutation == 1:
                child = np.concatenate((child, [child_3]), axis=0)
    
    return child, input_v    

##################################################################################################################################################################################
##################################################################################################################################################################################
##################################################################################################################################################################################
##Additional functions
    
##This function post processes the output from the parallel pools 
def post_process_para_indv_go (parallel_process_output, num_var, num_obj, input_v):
    
    ##parallel_process_output   --- a numpy array with variable, objective functions and the final column is a value of whether the individual had undergone 
    ##                              crossover or mutation
    ##num_var                   --- the number of variables per indivdual 
    ##num_obj                   --- the number of objective function values per individual 
    ##input_v = {}

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
    ##input_v['variable_list_conv_info']        ---     a dataframe of the intervals based on each variable type 

    import numpy as np 
    
    ##Determining the number of rows and columns
    dim_parallel_process_output = parallel_process_output.shape
    num_rows = dim_parallel_process_output[0]
    num_columns = dim_parallel_process_output[1]
    
    for i in range (0, num_rows):
        ##Determining if it had undergone crossover or mutation 
        if_mutation = parallel_process_output[i, num_columns-1]
        
        ##If it had undergone crossover 
        if int(if_mutation) == 0:
            ##Determining child_1
            child_1 = []
            for j in range (0, num_var + num_obj):
                child_1.append(parallel_process_output[i, j])
            ##Determining child_2
            child_2 = []
            for j in range (num_var + num_obj, 2*(num_var + num_obj)):
                child_2.append(parallel_process_output[i, j])
            
            ##Determining child_1_xall
            child_1_xall = []
            for j in range (0, num_var):
                child_1_xall.append(parallel_process_output[i, j])
            
            ##Determining child_2_xall
            child_2_xall = []
            for j in range (num_var + num_obj, num_var + num_obj + num_var):
                child_2_xall.append(parallel_process_output[i, j]) 
                
            ##Determining child_1_obj
            child_1_obj = []
            for j in range (num_var, num_var + num_obj):
                child_1_obj.append(parallel_process_output[i, j])
            
            ##Determining child_2_obj 
            child_2_obj = []
            for j in range (num_var + num_obj + num_var, num_var + num_obj + num_var + num_obj):
                child_2_obj.append(parallel_process_output[i, j])
                
            input_v['xAll'] = np.concatenate((input_v['xAll'] ,[child_1_xall]), axis=0)            
            input_v['xAll'] = np.concatenate((input_v['xAll'] ,[child_2_xall]), axis=0) 
            input_v['objAll'] = np.concatenate((input_v['objAll'] ,[child_1_obj]), axis=0)
            input_v['objAll'] = np.concatenate((input_v['objAll'] ,[child_2_obj]), axis=0)  
            
            if i == 0:
                child = np.concatenate(([child_1], [child_2]), axis=0)
            else:
                child = np.concatenate((child, [child_1]), axis=0)
                child = np.concatenate((child, [child_2]), axis=0)
        
        ##Else it had undergone mutation
        else:
            ##Determining child_3
            child_3 = []
            for j in range (0, num_var + num_obj):
                child_3.append(parallel_process_output[i, j])            
            
            ##Determining child_3_xall
            child_3_xall = []
            for j in range (0, num_var):
                child_3_xall.append(parallel_process_output[i, j])   
                
            ##Determining child_3_obj
            child_3_obj = []
            for j in range (num_var, num_var + num_obj):
                child_3_obj.append(parallel_process_output[i, j])      
                
            input_v['xAll'] = np.concatenate((input_v['xAll'] ,[child_3_xall]), axis=0)  
            input_v['objAll'] = np.concatenate((input_v['objAll'] ,[child_3_obj]), axis=0)
            
            if i == 0:
                child = [child_3]
            else:
                child = np.concatenate((child, [child_3]), axis=0)
                
    return child, input_v

##this function unpacks all the important information for parallel processing 
def unpack_information_for_para_indiv ():
    
    ##iteration     ---     the specific number 
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__))[:-40] + '\\'    
    import pandas as pd 
    import numpy as np
    
    ##Loading the variable_list_conv_info 
    file_name = current_path + 'master_level\\nsga_ii_para_implementation\\parallel_process_temp_storage\\variable_list_conv_info_go.csv'
    variable_list_conv_info = pd.read_csv(file_name)
    
    ##Loading the parent_chromosome 
    file_name1 = current_path + 'master_level\\nsga_ii_para_implementation\\parallel_process_temp_storage\\parent_chromosome_go.csv'
    parent_chromosome = np.genfromtxt(file_name1, delimiter=',')

    ##Loading other important information
    file_name2 = current_path + 'master_level\\nsga_ii_para_implementation\\parallel_process_temp_storage\\other_impt_info.csv'
    other_impt_info = pd.read_csv(file_name2)

    M = other_impt_info['M'][0]
    V = other_impt_info['V'][0]
    mu = other_impt_info['mu'][0]
    mum = other_impt_info['mum'][0]
    mutation_perc = other_impt_info['mutation_perc'][0]   
    
    ##Creating the upper and lower limit lists 
    l_limit, u_limit = create_variable_upper_lower_limits_para_imple (variable_list_conv_info)
    
    return parent_chromosome, M, V, mu, mum, variable_list_conv_info, mutation_perc, l_limit, u_limit

##This function creates limits in the form of lists for the lower and upper limits for each variable for the parallel function
def create_variable_upper_lower_limits_para_imple (variable_list_conv_info):
        
    ##variable_list_conv_info        ---     a dataframe of the intervals based on each variable type 
    
    ##Initializing return lists 
    l_limit = []
    u_limit = []
    
    ##Getting the variable information 
    dim_variable_list_conv_info = variable_list_conv_info.shape 
    num_var = dim_variable_list_conv_info[0]
    
    for i in range (0, num_var):
        ##Appending the lower bound 
        l_limit.append(variable_list_conv_info['Lower_bound'][i])
        ##Appending the upper bound 
        u_limit.append(variable_list_conv_info['Upper_bound'][i])
    
    return l_limit, u_limit 
    
##This function prepares the values in the suitable format for parallel processing 
def prepare_para_process_input_genetic_operator (parent_chromosome, M, V, mu, mum, variable_list_conv_info, mutation_perc):
    
    ##parent_chromosome         ---     the set of selected chromosomes.
    ##M                         ---     number of objective functions
    ##V                         ---     number of decision varaiables
    ##mu                        ---     distribution index for crossover (read the enlcosed pdf file)
    ##mum                       ---     distribution index for mutation (read the enclosed pdf file)
    ##variable_list_conv_info    ---     a dataframe of the intervals based on each variable type 
    ##mutation_perc             ---     percentage of the time the variables undergo mutation    
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__))[:-40] + '\\'
    import sys
    sys.path.append(current_path + 'master_level\\nsga_ii_para_implementation\\parallel_process_temp_storage\\')    
    import numpy as np 
    import pandas as pd 
    
    ##Saving the variable_list_conv_info
    file_name = current_path + 'master_level\\nsga_ii_para_implementation\\parallel_process_temp_storage\\variable_list_conv_info_go.csv'
    variable_list_conv_info.to_csv(file_name)
    
    ##Saving the parent_chromosome 
    file_name1 = current_path + 'master_level\\nsga_ii_para_implementation\\parallel_process_temp_storage\\parent_chromosome_go.csv'
    np.savetxt(file_name1, parent_chromosome, delimiter = ',')
    
    ##Placing the other important information into a dataframe and saving it 
    
    temp_data = [M, V, mu, mum, mutation_perc]
    other_impt_info = pd.DataFrame(data = [temp_data], columns = ['M', 'V', 'mu', 'mum', 'mutation_perc'])
    file_name2 = current_path + 'master_level\\nsga_ii_para_implementation\\parallel_process_temp_storage\\other_impt_info.csv'
    other_impt_info.to_csv(file_name2)
    
    ##Creating an iteration list based on the population size
    dim_parent_chromosome = parent_chromosome.shape 
    pop_size = dim_parent_chromosome[0]
    
    iter_list = []
    for i in range (0, pop_size):
        iter_list.append(i)
    
    return iter_list

##This function rounds off the variables to ensure that their types are compatible with the predefined 
def fix_variable_type_genetic_operator_serial (variable_list_conv_info, curr_variable_list):
    
    ##variable_list_conv_info   ---     a dataframe of the intervals based on each variable type 
    ##curr_variable_list        ---     the current list of variables 

    ##Determining the number of variables 
    dim_variable_list_conv_info = variable_list_conv_info.shape
    num_var = dim_variable_list_conv_info[0]
    
    ##initiating a return list 
    ret_list = []
    
    for i in range (0, num_var):
        var_type = variable_list_conv_info['Type'][i]
        if var_type == 'continuous':
            actual_value = round(curr_variable_list[i], int(variable_list_conv_info['Dec_prec'][i]))
        else:
            actual_value = int(round(actual_value)) 
        
        ret_list.append(actual_value)
            
    return ret_list

##This function creates limits in the form of lists for the lower and upper limits for each variable 
def create_variable_upper_lower_limits (input_v):
    
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
    ##input_v['variable_list_conv_info']        ---     a dataframe of the intervals based on each variable type 
    
    ##Initializing return lists 
    l_limit = []
    u_limit = []
    
    ##Getting the variable information 
    dim_variable_list_conv_info = input_v['variable_list_conv_info'].shape 
    num_var = dim_variable_list_conv_info[0]
    
    for i in range (0, num_var):
        ##Appending the lower bound 
        l_limit.append(input_v['variable_list_conv_info']['Lower_bound'][i])
        ##Appending the upper bound 
        u_limit.append(input_v['variable_list_conv_info']['Upper_bound'][i])
    
    return l_limit, u_limit  

##Copyright (c) 2009, Aravind Seshadri
##All rights reserved.

##Redistribution and use in source and binary forms, with or without  modification, are permitted provided that the following 
##conditions are met:

##   * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer 
##     in the documentation and/or other materials provided with the distribution
##     
##THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT 
##NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
##THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
##(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
##HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
##ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
