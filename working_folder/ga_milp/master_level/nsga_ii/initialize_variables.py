##This function initializes the chromosomes. Each chromosome has the followith at this stage
##      *set of decision variables 
##      *objective function values 
##where,
##N - Population size
##M - Number of objective functions
##V - Number of decision variables
##min_range - A vector of decimal values which indicate the minimum value
##for each decision variable.
##max_range - Vector of maximum possible values for decision variables.

def initialize_variables(input_v):
    from evaluate_objective import evaluate_objective 
    from random import uniform
    import numpy as np
    
    N = input_v['population']
    M = input_v['M']
    V = input_v['V']

    mini = input_v['min_range']
    maxi = input_v['max_range']

    K = M + V
    
    ##Initialize each chromosome 
    f_obj = np.zeros((N,M))             ##To only contain objective function values 
    f_x = np.zeros((N,V))               ##To contain only variables 
    
    for i in range (0, N):
        ##Initialize the decision variables based on the minimum and the maximum possible values.
        ##V is the number of decision variables. A random number is picked between the minimum and 
        ##maximum possible values for each decision variable.
            
        for j in range (0, V):
            f_x[i,j] = mini[j] + ((maxi[j] - mini[j])*uniform(0,1))
        
        ##For ease of computation and handling data the chromosome also has the value of the objective
        ##function concatenated at the end. The elements V + 1 to K has the objective function values.
        ##The function evaluate_objective takes one chromosome at a time, infact only the decision variables 
        ##are passed to the function along with information about the number of objective functions which are 
        ##processed and returns the value for the objective functions. These values are now stored at the end 
        ##of the chromosome itself.
        
        f_obj[i,:] = evaluate_objective(f_x[i,:], input_v)
        number = i + 1
        display_message = 'Initializing population ' + str(number) + ' of ' + str(N)
        print(display_message)
    
    input_v['objAll'] = f_obj
    input_v['xAll'] = f_x

    f_all = np.concatenate((f_x, f_obj), axis=1)       
    
    return f_all, input_v

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