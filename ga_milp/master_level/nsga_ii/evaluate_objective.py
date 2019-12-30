##Function to evaluate the objective functions for the given input vector x. x is an array of decision variables 
##and f(1), f(2), etc are the objective functions. The algorithm always minimizes the objective function hence if 
##you would like to maximize the function then multiply the function by negative one. M is the numebr of objective 
##functions and V is the number of decision variables.

##This functions is basically written by the user who defines his/her own objective function. Make sure that the M 
##and V matches your initial user input.

##An example objective function is given below. It has two six decision variables are two objective functions.

##Kursawe proposed by Frank Kursawe.
##Take a look at the following reference
##A variant of evolution strategies for vector optimization.
##In H. P. Schwefel and R. Männer, editors, Parallel Problem Solving from
##Nature. 1st Workshop, PPSN I, volume 496 of Lecture Notes in Computer
##Science, pages 193-197, Berlin, Germany, oct 1991. Springer-Verlag.

##Number of objective is two, while it can have arbirtarly many decision
##variables within the range -5 and 5. Common number of variables is 3.


def evaluate_objective(x, input_v):
    import sys
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\nsgaII_glpk_v1\\')
    import numpy as np
#    from math import exp, sqrt, fabs, sin
    from overall_exe import ecoenergies_opt
    
    V = input_v['V']
    objLength = input_v['M']

    obj = np.zeros((input_v['M'],1))
    
    ##Objective 1
    #val = 0
    
    val = ecoenergies_opt(x,V)    
    obj[0,0] = val

    ##Objective 2
    #val = 0

    obj[1,0] = val
    
    for i in range (0, objLength):
        if input_v['obj_func_values']['Value'][i] == 1:
            obj[i,0] = -1* obj[i,0]
    
    f = np.zeros((1, input_v['M']))

    for i in range (0, input_v['M']):
        f[0,i] = obj[i,0]

    ##Check for error 
    elem = f.shape
     
    if elem[1] != input_v['M']:
        print('The number of decision variables does not match you previous input. Kindly check your objective function')
        sys.exit()
    else:
       return f

#   for i in range (0, V-1):
#       val = val - 10*exp(-0.2*sqrt((pow(x[i],2)) + (pow(x[i+1],2))));
                                          
#   for i in range (0, V):
#       val = val + (pow(fabs(x[i]),0.8)) + 5*(pow(sin(x[i]),3))

                                         
 