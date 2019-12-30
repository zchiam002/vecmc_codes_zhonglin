## Glpk scripting 

def lpsolver_runscript(thread_num, solver_choice):
    ##thread_num --- the associated parallel thread number 
    ##solver_choice ---the solver choice 
    
    if solver_choice == 'gurobi':
        smooth, convergence = gurobi_runscript (thread_num)
        
    elif solver_choice == 'glpk':
        smooth, convergence = glpk_runscript(thread_num)
    
    return smooth, convergence

############################################################################################################################################################################
##Additional functions 

##This function runs gurobi 
def gurobi_runscript (thread_num):
    import subprocess
    import os
    
    ##thread_num --- the parallel thread number
    
    ##Directories 
    main_call = 'gurobi_cl'
    result_file_call = 'ResultFile=C:\Optimization_zlc\slave_convex_handlers\solver_lp_format_holder' + r'\t' + 'hread_' + str(thread_num) + '\out.sol'
    file_location = 'C:\Optimization_zlc\slave_convex_handlers\solver_lp_format_holder' + r'\t' + 'hread_' + str(thread_num) + '\script_' + str(thread_num) + '.lp'
    result_location = 'C:\Optimization_zlc\slave_convex_handlers\solver_lp_format_holder' + r'\t' + 'hread_' + str(thread_num) + '\out.sol'
    
    command = main_call + ' ' + result_file_call + ' ' + file_location
    o = subprocess.check_call(command, shell= True)    
    
    output = 0
    ##Checking is the output file exists, if it does, there is convergence
    if os.path.isfile(result_location) == True:
        with open(result_location, 'r') as fo:
            solver_msg = fo.read()
        if 'Objective value' in solver_msg:
            output = 1
    
    return o, output

##This function runs glpk
def glpk_runscript(thread_num):
    import subprocess
    import os
    
    
    ##Directories 
    main_call = 'C:\Optimization_zlc\winglpk-4.61\glpk-4.61\w64\glpsol --lp'
    file_location = 'C:\Optimization_zlc\slave_convex_handlers\solver_lp_format_holder' + r'\t' + 'hread_' + str(thread_num) + '\script_' + str(thread_num) + '.lp'
    result_location = 'C:\Optimization_zlc\slave_convex_handlers\solver_lp_format_holder' + r'\t' + 'hread_' + str(thread_num) + '\out.txt'
    
    command = main_call + ' ' + file_location + ' -o ' + result_location

    o = subprocess.check_call(command, shell= True)
    ## Checking for the output of the solver 
    if os.path.isfile(result_location) == False:
        #print ("No convergence")
        convergence = 0
        return o, convergence
    
    else:
        if os.path.getsize(result_location) == 0:
            #print ("No convergence")
            convergence = 0
            return o, convergence
    
    with open(result_location, 'r') as fo:
        solver_msg = fo.read()
    
    if 'OPTIMAL' in solver_msg:
        #print ("Ampl model converged!")
        convergence = 1
    
    else:
        #print ("No convergence")
        convergence = 0
    
    return o, convergence



