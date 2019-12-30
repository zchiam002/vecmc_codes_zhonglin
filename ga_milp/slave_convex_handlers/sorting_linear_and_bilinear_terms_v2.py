
def sorting_linear_and_bilinear_terms_v2 (layerslist, utilitylist, processlist, storagelist, streams, cons_eqns, cons_eqns_terms, obj_func, bilinear_pieces):
    
    import pandas as pd
    
    ##layerslist --- the list of all the layers in the optimization problem 
    ##utilitylist --- the list of all the utilities 
    ##storagelist --- the list of all the storages
    ##processlist --- the list of all the processes
    ##streams --- the list of all the streams
    ##cons_eqns --- the list of all the additional constraints 
    ##cons_eqns_terms --- the list of all the terms in the additional constraints 
    ##obj_func --- the objective function selected for the slave 
    ##bilinear_pieces --- the number of bilinear pieces for the linearization of the bilinear terms 
    
    ##Initializing empty Dataframes for storage of the sorted data
    utilitylist_bilinear, storagelist_bilinear, processlist_bilinear, streams_bilinear, cons_eqns_bilinear, cons_eqns_terms_bilinear = generate_linear_lists_v2 ()
    utilitylist_linear, storagelist_linear, processlist_linear, streams_linear, cons_eqns_all, cons_eqns_terms_linear = generate_linear_lists_v2 ()
    
    ##Determining the units which are affected by bilinear relationships
    affected_list = detect_bilinear_variables_v2 (utilitylist, storagelist, processlist, streams, cons_eqns_terms, obj_func)
    
    ##Initializing a list to store names of cons_eqns to modify 
    unit_binary_names_to_modify = pd.DataFrame(columns = ['Name'])
    unit_binary_equality = pd.DataFrame(columns = ['Name'])
    
    
    ##Forming the linearized lists 
    dim_utilitylist = utilitylist.shape
    dim_storagelist = storagelist.shape
    dim_processlist = processlist.shape

    
    ##Determining the key for checking the objective function 
    key = obj_function_detect (obj_func)
    
    ##Handling the utility units first 
    list_type = 'utility'
    for i in range (0, dim_utilitylist[0]):      
        print(i)
        ##Checking if the entries contain any bilinear terms
        if scan_bilinear_affected_list(affected_list, utilitylist['Name'][i], 'cont_x_cont') == 'yes':
            ul_bilin_temp, s_bilin_temp, cq_bilin_temp, cet_bilin_temp, unit_binary_names_to_modify, unit_binary_equality = gen_bilinear_lp_relax_data (utilitylist, streams, cons_eqns, cons_eqns_terms, i, key, bilinear_pieces, unit_binary_names_to_modify, unit_binary_equality, list_type)
            utilitylist_bilinear = utilitylist_bilinear.append(ul_bilin_temp, ignore_index = True)
            streams_bilinear = streams_bilinear.append(s_bilin_temp, ignore_index = True)
            cons_eqns_bilinear = cons_eqns_bilinear.append(cq_bilin_temp, ignore_index = True)
            cons_eqns_terms_bilinear = cons_eqns_terms_bilinear.append(cet_bilin_temp, ignore_index = True)
        ##If not it is purely linear 
        else:
            ul_lin_temp, s_lin_temp, cet_lin_temp = gen_linear_lp_data (utilitylist, streams, cons_eqns, cons_eqns_terms, i, key)
            utilitylist_linear = utilitylist_linear.append(ul_lin_temp, ignore_index = True)
            streams_linear = streams_linear.append(s_lin_temp, ignore_index = True)            
            cons_eqns_terms_linear = cons_eqns_terms_linear.append(cet_lin_temp, ignore_index = True)
            
    ##Handling the storage units 
    list_type = 'storage'
    for i in range (0, dim_storagelist[0]):      
        ##Checking if the entries contain any bilinear terms
        if scan_bilinear_affected_list(affected_list, storagelist['Name'][i], 'cont_x_cont') == 'yes':
            sto_bilin_temp, s_bilin_temp, cq_bilin_temp, cet_bilin_temp, unit_binary_names_to_modify, unit_binary_equality = gen_bilinear_lp_relax_data (storagelist, streams, cons_eqns, cons_eqns_terms, i, key, bilinear_pieces, unit_binary_names_to_modify, unit_binary_equality, list_type)
            storagelist_bilinear = storagelist_bilinear.append(sto_bilin_temp, ignore_index = True)
            streams_bilinear = streams_bilinear.append(s_bilin_temp, ignore_index = True)
            cons_eqns_bilinear = cons_eqns_bilinear.append(cq_bilin_temp, ignore_index = True)
            cons_eqns_terms_bilinear = cons_eqns_terms_bilinear.append(cet_bilin_temp, ignore_index = True)
        ##If not it is purely linear 
        else:
            sto_lin_temp, s_lin_temp, cet_lin_temp = gen_linear_lp_data (storagelist, streams, cons_eqns, cons_eqns_terms, i, key)
            storagelist_linear = storagelist_linear.append(sto_lin_temp, ignore_index = True)
            streams_linear = streams_linear.append(s_lin_temp, ignore_index = True)            
            cons_eqns_terms_linear = cons_eqns_terms_linear.append(cet_lin_temp, ignore_index = True)    
            
    ##Handling the process units next 
    list_type = 'process'
    for i in range (0, dim_processlist[0]):
        ##Checking if the entries contain any bilinear terms
        if scan_bilinear_affected_list(affected_list, processlist['Name'][i], 'cont_x_cont') == 'yes':
            pro_bilin_temp, s_bilin_temp, cq_bilin_temp, cet_bilin_temp, unit_binary_names_to_modify, unit_binary_equality = gen_bilinear_lp_relax_data (processlist, streams, cons_eqns, cons_eqns_terms, i, key, bilinear_pieces, unit_binary_names_to_modify, unit_binary_equality, list_type)
            processlist_bilinear = processlist_bilinear.append(pro_bilin_temp, ignore_index = True)
            streams_bilinear = streams_bilinear.append(s_bilin_temp, ignore_index = True)
            cons_eqns_bilinear = cons_eqns_bilinear.append(cq_bilin_temp, ignore_index = True)
            cons_eqns_terms_bilinear = cons_eqns_terms_bilinear.append(cet_bilin_temp, ignore_index = True)
        ##If not it is purely linear 
        else:
            pro_lin_temp, s_lin_temp, cet_lin_temp = gen_linear_lp_data (processlist, streams, cons_eqns, cons_eqns_terms, i, key)
            processlist_linear = processlist_linear.append(pro_lin_temp, ignore_index = True)
            streams_linear = streams_linear.append(s_lin_temp, ignore_index = True)            
            cons_eqns_terms_linear = cons_eqns_terms_linear.append(cet_lin_temp, ignore_index = True)
   
    ##Handling the unit_binary_names_to_modify list 
    cons_eqns_new, additional_cons_eqns_term = modify_unit_binary_for_bilinear (unit_binary_names_to_modify, cons_eqns, cons_eqns_terms, cons_eqns_bilinear)
    
    ##Combining the cons_eqns_terms
    cons_eqns_all = cons_eqns_all.append(cons_eqns_bilinear, ignore_index = True)
    cons_eqns_all = cons_eqns_all.append(cons_eqns_new, ignore_index = True)
    
    ##Appending the new terms to the bilinear cons_eqns_terms 
    cons_eqns_terms_bilinear = cons_eqns_terms_bilinear.append(additional_cons_eqns_term, ignore_index = True)
    
    ##Placing the return values into a dictionary 
    ret_dataframes = {}
    ret_dataframes['utilitylist_bilinear'] = utilitylist_bilinear
    ret_dataframes['storagelist_bilinear'] = storagelist_bilinear
    ret_dataframes['processlist_bilinear'] = processlist_bilinear
    ret_dataframes['streams_bilinear'] = streams_bilinear
    ret_dataframes['cons_eqns_terms_bilinear'] = cons_eqns_terms_bilinear
    ret_dataframes['utilitylist_linear'] = utilitylist_linear
    ret_dataframes['storagelist_linear'] = storagelist_linear
    ret_dataframes['processlist_linear'] = processlist_linear
    ret_dataframes['streams_linear'] = streams_linear
    ret_dataframes['cons_eqns_terms_linear'] = cons_eqns_terms_linear
    ret_dataframes['cons_eqns_all'] = cons_eqns_all
         
    return ret_dataframes, affected_list


