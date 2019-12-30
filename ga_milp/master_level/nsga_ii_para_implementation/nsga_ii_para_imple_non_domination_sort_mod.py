##This function sorts the current population based on non-domination. All the individuals in the first front are given a rank of 1, the second front individual are assigned rank 
##2 and so on. 


def nsga_ii_para_imple_non_domination_sort_mod (chromosome, num_obj_func, num_var):
    
    ##chromosome    ---     a record of the population which contains variables followed by the objective functions at the end 
    ##num_obj_func  ---     the number of objective functions 
    ##num_var       ---     the number of variables for each corresponding agent 
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__))[:-40] + '\\'
    import sys
    sys.path.append(current_path + 'master_level\\nsga_ii_para_implementation\\auxillary_functions\\')
    from auxillary_functions_nsga_ii_para_imple import index_sort_by_column
    import numpy as np 
    
    ##Determining the size of the population 
    dim_chromosome = chromosome.shape 
    pop_size = dim_chromosome[0]
    
    ##Initialize the front number to 1
    front = 1
    
    ##Setting up sets for storing information
    individual = {}
    F = {}
    F[front] = {}           
    F[front]['f'] = []                                      ##To store the number of variables which is dominated 
    
    ##To store the front information
    collector = np.zeros((pop_size, 1))
    
    for i in range (0, pop_size):
        ##initiating a dictionary for this individual 
        individual[i] = {}
        individual[i]['n'] = 0
        ##Individuals which this individual dominate 
        individual[i]['p'] = []        
        
        for j in range (0, pop_size):
            ##No point evaluating the same individual, it does not make sense
            if i != j:
                ##Initialzing counters
                dom_less = 0
                dom_equal = 0
                dom_more = 0
                ##Iterating through each objective function 
                for k in range (0, num_obj_func):
                    ##Case 1: When i is less than j
                    if chromosome[i, num_var+k] < chromosome[j, num_var+k]:
                        dom_less = dom_less + 1
                    ##Case 2: When i is equals to j
                    elif chromosome[i, num_var+k] == chromosome[j, num_var+k]:
                        dom_equal = dom_equal + 1                   
                    ##Case 3: When i is more than j
                    else:                
                        dom_more = dom_more + 1
                        
                ##For each individual  
                    ##If j dominates i completely  
                if (dom_less == 0) and (dom_equal != num_obj_func):
                    individual[i]['n'] = individual[i]['n'] + 1
                    ##If i dominates j completely or somewhat equal 
                elif (dom_more == 0) and (dom_equal != num_obj_func):
                    individual[i]['p'].append(j)  
                    
        ##If it is completely non-dominated, it belongs to the first front 
        if individual[i]['n'] == 0:
            collector[i,0] = 1
            F[front]['f'].append(i)
    
    chromosome = np.concatenate((chromosome, collector), axis=1)    
    
    ##Finding the subsequent fronts 
        ##While the preivous front is not empty
    counter = 0
    while F[front]['f']:
        ##Initialize an empty array 
        Q = []
        ##Scanning through the previous front list
        for i in range (0, len(F[front]['f'])):
            ##If p is not 0, that means there are individuals which i dominates
            if individual[F[front]['f'][i]]['p']:
                ##Scanning through the individuals which i dominates
                for j in range (0, len(individual[F[front]['f'][i]]['p'])):
                    individual[individual[F[front]['f'][i]]['p'][j]]['n'] = individual[individual[F[front]['f'][i]]['p'][j]]['n'] - 1
                    if individual[individual[F[front]['f'][i]]['p'][j]]['n'] == 0:
                        chromosome[individual[F[front]['f'][i]]['p'][j], num_obj_func + num_var] = front + 1
                        Q.append(individual[F[front]['f'][i]]['p'][j])
        counter = counter + 1
        if counter > pop_size:
            print('Error in determining fronts...')
            sys.exit()
        front = front + 1
        F[front] = {}
        F[front]['f'] = Q    
    
    dim_chromosome = chromosome.shape
    index = index_sort_by_column(chromosome, dim_chromosome[1]-1)
    
    sorted_based_on_front = np.zeros((dim_chromosome[0], dim_chromosome[1]))
    for i in range (0, dim_chromosome[0]):
        for j in range (0, dim_chromosome[1]):
            sorted_based_on_front[i,j] = chromosome[int(round(index[i])),j]  
    
    return sorted_based_on_front, F

##Non-Dominated sort. 
##The initialized population is sorted based on non-domination. The fast sort algorithm [1] is described as below for 
##each

##• for each individual p in main population P do the following
##  – Initialize Sp = []. This set would contain all the individuals that is being dominated by p.
##  – Initialize np = 0. This would be the number of individuals that dominate p.
##  – for each individual q in P
##      * if p dominated q then
##          · add q to the set Sp i.e. Sp = Sp ? {q}
##      * else if q dominates p then
##          · increment the domination counter for p i.e. np = np + 1
##  – if np = 0 i.e. no individuals dominate p then p belongs to the first front; Set rank of individual p to one i.e 
##    prank = 1. Update the first front set by adding p to front one i.e F1 = F1 ? {p}
##• This is carried out for all the individuals in main population P.
##• Initialize the front counter to one. i = 1
##• following is carried out while the ith front is nonempty i.e. Fi != []
##  – Q = []. The set for storing the individuals for (i + 1)th front.
##  – for each individual p in front Fi
##      * for each individual q in Sp (Sp is the set of individuals dominated by p)
##          · nq = nq?1, decrement the domination count for individual q.
##          · if nq = 0 then none of the individuals in the subsequent fronts would dominate q. Hence set qrank = i + 1. 
##            Update the set Q with individual q i.e. Q = Q ? q.
##  – Increment the front counter by one.
##  – Now the set Q is the next front and hence Fi = Q.
##
##This algorithm is better than the original NSGA ([2]) since it utilize the informatoion about the set that an individual 
##dominate (Sp) and number of individuals that dominate the individual (np).


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