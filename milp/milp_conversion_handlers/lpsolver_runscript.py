## Glpk scripting 

def lpsolver_runscript(thread_num, solver_choice):
    
    ##thread_num --- the associated parallel thread number 
    ##solver_choice ---the solver choice 

    import sys    
    
    if solver_choice == 'glpk':
        smooth, convergence = glpk_runscript(thread_num)
        
    else:
        print('Solver unavailable... ...')
        sys.exit()
    
    return smooth, convergence

############################################################################################################################################################################
##Additional functions 
    
##This function runs glpk solver
def glpk_runscript(thread_num):
    import subprocess
    import os
    current_path = os.path.dirname(__file__)[:-25] + '/' 
    
    ##Directories 
    main_call = current_path + 'winglpk-4.61\glpk-4.61\w64\glpsol --lp'
    file_location = current_path + 'milp_conversion_handlers\solver_lp_format_holder' + r'\t' + 'hread_' + str(thread_num) + '\script_' + str(thread_num) + '.lp'
    result_location = current_path + 'milp_conversion_handlers\solver_lp_format_holder' + r'\t' + 'hread_' + str(thread_num) + '\out.txt'
    
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


    