##############################################################################################################################################################

##Additional functions

##This function takes in the names of the list to modify and performs the modification accordingly 
def modify_unit_binary_for_bilinear (unit_binary_names_to_modify, cons_eqns, cons_eqns_terms, cons_eqns_bilinear):
    
    import pandas as pd 
    
    ##unit_binary_names_to_modify --- a list of all the names to modify 
    ##cons_eqns --- the list of equations 
    ##cons_eqns_terms --- the list of terms in the original cons_eqns_terms
    ##cons_eqns_bilinear --- the list of all the bilinear cons_eqns
    ##unit_binary_equality --- the list of unit_binary_equality terms to add
    
    ##Initiating a dataframe to hold the return values 
    ret_values_bilin_ub_terms = pd.DataFrame(columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
    
    dim_unit_binary_names_to_modify = unit_binary_names_to_modify.shape
    dim_cons_eqns_terms = cons_eqns_terms.shape
    dim_cons_eqns_bilinear = cons_eqns_bilinear.shape
            
    ##Need to add the terms to it, for now only the unit_binary type is affected 
    for i in range (0, dim_unit_binary_names_to_modify[0]):
        temp_eqn_name = unit_binary_names_to_modify['Name'][i]
        ##Now determine the type of the associated equation 
        eqn_type = determine_eqn_type (temp_eqn_name, cons_eqns)
        if eqn_type == 'unit_binary':
            for j in range (0, dim_cons_eqns_terms[0]):
                if cons_eqns_terms['Parent_eqn'][j] == temp_eqn_name:
                    var_name_u = cons_eqns_terms['Parent_unit'][j]
                    temp_data = [var_name_u, cons_eqns_terms['Parent_unit'][j], cons_eqns_terms['Parent_eqn'][j], cons_eqns_terms['Parent_stream'][j], cons_eqns_terms['Coefficient'][j], 0, 0]
                    temp_df = pd.DataFrame(data = [temp_data], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
                    ret_values_bilin_ub_terms = ret_values_bilin_ub_terms.append(temp_df, ignore_index = True)
                    
    ##Need to add parent terms to the '_uv_activated' equations 
    for i in range (0, dim_cons_eqns_bilinear[0]):
        if '_uv_activated' in cons_eqns_bilinear['Name'][i]:
            var_name_temp = cons_eqns_bilinear['Name'][i]
            var_name_temp = var_name_temp.replace('_uv_activated', '')
            temp_data = [var_name_temp, var_name_temp, cons_eqns_bilinear['Name'][i], '-', -2, 0, 0]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
            ret_values_bilin_ub_terms = ret_values_bilin_ub_terms.append(temp_df, ignore_index = True)            
                    
    return cons_eqns, ret_values_bilin_ub_terms

##This function deals with purely linear data 
def gen_linear_lp_data (utilityproclist, streams, cons_eqns, cons_eqns_terms, index, key):

    import pandas as pd
        
    ##utilityproclist --- either utility, storage or processlist 
    ##streams --- the list of streams 
    ##cons_eqns --- the list of additional constraints 
    ##cons_eqns_terms --- the list of additional constraints 
    ##index --- the associated index
    ##key --- list of objective functions which were chosen 
    
    ##Generating linear lists for return values 
    ul_lin, sto_lin, pl_lin, s_lin, cq_lin, cet_lin = generate_linear_lists_v2 ()
    
    ##Filling up the first variable 
    ##The constant term is placed with the first variable 
    variable_name = 'Variable1'
    temp_df = fill_obj_func_values (key, utilityproclist, index, variable_name)
    ul_lin = ul_lin.append(temp_df, ignore_index = True)
    ##Filling up the second variable 
    if utilityproclist['Variable2'][index] != '-':
        variable_name = 'Variable2'
        temp_df = fill_obj_func_values (key, utilityproclist, index, variable_name)
        ul_lin = ul_lin.append(temp_df, ignore_index = True)
        
    ##Handling the streams 
    dim_streams = streams.shape
    for i in range (0, dim_streams[0]):
        if streams['Parent'][i] == utilityproclist['Name'][index]:
            ##Handling variable 1 first 
            ##The constant term is placed with the first variable
            data_temp = [streams['Parent'][i], utilityproclist['Variable1'][index], streams['Type'][i], streams['Name'][i], streams['Layer'][i], streams['Stream_coeff_cst'][i], streams['Stream_coeff_v1_1'][i], streams['InOut'][i]]
            temp_df = pd.DataFrame(data = [data_temp], columns = ['Parent', 'Variable', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
            s_lin = s_lin.append(temp_df, ignore_index = True)
            ##Handling variable 2 next 
            if utilityproclist['Variable2'][index] != '-':
                data_temp = [streams['Parent'][i], utilityproclist['Variable2'][index], streams['Type'][i], streams['Name'][i], streams['Layer'][i], 0, streams['Stream_coeff_v2_1'][i], streams['InOut'][i]]
                temp_df = pd.DataFrame(data = [data_temp], columns = ['Parent', 'Variable', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
                s_lin = s_lin.append(temp_df, ignore_index = True)                
    
    ##Handling the cons_eqn_terms 
    dim_cons_eqns_terms = cons_eqns_terms.shape
    for i in range (0, dim_cons_eqns_terms[0]):
        if cons_eqns_terms['Parent_unit'][i] == utilityproclist['Name'][index]:
            ##Determine the type of constraint 
            cons_type = check_constraint_type(cons_eqns, cons_eqns_terms['Parent_eqn'][i])
            if cons_type == 'stream_limit_modified':
                ##Handling variable 1 first 
                ##The constant term is placed with the first variable
                data_temp = [utilityproclist['Variable1'][index], utilityproclist['Name'][index], cons_eqns_terms['Parent_eqn'][i], cons_eqns_terms['Parent_stream'][i], 0, cons_eqns_terms['Coeff_v1_1'][i], cons_eqns_terms['Coeff_cst'][i]]
                data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
                cet_lin = cet_lin.append(data_temp_df, ignore_index = True)
                ##Handling variable 2 next 
                if utilityproclist['Variable2'][index] != '-':  
                    data_temp = [utilityproclist['Variable2'][index], utilityproclist['Name'][index], cons_eqns_terms['Parent_eqn'][i], cons_eqns_terms['Parent_stream'][i], 0, cons_eqns_terms['Coeff_v2_1'][i], 0]
                    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
                    cet_lin = cet_lin.append(data_temp_df, ignore_index = True)
            elif cons_type == 'unit_binary':
                ##Just append 
                data_temp = ['-', utilityproclist['Name'][index], cons_eqns_terms['Parent_eqn'][i], cons_eqns_terms['Parent_stream'][i], 1, 0, 0]
                data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
                cet_lin = cet_lin.append(data_temp_df, ignore_index = True)   
                              
    return ul_lin, s_lin, cet_lin

##A function to determine the parameters linearized bilinear variables 
def gen_bilinear_lp_relax_data (utilitystoproclist, streams, cons_eqns, cons_eqns_terms, index, key, bilinear_pieces, unit_binary_names_to_modify, unit_binary_equality, list_type):
    
    import pandas as pd
    
    ##utilitystoproclist --- either utility, storage or processlist 
    ##streams --- the list of streams 
    ##cons_eqns --- the list of additional constraints 
    ##cons_eqns_terms --- the list of additional constraints 
    ##index --- the associated index
    ##key --- list of objective functions which were chosen 
    ##bilinear_pieces --- the number of bilinear pieces 
    ##unit_binary_names_to_modify -- a record of binary names to modify
    ##unit_binary_equality --- a record of binary equality terms to add
    ##list_type --- utility or process
    
    ##Generating linear lists for return values 
    ul_bilin, sto_bilin, pl_bilin, s_bilin, cq_bilin, cet_bilin = generate_linear_lists_v2 ()
    
    ##Determine the lower and upper bound of u and v 
    u_overall_min = utilitystoproclist['Fmin_v1'][index] + utilitystoproclist['Fmin_v2'][index]
    u_overall_max = utilitystoproclist['Fmax_v1'][index] + utilitystoproclist['Fmax_v2'][index]
    v_overall_min = utilitystoproclist['Fmin_v1'][index] - utilitystoproclist['Fmax_v2'][index]
    v_overall_max = utilitystoproclist['Fmax_v1'][index] - utilitystoproclist['Fmin_v2'][index]
    
    ##Step_increment 
    u_step = (u_overall_max - u_overall_min) / bilinear_pieces
    v_step = (v_overall_max - v_overall_min) / bilinear_pieces
    
    ##Creating a dataframe for new cons_eqns types to be added on 
    cons_eqns_add = pd.DataFrame(columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    
    ##Finding the gradient and the intercept of each bilinear piece
    for i in range (0, bilinear_pieces):
        
        ##Variable name
        var_name_u = utilitystoproclist['Name'][index] + '_u' + str(i)
        var_name_v = utilitystoproclist['Name'][index] + '_v' + str(i)
        
        ##Initial coefficients for the objective functions
        x_coeff_new = []
        y_coeff_new = []
        bilin_coeff_new = []
        cst_new = []
        
        for j in range (0, len(key)):
            x_coeff_new.append(utilitystoproclist[key[j] + '_v1_1'][index] )
            y_coeff_new.append(utilitystoproclist[key[j] + '_v2_1'][index])
            bilin_coeff_new.append(utilitystoproclist[key[j] + '_v1_v2'][index])
            cst_new.append(utilitystoproclist[key[j] + '_cst'][index])
        
        ##Handling u values first 
        u_min = (i * u_step) + u_overall_min
        u_max = ((i + 1) * u_step) + u_overall_min
        fu_min = 0.25 * pow(u_min, 2)
        fu_max = 0.25 * pow(u_max, 2)
        u_grad = (fu_max - fu_min) / (u_max - u_min)
        u_int = fu_max - (u_grad * u_max)

        ##Handling v values next 
        v_min = (i * v_step) + v_overall_min
        v_max = ((i + 1) * v_step) + v_overall_min
        fv_min = 0.25 * pow(v_min, 2)
        fv_max = 0.25 * pow(v_max, 2)
        v_grad = (fv_max - fv_min) / (v_max - v_min)
        v_int = fv_max - (v_grad * v_max)
     
        ##Converting the whole equation in terms of only u and v 
        u_coeff_new = []
        u_cst_new = []
        v_coeff_new = []
        v_cst_new = []
        
        for j in range (0, len(key)):
            u_coeff_new.append((x_coeff_new[j] / 2) + (y_coeff_new[j] / 2) + (bilin_coeff_new[j] * u_grad))
            u_cst_new.append((bilin_coeff_new[j] * u_int) + cst_new[j] )
            v_coeff_new.append((x_coeff_new[j] / 2) - (y_coeff_new[j] / 2) - (bilin_coeff_new[j] * v_grad))
            v_cst_new.append((-1 * bilin_coeff_new[j] * v_int))
        
        ##Writing the data to the new linear dataframe 
            ##Handling u values first
            
        temp_df = fill_obj_func_values_lin_bilin (key, u_coeff_new, u_cst_new, utilitystoproclist['Name'][index], var_name_u, u_min, u_max) 
        ul_bilin = ul_bilin.append(temp_df, ignore_index = True)
            ##Handling v values next 
            
        temp_df = fill_obj_func_values_lin_bilin (key, v_coeff_new, v_cst_new, utilitystoproclist['Name'][index], var_name_v, v_min, v_max)
        ul_bilin = ul_bilin.append(temp_df, ignore_index = True)
        
        ##Scanning through the streams 
        temp_streams =  convert_streams_variables_linear (streams, utilitystoproclist['Name'][index], var_name_u, var_name_v, u_grad, u_int, v_grad, v_int)
        s_bilin = s_bilin.append(temp_streams, ignore_index = True)
        
        ##Modifying the constraint
        cons_eqns_add, ret_cons_eqns_terms_lin, unit_binary_names_to_modify, unit_binary_equality = convert_constraint_variables_linear (utilitystoproclist, cons_eqns_terms, cons_eqns_add, utilitystoproclist['Name'][index], var_name_u, var_name_v, u_grad, u_int, v_grad, v_int, unit_binary_names_to_modify, unit_binary_equality, cons_eqns, list_type)
        cet_bilin = cet_bilin.append(ret_cons_eqns_terms_lin, ignore_index = True)
    
    ##Modifying the cons_eqn list 
    cq_bilin = cq_bilin.append(cons_eqns_add, ignore_index = True)
    
    return ul_bilin, s_bilin, cq_bilin, cet_bilin, unit_binary_names_to_modify, unit_binary_equality

##A function to deal with the additional constraints of the linearization of bilinear variables
def convert_constraint_variables_linear (utilityproclist, cons_eqns_terms, cons_eqns_add, parent, u_name, v_name, u_grad, u_int, v_grad, v_int, unit_binary_names_to_modify, unit_binary_equality, cons_eqns, list_type):

    import sys
    import pandas as pd 
    
    eps = sys.float_info.epsilon

    ##utilityproclist --- either utility, storage or processlist 
    ##cons_eqns_terms --- the list of all the streams 
    ##cons_eqns_add --- a list of additional constraints to be added
    ##parent --- the name of the parent unit 
    ##u_name --- the name of the newly introduced u variable 
    ##v_name --- the name of the newly introduced v variable
    ##u_grad --- the associated gradient of the u variable 
    ##u_int --- the associated intercept of the u variable 
    ##v_grad --- the associated gradient of the v variable 
    ##v_int --- the associated intercept of the v variable 
    ##unit_binary_names_to_modify --- a dataframe containing names of 'unit_binary' constraints to be modified
    ##unit_binary_equality --- a dataframe containing names of 'unit_binary_equality' constraints to be modified 
    ##cons_eqns --- a list of all the additional constraints 
    ##list_type --- utility or process
    
    ##Initialize a temporary dataframe to hold the return values 
    ret_cons_eqns_terms_lin = pd.DataFrame(columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
    
    
    ##Adding the constraint such that only 1 u/v of the parent are activated at all times   
    ##Handling u values terms 
    new_eqn_name_u = parent + '_u_activated'
    new_eqn_type_u = 'unit_binary'   
    ##Checking if the new equation has be initialized, if not, add it
    check_list = cons_eqns_add['Name'][:]
    check_indicator = check_if_exists(new_eqn_name_u, check_list)
    if check_indicator == 0:
        if (list_type == 'utility') or (list_type == 'storage'):
            data_temp = [new_eqn_name_u, new_eqn_type_u, 'less_than_equal_to', 1]
        elif list_type == 'process':
            data_temp = [new_eqn_name_u, new_eqn_type_u, 'equal_to', 1]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Type', 'Sign', 'RHS_value']) 
        cons_eqns_add = cons_eqns_add.append(temp_df, ignore_index = True)
    data_temp = [u_name, parent, new_eqn_name_u, '-', 1, 0, 0]
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
    ret_cons_eqns_terms_lin = ret_cons_eqns_terms_lin.append(temp_df, ignore_index = True)   
    ##Handling v values terms 
    new_eqn_name_v = parent + '_v_activated'
    new_eqn_type_v = 'unit_binary'   
    ##Checking if the new equation has be initialized, if not, add it
    check_list = cons_eqns_add['Name'][:]
    check_indicator = check_if_exists(new_eqn_name_v, check_list)
    if check_indicator == 0:
        if (list_type == 'utility') or (list_type == 'storage'):
            data_temp = [new_eqn_name_v, new_eqn_type_v, 'less_than_equal_to', 1]
        elif list_type == 'process':
            data_temp = [new_eqn_name_u, new_eqn_type_u, 'equal_to', 1]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Type', 'Sign', 'RHS_value']) 
        cons_eqns_add = cons_eqns_add.append(temp_df, ignore_index = True)
    data_temp = [v_name, parent, new_eqn_name_v, '-', 1, 0, 0]
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
    ret_cons_eqns_terms_lin = ret_cons_eqns_terms_lin.append(temp_df, ignore_index = True)            
    
    
    ##Adding the constraint such that if 1 u and 1 v are in sync, not needed for processes
    if (list_type == 'utility') or (list_type == 'storage'):
        new_eqn_name = parent + '_uv_activated'
        new_eqn_type = 'unit_binary_equality'   
        ##Checking if the new equation has be initialized, if not, add it
        check_list = cons_eqns_add['Name'][:]
        check_indicator = check_if_exists(new_eqn_name, check_list)
        if check_indicator == 0:
            data_temp = [new_eqn_name, new_eqn_type, 'equal_to', 0]
            temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Type', 'Sign', 'RHS_value'])   
            cons_eqns_add = cons_eqns_add.append(temp_df, ignore_index = True)
        ##Handling u values terms
        data_temp = [u_name, parent, new_eqn_name, '-', 1, 0, 0]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
        ret_cons_eqns_terms_lin = ret_cons_eqns_terms_lin.append(temp_df, ignore_index = True)   
        ##Handling the v values terms     
        data_temp = [v_name, parent, new_eqn_name, '-', 1, 0, 0]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
        ret_cons_eqns_terms_lin = ret_cons_eqns_terms_lin.append(temp_df, ignore_index = True)      

    ##Adding constraints if there are present in the unit definition 
    dim_utilityproclist = utilityproclist.shape
    
    for i in range (0, dim_utilityproclist[0]):
        if utilityproclist['Name'][i] == parent:
            sum_coeff = abs(utilityproclist['Coeff_v1_2'][i]) + abs(utilityproclist['Coeff_v1_1'][i]) + abs(utilityproclist['Coeff_v2_2'][i]) + abs(utilityproclist['Coeff_v2_1'][i]) + abs(utilityproclist['Coeff_cst'][i])
            fmin_new = utilityproclist['Fmin'][i]
            fmax_new = utilityproclist['Fmax'][i]
            if sum_coeff > eps:
                ##We need to introduce another constraint known as bilinear limits
                ##Initial coefficients for the constraint 
                x_coeff = utilityproclist['Coeff_v1_1'][i] 
                y_coeff = utilityproclist['Coeff_v2_1'][i]
                bilin_coeff = utilityproclist['Coeff_v1_v2'][i]
                cst = utilityproclist['Coeff_cst'][i]  
                
                ##Handling fmin first 
                if (list_type == 'utility') or (list_type == 'storage'):                
                    new_eqn_name = parent + '_bilin_cons_fmin'
                    new_eqn_type = 'bilinear_limits_fmin_util'
                        
                    check_list = cons_eqns_add['Name'][:]
                    check_indicator = check_if_exists(new_eqn_name, check_list)
                    if check_indicator == 0:                    
                        data_temp = [new_eqn_name, new_eqn_type, 'greater_than_equal_to', fmin_new]
                        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
                        cons_eqns_add = cons_eqns_add.append(temp_df, ignore_index = True)
                    ##Handling u values terms
                    u_coeff = (x_coeff / 2) + (y_coeff / 2) + (bilin_coeff * u_grad)
                    u_cst = (bilin_coeff * u_int) + cst                                     ##Absorbed the coefficient of the main equation
                    data_temp = [u_name, parent, new_eqn_name, '-', 0, u_coeff, u_cst]
                    temp_df = pd.DataFrame(data = [data_temp], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
                    ret_cons_eqns_terms_lin = ret_cons_eqns_terms_lin.append(temp_df, ignore_index = True) 
                    ##Handling v values terms 
                    v_coeff = (x_coeff / 2) - (y_coeff / 2) - (bilin_coeff * v_grad)
                    v_cst = (-1 * bilin_coeff * v_int)                  
                    data_temp = [v_name, parent, new_eqn_name, '-', 0, v_coeff, v_cst]
                    temp_df = pd.DataFrame(data = [data_temp], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
                    ret_cons_eqns_terms_lin = ret_cons_eqns_terms_lin.append(temp_df, ignore_index = True)    
            
                ##Handling fmax next
                new_eqn_name = parent + '_bilin_cons_fmax'
                if (list_type == 'utility') or (list_type == 'storage'):
                    new_eqn_type = 'bilinear_limits_fmax_util'
                elif list_type == 'process':
                    new_eqn_type = 'bilinear_limits_fmax_proc'
                
                check_list = cons_eqns_add['Name'][:]
                check_indicator = check_if_exists(new_eqn_name, check_list)
                if check_indicator == 0:
                    data_temp = [new_eqn_name, new_eqn_type, 'less_than_equal_to', fmax_new]
                    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Type', 'Sign', 'RHS_value'])
                    cons_eqns_add = cons_eqns_add.append(temp_df, ignore_index = True)
                ##Handling u values terms
                u_coeff = (x_coeff / 2) + (y_coeff / 2) + (bilin_coeff * u_grad)
                u_cst = (bilin_coeff * u_int) + cst                                     ##Absorbed the coefficient of the main equation 
                data_temp = [u_name, parent, new_eqn_name, '-', 0, u_coeff, u_cst]
                temp_df = pd.DataFrame(data = [data_temp], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
                ret_cons_eqns_terms_lin = ret_cons_eqns_terms_lin.append(temp_df, ignore_index = True) 
                ##Handling v values terms 
                v_coeff = (x_coeff / 2) - (y_coeff / 2) - (bilin_coeff * v_grad)
                v_cst = (-1 * bilin_coeff * v_int)                  
                data_temp = [v_name, parent, new_eqn_name, '-', 0, v_coeff, v_cst]
                temp_df = pd.DataFrame(data = [data_temp], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
                ret_cons_eqns_terms_lin = ret_cons_eqns_terms_lin.append(temp_df, ignore_index = True) 

            break                                        
                    
    ##Modifying the unit_binary constraint if there are any 
    dim_cons_eqns_terms = cons_eqns_terms.shape
    dim_cons_eqns = cons_eqns.shape
    
    for i in range (0, dim_cons_eqns_terms[0]):
        if cons_eqns_terms['Parent_unit'][i] == parent:
            for j in range (0, dim_cons_eqns[0]):
                if (cons_eqns['Name'][j] == cons_eqns_terms['Parent_eqn'][i]) and (cons_eqns['Type'][j] == 'unit_binary'):
                    ##Checking to see if it is already entered
                    check_list = unit_binary_names_to_modify['Name'][:]
                    check_indicator = check_if_exists(cons_eqns_terms['Parent_eqn'][i], check_list)
                    if check_indicator == 0:
                        temp_data = [cons_eqns_terms['Parent_eqn'][i]]
                        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name'])
                        unit_binary_names_to_modify = unit_binary_names_to_modify.append(temp_df, ignore_index = True)
                    break
                
    for i in range (0, dim_cons_eqns_terms[0]):
        if cons_eqns_terms['Parent_unit'][i] == parent:
            for j in range (0, dim_cons_eqns[0]):
                if (cons_eqns['Name'][j] == cons_eqns_terms['Parent_eqn'][i]) and (cons_eqns['Type'][j] == 'unit_binary'):
                    ##Checking to see if it is already entered
                    check_list = unit_binary_equality['Name'][:]
                    check_indicator = check_if_exists(cons_eqns_terms['Parent_eqn'][i], check_list)
                    if check_indicator == 0:
                        temp_data = [cons_eqns_terms['Parent_eqn'][i]]
                        temp_df = pd.DataFrame(data = [temp_data], columns = ['Name'])
                        unit_binary_equality = unit_binary_equality.append(temp_df, ignore_index = True)
                    break
                            
    ##Modifying the stream_limit_modified constraint if there are any 
    for i in range (0, dim_cons_eqns_terms[0]):
        if cons_eqns_terms['Parent_unit'][i] == parent:
            sum_coeff = abs(cons_eqns_terms['Coeff_v1_2'][i]) + abs(cons_eqns_terms['Coeff_v1_1'][i]) + abs(cons_eqns_terms['Coeff_v2_2'][i]) + abs(cons_eqns_terms['Coeff_v2_1'][i]) + abs(cons_eqns_terms['Coeff_cst'][i])
            if sum_coeff > eps:
                x_coeff = cons_eqns_terms['Coeff_v1_1'][i] 
                y_coeff = cons_eqns_terms['Coeff_v2_1'][i]
                bilin_coeff = cons_eqns_terms['Coeff_v1_v2'][i]
                cst = cons_eqns_terms['Coeff_cst'][i]
                
                ##Converting the whole equation in terms of only u and v 
                u_coeff = (x_coeff / 2) + (y_coeff / 2) + (bilin_coeff * u_grad)
                u_cst = (bilin_coeff * u_int) + cst                                     ##Absorbed the coefficient of the main equation 
                v_coeff = (x_coeff / 2) - (y_coeff / 2) - (bilin_coeff * v_grad)
                v_cst = (-1 * bilin_coeff * v_int)
                              
                ##Writing the data to the new linear dataframe
                    ##Handling the u_values first 
                temp_data = [u_name, parent, cons_eqns_terms['Parent_eqn'][i], cons_eqns_terms['Parent_stream'][i], 0, u_coeff, u_cst]
                temp_df = pd.DataFrame(data = [temp_data], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])  
                ret_cons_eqns_terms_lin = ret_cons_eqns_terms_lin.append(temp_df, ignore_index = True)
                    ##Handling the v_values now 
                temp_data = [v_name, parent, cons_eqns_terms['Parent_eqn'][i], cons_eqns_terms['Parent_stream'][i], 0, v_coeff, v_cst]
                temp_df = pd.DataFrame(data = [temp_data], columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])  
                ret_cons_eqns_terms_lin = ret_cons_eqns_terms_lin.append(temp_df, ignore_index = True)
    
    return cons_eqns_add, ret_cons_eqns_terms_lin, unit_binary_names_to_modify, unit_binary_equality


##A function to scan through the streams, and convert the variables into the bilinear counter part 
def convert_streams_variables_linear (streams, parent, u_name, v_name, u_grad, u_int, v_grad, v_int):
    
    import pandas as pd
    
    ##streams --- the list of all the streams 
    ##parent --- the name of the parent unit 
    ##u_name --- the name of the newly introduced u variable 
    ##v_name --- the name of the newly introduced v variable
    ##u_grad --- the associated gradient of the u variable 
    ##u_int --- the associated intercept of the u variable 
    ##v_grad --- the associated gradient of the v variable 
    ##v_int --- the associated intercept of the v variable 
    
    
    ##Initialize a temporary dataframe to hold the return values 
    ret_streams = pd.DataFrame(columns = ['Parent', 'Variable', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    dim_streams = streams.shape 
    
    for i in range (0, dim_streams[0]):
        if streams['Parent'][i] == parent:
            ##Gathering information about initial coefficients 
            x_coeff = streams['Stream_coeff_v1_1'][i] 
            y_coeff = streams['Stream_coeff_v2_1'][i]
            bilin_coeff = streams['Stream_coeff_v1_v2'][i]
            cst = streams['Stream_coeff_cst'][i]  
            
            ##Converting the whole equation in terms of only u and v 
            u_coeff = (x_coeff / 2) + (y_coeff / 2) + (bilin_coeff * u_grad)
            u_cst = (bilin_coeff * u_int) + cst                                     ##Absorbed the coefficient of the main equation 
            v_coeff = (x_coeff / 2) - (y_coeff / 2) - (bilin_coeff * v_grad)
            v_cst = (-1 * bilin_coeff * v_int)

            ##Writing the data to the new linear dataframe
                ##Handling the u_values first 
            temp_data = [parent, u_name, streams['Type'][i], streams['Name'][i] + '_u', streams['Layer'][i], u_cst, u_coeff, streams['InOut'][i]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Parent', 'Variable', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])  
            ret_streams = ret_streams.append(temp_df, ignore_index = True)
                ##Handling the v_values now 
            temp_data = [parent, v_name, streams['Type'][i], streams['Name'][i] + '_v', streams['Layer'][i], v_cst, v_coeff, streams['InOut'][i]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Parent', 'Variable', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])  
            ret_streams = ret_streams.append(temp_df, ignore_index = True)    
    
    return ret_streams

##A scanning function to determine if the requested unit has bilinear variables or not 
def scan_bilinear_affected_list (affected_list, string, bilin_type):
    
    ##affected_list --- the record of affected units
    ##string --- the unit name to be checked 
    ##bilin_type --- the type of bilinear variable to be checked for 
    
    dim_affected_list = affected_list.shape
    ret_val = 'no'
    for i in range (0, dim_affected_list[0]):
        if (string == affected_list['Names'][i]) and (bilin_type == affected_list['Bilinear_Type'][i]):
            ret_val = 'yes'
            break
    
    return ret_val

##This function scans the affected lists and records the unit name if it is affected by bilinear variable relationships
def detect_bilinear_variables_v2 (utilitylist, storagelist, processlist, streams, cons_eqns_terms, obj_func):

    ##utilitylist --- the list of all the utilities 
    ##storagelist --- the list of all the storages
    ##processlist --- the list of all the processes
    ##streams --- the list of all the streams
    ##cons_eqns_terms --- the list of all the terms in the additional constraints 
    ##obj_func --- the objective function selected for the slave
    
    import sys    
    import pandas as pd 

    eps = sys.float_info.epsilon
    
    ##Initializing a dataframe to hold the names of the affected units
    affected_list = pd.DataFrame(columns = ['Names', 'Bilinear_Type'])
    
    ##Determining the number of objective functions 
    num_obj = len(obj_func)
    
    ##Getting the dataframe key based on the objective function 
    key = obj_function_detect (obj_func)
    
    for i in range (0, num_obj):
        key[i] = key[i] + '_v1_v2'
    
    dim_utilitylist = utilitylist.shape
    dim_storagelist = storagelist.shape
    dim_processlist = processlist.shape
    dim_streams = streams.shape
    dim_cons_eqns_terms = cons_eqns_terms.shape
    
    ##Handling utilities first 
    for i in range (0, dim_utilitylist[0]):
        ##Searching through the utilitylist
        obj_func_affected_bilin_util = check_obj_func_affected_bilinear (utilitylist, i, key)
        if (abs(utilitylist['Coeff_v1_v2'][i]) >= eps) or (obj_func_affected_bilin_util > 0):
            temp = utilitylist['Name'][i]
            bilin_type = 'cont_x_cont'
            temp_data = [temp, bilin_type]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Names', 'Bilinear_Type'])
            affected_list = affected_list.append(temp_df, ignore_index = True)
        ##Checking the streams and the cons_eqns_terms if it is not reflected in the utilitylist
        else:
            name = utilitylist['Name'][i]
            found = 0
            ##Checking through the streams
            for j in range (0, dim_streams[0]):
                if ((streams['Parent'][j] == name) and (streams['Stream_coeff_v1_v2'][j] >= eps)) or (streams['Type'][j] == 'network_parallel'):
                    temp = name 
                    if streams['Type'][j] == 'network_parallel':
                        bilin_type = 'bin_x_cont'
                    else:
                        bilin_type = 'cont_x_cont'
                    temp_data = [temp, bilin_type]
                    temp_df = pd.DataFrame(data = [temp_data], columns = ['Names', 'Bilinear_Type'])
                    affected_list = affected_list.append(temp_df, ignore_index = True)
                    found = 1
                    break
            if found < 1:
                ##Checking through the cons_eqn_terms 
                for j in range (0, dim_cons_eqns_terms[0]):
                    if (cons_eqns_terms['Parent_unit'][j] == name) and (cons_eqns_terms['Coeff_v1_v2'][j] >= eps):
                        temp = name 
                        bilin_type = 'cont_x_cont'
                        temp_data = [temp, bilin_type]
                        temp_df = pd.DataFrame(data = [temp_data], columns = ['Names', 'Bilinear_Type'])
                        affected_list = affected_list.append(temp_df, ignore_index = True)
                        found = 1
                        break  

    ##Handling the storages
    for i in range (0, dim_storagelist[0]):
        ##Searching through the storagelist
        obj_func_affected_bilin_sto = check_obj_func_affected_bilinear (storagelist, i, key)
        if (abs(storagelist['Coeff_v1_v2'][i]) >= eps) or (obj_func_affected_bilin_sto > 0):
            temp = storagelist['Name'][i]
            bilin_type = 'cont_x_cont'
            temp_data = [temp, bilin_type]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Names', 'Bilinear_Type'])
            affected_list = affected_list.append(temp_df, ignore_index = True)
        ##Checking the streams and the cons_eqns_terms if it is not reflected in the storagelist
        else:
            name = storagelist['Name'][i]
            found = 0
            ##Checking through the streams
            for j in range (0, dim_streams[0]):
                if ((streams['Parent'][j] == name) and (streams['Stream_coeff_v1_v2'][j] >= eps)) or (streams['Type'][j] == 'network_parallel'):
                    temp = name 
                    if streams['Type'][j] == 'network_parallel':
                        bilin_type = 'bin_x_cont'
                    else:
                        bilin_type = 'cont_x_cont'
                    temp_data = [temp, bilin_type]
                    temp_df = pd.DataFrame(data = [temp_data], columns = ['Names', 'Bilinear_Type'])
                    affected_list = affected_list.append(temp_df, ignore_index = True)
                    found = 1
                    break
            if found < 1:
                ##Checking through the cons_eqn_terms 
                for j in range (0, dim_cons_eqns_terms[0]):
                    if (cons_eqns_terms['Parent_unit'][j] == name) and (cons_eqns_terms['Coeff_v1_v2'][j] >= eps):
                        temp = name 
                        bilin_type = 'cont_x_cont'
                        temp_data = [temp, bilin_type]
                        temp_df = pd.DataFrame(data = [temp_data], columns = ['Names', 'Bilinear_Type'])
                        affected_list = affected_list.append(temp_df, ignore_index = True)
                        found = 1
                        break      
          
    ##Handling the processes
    for i in range (0, dim_processlist[0]):
        ##Searching through the processlist
        obj_func_affected_bilin_pro = check_obj_func_affected_bilinear (processlist, i, key)
        if (abs(processlist['Coeff_v1_v2'][i]) >= eps) or (obj_func_affected_bilin_pro > 0):
            temp = processlist['Name'][i]
            bilin_type = 'cont_x_cont'
            temp_data = [temp, bilin_type]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Names', 'Bilinear_Type'])
            affected_list = affected_list.append(temp_df, ignore_index = True)
        ##Checking the streams and the cons_eqns_terms if it is not reflected in the processlist
        else:
            name = processlist['Name'][i]
            found = 0
            ##Checking through the streams
            for j in range (0, dim_streams[0]):
                if ((streams['Parent'][j] == name) and (streams['Stream_coeff_v1_v2'][j] >= eps)) or (streams['Type'][j] == 'network_parallel'):
                    temp = name 
                    if streams['Type'][j] == 'network_parallel':
                        bilin_type = 'bin_x_cont'
                    else:
                        bilin_type = 'cont_x_cont'
                    temp_data = [temp, bilin_type]
                    temp_df = pd.DataFrame(data = [temp_data], columns = ['Names', 'Bilinear_Type'])
                    affected_list = affected_list.append(temp_df, ignore_index = True)
                    found = 1
                    break
            if found < 1:
                ##Checking through the cons_eqn_terms 
                for j in range (0, dim_cons_eqns_terms[0]):
                    if (cons_eqns_terms['Parent_unit'][j] == name) and (cons_eqns_terms['Coeff_v1v2'][j] >= eps):
                        temp = name 
                        bilin_type = 'cont_x_cont'
                        temp_data = [temp, bilin_type]
                        temp_df = pd.DataFrame(data = [temp_data], columns = ['Names', 'Bilinear_Type'])
                        affected_list = affected_list.append(temp_df, ignore_index = True)
                        found = 1
                        break      
    
    return affected_list

##This function is just to generate empty DataFrames in the linearized form  
def generate_linear_lists_v2 ():
    
    import pandas as pd
    
    utilitylist_linear = pd.DataFrame(columns = ['Parent', 'Name', 'Fmin', 'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    storagelist_linear = pd.DataFrame(columns = ['Parent', 'Name', 'Fmin', 'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    processlist_linear = pd.DataFrame(columns = ['Parent', 'Name', 'Fmin', 'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    streams_linear = pd.DataFrame(columns = ['Parent', 'Variable', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    cons_eqns_linear = pd.DataFrame(columns = ['Name', 'Type', 'Sign', 'RHS_value'])
    cons_eqns_terms_linear = pd.DataFrame(columns = ['Variable', 'Parent_unit', 'Parent_eqn', 'Parent_stream', 'Coefficient', 'Grad', 'Cst'])
    
    return utilitylist_linear, storagelist_linear, processlist_linear, streams_linear, cons_eqns_linear, cons_eqns_terms_linear

##This function just returns the appropriate key to seach based on the entered objective function for the slave
def obj_function_detect (obj_func):
    
    ##obj_func --- a string of values
    
    key = []
    
    for i in range (0, len(obj_func)):
    
        if obj_func[i] == 'investment_cost':
            key.append('Cinv')
        elif obj_func[i] == 'operation_cost':
            key.append('Cost')
        elif obj_func[i] == 'power':
            key.append('Power')
        elif obj_func[i] == 'impact':
            key.append('Impact')
        
    return key

##This function fills up the array for the dataframe with the appropriate key 
def fill_obj_func_values (key, listdata, iteration, variable_name):
    
    import pandas as pd 
    
    ##key --- the associated key for the objective function 
    ##listdata --- the utility, process and storagelist
    
    grad_Cinv = 0
    intercept_Cinv = 0
    grad_Cost = 0
    intercept_Cost = 0
    grad_Power = 0
    intercept_Power = 0
    grad_Impact = 0
    intercept_Impact = 0    
    
    if variable_name == 'Variable1':
        if 'Cinv' in key:
            grad_Cinv = listdata['Cinv_v1_1'][iteration]
            intercept_Cinv = listdata['Cinv_cst'][iteration]
        if 'Cost' in key:
            grad_Cost = listdata['Cost_v1_1'][iteration]
            intercept_Cost = listdata['Cost_cst'][iteration]
        if 'Power' in key:
            grad_Power = listdata['Power_v1_1'][iteration]
            intercept_Power = listdata['Power_cst'][iteration]
        if 'Impact' in key:
            grad_Impact = listdata['Impact_v1_1'][iteration]
            intercept_Impact = listdata['Impact_cst'][iteration]   
        
        ret_values = [listdata['Name'][iteration], listdata[variable_name][iteration], listdata['Fmin_v1'][iteration], listdata['Fmax_v1'][iteration], grad_Cost, intercept_Cost, grad_Cinv, intercept_Cinv,
                      grad_Power, intercept_Power, grad_Impact, intercept_Impact]
        
        ret_df = pd.DataFrame(data = [ret_values], columns = ['Parent', 'Name', 'Fmin', 'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])

    elif variable_name == 'Variable2':
        if 'Cinv' in key:
            grad_Cinv = listdata['Cinv_v1_1'][iteration]
        if 'Cost' in key:
            grad_Cost = listdata['Cost_v1_1'][iteration]
        if 'Power' in key:
            grad_Power = listdata['Power_v1_1'][iteration]
        if 'Impact' in key:
            grad_Impact = listdata['Impact_v1_1'][iteration]

        ret_values = [listdata['Name'][iteration], listdata[variable_name][iteration], listdata['Fmin_v2'][iteration], listdata['Fmax_v2'][iteration], grad_Cost, intercept_Cost, grad_Cinv, intercept_Cinv,
                      grad_Power, intercept_Power, grad_Impact, intercept_Impact]
        
        ret_df = pd.DataFrame(data = [ret_values], columns = ['Parent', 'Name', 'Fmin', 'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
        
    return ret_df

##This function is to check if the given value exists in the list 
def check_if_exists(value, check_list):
    ##value --- the value to be checked
    ##check_list --- the list to be checked for 
    
    ret_value = 0
    for i in range (0, len(check_list)):
        if check_list[i] == value:
            ret_value = 1
            break
    
    return ret_value

##This function takes in the constraint name and returns the type of constraint 
def check_constraint_type(cons_eqns, name):
    
    ##cons_eqn --- a list of all the additional constraints 
    ##name --- the name of the constraint 
    
    dim_cons_eqns = cons_eqns.shape 
    for i in range (0, dim_cons_eqns[0]):
        if cons_eqns['Name'][i] == name:
            ret_value = cons_eqns['Type'][i]
            break
    return ret_value

##This function determines the type of equation, given its name 
def determine_eqn_type (eqn_name, cons_eqns):

    ##eqn_name --- the name of the equation 
    ##cons_eqns --- a dataframe containing all the equations 
    
    dim_cons_eqns = cons_eqns.shape 
    
    for i in range (0, dim_cons_eqns[0]):
        if cons_eqns['Name'][i] == eqn_name:
            type_ret = cons_eqns['Type'][i]
            break
    
    return type_ret

##This function checks if the objective function is affected by bilinear variables 
def check_obj_func_affected_bilinear (list_name, iteration_num, key):
    
    import sys    
    
    ##list_name --- utilitylist, processlist, storagelist, etc.
    ##iteration_number --- the iteration number in the for loop
    ##key --- the list of predefined objective functions 

    eps = sys.float_info.epsilon
    
    ret_val = 0
    
    for i in range (0, len(key)):
        if abs(list_name[key[i]][iteration_num]) >= eps:
            ret_val = 1
    
    
    return ret_val

##This function fills up the objective function for linearized bilinear variables 
def fill_obj_func_values_lin_bilin (key, uv_coeff_data, uv_cst_data, unit_name, var_name_uv, uv_min, uv_max):
    
    import pandas as pd 
    
    ##key --- list of objective functions 
    ##uv_coeff_data --- list of gradient data 
    ##uv_cst_data --- list of intercept data 
    ##unit_name --- the associated unit name 
    ##var_name_uv --- the associated variable name 
    ##uv_min --- the lower bound 
    ##uv_max --- the upper bound  
    
    grad_Cinv = 0
    intercept_Cinv = 0
    grad_Cost = 0
    intercept_Cost = 0
    grad_Power = 0
    intercept_Power = 0
    grad_Impact = 0
    intercept_Impact = 0      
    
    for i in range (0, len(key)):
        
        if 'Cinv' in key:
            grad_Cinv = uv_coeff_data[i]
            intercept_Cinv = uv_cst_data[i]
        elif 'Cost' in key:
            grad_Cost = uv_coeff_data[i]
            intercept_Cost = uv_cst_data[i]
        elif 'Power' in key:
            grad_Power = uv_coeff_data[i]
            intercept_Power = uv_cst_data[i]
        elif 'Impact' in key:
            grad_Impact = uv_coeff_data[i]
            intercept_Impact = uv_cst_data[i]    
    
    temp_data = [unit_name, var_name_uv, uv_min, uv_max, grad_Cost, intercept_Cost, grad_Cinv, intercept_Cinv, grad_Power, intercept_Power, grad_Impact,
                 intercept_Impact]
    ret_vals = pd.DataFrame(data = [temp_data], columns = ['Parent', 'Name', 'Fmin', 'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    
    return ret_vals
    
    

