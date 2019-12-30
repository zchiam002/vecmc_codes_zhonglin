##This function replaces the chromosomes based on rank and crowding distance. Initially until the population size is reached each 
##front is added one by one until addition of a complete front which results in exceeding the population size. At this point the 
##chromosomes in that front is added subsequently to the population based on crowding distance.

def nsga_ii_para_imple_replace_chromosome(intermediate_chromosome, M, V, pop):
    
    ##intermediate_chromosome   ---     original population and the child/mutated chromosomes 
    ##M                         ---     the number of objective functions 
    ##V                         ---     the number of variables 
    ##pop                       ---     the original populaation size 
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__))[:-40] + '\\' 
    import sys
    sys.path.append(current_path + 'master_level\\nsga_ii_para_implementation\\auxillary_functions')
    from auxillary_functions_nsga_ii_para_imple import index_sort_by_column    
    from auxillary_functions_nsga_ii_para_imple import find_max_index    
    import numpy as np

    ##Finding the dimensions of the intermediate_chromosome 
    
    dim_intermediate_chromosome = intermediate_chromosome.shape 
    N = dim_intermediate_chromosome[0]

    ##Get the index for the population sort based on rank 
    index = index_sort_by_column(intermediate_chromosome, M+V)
    
    ##Now sort the individuals based on the index
    sorted_chromosome = np.zeros((N, dim_intermediate_chromosome[1]))
    for i in range (0, N):
        for j in range (0, dim_intermediate_chromosome[1]):
            sorted_chromosome[i,j] = intermediate_chromosome[int(round(index[i])),j]
    
    ##Find the maximum rank of the current population 
    rank = []
    for i in range (0, N):
        rank.append(sorted_chromosome[i, M+V])
    max_rank = max(rank)

    ##Start adding each front based on rank and crowding distance until the whole population is filled 
    f = np.zeros((pop, dim_intermediate_chromosome[1]))
    previous_index = 0
    for i in range (1, int(round(max_rank))):
        ##Get the index for current rank i.e. the last element in the sorted_chromosome with rank i
        current_index = int(round(find_max_index(sorted_chromosome, M+V, i)))
        
        ##Check to see if the population is fulled if all the individuals with rank i in added to the population
        if current_index > pop-1:
            ##If so, then find the number of individuals with current rank i 
            remaining = pop - previous_index
            ##get information about the individuals in the current rank i
            temp_pop = np.zeros((current_index+1-previous_index, dim_intermediate_chromosome[1]))
            
            for j in range (0, current_index - previous_index + 1):
                for k in range (0, dim_intermediate_chromosome[1]):
                    temp_pop[j,k] = sorted_chromosome[previous_index + j, k]
            ##Sort the individuals with rank i in the descending order based on the crowding distance 
            index = index_sort_by_column(temp_pop, M+V+1)
            index_rev = []
            for j in range (0, len(index)):
                index_rev.append(index[len(index)-1-j])
            
            ##Start filling individuals into the population in descending order until population is filled
            for j in range (0, remaining):
                for k in range (0, dim_intermediate_chromosome[1]):
                    f[previous_index+j,k] = temp_pop[int(round(index_rev[j])),k]

            return f
        
        elif current_index < pop-1:
            ##Add all the individuals with rank i into the population
            for j in range (0, current_index - previous_index + 1):
                for k in range (0, dim_intermediate_chromosome[1]):
                    f[previous_index + j,k] = sorted_chromosome[previous_index+j,k]
            ##Get the index for the lat added individual 
            previous_index = current_index+1 
    
        else:
            ##Add all the individuals with rank i into the population.
            for j in range (0, dim_intermediate_chromosome[1]):
                f[current_index, j] = sorted_chromosome[current_index, j]
            
            return f
            
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
                