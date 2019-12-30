##This is main function that executes the NSGA-II algorithm

def nsga_2(input_v,activate_parallel,num_cores,crossover_perc,mutation_perc,obj_func_plot):
    ##import sys
    import numpy as np
    from objective_description_function import objective_description_function
    from initialize_variables import initialize_variables
    from non_domination_sort_mod import non_domination_sort_mod
    from tournament_selection import tournament_selection
    import genetic_operator_adv
    from replace_chromosome import replace_chromosome 
    import matplotlib.pyplot as plt
    from nsga_II_binary_conv_info import nsga_II_binary_conv_info
    print('Running Optimization...')
    input_v['objAll'] = []
    input_v['xAll'] = []
    import os
    import timing
    import time
    ##Making sure thet population and generations are integers 
    input_v['population'] = round(input_v['population'])
    input_v['generations'] = round(input_v['generations'])
    
    bin_info_variable_list =  nsga_II_binary_conv_info(input_v['range_of_decision_variables'])
    total_binary_len = sum(bin_info_variable_list['Bits'][:])
    
    ##Forming the objective function 
    ##input_v['M'] --- number of objective functions
    ##input_v['V'] --- number of decision variables 
    ##input_v['min_range'] --- list of corresponding lowerbound of the decision variables 
    ##input_v['max_range'] --- list of corresponding upperbound of the decision variables 
    input_v['M'], input_v['V'], input_v['min_range'], input_v['max_range'] = objective_description_function(input_v)    
    
    ##Initialize the population 
    ##Population is initialzied with random values which are within the specified range. Each chromosome consist of the
    ##decision variables. Also the value fo the objective functions, rank and crowding distance information are also added
    ##to the chromosome vector but only the elements of the vector which has the decision variables are operatedupon to 
    ##perform the genetic operations like crossover and mutation

    chromosome, input_v = initialize_variables(input_v,activate_parallel,num_cores,bin_info_variable_list)    
    
    ##Sort the initialized population 
    ##Sort the population using non-domination-sort. This returns two columns for each individual which are the rank and the 
    ##crowding distance corresponding to their position in the front they belong. At this stage the rank and the crowding distance 
    ##for each chromosome is added to the chromosome vector for easy of computation.
    chromosome = non_domination_sort_mod(chromosome, input_v['M'], input_v['V'])
    
    ## Start the evolution process
    # The following are performed in each generation
    # * Select the parents which are fit for reproduction
    # * Perfrom crossover and Mutation operator on the selected parents
    # * Perform Selection from the parents and the offsprings
    # * Replace the unfit individuals with the fit individuals to maintain a
    #   constant population size.
    
    ##Generating probability reference for the mutation process
    mutation_prob = mutation_probab (bin_info_variable_list, total_binary_len)
    axes = plt.gca()
    print('Starting search process...')

    for i in range (0, input_v['generations']):
        
        ## Select the parents
        ## Parents are selected for reproduction to generate offspring. The
        ## original NSGA-II uses a binary tournament selection based on the
        ## crowded-comparision operator. The arguments are 
        ## pool - size of the mating pool. It is common to have this to be half the
        ##        population size.
        ## tour - Tournament size. Original NSGA-II uses a binary tournament
        ##        selection, but to see the effect of tournament size this is kept
        ##        arbitary, to be choosen by the user.
        
        pool = int(round(input_v['population']/2))
        tour = 2
        
        ## Selection process
        ## A binary tournament selection is employed in NSGA-II. In a binary
        ## tournament selection process two individuals are selected at random
        ## and their fitness is compared. The individual with better fitness is
        ## selcted as a parent. Tournament selection is carried out until the
        ## pool size is filled. Basically a pool size is the number of parents
        ## to be selected. The input arguments to the function
        ## tournament_selection are chromosome, pool, tour. The function uses
        ## only the information from last two elements in the chromosome vector.
        ## The last element has the crowding distance information while the
        ## penultimate element has the rank information. Selection is based on
        ## rank and if individuals with same rank are encountered, crowding
        ## distance is compared. A lower rank and higher crowding distance is
        ## the selection criteria.

        parent_chromosome = tournament_selection(chromosome, pool, tour)

        ## Perfrom crossover and Mutation operator
        ## The original NSGA-II algorithm uses Simulated Binary Crossover (SBX) and
        ## Polynomial  mutation. Crossover probability pc = 0.9 and mutation
        ## probability is pm = 1/n, where n is the number of decision variables.
        ## Both real-coded GA and binary-coded GA are implemented in the original
        ## algorithm, while in this program only the real-coded GA is considered.
        ## The distribution indeices for crossover and mutation operators as mu = 20
        ## and mum = 20 respectively.
        
        mu = 20 
        mum = 20
        parent_chrom_bin = conv_dec_to_bin(bin_info_variable_list,parent_chromosome,input_v['M'])
        
        offspring_chromosome, input_v = genetic_operator_adv.genetic_operator_adv(parent_chrom_bin,mutation_prob,input_v,bin_info_variable_list,activate_parallel,num_cores)
        
        ##Intermediate population 
        ##Intermediate population is the combined population of parents and offsprings of the current generation. The population
        ##size is two times the initial population.
        
        dim_chromosome = chromosome.shape 
        main_pop = dim_chromosome[0]

        dim_offspring_chromosome = offspring_chromosome.shape 
        offspring_pop = dim_offspring_chromosome[0]

        ##Intermediate_chromosome is a concatenation of current population and the offspring population.
        intermediate_chromosome = np.zeros((main_pop + offspring_pop, input_v['M'] + input_v['V']))
        for j in range (0, main_pop):
            for k in range (0, input_v['M'] + input_v['V']):
                intermediate_chromosome[j,k] = chromosome[j,k]
        for j in range (main_pop, main_pop + offspring_pop):
            for k in range (0, input_v['M'] + input_v['V']):
                intermediate_chromosome[j,k] = offspring_chromosome[j-main_pop,k]        
        
        ##Non-domination-sort of intermediate population
        ##The intermediate population is sorted again based on non-domination sort before the replacement operator is performed 
        ##on the intermediate population.
        
        intermediate_chromosome = non_domination_sort_mod(intermediate_chromosome, input_v['M'], input_v['V'])
        ##np.savetxt('C:\\Optimization_zlc\\solution.csv', intermediate_chromosome, delimiter=',')
        ##sys.exit()
        
        ##Perform Selection
        ##Once the intermediate population is sorted only the best solution is selected based on it rank and crowding distance. 
        ##Each front is filled in ascending order until the addition of population size is reached. The last front is included 
        ##in the population based on the individuals with least crowding distance
        

        chromosome = replace_chromosome(intermediate_chromosome, input_v['M'], input_v['V'], input_v['population'])
        
     
        if obj_func_plot == 'yes':
            plt.plot(chromosome[:, input_v['V']], chromosome[:, input_v['V']+1], '*')
            plt.title('Objective function last population')
            plt.xlabel('Objective 1')
            plt.ylabel('Objective 2')

            plt.draw()
            plt.pause(1e-17)
            axes.clear()


        print('Search ' + 'iteration ' + str(i))
        
