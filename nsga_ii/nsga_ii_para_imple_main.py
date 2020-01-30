##This is main function that executes the NSGA-II algorithm

def nsga_ii_para_imple_main(input_v):
    
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
    
    import numpy as np
    import time 
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__)) + '\\'             ##Incase relative directories are needed
    
    
    from nsga_ii_para_imple_objective_description_function import nsga_ii_para_imple_objective_description_function
    from nsga_ii_para_imple_conv_info import nsga_ii_para_imple_conv_info
    from nsga_ii_para_imple_initialize_variables import nsga_ii_para_imple_initialize_variables
    from nsga_ii_para_imple_non_domination_sort_mod import nsga_ii_para_imple_non_domination_sort_mod
    from nsga_ii_para_imple_calc_crowding_dist import nsga_ii_para_imple_calc_crowding_dist
    from nsga_ii_para_imple_tournament_selection import nsga_ii_para_imple_tournament_selection
    from nsga_ii_para_imple_genetic_operator import nsga_ii_para_imple_genetic_operator
    from nsga_ii_para_imple_replace_chromosome import nsga_ii_para_imple_replace_chromosome 
    
    import matplotlib.pyplot as plt
    print('Running Multi-Objective Optimization...')
    
    ##Lists for storing records of objective functions and variable values 
    input_v['objAll'] = []
    input_v['xAll'] = []

    ##Making sure thet population and generations are integers 
    input_v['population'] = round(input_v['population'])
    input_v['generations'] = round(input_v['generations'])
    
    
    ##Forming the objective function 
    ##input_v['M'] --- number of objective functions
    ##input_v['V'] --- number of decision variables 

    ##IF THERE IS ONLY ONE OBJECTIVE FUNCTION, THIS FUNCTION WILL RETURN AN ERROR
    input_v['M'], input_v['V'] = nsga_ii_para_imple_objective_description_function(input_v) 
    
    
    ##Processing the variable information to identify the range and so on
    input_v['variable_list_conv_info'] = nsga_ii_para_imple_conv_info (input_v)
    
    
    ##Initialize the population 
    ##Population is initialzied with random values which are within the specified range. Each chromosome consist of the
    ##decision variables. Besides, initial seeds are also added. This should aid convergence. The value of the objective functions, 
    ##rank and crowding distance information are also added to the chromosome vector but only the elements of the vector which has 
    ##the decision variables are operated upon to perform the genetic operations like crossover and mutation
    chromosome, input_v = nsga_ii_para_imple_initialize_variables(input_v)  
    
    ##Sort the initialized population 
    ##Sort the population using non-domination-sort. 
    chromosome_sorted_by_rank, dominated_info = nsga_ii_para_imple_non_domination_sort_mod(chromosome, input_v['M'], input_v['V'])
        
    ##This returns two columns for each individual which are the rank and the crowding distance corresponding to their position in the front 
    ##they belong. At this stage the rank and the crowding distance for each chromosome is added to the chromosome vector for easy of computation.
    chromosome = nsga_ii_para_imple_calc_crowding_dist(chromosome_sorted_by_rank, dominated_info, input_v['M'], input_v['V'])

    ##Setting up the dynamic graph for 2 or 3 objectives only 
    if (input_v['obj_func_plot'] == 'yes') and (int(input_v['num_obj_func']) == 2):
        ##Setting up the dynamic graph 
        obj_1 = []
        obj_2 = []
        plt.show()
        axes = plt.gca()
    
    elif (input_v['obj_func_plot'] == 'yes') and (int(input_v['num_obj_func']) == 3):
        ##Setting up the dynamic graph 
        obj_1 = []
        obj_2 = []
        obj_3 = []
        plt.show()
        axes = plt.gca()    
    
    
    ## Start the evolution process
    # The following are performed in each generation
    # * Select the parents which are fit for reproduction
    # * Perfrom crossover and Mutation operator on the selected parents
    # * Perform Selection from the parents and the offsprings
    # * Replace the unfit individuals with the fit individuals to maintain a
    #   constant population size.

    
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
        
        pool = int(input_v['crossover_perc'] * input_v['population'])
        tour = int(input_v['selection_choice_data']['tournament_size'])
        
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
        parent_chromosome = nsga_ii_para_imple_tournament_selection(chromosome, pool, tour)

        ## Perfrom crossover and Mutation operator
        ## The original NSGA-II algorithm uses Simulated Binary Crossover (SBX) and
        ## Polynomial  mutation. Crossover probability pc = 0.9 and mutation
        ## probability is pm = 1/n, where n is the number of decision variables.
        ## Both real-coded GA and binary-coded GA are implemented in the original
        ## algorithm, while in this program only the real-coded GA is considered.
        ## The distribution indices for crossover and mutation operators as mu = 20
        ## and mum = 20 respectively.
        offspring_chromosome, input_v = nsga_ii_para_imple_genetic_operator(parent_chromosome, input_v)        
        
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
        intermediate_chromosome_sorted_by_rank, dominated_info = nsga_ii_para_imple_non_domination_sort_mod(intermediate_chromosome, input_v['M'], input_v['V'])
        
        ##This returns two columns for each individual which are the rank and the crowding distance corresponding to their position in the front 
        ##they belong. At this stage the rank and the crowding distance for each chromosome is added to the chromosome vector for easy of computation.
        intermediate_chromosome = nsga_ii_para_imple_calc_crowding_dist(intermediate_chromosome_sorted_by_rank, dominated_info, input_v['M'], input_v['V']) 
        
        ##Perform Selection
        ##Once the intermediate population is sorted only the best solution is selected based on it rank and crowding distance. 
        ##Each front is filled in ascending order until the addition of population size is reached. The last front is included 
        ##in the population based on the individuals with least crowding distance
        chromosome = nsga_ii_para_imple_replace_chromosome(intermediate_chromosome, input_v['M'], input_v['V'], input_v['population'])
        
        ##Plotting the dynamic graphs 
        if (input_v['obj_func_plot'] == 'yes') and (int(input_v['num_obj_func']) == 2):
            ##Dynamic plotting
            dim_chromosome = chromosome.shape 
            num_rows = dim_chromosome[0]
            num_cols = dim_chromosome[1]
            
            ##Update the x and y axes plots
            for kk in range (0, num_rows):
                obj_1.append(chromosome[kk, input_v['V']])
                obj_2.append(chromosome[kk, input_v['V']+1])
            
            ##Dynamic axes
            axes.clear()
            line, = axes.plot(obj_1, obj_2, 'b*')
            plt.title('2D')
            plt.xlabel('Objective 1')
            plt.ylabel('Objective 2')  
            
            ##To determine scaling             
            if min(obj_1) == 0:
                axes.set_xlim(min(obj_1) - (0.1 * abs(max(obj_1))), 1.1 * max(obj_1)) 
            elif max(obj_1) == 0:
                axes.set_xlim(0.9 * min(obj_1), max(obj_1) + (0.1 * abs(min(obj_1))))
          
            if min(obj_2) == 0:
                axes.set_xlim(min(obj_2) - (0.1 * abs(max(obj_2))), 1.1 * max(obj_2)) 
            elif max(obj_2) == 0:
                axes.set_xlim(0.9 * min(obj_2), max(obj_2) + (0.1 * abs(min(obj_2))))                 
   
            line.set_xdata(obj_1)
            line.set_ydata(obj_2)
            curr_msg = 'Current Iteration: \n' + str(i)
            plt.text(0.7, 0.9, curr_msg, horizontalalignment='center', verticalalignment='center', transform = axes.transAxes)
            plt.draw()
            plt.pause(1e-17)
            time.sleep(0.1)
            
        elif (input_v['obj_func_plot'] == 'yes') and (int(input_v['num_obj_func']) == 3):
            ##Dynamic plotting
            dim_chromosome = chromosome.shape 
            num_rows = dim_chromosome[0]
            num_cols = dim_chromosome[1]
            
            ##Update the x and y axes plots
            for kk in range (0, num_rows):
                obj_1.append(chromosome[kk, input_v['V']])
                obj_2.append(chromosome[kk, input_v['V']+1])
                obj_3.append(chromosome[kk, input_v['V']+2])
                
            ##Dynamic axes
            axes.clear()
            line, = axes.plot(obj_1, obj_2, obj_3, 'b*')
            plt.title('3D')
            plt.xlabel('Objective 1')
            plt.ylabel('Objective 2') 
            plt.zlabel('Objective 3')
            
            if min(obj_1) == 0:
                axes.set_xlim(min(obj_1) - (0.1 * abs(max(obj_1))), 1.1 * max(obj_1)) 
            elif max(obj_1) == 0:
                axes.set_xlim(0.9 * min(obj_1), max(obj_1) + (0.1 * abs(min(obj_1)))) 
                
            if min(obj_2) == 0:
                axes.set_xlim(min(obj_2) - (0.1 * abs(max(obj_2))), 1.1 * max(obj_2)) 
            elif max(obj_2) == 0:
                axes.set_xlim(0.9 * min(obj_2), max(obj_2) + (0.1 * abs(min(obj_2))))
                
            if min(obj_3) == 0:
                axes.set_xlim(min(obj_3) - (0.1 * abs(max(obj_3))), 1.1 * max(obj_3)) 
            elif max(obj_3) == 0:
                axes.set_xlim(0.9 * min(obj_3), max(obj_3) + (0.1 * abs(min(obj_3)))) 
                
            line.set_xdata(obj_1)
            line.set_ydata(obj_2)
            line.set_zdata(obj_3)
            curr_msg = 'Current Iteration: \n' + str(i)
            plt.text(0.7, 0.9, curr_msg, horizontalalignment='center', verticalalignment='center', transform = axes.transAxes)
            plt.draw()
            plt.pause(1e-17)
            time.sleep(0.1)
            
        print('Search ' + 'iteration ' + str(i))
    
    
    ##Result
    ##Save the result in csv format
    xAll = input_v['xAll']
    objAll = input_v['objAll']
    
    save_file_loc = current_path + 'solution\\solution.csv'
    save_file_loc1 = current_path + 'solution\\solutionX.csv'
    save_file_loc2 = current_path + 'solution\\solutionObj.csv'
    
    
    np.savetxt(save_file_loc, chromosome, delimiter=',')
    np.savetxt(save_file_loc1, xAll, delimiter=',')
    np.savetxt(save_file_loc2, objAll, delimiter=',')
    
    ##Visualize 
    ##The following is used to visualize the result if objective space dimension can be displayed i.e. 2D, 3D
    
    if input_v['M'] == 2:
        ##Objective functions
        plt.figure()
        plt.plot(chromosome[:, input_v['V']], chromosome[:, input_v['V']+1], '*')
        plt.title('Objective function last population')
        plt.xlabel('Objective 1')
        plt.ylabel('Objective 2')
        plt.show()
        
        ##All populations 
        plt.figure()
        plt.plot(objAll[:, 0], objAll[:, 1], '*')
        plt.title('Objective function all populations')
        plt.xlabel('Objective 1')
        plt.ylabel('Objective 2')
        plt.show()        
    
    elif input_v['M'] == 3:
        ##Objective functions 
        plt.figure()
        plt.plot(chromosome[:, input_v['V']], chromosome[:, input_v['V']+1], chromosome[:, input_v['V']+2], '*')
        plt.title('Objective function last population')
        plt.xlabel('Objective 1')
        plt.ylabel('Objective 2')
        plt.zlabel('Objective 3')
        plt.show()
        
        ##All populations
        plt.figure()
        plt.plot(objAll[:,0], objAll[:,1], objAll[:,2], '*')
        plt.title('Objective function all populations')
        plt.xlabel('Objective 1')
        plt.ylabel('Objective 2')
        plt.zlabel('Objective 3')        
        plt.show()           

    
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