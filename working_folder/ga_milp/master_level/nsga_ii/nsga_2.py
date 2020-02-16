##This is main function that executes the NSGA-II algorithm

def nsga_2(input_v):
    ##import sys
    import numpy as np
    from objective_description_function import objective_description_function
    from initialize_variables import initialize_variables
    from non_domination_sort_mod import non_domination_sort_mod
    from tournament_selection import tournament_selection
    from genetic_operator import genetic_operator
    from replace_chromosome import replace_chromosome 
    import matplotlib.pyplot as plt
    print('Running Optimization...')
    
    input_v['objAll'] = []
    input_v['xAll'] = []

    ##Making sure thet population and generations are integers 
    input_v['population'] = round(input_v['population'])
    input_v['generations'] = round(input_v['generations'])
    
    
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

    chromosome, input_v = initialize_variables(input_v)    
    
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
        offspring_chromosome, input_v = genetic_operator(parent_chromosome, input_v['M'], input_v['V'], mu, mum, 
                                                         input_v['min_range'], input_v['max_range'], input_v)
        
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

        print('Search ' + 'iteration ' + str(i))
        
#        if not(i%100) and (i !=0):
#            disp_msg = str(i) + ' generations completed \n'
#            print(disp_msg)
    
    ##Result
    ##Save the result in csv format
    xAll = input_v['xAll']
    objAll = input_v['objAll']

    np.savetxt('C:\\Optimization_zlc\\master_level\\NSGA_II\\solution\\solution.csv', chromosome, delimiter=',')
    np.savetxt('C:\\Optimization_zlc\\master_level\\NSGA_II\\solution\\solutionX.csv', xAll, delimiter=',')
    np.savetxt('C:\\Optimization_zlc\\master_level\\NSGA_II\\solution\\solutionObj.csv', objAll, delimiter=',')
    
    ##Visualize 
    ##The following is used to visualize the result if objective space dimension can be displayed i.e. 2D, 3D
    
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