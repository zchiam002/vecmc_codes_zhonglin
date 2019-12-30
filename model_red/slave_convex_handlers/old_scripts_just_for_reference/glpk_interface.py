## This is the interface to access lpsolver



##Creating the batch file 
def glpk_interface(solver_dir, input_dir, output_dir):
    import subprocess
    import os
    
    command = solver_dir + ' -lp ' + input_dir + ' -o ' + output_dir
    o = subprocess.check_call(command, shell= True)

    #time.sleep(0.5)

    ## Checking for the output of the solver 
    if not os.path.isfile(output_dir):
        #print ("No convergence")
        convergence = 0
        return o, convergence
    
    else:
        if os.path.getsize(output_dir) == 0:
            #print ("No convergence")
            convergence = 0
            return o, convergence
    
    with open(output_dir, 'r') as fo:
        solver_msg = fo.read()
    
    if 'OPTIMAL' in solver_msg:
        #print ("Ampl model converged!")
        convergence = 1
    
    else:
        #print ("No convergence")
        convergence = 0
    
    return o, convergence