#        if not(i%100) and (i !=0):
#            disp_msg = str(i) + ' generations completed \n'
#            print(disp_msg)
    
    ##Result
    ##Save the result in csv format
    xAll = input_v['xAll']
    objAll = input_v['objAll']

    np.savetxt(os.path.dirname(__file__)+'\\solution\\solution.csv', chromosome, delimiter=',')
    np.savetxt(os.path.dirname(__file__)+'\\solution\\solutionX.csv', xAll, delimiter=',')
    np.savetxt(os.path.dirname(__file__)+'\\solution\\solutionObj.csv', objAll, delimiter=',')
    
    ##Visualize 
    ##The following is used to visualize the result if objective space dimension can be displayed i.e. 2D, 3D
    timing.log("NOW")
    if input_v['M'] == 2:
        ##Objective functions
        plt.plot(chromosome[:, input_v['V']], chromosome[:, input_v['V']+1], '*')
        plt.title('Objective function last population')
        plt.xlabel('Objective 1')
        plt.ylabel('Objective 2')
        plt.show()
        
        ##All populations 
        plt.plot(objAll[:, 0], objAll[:, 1], '*')
        plt.title('Objective function all populations')
        plt.xlabel('Objective 1')
        plt.ylabel('Objective 2')
        plt.show()        
    
    elif input_v['M'] == 3:
        ##Objective functions 
        plt.plot(chromosome[:, input_v['V']], chromosome[:, input_v['V']+1], chromosome[:, input_v['V']+2], '*')
        plt.title('Objective function last population')
        plt.xlabel('Objective 1')
        plt.ylabel('Objective 2')
        plt.zlabel('Objective 3')
        plt.show()
        
        ##All populations 
        plt.plot(objAll[:,0], objAll[:,1], objAll[:,2], '*')
        plt.title('Objective function all populations')
        plt.xlabel('Objective 1')
        plt.ylabel('Objective 2')
        plt.zlabel('Objective 3')        
        plt.show()           

