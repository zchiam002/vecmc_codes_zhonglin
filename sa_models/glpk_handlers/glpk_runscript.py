## Glpk scripting 

def glpk_runscript(input_dir, output_dir, file_format):
    from glpk_interface import glpk_interface
    
    ## Enter the directories
    
    solver_dir = 'C:\\Optimization_zlc\\winglpk-4.61\\glpk-4.61\\w64\\glpsol'
    
    ##Older entries 
    ##input_dir = 'C:\\Optimization_zlc\\glpk_handlers\\input_output\\data_set.txt'
    ##output_dir = 'C:\\Optimization_zlc\\glpk_handlers\\input_output\\glpk_output.txt'
    
    ## Using the solver 
    
    output = glpk_interface(solver_dir, input_dir, output_dir, file_format)
    
    return output










