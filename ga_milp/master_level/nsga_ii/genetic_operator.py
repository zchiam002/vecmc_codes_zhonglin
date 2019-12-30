##This function is utilized to produce offsprings from parent chromosomes. 
##The genetic operators corssover and mutation which are carried out with slight modifications from the original design. 
##For more information read
##the document enclosed. 
##
##parent_chromosome - the set of selected chromosomes.
##M - number of objective functions
##V - number of decision varaiables
##mu - distribution index for crossover (read the enlcosed pdf file)
##mum - distribution index for mutation (read the enclosed pdf file)
##l_limit - a vector of lower limit for the corresponding decsion variables
##u_limit - a vector of upper limit for the corresponding decsion variables
##
##The genetic operation is performed only on the decision variables, that
##is the first V elements in the chromosome vector. 

def nsga_ii_para_imple_genetic_operator(parent_chromosome, M, V, mu, mum, l_limit, u_limit, input_v):
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level\\NSGA_II\\add_functions\\')
    from identical_array import identical_array
    sys.path.append('C:\\Optimization_zlc\\master_level\\NSGA_II\\')
    from evaluate_objective import evaluate_objective 
    import numpy as np
    from random import uniform
    
    dim_parent_chromosome = parent_chromosome.shape
    N = dim_parent_chromosome[0]
    
    ##Flags wsed to set if crossover and mutation were actually performed 
    was_crossover = 0
    was_mutation = 0
    
    for i in range (0, N):
        ##With 90% probability perform crossover 
        if uniform(0,1) < 0.9:
            ##Initialize the children to be numm vectors 
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
            
            input_v['xAll'] = np.concatenate((input_v['xAll'] , [child_1]), axis=0)
            child_1_obj = evaluate_objective(child_1, input_v)
            input_v['objAll'] = np.concatenate((input_v['objAll'] ,child_1_obj), axis=0)
            
            input_v['xAll'] = np.concatenate((input_v['xAll'] ,[child_2]), axis=0)
            child_2_obj = evaluate_objective(child_2, input_v)
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
        
        ##With 10% probability perform mutation. Mutation is based on polynomial mutation 
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
            input_v['xAll'] = np.concatenate((input_v['xAll'] ,[child_3]), axis=0)
            child_3_obj = evaluate_objective(child_3, input_v)
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