def mutation_probab (bin_info_variable_list, total_binary_len):
    
    ##bin_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes    
    ##total_binary_len --- total length of binary bits for all represented variables 
    
    
    dim_bin_info_variable_list = bin_info_variable_list.shape
    
    ##Ensuring that each variable has an equal chance of being mutated 
    num_var = dim_bin_info_variable_list[0]
    var_prob = 1 / num_var 
    
    ind_var_prob = []
    
    for i in range (0, num_var):
        ##Performing linear ranking
        prob = range(1, bin_info_variable_list['Bits'][i] + 1)
        denom = sum(prob)
        for j in range (0, bin_info_variable_list['Bits'][i]):
            bit_prob = (prob[j] / denom) * var_prob
            ind_var_prob.append(bit_prob)
            
    return ind_var_prob

def conv_dec_to_bin (bin_info_variable_list, initial_variable_values,num_obj):
    
    import sys 
    import numpy as np
    import math
    
    ##bin_info_variable_list --- the list of variables and its corresponding attributes, with binary attributes
    ##initial_variable_values --- starting values to seed the initial population

    ##Determine the number of variables 
    dim_bin_info_variable_list = bin_info_variable_list.shape
    dim_initial_variable_values = initial_variable_values.shape
    
    ##Checking if the seeded values are of the same order
    if dim_bin_info_variable_list[0] != (dim_initial_variable_values[1] - num_obj - 2):
        print('Error in seeding entries')
        sys.exit()
    
    ##Establishing the return value array 
    total_bits = sum(bin_info_variable_list['Bits'][:])
    ##The addition of an additional column is for the storage of the objective function 
    ret_vals = np.zeros((dim_initial_variable_values[0], total_bits + num_obj + 2))
    
    ##Determining the closest binary representation of the seeded variables
    
    ##i variable handles each set of seeded variables 
    for i in range (0, dim_initial_variable_values[0]):
        ##j variable handles the processes within each set of variables
        ##This array index is to handle the input column of the return numpy array 
        array_index = 0

        for j in range (0, dim_bin_info_variable_list[0]):
            if (bin_info_variable_list['Type'][j] == 'continuous'):
                ##The binary representation is just a ratio of the min and max within the range 
                lb_dec = bin_info_variable_list['Lower_bound'][j]
                ub_dec = bin_info_variable_list['Upper_bound'][j]
                seed_val = initial_variable_values[i,j]
                ub_binary_in_dec = pow(2, bin_info_variable_list['Bits'][j]) - 1
                frac_rep_dec = (seed_val - lb_dec) / (ub_dec - lb_dec)
                seed_val_bin_in_dec = frac_rep_dec * ub_binary_in_dec
                ##We need a whole number, so round it off to the nearest approximation 
                seed_val_bin_in_dec = int(round(seed_val_bin_in_dec))
                ##Converting the number to binary form 
                bin_form_str = "{0:b}".format(seed_val_bin_in_dec)
                ##Checking for the length of the returned string 
                len_value_bits = len(bin_form_str)
                ##Calculating the number of preceding zeros 
                len_preceding_zeros = bin_info_variable_list['Bits'][j] - len_value_bits
                ##Populating the return numpy array 
                for k in range (0, len_preceding_zeros):
                    ret_vals[i,array_index] = 0
                    array_index = array_index + 1
                ##Populating the return array with the bits 
                for k in range (0, len_value_bits):
                    ret_vals[i, array_index] = bin_form_str[k]
                    array_index = array_index + 1
            
            elif bin_info_variable_list['Type'][j] == 'binary':
                ##This is straightforaward, just fill in the values
                ret_vals[i, array_index] = initial_variable_values[i,j]
                array_index = array_index + 1
                
            elif (bin_info_variable_list['Type'][j] == 'discrete'):
                ##The binary representation is just a ratio of the min and max within the range 
                lb_dec = bin_info_variable_list['Lower_bound'][j]
                ub_dec = bin_info_variable_list['Upper_bound'][j]
                seed_val = initial_variable_values[i,j]
                ub_binary_in_dec = pow(2, bin_info_variable_list['Bits'][j]) - 1
                frac_rep_dec = (seed_val - lb_dec) / (ub_dec - lb_dec)
                seed_val_bin_in_dec = frac_rep_dec * ub_binary_in_dec
                ##We need a whole number, so round it off to the nearest approximation 
                seed_val_bin_in_dec = int(math.ceil(seed_val_bin_in_dec))
                ##Converting the number to binary form 
                bin_form_str = "{0:b}".format(seed_val_bin_in_dec)
                ##Checking for the length of the returned string 
                len_value_bits = len(bin_form_str)
                ##Calculating the number of preceding zeros 
                len_preceding_zeros = bin_info_variable_list['Bits'][j] - len_value_bits
                ##Populating the return numpy array 
                for k in range (0, len_preceding_zeros):
                    ret_vals[i,array_index] = 0
                    array_index = array_index + 1
                ##Populating the return array with the bits 
                for k in range (0, len_value_bits):
                    ret_vals[i, array_index] = bin_form_str[k]
                    array_index = array_index + 1
                    
        for k in range(0,num_obj + 2):
            ret_vals[i][total_bits + k] = initial_variable_values[i][dim_initial_variable_values[1] - num_obj - 2 + k]
        
        #ret_vals[i][total_bits] = initial_variable_values[i][dim_initial_variable_values[1] - 3]
        #ret_vals[i][total_bits +1] = initial_variable_values[i][dim_initial_variable_values[1] - 2]
        #ret_vals[i][total_bits +2] = initial_variable_values[i][dim_initial_variable_values[1] - 1]
        
    return ret_vals

    
##Copyright (c) 2009, Aravind Seshadri
##All rights reserved.

##Redistribution and use in source and binary forms, with or without  modification, are permitted provided that the following 
##conditions are met:

##   * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
##   * Mohit Gupta -  June 6 Nsga 2 functions coded
##   * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer 
##     in the documentation and/or other materials provided with the distribution
##   * Mohit Gupta - May - Developed he Milp and read the whole system
##     
##THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT 
##NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL
##Mohit Gupta Errors, parallel implementation and code completed - Now giving correct output :)
##THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
##(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
##Mohit Gupta Errors identfied 7 (Fix them !)
##HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
##ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.