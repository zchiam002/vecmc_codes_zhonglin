##This function handles all the backend operation for communicating with GLPK

def slave_convex_backend(files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces):
    
    import pandas as pd
    import sys
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\auxillary')                       ##Add directories to working directories 
    from get_values_models import get_values_models
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers')
    sys.path.append(slave_models_location)
    from sorting_linear_and_bilinear_terms import sorting_linear_and_bilinear_terms
    from bilinear_continuous_x_continuous import bilinear_continuous_x_continuous
    from bilinear_continuous_x_binary import bilinear_continuous_x_binary 
    from genscript_lp_format import genscript_lp_format
    from lpsolver_runscript import lpsolver_runscript
    #from gurobi_output_extractor import gurboi_output_extractor 
    
    ##Getting the values from the models
    layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms = get_values_models(files, multi_time, package_name, parallel_thread_num, slave_models_location) 
    
    ##Identifying Bilinear and linear terms
    sorted_terms = sorting_linear_and_bilinear_terms(layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms)
    
    ##sorted_terms['objective_function_utility_bilinear']
    ##sorted_terms['dual_variable_constraint_utility_bilinear']
    ##sorted_terms['objective_function_utility_linear']
    ##sorted_terms['objective_function_process_bilinear']
    ##sorted_terms['dual_variable_constraint_process_bilinear']
    ##sorted_terms['objective_function_process_linear']
    ##sorted_terms['streams_bilinear']
    ##sorted_terms['streams_linear']
    ##sorted_terms['cons_eqn_terms_bilinear']
    ##sorted_terms['cons_eqn_terms_linear']
    
    ##Continuous x continuous type 
    continuous_x_continuous_terms = {}
    continuous_x_continuous_terms['objective_function_utility_bilinear'] = sorted_terms['objective_function_utility_bilinear']
    continuous_x_continuous_terms['dual_variable_constraint_utility_bilinear'] = sorted_terms['dual_variable_constraint_utility_bilinear']
    continuous_x_continuous_terms['objective_function_process_bilinear'] = sorted_terms['objective_function_process_bilinear']
    continuous_x_continuous_terms['dual_variable_constraint_process_bilinear'] = sorted_terms['dual_variable_constraint_process_bilinear']    
    continuous_x_continuous_terms['streams_bilinear'] = sorted_terms['streams_bilinear'] 
    continuous_x_continuous_terms['cons_eqn_terms_bilinear'] = sorted_terms['cons_eqn_terms_bilinear']   
    
    linearized_list = bilinear_continuous_x_continuous(continuous_x_continuous_terms, bilinear_pieces)

    ##linearized_list = {}
    ##linearized_list['obj_func_u_bilin_new'] = obj_func_u_bilin_new
    ##linearized_list['dual_v_c_util_bilin_new'] = dual_v_c_util_bilin_new
    ##linearized_list['obj_func_p_bilin_new'] = obj_func_p_bilin_new
    ##linearized_list['dual_v_c_proc_bilin_new'] = dual_v_c_proc_bilin_new
    ##linearized_list['streams_bilin_new'] = streams_bilin_new    
    ##linearized_list['cons_eqn_terms_bilin_new'] = cons_eqn_terms_bilin_new
    
    ##Continuous x binary type
    
    streams_bilin_contbin_new = bilinear_continuous_x_binary(streams, utilitylist, processlist) 
            
    ##Consolidating the original data into a dictionary 
    original_data = {}
    original_data['layerslist'] = layerslist
    original_data['utilitylist'] = utilitylist
    original_data['processlist'] = processlist
    original_data['streams'] = streams
    original_data['cons_eqns'] = cons_eqns
    original_data['cons_eqns_terms'] = cons_eqns_terms
    
    ##Generating linear program script in LP format 
    genscript_lp_format(original_data, sorted_terms, linearized_list, streams_bilin_contbin_new, parallel_thread_num, obj_func[0], bilinear_pieces)
    
