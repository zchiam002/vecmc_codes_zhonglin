##This function handles all the backend operation for communicating with GLPK involving multi-objective 

def slave_convex_backend_v2 (files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice, obj_weights, time_steps):
    
    ##If the problem does not involve multi-time 
    if multi_time == 0:
        import sys
        sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\')
        from slave_convex_backend import slave_convex_backend
        
        obj_value, results, results_y = slave_convex_backend (files, multi_time, obj_func, package_name, parallel_thread_num, slave_models_location, bilinear_pieces, solver_choice)
        
        return obj_value, results, results_y
    
    ##If it involves a multi-time problem 
    else:
        import pandas as pd
        import sys
        sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\auxillary')                       ##Add directories to working directories 
        from get_values_models_v2 import get_values_models_v2
        sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers')
        sys.path.append(slave_models_location)
        from sorting_linear_and_bilinear_terms_v2 import sorting_linear_and_bilinear_terms_v2           ##This function is for checking only
        from sorting_linear_and_bilinear_terms_v3 import sorting_linear_and_bilinear_terms_v3           ##This function is similar to sorting_linear_and_bilinear_terms, with added storage capabilities
        from modifying_storage_for_multi_time import modifying_storage_for_multi_time
        from normalize_obj_funct_values import normalize_obj_funct_values
        from condense_multi_objective_into_one import condense_multi_objective_into_one
        from genscript_lp_format_v2 import genscript_lp_format_v2
        from lpsolver_runscript import lpsolver_runscript
        from extract_and_process_values_v2 import extract_and_process_values_v2
        from determine_ind_obj_func_value import determine_ind_obj_func_value
        
        ##Getting the values from the models
        layerslist, utilitylist, storagelist, processlist, streams, cons_eqns, cons_eqns_terms, thermal_loss = get_values_models_v2(files, package_name, parallel_thread_num, slave_models_location, time_steps) 
    
        ##Identifying streams affected by multi-time 
        streams = modifying_storage_for_multi_time (storagelist, streams, time_steps, thermal_loss)
        
        ##Linearizing the bilinear terms, for checking purposes only 
        ##ret_dataframes, affected_list = sorting_linear_and_bilinear_terms_v2 (layerslist, utilitylist, storagelist, processlist, streams, cons_eqns, cons_eqns_terms, obj_func, bilinear_pieces)
        
        ##'Normalizing' the objective function values 
        obj_func_scale_list = normalize_obj_funct_values (utilitylist, storagelist, processlist, obj_func, obj_weights, time_steps)
        
        ##Incorporating the weights into the common objective function    
        utilitylist_mono, storagelist_mono, processlist_mono, obj_func_mono = condense_multi_objective_into_one (utilitylist, storagelist, processlist, obj_func, obj_weights, obj_func_scale_list)
        
        ##Linearizing the bilinear terms,for the 'mono-objective' representation of the problem
        ret_dataframes, affected_list = sorting_linear_and_bilinear_terms_v3 (layerslist, utilitylist_mono, storagelist_mono, processlist_mono, streams, cons_eqns, cons_eqns_terms, obj_func_mono, bilinear_pieces)
        
        ##Save function for debug
        save_file = 'no'
        save_function_v2 (ret_dataframes, layerslist, utilitylist, storagelist, processlist, streams, cons_eqns, cons_eqns_terms, thermal_loss, save_file)
        
        obj_value = 0
        results = 0
        results_y = 0
        
        ##Generating linear program script in LP format 
        genscript_lp_format_v2(ret_dataframes, utilitylist_mono, storagelist_mono, processlist_mono, layerslist, parallel_thread_num, obj_func_mono, bilinear_pieces)
        
        ##Running LP solver 
        smooth, convergence = lpsolver_runscript(parallel_thread_num, solver_choice)
        
        ##The value of convergence can only be 1 or 0, 1 represents convergence, 0 otherwise
        if solver_choice == 'glpk':
            if convergence == 1:
                obj_value, results, results_y = extract_and_process_values_v2(ret_dataframes, utilitylist_mono, storagelist_mono, processlist_mono, bilinear_pieces, solver_choice, parallel_thread_num, affected_list)
            else:
                obj_value = 'na'
                results = 'na'
                results_y = 'na'
        elif solver_choice == 'gurobi':
            if convergence == 1:
                obj_value, results, results_y = extract_and_process_values_v2(ret_dataframes, utilitylist_mono, storagelist_mono, processlist_mono, bilinear_pieces, solver_choice, parallel_thread_num, affected_list)
            else:
                obj_value = 'na'
                results = 'na'
                results_y = 'na'    
                
        ##To calculate the original objective function values
        
        if obj_value != 'na':
            obj_func_table_dict, ind_obj_value = determine_ind_obj_func_value (utilitylist, storagelist, processlist, obj_func, obj_weights, obj_value, results, results_y)
        else:
            obj_func_table_dict = 'na'
            ind_obj_value = 'na'
                
        return obj_value, results, results_y, ind_obj_value, obj_func_table_dict
        
        
        
