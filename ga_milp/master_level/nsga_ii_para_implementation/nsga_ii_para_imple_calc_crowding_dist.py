##This function calculates the corresponding crowding distance for the sorted chromosomes 
def nsga_ii_para_imple_calc_crowding_dist (sorted_by_rank_chromosome, dominated_info, num_obj_func, num_var):
    
    ##sorted_by_rank_chromosome     ---     a numpy array with variable, objective function and rank values 
    ##dominated_info                ---     a dictionary containing information about how much an individual is dominated
    ##num_obj_func                  ---     the number of objectives 
    ##num_var                       ---     the number of variables 
    
    
    import os 
    current_path = os.path.dirname(os.path.abspath(__file__))[:-40] + '\\'
    import sys
    sys.path.append(current_path + 'master_level\\nsga_ii_para_implementation\\auxillary_functions\\')
    from auxillary_functions_nsga_ii_para_imple import index_sort_by_column    
    import numpy as np 
    
    ##Finding the dimensions 
    dim_sorted_by_rank_chromosome = sorted_by_rank_chromosome.shape  

    ##Initialize a counted 
    current_index = 0
    ##Finding the crowding distance for each individual in each front 
    z = np.zeros((dim_sorted_by_rank_chromosome[0], num_obj_func+num_var+2))
    dict1 = {}
    dict_obj_sorted = {}
    for front in range (1, len(dominated_info)):
        
        distance = 0
    
        dict1[front] = np.zeros((len(dominated_info[front]['f']), dim_sorted_by_rank_chromosome[1]))
        previous_index = current_index + 1
        
        for i in range (0, len(dominated_info[front]['f'])):
            for j in range (0, dim_sorted_by_rank_chromosome[1]):
                dict1[front][i,j] = sorted_by_rank_chromosome[current_index+i, j]
        
        current_index = current_index + 1 + i
        
        ##Sort each individual based on objective
        dict_obj_sorted[front] = {}
        for i in range (0, num_obj_func):
            
            dim = dict1[front].shape
            index_of_objectives = index_sort_by_column(dict1[front], num_var+i)
            dict_obj_sorted[front][i] = np.zeros((len(index_of_objectives), dim[1]))
            
            for j in range (0, len(index_of_objectives)):
                for k in range (0, dim[1]):
                    dict_obj_sorted[front][i][j,k] = dict1[front][int(round(index_of_objectives[j])), k]
        
            f_max = dict_obj_sorted[front][i][len(index_of_objectives)-1, num_var+i]
            f_min = dict_obj_sorted[front][i][0, num_var+i]
            
            temp = np.zeros((dim[0],1))
            temp[(int(round(index_of_objectives[len(index_of_objectives)-1]))), 0] = float('Inf')
            temp[(int(round(index_of_objectives[0]))), 0] = float('Inf')
            dict1[front] = np.concatenate((dict1[front],temp), axis=1)
        
            for j in range (1, len(index_of_objectives)-1):
                next_obj = dict_obj_sorted[front][i][j+1, num_var+i]
                prev_obj = dict_obj_sorted[front][i][j-1, num_var+i]
            
                if f_max - f_min == 0:
                    dict1[front][(int(round(index_of_objectives[j]))), num_obj_func+num_var+i+1] = float('Inf')
                else:
                    dict1[front][(int(round(index_of_objectives[j]))), num_obj_func+num_var+i+1] = (next_obj - prev_obj)/(f_max - f_min)

        distance = np.zeros((len(dominated_info[front]['f']),1))
        for i in range (0, num_obj_func):
            for j in range (0, len(dominated_info[front]['f'])):
                distance[j,0] = distance[j,0] + dict1[front][j, num_obj_func+num_var+i+1]
        
        dim1 = dict1[front].shape
        temp1 = dict1[front]
        dict1[front] = np.zeros((dim1[0],dim1[1]-num_obj_func))
        
        for i in range (0, dim1[1]-num_obj_func):
            for j in range (0, dim1[0]):
                dict1[front][j,i] = temp1[j,i]
        
        dict1[front] = np.concatenate((dict1[front], distance), axis=1)
        
        for i in range (previous_index-1, current_index):
            for j in range (0, num_obj_func+num_var+2):
                z[i,j] = dict1[front][i - previous_index,j]
    
    return z 

##Crowding distance
##The crowing distance is calculated as below
## • For each front Fi, n is the number of individuals.
##   – initialize the distance to be zero for all the individuals i.e. Fi(dj ) = 0,
##     where j corresponds to the jth individual in front Fi.
##   – for each objective function m
##       * Sort the individuals in front Fi based on objective m i.e. I =
##         sort(Fi,m).
##       * Assign infinite distance to boundary values for each individual
##         in Fi i.e. I(d1) = ? and I(dn) = ?
##       * for k = 2 to (n ? 1)
##           · I(dk) = I(dk) + (I(k + 1).m ? I(k ? 1).m)/fmax(m) - fmin(m)
##           · I(k).m is the value of the mth objective function of the kth
##             individual in I
    
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