#    layerslist.to_csv('C:\\Optimization_zlc\\01.layerslist.csv')    
#    utilitylist.to_csv('C:\\Optimization_zlc\\02.utilitylist.csv') 
#    processlist.to_csv('C:\\Optimization_zlc\\03.processlist.csv')  
#    streams.to_csv('C:\\Optimization_zlc\\04.streams.csv')    
#    cons_eqns.to_csv('C:\\Optimization_zlc\\05.cons_eqns.csv') 
#    cons_eqns_terms.to_csv('C:\\Optimization_zlc\\06.cons_eqns_terms.csv')
     
    sorted_terms['objective_function_utility_bilinear'].to_csv('C:\\Optimization_zlc\\07.objective_function_utility_bilinear.csv')    
    sorted_terms['dual_variable_constraint_utility_bilinear'].to_csv('C:\\Optimization_zlc\\08.dual_variable_constraint_utility_bilinear.csv') 
    sorted_terms['objective_function_utility_linear'].to_csv('C:\\Optimization_zlc\\09.objective_function_utility_linear.csv')    
    sorted_terms['objective_function_process_bilinear'].to_csv('C:\\Optimization_zlc\\10.objective_function_process_bilinear.csv')    
    sorted_terms['dual_variable_constraint_process_bilinear'].to_csv('C:\\Optimization_zlc\\11.dual_variable_constraint_process_bilinear.csv') 
    sorted_terms['objective_function_process_linear'].to_csv('C:\\Optimization_zlc\\12.objective_function_process_linear.csv')
    sorted_terms['streams_bilinear'].to_csv('C:\\Optimization_zlc\\13.streams_bilinear.csv')    
    sorted_terms['streams_linear'].to_csv('C:\\Optimization_zlc\\14.streams_linear.csv')    
    sorted_terms['cons_eqn_terms_bilinear'].to_csv('C:\\Optimization_zlc\\15.cons_eqn_terms_bilinear.csv') 
    sorted_terms['cons_eqn_terms_linear'].to_csv('C:\\Optimization_zlc\\16.cons_eqn_terms_linear.csv')        
    
    linearized_list['obj_func_u_bilin_new'].to_csv('C:\\Optimization_zlc\\17.obj_func_u_bilin_new.csv')
    linearized_list['dual_v_c_util_bilin_new'].to_csv('C:\\Optimization_zlc\\18.dual_v_c_util_bilin_new.csv')    
    linearized_list['obj_func_p_bilin_new'].to_csv('C:\\Optimization_zlc\\19.obj_func_p_bilin_new.csv')
    linearized_list['dual_v_c_proc_bilin_new'].to_csv('C:\\Optimization_zlc\\20.dual_v_c_proc_bilin_new.csv')   
    linearized_list['streams_bilin_new'].to_csv('C:\\Optimization_zlc\\21.streams_bilin_new.csv')
    linearized_list['cons_eqn_terms_bilin_new'].to_csv('C:\\Optimization_zlc\\22.cons_eqn_terms_bilin_new.csv')    
    
#    streams_bilin_contbin_new.to_csv('C:\\Optimization_zlc\\23.streams_bilin_contbin_new.csv')
    
    ##Running LP solver 
    #output, convergence = lpsolver_runscript(parallel_thread_num)
    
    ##The value of output can only be 1 or 0, if it is 0 everything is running smoothly
    ##The value of convergence can only be 1 or 0, 1 represents convergence, 0 otherwise
    
    ##Extracting units utilizations
    #dim_utilitylist = utilitylist.shape
    #dim_processlist = processlist.shape
    
    #units = []
    #for i in range (0, dim_utilitylist[0]):
    #    units.append(utilitylist['Name'][i])
    #for i in range (0, dim_processlist[0]):
    #    units.append(processlist['Name'][i])
    
    ##If the linear program is infeasible, this is the message communicated to the master solver else it will return the 
    ##objective function value and corresponding utilization rate of each of the units
    
    #if convergence == 1:
    #    util = pd.DataFrame(columns = ['Unit', 'Utilization'])
    #    obj_value, util = glpk_output_extractor(obj_func, units, util)
    #    return obj_value, util

    #if convergence == 0:
    #    util = pd.DataFrame(columns = ['Unit', 'Utilization'])
    #    obj_value = -1000
    #    return obj_value, util
    return linearized_list