####################################################################################################################################################################################

##Additional functions

##This function saved the dataframes into csvfiles for checking purposes 
def save_function_v2 (ret_dataframes, layerslist, utilitylist, storagelist, processlist, streams, cons_eqns, cons_eqns_terms, thermal_loss, save_file):
    
    ##ret_dataframes = {}                                     --- it is a dictionary of dataframes
    ##ret_dataframes['utilitylist_bilinear']                  --- list of bilinear utilities 
    ##ret_dataframes['storagelist_bilinear']                  --- list of bilinear storages
    ##ret_dataframes['processlist_bilinear']                  --- list of bilinear processes
    ##ret_dataframes['streams_bilinear']                      --- list of bilinear streams 
    ##ret_dataframes['cons_eqns_terms_bilinear']              --- list of bilinear cons_eqns_terms
    ##ret_dataframes['utilitylist_linear']                    --- linear utility list 
    ##ret_dataframes['storagelist_linear']                    --- linear storage list
    ##ret_dataframes['processlist_linear']                    --- linear process list 
    ##ret_dataframes['streams_linear']                        --- linear streams list 
    ##ret_dataframes['cons_eqns_terms_linear']                --- linear cons_eqns_terms 
    ##ret_dataframes['cons_eqns_all']                         --- all cons_eqns
    
    ##layerslist --- the list of all the layers in the optimization problem 
    ##utilitylist --- the list of all the utilities 
    ##storagelist --- the list of all the storages
    ##processlist --- the list of all the processes
    ##streams --- the list of all the streams
    ##cons_eqns --- the list of all the additional constraints 
    ##cons_eqns_terms --- the list of all the terms in the additional constraints   
    ##thermal_loss --- the list of all thermal loss coefficients
    
    if save_file == 'yes':
        ret_dataframes['utilitylist_bilinear'].to_csv('C:\\Optimization_zlc\\01.utilitylist_bilinear_mono_Cinv.csv')
        ret_dataframes['storagelist_bilinear'].to_csv('C:\\Optimization_zlc\\02.storagelist_bilinear_mono_Cinv.csv')
        ret_dataframes['processlist_bilinear'].to_csv('C:\\Optimization_zlc\\03.processlist_bilinear_mono_Cinv.csv')
        ret_dataframes['streams_bilinear'].to_csv('C:\\Optimization_zlc\\04.streams_bilinear.csv')
        ret_dataframes['cons_eqns_terms_bilinear'].to_csv('C:\\Optimization_zlc\\05.cons_eqns_terms_bilinear.csv')
        ret_dataframes['utilitylist_linear'].to_csv('C:\\Optimization_zlc\\06.utilitylist_linear_mono_Cinv.csv')
        ret_dataframes['storagelist_linear'].to_csv('C:\\Optimization_zlc\\07.storagelist_linear_mono_Cinv.csv')
        ret_dataframes['processlist_linear'].to_csv('C:\\Optimization_zlc\\08.processlist_linear_mono_Cinv.csv')
        ret_dataframes['streams_linear'].to_csv('C:\\Optimization_zlc\\09.streams_linear.csv')
        ret_dataframes['cons_eqns_terms_linear'].to_csv('C:\\Optimization_zlc\\10.cons_eqns_terms_linear.csv')
        ret_dataframes['cons_eqns_all'].to_csv('C:\\Optimization_zlc\\11.cons_eqns_all.csv')
        
        layerslist.to_csv('C:\\Optimization_zlc\\12.layerslist_orginal.csv')
        utilitylist.to_csv('C:\\Optimization_zlc\\13.utilitylist_orginal.csv')
        storagelist.to_csv('C:\\Optimization_zlc\\14.storagelist_orginal.csv')
        processlist.to_csv('C:\\Optimization_zlc\\15.processlist_orginal.csv')
        streams.to_csv('C:\\Optimization_zlc\\16.streams_orginal.csv')
        cons_eqns.to_csv('C:\\Optimization_zlc\\17.cons_eqns_orginal.csv')
        cons_eqns_terms.to_csv('C:\\Optimization_zlc\\18.cons_eqns_terms_orginal.csv')  
        thermal_loss.to_csv('C:\\Optimization_zlc\\19.thermal_loss_orginal.csv')
    
    return 

