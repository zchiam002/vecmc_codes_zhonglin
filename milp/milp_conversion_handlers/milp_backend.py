##This function handles all the backend operation for communicating with GLPK

def milp_backend(files, obj_func, parallel_thread_num, models_location, bilinear_pieces, solver_choice):
    
    ##files                     --- dataframe of all the file names of the models 
    ##obj_func                  --- the chosen objective function to be evaluated against 
    ##parallel_thread_num       --- unique parallel thread identifier
    ##models_location           --- the location of the models 
    ##bilinear_pieces           --- the number of bilinear pieces for linearization of bilinear variables 
    ##solver_choice             --- only GLPK is available for now
    
    import pandas as pd
    import os 
    current_path = os.path.dirname(__file__) + '//'  
    import sys 
    sys.path.append(current_path + 'auxillary//')
    sys.path.append(models_location)
    from get_values_models import get_values_models
    from sorting_linear_and_bilinear_terms import sorting_linear_and_bilinear_terms
    from genscript_lp_format import genscript_lp_format
    from lpsolver_runscript import lpsolver_runscript
    
    ##Initial inputs 
    save_file = 'yes'           ##Determine if the intermediate dataframes are to be saved or not
    
    ##Getting the values from the models 
    layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms = get_values_models(files, parallel_thread_num, models_location)     

    ##Linearizing the bilinear terms 
    ret_dataframes, affected_list = sorting_linear_and_bilinear_terms (layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms, obj_func, bilinear_pieces)    
    
    ##Saving the dataframes for checking 
    save_function (ret_dataframes, layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms, save_file)

    ##Generating linear program script in LP format 
    genscript_lp_format(ret_dataframes, utilitylist, processlist, layerslist, parallel_thread_num, obj_func, bilinear_pieces)
    
    ##Running the linear programming solver 
    smooth, convergence = lpsolver_runscript(parallel_thread_num, solver_choice)    

#    ##The value of convergence can only be 1 or 0, 1 represents convergence, 0 otherwise
#    if solver_choice == 'glpk':
#        if convergence == 1:
#            obj_value, results, results_y = extract_and_process_values(ret_dataframes, utilitylist, processlist, bilinear_pieces, solver_choice, parallel_thread_num, affected_list)
#        else:
#            obj_value = 'na'
#            results = 'na'
#            results_y = 'na'

   
    print(layerslist)
    import sys 
    sys.exit()
    
    return 

###############################################################################################################################################################################

##Additional functions

##This function saved the dataframes into csvfiles for checking purposes 
def save_function (ret_dataframes, layerslist, utilitylist, processlist, streams, cons_eqns, cons_eqns_terms, save_file):
    
    ##ret_dataframes                                          --- it is a dictionary of dataframes
    ##ret_dataframes['utilitylist_bilinear']                  --- list of bilinear utilities 
    ##ret_dataframes['processlist_bilinear']                  --- list of bilinear processes
    ##ret_dataframes['streams_bilinear']                      --- list of bilinear streams 
    ##ret_dataframes['cons_eqns_terms_bilinear']              --- list of bilinear cons_eqns_terms
    ##ret_dataframes['utilitylist_linear']                    --- linear utility list 
    ##ret_dataframes['processlist_linear']                    --- linear process list 
    ##ret_dataframes['streams_linear']                        --- linear streams list 
    ##ret_dataframes['cons_eqns_terms_linear']                --- linear cons_eqns_terms 
    ##ret_dataframes['cons_eqns_all']                         --- all cons_eqns
    
    ##layerslist                --- the list of all the layers in the optimization problem 
    ##utilitylist               --- the list of all the utilities 
    ##processlist               --- the list of all the processes
    ##streams                   --- the list of all the streams
    ##cons_eqns                 --- the list of all the additional constraints 
    ##cons_eqns_terms           --- the list of all the terms in the additional constraints     
    
    import os 
    current_path = os.path.dirname(__file__) + '//' 
    
    ##Determining the save path 
    save_path = current_path + 'save_dataframes//'
    
    if save_file == 'yes':
        ret_dataframes['utilitylist_bilinear'].to_csv(save_path + '01.utilitylist_bilinear.csv')
        ret_dataframes['processlist_bilinear'].to_csv(save_path + '02.processlist_bilinear.csv')
        ret_dataframes['streams_bilinear'].to_csv(save_path + '03.streams_bilinear.csv')
        ret_dataframes['cons_eqns_terms_bilinear'].to_csv(save_path + '04.cons_eqns_terms_bilinear.csv')
        ret_dataframes['utilitylist_linear'].to_csv(save_path + '05.utilitylist_linear.csv')
        ret_dataframes['processlist_linear'].to_csv(save_path + '06.processlist_linear.csv')
        ret_dataframes['streams_linear'].to_csv(save_path + '07.streams_linear.csv')
        ret_dataframes['cons_eqns_terms_linear'].to_csv(save_path + '08.cons_eqns_terms_linear.csv')
        ret_dataframes['cons_eqns_all'].to_csv(save_path + '09.cons_eqns_all.csv')
        
        layerslist.to_csv(save_path + '10.layerslist_orginal.csv')
        utilitylist.to_csv(save_path + '11.utilitylist_orginal.csv')
        processlist.to_csv(save_path + '12.processlist_orginal.csv')
        streams.to_csv(save_path + '13.streams_orginal.csv')
        cons_eqns.to_csv(save_path + '14.cons_eqns_orginal.csv')
        cons_eqns_terms.to_csv(save_path + '15.cons_eqns_terms_orginal.csv')  
    
    return 

    
