##This function sort the current popultion based on non-domination. All the individuals in the first front are given 
##a rank of 1, the second front individuals are assigned rank 2 and so on. After assigning the rank the crowding in each 
##front is calculated.

def non_domination_sort_mod(x, M, V):
    import sys,os
    sys.path.append(os.path.dirname(__file__)+'\\add_functions')
    from index_sort_by_column import index_sort_by_column
    import numpy as np
    
    dim_x = x.shape 
    N = dim_x[0]
    
    ##Initialize the front number to 1.
    front = 1
    
    individual = {}
    F = {}
    F[front] = {}
    F[front]['f'] = []
    z = np.zeros((dim_x[0], M+V+2))
    
    collector = np.zeros((N,1))
    
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
    
    for i in range (0, N):
    
        individual[i] = {}
        ##Number of individuals that dominate this individual 
        individual[i]['n'] = 0
        ##Induviduals which this individual dominate 
        individual[i]['p'] = []
    
        for j in range (0, N):
            dom_less = 0
            dom_equal = 0
            dom_more = 0
            for k in range (0, M):
                if x[i, V+k] < x[j, V+k]:
                    dom_less = dom_less + 1
                elif x[i, V+k] == x[j, V+k]:
                    dom_equal = dom_equal + 1
                else: 
                    dom_more = dom_more + 1
            if (dom_less == 0) and (dom_equal != M):
                individual[i]['n'] = individual[i]['n'] + 1
            elif (dom_more == 0) and (dom_equal != M):
                individual[i]['p'].append(j)
    
        if individual[i]['n'] == 0:
            collector[i,0] = 1
            F[front]['f'].append(i)
    
    x = np.concatenate((x, collector), axis=1)
    
    ##Find subsequent fronts 
    while F[front]['f']:
        Q = []
        for i in range (0, len(F[front]['f'])):
            if individual[F[front]['f'][i]]['p']:
                for j in range (0, len(individual[F[front]['f'][i]]['p'])):
                    individual[individual[F[front]['f'][i]]['p'][j]]['n'] = individual[individual[F[front]['f'][i]]['p'][j]]['n'] - 1
                    if individual[individual[F[front]['f'][i]]['p'][j]]['n'] == 0:
                        x[individual[F[front]['f'][i]]['p'][j],M+V] = front + 1
                        Q.append(individual[F[front]['f'][i]]['p'][j])
    
        front = front + 1
        F[front] = {}
        F[front]['f'] = Q
    
    dim_x = x.shape
    index = index_sort_by_column(x, dim_x[1]-1)
    
    sorted_based_on_front = np.zeros((dim_x[0], dim_x[1]))
    for i in range (0, dim_x[0]):
        for j in range (0, dim_x[1]):
            sorted_based_on_front[i,j] = x[int(round(index[i])),j]
    
    current_index = 0
    
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
    
    ##Finding the crowding distance for each individual in each front 
    dict1 = {}
    dict_obj_sorted = {}
    for front in range (1, len(F)):
        
        distance = 0
    
        dict1[front] = np.zeros((len(F[front]['f']), dim_x[1]))
        previous_index = current_index + 1
        
        for i in range (0, len(F[front]['f'])):
            for j in range (0, dim_x[1]):
                dict1[front][i,j] = sorted_based_on_front[current_index+i, j]
        
        current_index = current_index + 1 + i
        
        ##Sort each individual based on objective
        dict_obj_sorted[front] = {}
        for i in range (0, M):
            
            dim = dict1[front].shape
            index_of_objectives = index_sort_by_column(dict1[front], V+i)
            dict_obj_sorted[front][i] = np.zeros((len(index_of_objectives), dim[1]))
            
            for j in range (0, len(index_of_objectives)):
                for k in range (0, dim[1]):
                    dict_obj_sorted[front][i][j,k] = dict1[front][int(round(index_of_objectives[j])), k]
        
            f_max = dict_obj_sorted[front][i][len(index_of_objectives)-1, V+i]
            f_min = dict_obj_sorted[front][i][0, V+i]
            
            temp = np.zeros((dim[0],1))
            temp[(int(round(index_of_objectives[len(index_of_objectives)-1]))), 0] = float('Inf')
            temp[(int(round(index_of_objectives[0]))), 0] = float('Inf')
            dict1[front] = np.concatenate((dict1[front],temp), axis=1)
        
            for j in range (1, len(index_of_objectives)-1):
                next_obj = dict_obj_sorted[front][i][j+1, V+i]
                prev_obj = dict_obj_sorted[front][i][j-1, V+i]
            
                if f_max - f_min == 0:
                    dict1[front][(int(round(index_of_objectives[j]))), M+V+i+1] = float('Inf')
                else:
                    dict1[front][(int(round(index_of_objectives[j]))), M+V+i+1] = (next_obj - prev_obj)/(f_max - f_min)

        distance = np.zeros((len(F[front]['f']),1))
        for i in range (0, M):
            for j in range (0, len(F[front]['f'])):
                distance[j,0] = distance[j,0] + dict1[front][j, M+V+i+1]
        
        dim1 = dict1[front].shape
        temp1 = dict1[front]
        dict1[front] = np.zeros((dim1[0],dim1[1]-M))
        
        for i in range (0, dim1[1]-M):
            for j in range (0, dim1[0]):
                dict1[front][j,i] = temp1[j,i]
        
        dict1[front] = np.concatenate((dict1[front], distance), axis=1)
        
        for i in range (previous_index-1, current_index):
            for j in range (0, M+V+2):
                z[i,j] = dict1[front][i - previous_index,j]
        
        f = z

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