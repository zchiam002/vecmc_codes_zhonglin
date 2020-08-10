##This function handles all the backend operation for communicating with GLPK

def glpk_backend(files, multi_time, obj_func):
    
    import pandas as pd
    import sys
    sys.path.append('C:\\Optimization_zlc\\glpk_handlers\\auxillary')                       ##Add directories to working directories 
    from get_values_models import get_values_models
    sys.path.append('C:\\Optimization_zlc\\glpk_handlers')
    from gen_glpkscript import gen_glpkscript
    from glpk_runscript import glpk_runscript
    from glpk_output_extractor import glpk_output_extractor 
    
    ##Getting the values from the models
    layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms = get_values_models(files,multi_time)

#    layerslist.to_csv('C:\\Optimization_zlc\\layerslist.csv')    
#    utilitylist.to_csv('C:\\Optimization_zlc\\utilitylist.csv')
#    processlist.to_csv('C:\\Optimization_zlc\\processlist.csv')
#    streams.to_csv('C:\\Optimization_zlc\\streams.csv')
#    cons_eqns.to_csv('C:\\Optimization_zlc\\cons_eqns.csv')
#    cons_eqns_terms.to_csv('C:\\Optimization_zlc\\cons_eqns_terms.csv')    


    ##Generating the script for using GLPK
    gen_glpkscript(layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms, obj_func)
    
    ##Running GLPK
    output, convergence = glpk_runscript()
    
    ##The value of output can only be 1 or 0, if it is 0 everything is running smoothly
    ##The value of convergence can only be 1 or 0, 1 represents convergence, 0 otherwise
    
    ##Extracting units utilizations
    dim_utilitylist = utilitylist.shape
    dim_processlist = processlist.shape
    
    units = []
    for i in range (0, dim_utilitylist[0]):
        units.append(utilitylist['Name'][i])
    for i in range (0, dim_processlist[0]):
        units.append(processlist['Name'][i])
    
    #layerslist.to_csv('C:\\Optimization_zlc\\layerslist.csv')    
    #utilitylist.to_csv('C:\\Optimization_zlc\\utilitylist.csv')
    #processlist.to_csv('C:\\Optimization_zlc\\processlist.csv')
    #streams.to_csv('C:\\Optimization_zlc\\streams.csv')
    #cons_eqns.to_csv('C:\\Optimization_zlc\\cons_eqns.csv')
    #cons_eqns_terms.to_csv('C:\\Optimization_zlc\\cons_eqns_terms.csv')
    
    ##If the linear program is infeasible, this is the message communicated to the master solver else it will return the 
    ##objective function value and corresponding utilization rate of each of the units
    
    if convergence == 1:
        util = pd.DataFrame(columns = ['Unit', 'Utilization'])
        obj_value, util = glpk_output_extractor(obj_func, units, util)
        return obj_value, util

    if convergence == 0:
        util = pd.DataFrame(columns = ['Unit', 'Utilization'])
        obj_value = -1000
        return obj_value, util
