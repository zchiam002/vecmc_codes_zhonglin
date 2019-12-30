
def genscript_lp_format (original_data, sorted_terms, linearized_list, streams_bilin_contbin_new, parallel_thread_num, obj_func, bilinear_pieces):

    import os
    import pandas as pd
    
    ##Dealing with the storage directory for this script 
    ##Setting the path directory 
    master_folder = 'C:\\Optimization_zlc\\slave_convex_handlers\\solver_lp_format_holder\\'
    sub_folder = 'thread_' + str(parallel_thread_num) + '\\'
    script = 'script_' + str(parallel_thread_num) + '.lp'
    
    ##First check if the sub folder directory exists, if it does, delete it 
    sub_folder_path = master_folder + sub_folder 
#    if os.path.exists(sub_folder_path):
#        shutil.rmtree(sub_folder_path)
        
    ##Now, create the sub folder directory for storing the lp format script for the specific thread
    if not os.path.exists(sub_folder_path):
        os.makedirs(sub_folder_path)
        
    ##The final file location should be 
    script_loc = sub_folder_path + script 
    
###############################################################################################################################################################################################
###############################################################################################################################################################################################
###############################################################################################################################################################################################
    ##Legend of the inputs
    
    ##original_data = {}
    ##original_data['layerslist'] = layerslist
    ##original_data['utilitylist'] = utilitylist
    ##original_data['processlist'] = processlist
    ##original_data['streams'] = streams
    ##original_data['cons_eqns'] = cons_eqns
    ##original_data['cons_eqns_terms'] = cons_eqns_terms
    
    ##sorted_terms['objective_function_utility_bilinear']
    ##sorted_terms['dual_variable_constraint_utility_bilinear']
    ##sorted_terms['objective_function_utility_linear']                         --- important
    ##sorted_terms['objective_function_process_bilinear']
    ##sorted_terms['dual_variable_constraint_process_bilinear']
    ##sorted_terms['objective_function_process_linear']                         --- important
    ##sorted_terms['streams_bilinear']
    ##sorted_terms['streams_linear']                                            --- important
    ##sorted_terms['cons_eqn_terms_bilinear']
    ##sorted_terms['cons_eqn_terms_linear']                                     --- important
    
    ##linearized_list = {}
    ##linearized_list['obj_func_u_bilin_new'] = obj_func_u_bilin_new
    ##linearized_list['dual_v_c_util_bilin_new'] = dual_v_c_util_bilin_new
    ##linearized_list['obj_func_p_bilin_new'] = obj_func_p_bilin_new
    ##linearized_list['dual_v_c_proc_bilin_new'] = dual_v_c_proc_bilin_new
    ##linearized_list['streams_bilin_new'] = streams_bilin_new    
    ##linearized_list['cons_eqn_terms_bilin_new'] = cons_eqn_terms_bilin_new
    
    ##streams_bilin_contbin_new --- the affected terms which involve linearization of bilinear terms continuous x binary 
    
    ##parallel_thread_num --- the number to append for the directory to be unique 
    ##obj_func --- the objective function, it can be of 4 types 
    ##bilinear_pieces --- the number of bilinear pieces
    
###############################################################################################################################################################################################
###############################################################################################################################################################################################
###############################################################################################################################################################################################
    ##Problem definition section
    f_data_set = open(script_loc, 'w')
    
###############################################################################################################################################################################################
###############################################################################################################################################################################################
###############################################################################################################################################################################################    
    ##Objective function section 
    f_data_set.write('Minimize \n')
    f_data_set.write('\n') 
    
    ##The overall string to contain all the objective function values 
    obj_function_input = ''
    
    ##Writing the utility terms in the objective function for strictly linear terms
    dim_objective_function_utility_linear = sorted_terms['objective_function_utility_linear'].shape
    
    ##Before implementing the rest, check if the dataframe is empty or not  
    if dim_objective_function_utility_linear[0] > 0:
        if obj_func == 'operation_cost':
            for i in range (0, dim_objective_function_utility_linear[0]):
                term2 = ''
                term1_name = sorted_terms['objective_function_utility_linear']['Name'][i] + '_' + sorted_terms['objective_function_utility_linear']['Variable1'][i]
                if sorted_terms['objective_function_utility_linear']['Variable2'][i] != '-':
                    term2_name = sorted_terms['objective_function_utility_linear']['Name'][i] + '_' + sorted_terms['objective_function_utility_linear']['Variable2'][i]
                    term2 = 'present'
                term3_name = sorted_terms['objective_function_utility_linear']['Name'][i] + '_y'
                
                if i == 0:
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Cost_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Cost_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Cost_cst'][i]) + ' ' + term3_name
                else:
                    obj_function_input = obj_function_input + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Cost_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Cost_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Cost_cst'][i]) + ' ' + term3_name
          
        elif obj_func == 'investment_cost':
            for i in range (0, dim_objective_function_utility_linear[0]):
                term2 = ''
                term1_name = sorted_terms['objective_function_utility_linear']['Name'][i] + '_' + sorted_terms['objective_function_utility_linear']['Variable1'][i]
                if sorted_terms['objective_function_utility_linear']['Variable2'][i] != '-':
                    term2_name = sorted_terms['objective_function_utility_linear']['Name'][i] + '_' + sorted_terms['objective_function_utility_linear']['Variable2'][i]
                    term2 = 'present'
                term3_name = sorted_terms['objective_function_utility_linear']['Name'][i] + '_y'
                
                if i == 0:
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Cinv_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Cinv_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Cinv_cst'][i]) + ' ' + term3_name
                else:
                    obj_function_input = obj_function_input + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Cinv_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Cinv_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Cinv_cst'][i]) + ' ' + term3_name
    
        elif obj_func == 'power':
            for i in range (0, dim_objective_function_utility_linear[0]):
                term2 = ''
                term1_name = sorted_terms['objective_function_utility_linear']['Name'][i] + '_' + sorted_terms['objective_function_utility_linear']['Variable1'][i]
                if sorted_terms['objective_function_utility_linear']['Variable2'][i] != '-':
                    term2_name = sorted_terms['objective_function_utility_linear']['Name'][i] + '_' + sorted_terms['objective_function_utility_linear']['Variable2'][i]
                    term2 = 'present'
                term3_name = sorted_terms['objective_function_utility_linear']['Name'][i] + '_y'
                
                if i == 0:
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Power_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Power_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Power_cst'][i]) + ' ' + term3_name
                else:
                    obj_function_input = obj_function_input + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Power_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Power_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Power_cst'][i]) + ' ' + term3_name
    
        elif obj_func == 'impact':
            for i in range (0, dim_objective_function_utility_linear[0]):
                term2 = ''
                term1_name = sorted_terms['objective_function_utility_linear']['Name'][i] + '_' + sorted_terms['objective_function_utility_linear']['Variable1'][i]
                if sorted_terms['objective_function_utility_linear']['Variable2'][i] != '-':
                    term2_name = sorted_terms['objective_function_utility_linear']['Name'][i] + '_' + sorted_terms['objective_function_utility_linear']['Variable2'][i]
                    term2 = 'present'
                term3_name = sorted_terms['objective_function_utility_linear']['Name'][i] + '_y'
                
                if i == 0:
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Impact_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Impact_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Impact_cst'][i]) + ' ' + term3_name
                else:
                    obj_function_input = obj_function_input + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Impact_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Impact_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_utility_linear']['Impact_cst'][i]) + ' ' + term3_name

############################################################################################################################################################################################

    ##Writing the process terms in the objective function for strictly linear terms
    dim_objective_function_process_linear = sorted_terms['objective_function_process_linear'].shape    

    ##Before implementing the rest, check if the dataframe is empty or not  
    if dim_objective_function_process_linear[0] > 0:
        ##Checking if it is the first element in the string
        if not obj_function_input:
            result_empty = 1
        else:
            result_empty = 0
        term2 = ''
        if obj_func == 'operation_cost':
            for i in range (0, dim_objective_function_process_linear[0]):
                term2 = ''
                term1_name = sorted_terms['objective_function_process_linear']['Name'][i] + '_' + sorted_terms['objective_function_process_linear']['Variable1'][i]
                if sorted_terms['objective_function_process_linear']['Variable2'][i] != '-':
                    term2_name = sorted_terms['objective_function_process_linear']['Name'][i] + '_' + sorted_terms['objective_function_process_linear']['Variable2'][i]
                    term2 = 'present'
                term3_name = sorted_terms['objective_function_process_linear']['Name'][i] + '_y'
                
                if result_empty == 1:
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Cost_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Cost_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Cost_cst'][i]) + ' ' + term3_name
                else:
                    obj_function_input = obj_function_input + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Cost_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Cost_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Cost_cst'][i]) + ' ' + term3_name
          
        elif obj_func == 'investment_cost':
            for i in range (0, dim_objective_function_process_linear[0]):
                term2 = ''
                term1_name = sorted_terms['objective_function_process_linear']['Name'][i] + '_' + sorted_terms['objective_function_process_linear']['Variable1'][i]
                if sorted_terms['objective_function_process_linear']['Variable2'][i] != '-':
                    term2_name = sorted_terms['objective_function_process_linear']['Name'][i] + '_' + sorted_terms['objective_function_process_linear']['Variable2'][i]
                    term2 = 'present'
                term3_name = sorted_terms['objective_function_process_linear']['Name'][i] + '_y'
                
                if result_empty == 1:
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Cinv_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Cinv_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Cinv_cst'][i]) + ' ' + term3_name
                else:
                    obj_function_input = obj_function_input + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Cinv_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Cinv_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Cinv_cst'][i]) + ' ' + term3_name
    
        elif obj_func == 'power':
            for i in range (0, dim_objective_function_process_linear[0]):
                term2 = ''
                term1_name = sorted_terms['objective_function_process_linear']['Name'][i] + '_' + sorted_terms['objective_function_process_linear']['Variable1'][i]
                if sorted_terms['objective_function_process_linear']['Variable2'][i] != '-':
                    term2_name = sorted_terms['objective_function_process_linear']['Name'][i] + '_' + sorted_terms['objective_function_process_linear']['Variable2'][i]
                    term2 = 'present'
                term3_name = sorted_terms['objective_function_process_linear']['Name'][i] + '_y'
                
                if result_empty == 1:
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Power_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Power_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Power_cst'][i]) + ' ' + term3_name
                else:
                    obj_function_input = obj_function_input + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Power_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Power_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Power_cst'][i]) + ' ' + term3_name
    
        elif obj_func == 'impact':
            for i in range (0, dim_objective_function_process_linear[0]):
                term2 = ''
                term1_name = sorted_terms['objective_function_process_linear']['Name'][i] + '_' + sorted_terms['objective_function_process_linear']['Variable1'][i]
                if sorted_terms['objective_function_process_linear']['Variable2'][i] != '-':
                    term2_name = sorted_terms['objective_function_process_linear']['Name'][i] + '_' + sorted_terms['objective_function_process_linear']['Variable2'][i]
                    term2 = 'present'
                term3_name = sorted_terms['objective_function_process_linear']['Name'][i] + '_y'
                
                if result_empty == 1:
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Impact_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Impact_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Impact_cst'][i]) + ' ' + term3_name
                else:
                    obj_function_input = obj_function_input + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Impact_v1_1'][i]) + ' ' + term1_name + ' + '
                    if term2 == 'present':
                        obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Impact_v2_1'][i]) + ' ' + term2_name + ' + '
                    obj_function_input = obj_function_input + str(sorted_terms['objective_function_process_linear']['Impact_cst'][i]) + ' ' + term3_name 

############################################################################################################################################################################################
    
    ##Writing the utility terms in the objective function for the linearized bilinear terms 
    dim_obj_func_util_bilin = sorted_terms['objective_function_utility_bilinear'].shape                 ##This is the list containing all the original terms 
    
    ##Before implementing the rest, check if the dataframe is empty or not  
    if dim_obj_func_util_bilin[0] > 0:

        ##Checking if it is the first element in the string
        if not obj_function_input:
            result_empty = 1
        else:
            result_empty = 0
        
        temp_input = ''
        
        if obj_func == 'operation_cost':
            for i in range (0, dim_obj_func_util_bilin[0]):
                org_coeff_v1_1 = sorted_terms['objective_function_utility_bilinear']['Cost_v1_1'][i]
                org_coeff_v2_1 = sorted_terms['objective_function_utility_bilinear']['Cost_v2_1'][i]
                org_coeff_v1v2 = sorted_terms['objective_function_utility_bilinear']['Cost_v1_v2'][i]
                org_coeff_cst = sorted_terms['objective_function_utility_bilinear']['Cost_cst'][i]
    
                org_term1 = sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_utility_bilinear']['Variable1'][i]
                org_term2 = sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_utility_bilinear']['Variable2'][i]
    
                temp_input = temp_input + str(org_coeff_v1_1) + ' ' + org_term1 + ' + '
                temp_input = temp_input + str(org_coeff_v2_1) + ' ' + org_term2 + ' + '
                
                lowerlimit = i * bilinear_pieces * 2
                upperlimit = i * bilinear_pieces * 2 + bilinear_pieces * 2                                  ##To avoid scanning through the entire list 
    
                for j in range (lowerlimit, upperlimit):
                    if linearized_list['obj_func_u_bilin_new']['Name_parent'][j] == sorted_terms['objective_function_utility_bilinear']['Name'][i]:
                        temp_term_coeff = org_coeff_v1v2 * linearized_list['obj_func_u_bilin_new']['Coeff'][j]
                        temp_term_intercept = org_coeff_v1v2 * linearized_list['obj_func_u_bilin_new']['Intercept'][j]
                        
                        if linearized_list['obj_func_u_bilin_new']['Variable'][j] == 'u':
                            temp_input = temp_input + str(temp_term_coeff) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(temp_term_intercept) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + '_y + '
                        
                        elif linearized_list['obj_func_u_bilin_new']['Variable'][j] == 'v':
                            temp_input = temp_input + str(-1 * temp_term_coeff) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(-1 * temp_term_intercept) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + '_y + '
                            
                if i < dim_obj_func_util_bilin[0] - 1:      
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_y + '
                else:
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_y '
                    
            if result_empty == 1:
                obj_function_input = obj_function_input + temp_input
            else:
                obj_function_input = obj_function_input + ' + ' + temp_input
                
        elif obj_func == 'investment_cost':
            for i in range (0, dim_obj_func_util_bilin[0]):
                org_coeff_v1_1 = sorted_terms['objective_function_utility_bilinear']['Cinv_v1_1'][i]
                org_coeff_v2_1 = sorted_terms['objective_function_utility_bilinear']['Cinv_v2_1'][i]
                org_coeff_v1v2 = sorted_terms['objective_function_utility_bilinear']['Cinv_v1_v2'][i]
                org_coeff_cst = sorted_terms['objective_function_utility_bilinear']['Cinv_cst'][i]
    
                org_term1 = sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_utility_bilinear']['Variable1'][i]
                org_term2 = sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_utility_bilinear']['Variable2'][i]
    
                temp_input = temp_input + str(org_coeff_v1_1) + ' ' + org_term1 + ' + '
                temp_input = temp_input + str(org_coeff_v2_1) + ' ' + org_term2 + ' + '
                
                lowerlimit = i * bilinear_pieces * 2
                upperlimit = i * bilinear_pieces * 2 + bilinear_pieces * 2                                  ##To avoid scanning through the entire list 
    
                for j in range (lowerlimit, upperlimit):
                    if linearized_list['obj_func_u_bilin_new']['Name_parent'][j] == sorted_terms['objective_function_utility_bilinear']['Name'][i]:
                        temp_term_coeff = org_coeff_v1v2 * linearized_list['obj_func_u_bilin_new']['Coeff'][j]
                        temp_term_intercept = org_coeff_v1v2 * linearized_list['obj_func_u_bilin_new']['Intercept'][j]
                        
                        if linearized_list['obj_func_u_bilin_new']['Variable'][j] == 'u':
                            temp_input = temp_input + str(temp_term_coeff) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(temp_term_intercept) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + '_y + '
                        
                        elif linearized_list['obj_func_u_bilin_new']['Variable'][j] == 'v':
                            temp_input = temp_input + str(-1 * temp_term_coeff) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(-1 * temp_term_intercept) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + '_y + '
                            
                if i < dim_obj_func_util_bilin[0] - 1:      
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_y + '
                else:
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_y '
                    
            if result_empty == 1:
                obj_function_input = obj_function_input + temp_input
            else:
                obj_function_input = obj_function_input + ' + ' + temp_input
                
        elif obj_func == 'power':
            for i in range (0, dim_obj_func_util_bilin[0]):
                org_coeff_v1_1 = sorted_terms['objective_function_utility_bilinear']['Power_v1_1'][i]
                org_coeff_v2_1 = sorted_terms['objective_function_utility_bilinear']['Power_v2_1'][i]
                org_coeff_v1v2 = sorted_terms['objective_function_utility_bilinear']['Power_v1_v2'][i]
                org_coeff_cst = sorted_terms['objective_function_utility_bilinear']['Power_cst'][i]
    
                org_term1 = sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_utility_bilinear']['Variable1'][i]
                org_term2 = sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_utility_bilinear']['Variable2'][i]
    
                temp_input = temp_input + str(org_coeff_v1_1) + ' ' + org_term1 + ' + '
                temp_input = temp_input + str(org_coeff_v2_1) + ' ' + org_term2 + ' + '
                
                lowerlimit = i * bilinear_pieces * 2
                upperlimit = i * bilinear_pieces * 2 + bilinear_pieces * 2                                  ##To avoid scanning through the entire list 
    
                for j in range (lowerlimit, upperlimit):
                    if linearized_list['obj_func_u_bilin_new']['Name_parent'][j] == sorted_terms['objective_function_utility_bilinear']['Name'][i]:
                        temp_term_coeff = org_coeff_v1v2 * linearized_list['obj_func_u_bilin_new']['Coeff'][j]
                        temp_term_intercept = org_coeff_v1v2 * linearized_list['obj_func_u_bilin_new']['Intercept'][j]
                        
                        if linearized_list['obj_func_u_bilin_new']['Variable'][j] == 'u':
                            temp_input = temp_input + str(temp_term_coeff) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(temp_term_intercept) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + '_y + '
                        
                        elif linearized_list['obj_func_u_bilin_new']['Variable'][j] == 'v':
                            temp_input = temp_input + str(-1 * temp_term_coeff) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(-1 * temp_term_intercept) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + '_y + '
                            
                if i < dim_obj_func_util_bilin[0] - 1:      
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_y + '
                else:
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_y '
                    
            if result_empty == 1:
                obj_function_input = obj_function_input + temp_input
            else:
                obj_function_input = obj_function_input + ' + ' + temp_input 
                
        elif obj_func == 'impact':
            for i in range (0, dim_obj_func_util_bilin[0]):
                org_coeff_v1_1 = sorted_terms['objective_function_utility_bilinear']['Impact_v1_1'][i]
                org_coeff_v2_1 = sorted_terms['objective_function_utility_bilinear']['Impact_v2_1'][i]
                org_coeff_v1v2 = sorted_terms['objective_function_utility_bilinear']['Impact_v1_v2'][i]
                org_coeff_cst = sorted_terms['objective_function_utility_bilinear']['Impact_cst'][i]
    
                org_term1 = sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_utility_bilinear']['Variable1'][i]
                org_term2 = sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_utility_bilinear']['Variable2'][i]
    
                temp_input = temp_input + str(org_coeff_v1_1) + ' ' + org_term1 + ' + '
                temp_input = temp_input + str(org_coeff_v2_1) + ' ' + org_term2 + ' + '
                
                lowerlimit = i * bilinear_pieces * 2
                upperlimit = i * bilinear_pieces * 2 + bilinear_pieces * 2                                  ##To avoid scanning through the entire list 
    
                for j in range (lowerlimit, upperlimit):
                    if linearized_list['obj_func_u_bilin_new']['Name_parent'][j] == sorted_terms['objective_function_utility_bilinear']['Name'][i]:
                        temp_term_coeff = org_coeff_v1v2 * linearized_list['obj_func_u_bilin_new']['Coeff'][j]
                        temp_term_intercept = org_coeff_v1v2 * linearized_list['obj_func_u_bilin_new']['Intercept'][j]
                        
                        if linearized_list['obj_func_u_bilin_new']['Variable'][j] == 'u':
                            temp_input = temp_input + str(temp_term_coeff) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(temp_term_intercept) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + '_y + '
                        
                        elif linearized_list['obj_func_u_bilin_new']['Variable'][j] == 'v':
                            temp_input = temp_input + str(-1 * temp_term_coeff) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(-1 * temp_term_intercept) + ' ' + linearized_list['obj_func_u_bilin_new']['Name'][j] + '_y + '
                            
                if i < dim_obj_func_util_bilin[0] - 1:      
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_y + '
                else:
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_y '
                    
            if result_empty == 1:
                obj_function_input = obj_function_input + temp_input
            else:
                obj_function_input = obj_function_input + ' + ' + temp_input         

###############################################################################################################################################################################################            

    ##Writing the process terms in the objective function for the linearized bilinear terms                 
                    
    dim_obj_func_proc_bilin = sorted_terms['objective_function_process_bilinear'].shape                 ##This is the list containing all the original terms 

    ##Before implementing the rest, check if the dataframe is empty or not  
    if dim_obj_func_proc_bilin[0] > 0:

        ##Checking if it is the first element in the string
        if not obj_function_input:
            result_empty = 1
        else:
            result_empty = 0
        
        temp_input = ''
        
        if obj_func == 'operation_cost':
            for i in range (0, dim_obj_func_proc_bilin[0]):
                org_coeff_v1_1 = sorted_terms['objective_function_process_bilinear']['Cost_v1_1'][i]
                org_coeff_v2_1 = sorted_terms['objective_function_process_bilinear']['Cost_v2_1'][i]
                org_coeff_v1v2 = sorted_terms['objective_function_process_bilinear']['Cost_v1_v2'][i]
                org_coeff_cst = sorted_terms['objective_function_process_bilinear']['Cost_cst'][i]
    
                org_term1 = sorted_terms['objective_function_process_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_process_bilinear']['Variable1'][i]
                org_term2 = sorted_terms['objective_function_process_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_process_bilinear']['Variable2'][i]
    
                temp_input = temp_input + str(org_coeff_v1_1) + ' ' + org_term1 + ' + '
                temp_input = temp_input + str(org_coeff_v2_1) + ' ' + org_term2 + ' + '
                
                lowerlimit = i * bilinear_pieces * 2
                upperlimit = i * bilinear_pieces * 2 + bilinear_pieces * 2                                  ##To avoid scanning through the entire list 
    
                for j in range (lowerlimit, upperlimit):
                    if linearized_list['obj_func_p_bilin_new']['Name_parent'][j] == sorted_terms['objective_function_process_bilinear']['Name'][i]:
                        temp_term_coeff = org_coeff_v1v2 * linearized_list['obj_func_p_bilin_new']['Coeff'][j]
                        temp_term_intercept = org_coeff_v1v2 * linearized_list['obj_func_p_bilin_new']['Intercept'][j]
                        
                        if linearized_list['obj_func_p_bilin_new']['Variable'][j] == 'u':
                            temp_input = temp_input + str(temp_term_coeff) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(temp_term_intercept) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + '_y + '
                        
                        elif linearized_list['obj_func_p_bilin_new']['Variable'][j] == 'v':
                            temp_input = temp_input + str(-1 * temp_term_coeff) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(-1 * temp_term_intercept) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + '_y + '
                            
                if i < dim_obj_func_proc_bilin[0] - 1:      
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_process_bilinear']['Name'][i] + '_y + '
                else:
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_process_bilinear']['Name'][i] + '_y '
                    
            if result_empty == 1:
                obj_function_input = obj_function_input + temp_input
            else:
                obj_function_input = obj_function_input + ' + ' + temp_input
                
        elif obj_func == 'investment_cost':
            for i in range (0, dim_obj_func_proc_bilin[0]):
                org_coeff_v1_1 = sorted_terms['objective_function_process_bilinear']['Cinv_v1_1'][i]
                org_coeff_v2_1 = sorted_terms['objective_function_process_bilinear']['Cinv_v2_1'][i]
                org_coeff_v1v2 = sorted_terms['objective_function_process_bilinear']['Cinv_v1_v2'][i]
                org_coeff_cst = sorted_terms['objective_function_process_bilinear']['Cinv_cst'][i]
    
                org_term1 = sorted_terms['objective_function_process_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_process_bilinear']['Variable1'][i]
                org_term2 = sorted_terms['objective_function_process_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_process_bilinear']['Variable2'][i]
    
                temp_input = temp_input + str(org_coeff_v1_1) + ' ' + org_term1 + ' + '
                temp_input = temp_input + str(org_coeff_v2_1) + ' ' + org_term2 + ' + '
                
                lowerlimit = i * bilinear_pieces * 2
                upperlimit = i * bilinear_pieces * 2 + bilinear_pieces * 2                                  ##To avoid scanning through the entire list 
    
                for j in range (lowerlimit, upperlimit):
                    if linearized_list['obj_func_p_bilin_new']['Name_parent'][j] == sorted_terms['objective_function_process_bilinear']['Name'][i]:
                        temp_term_coeff = org_coeff_v1v2 * linearized_list['obj_func_p_bilin_new']['Coeff'][j]
                        temp_term_intercept = org_coeff_v1v2 * linearized_list['obj_func_p_bilin_new']['Intercept'][j]
                        
                        if linearized_list['obj_func_p_bilin_new']['Variable'][j] == 'u':
                            temp_input = temp_input + str(temp_term_coeff) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(temp_term_intercept) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + '_y + '
                        
                        elif linearized_list['obj_func_p_bilin_new']['Variable'][j] == 'v':
                            temp_input = temp_input + str(-1 * temp_term_coeff) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(-1 * temp_term_intercept) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + '_y + '
                            
                if i < dim_obj_func_proc_bilin[0] - 1:      
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_process_bilinear']['Name'][i] + '_y + '
                else:
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_process_bilinear']['Name'][i] + '_y '
                    
            if result_empty == 1:
                obj_function_input = obj_function_input + temp_input
            else:
                obj_function_input = obj_function_input + ' + ' + temp_input
                
        elif obj_func == 'power':
            for i in range (0, dim_obj_func_proc_bilin[0]):
                org_coeff_v1_1 = sorted_terms['objective_function_process_bilinear']['Power_v1_1'][i]
                org_coeff_v2_1 = sorted_terms['objective_function_process_bilinear']['Power_v2_1'][i]
                org_coeff_v1v2 = sorted_terms['objective_function_process_bilinear']['Power_v1_v2'][i]
                org_coeff_cst = sorted_terms['objective_function_process_bilinear']['Power_cst'][i]
    
                org_term1 = sorted_terms['objective_function_process_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_process_bilinear']['Variable1'][i]
                org_term2 = sorted_terms['objective_function_process_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_process_bilinear']['Variable2'][i]
    
                temp_input = temp_input + str(org_coeff_v1_1) + ' ' + org_term1 + ' + '
                temp_input = temp_input + str(org_coeff_v2_1) + ' ' + org_term2 + ' + '
                
                lowerlimit = i * bilinear_pieces * 2
                upperlimit = i * bilinear_pieces * 2 + bilinear_pieces * 2                                  ##To avoid scanning through the entire list 
    
                for j in range (lowerlimit, upperlimit):
                    if linearized_list['obj_func_p_bilin_new']['Name_parent'][j] == sorted_terms['objective_function_process_bilinear']['Name'][i]:
                        temp_term_coeff = org_coeff_v1v2 * linearized_list['obj_func_p_bilin_new']['Coeff'][j]
                        temp_term_intercept = org_coeff_v1v2 * linearized_list['obj_func_p_bilin_new']['Intercept'][j]
                        
                        if linearized_list['obj_func_p_bilin_new']['Variable'][j] == 'u':
                            temp_input = temp_input + str(temp_term_coeff) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(temp_term_intercept) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + '_y + '
                        
                        elif linearized_list['obj_func_p_bilin_new']['Variable'][j] == 'v':
                            temp_input = temp_input + str(-1 * temp_term_coeff) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(-1 * temp_term_intercept) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + '_y + '
                            
                if i < dim_obj_func_proc_bilin[0] - 1:      
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_process_bilinear']['Name'][i] + '_y + '
                else:
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_process_bilinear']['Name'][i] + '_y '
                  
            if result_empty == 1:
                obj_function_input = obj_function_input + temp_input
            else:
                obj_function_input = obj_function_input + ' + ' + temp_input 
                
        elif obj_func == 'impact':
            for i in range (0, dim_obj_func_proc_bilin[0]):
                org_coeff_v1_1 = sorted_terms['objective_function_process_bilinear']['Impact_v1_1'][i]
                org_coeff_v2_1 = sorted_terms['objective_function_process_bilinear']['Impact_v2_1'][i]
                org_coeff_v1v2 = sorted_terms['objective_function_process_bilinear']['Impact_v1_v2'][i]
                org_coeff_cst = sorted_terms['objective_function_process_bilinear']['Impact_cst'][i]
    
                org_term1 = sorted_terms['objective_function_process_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_process_bilinear']['Variable1'][i]
                org_term2 = sorted_terms['objective_function_process_bilinear']['Name'][i] + '_' + sorted_terms['objective_function_process_bilinear']['Variable2'][i]
    
                temp_input = temp_input + str(org_coeff_v1_1) + ' ' + org_term1 + ' + '
                temp_input = temp_input + str(org_coeff_v2_1) + ' ' + org_term2 + ' + '
                
                lowerlimit = i * bilinear_pieces * 2
                upperlimit = i * bilinear_pieces * 2 + bilinear_pieces * 2                                  ##To avoid scanning through the entire list 
    
                for j in range (lowerlimit, upperlimit):
                    if linearized_list['obj_func_p_bilin_new']['Name_parent'][j] == sorted_terms['objective_function_process_bilinear']['Name'][i]:
                        temp_term_coeff = org_coeff_v1v2 * linearized_list['obj_func_p_bilin_new']['Coeff'][j]
                        temp_term_intercept = org_coeff_v1v2 * linearized_list['obj_func_p_bilin_new']['Intercept'][j]
                        
                        if linearized_list['obj_func_p_bilin_new']['Variable'][j] == 'u':
                            temp_input = temp_input + str(temp_term_coeff) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(temp_term_intercept) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + '_y + '
                        
                        elif linearized_list['obj_func_p_bilin_new']['Variable'][j] == 'v':
                            temp_input = temp_input + str(-1 * temp_term_coeff) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + ' + '
                            temp_input = temp_input + str(-1 * temp_term_intercept) + ' ' + linearized_list['obj_func_p_bilin_new']['Name'][j] + '_y + '
                            
                if i < dim_obj_func_proc_bilin[0] - 1:      
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_process_bilinear']['Name'][i] + '_y + '
                else:
                    temp_input = temp_input + str(org_coeff_cst) + ' ' + sorted_terms['objective_function_utility_bilinear']['Name'][i] + '_y '
                    
            if result_empty == 1:
                obj_function_input = obj_function_input + temp_input
            else:
                obj_function_input = obj_function_input + ' + ' + temp_input                             

    f_data_set.write('obj: ' + obj_function_input) 
    f_data_set.write('\n \n')      
    
###############################################################################################################################################################################################    
###############################################################################################################################################################################################
###############################################################################################################################################################################################
    ##Constraint section 
    f_data_set.write('Subject To \n \n')
    
    current_index = 0
###############################################################################################################################################################################################
    ##Writing common constraints for all utility terms 
    f_data_set.write('\\\\ Constraints for all utility terms \n \n')
    
    dim_utility_terms = original_data['utilitylist'].shape

    if dim_utility_terms[0] > 0:
        
        for i in range (0, dim_utility_terms[0]):
            current_index = current_index + 1
            temp_term = 'c' + str(current_index) + ': '
            temp_term = temp_term + str(original_data['utilitylist']['Fmin_v1'][i]) + ' ' + original_data['utilitylist']['Name'][i] + '_y'
            temp_term = temp_term + ' - ' + original_data['utilitylist']['Name'][i] + '_' + original_data['utilitylist']['Variable1'][i]
            temp_term = temp_term + ' <= 0'
            
            f_data_set.write(temp_term + '\n')
            
            current_index = current_index + 1
            temp_term = 'c' + str(current_index) + ': '
            temp_term = temp_term + original_data['utilitylist']['Name'][i] + '_' + original_data['utilitylist']['Variable1'][i]
            temp_term = temp_term + ' - ' + str(original_data['utilitylist']['Fmax_v1'][i]) + ' ' + original_data['utilitylist']['Name'][i] + '_y'
            temp_term = temp_term + ' <= 0'

            f_data_set.write(temp_term + '\n')
            
            ##Checking if the second term exists or not 
            if original_data['utilitylist']['Variable2'][i] != '-':
                current_index = current_index + 1
                temp_term = 'c' + str(current_index) + ': '
                temp_term = temp_term + str(original_data['utilitylist']['Fmin_v2'][i]) + ' ' + original_data['utilitylist']['Name'][i] + '_y'
                temp_term = temp_term + ' - ' + original_data['utilitylist']['Name'][i] + '_' + original_data['utilitylist']['Variable2'][i]
                temp_term = temp_term + ' <= 0'
            
                f_data_set.write(temp_term + '\n')
                
                current_index = current_index + 1
                temp_term = 'c' + str(current_index) + ': '
                temp_term = temp_term + original_data['utilitylist']['Name'][i] + '_' + original_data['utilitylist']['Variable2'][i]
                temp_term = temp_term + ' - ' + str(original_data['utilitylist']['Fmax_v2'][i]) + ' ' + original_data['utilitylist']['Name'][i] + '_y'
                temp_term = temp_term + ' <= 0'

                f_data_set.write(temp_term + '\n')
                
    f_data_set.write('\n')
            
###############################################################################################################################################################################################
    ##Writing common constraints for all process terms 
    f_data_set.write('\\\\ Constraints for all process terms \n \n')         
    
    dim_process_terms = original_data['processlist'].shape
    
    if dim_process_terms[0] > 0:
        
        for i in range (0, dim_process_terms[0]):
            current_index = current_index + 1
            temp_term = 'c' + str(current_index) + ': '
            temp_term = temp_term + str(original_data['processlist']['Fmax_v1'][i]) + ' ' + original_data['processlist']['Name'][i] + '_y'
            temp_term = temp_term + ' - ' + original_data['processlist']['Name'][i] + '_' + original_data['processlist']['Variable1'][i]
            temp_term = temp_term + ' <= 0'
            
            f_data_set.write(temp_term + '\n')
            
            current_index = current_index + 1
            temp_term = 'c' + str(current_index) + ': '
            temp_term = temp_term + original_data['processlist']['Name'][i] + '_' + original_data['processlist']['Variable1'][i]
            temp_term = temp_term + ' - ' + str(original_data['processlist']['Fmax_v1'][i]) + ' ' + original_data['processlist']['Name'][i] + '_y'
            temp_term = temp_term + ' <= 0'

            f_data_set.write(temp_term + '\n')
            
            ##Checking if the second term exists or not 
            if original_data['processlist']['Variable2'][i] != '-':
                current_index = current_index + 1
                temp_term = 'c' + str(current_index) + ': '
                temp_term = temp_term + str(original_data['processlist']['Fmax_v2'][i]) + ' ' + original_data['processlist']['Name'][i] + '_y'
                temp_term = temp_term + ' - ' + original_data['processlist']['Name'][i] + '_' + original_data['processlist']['Variable2'][i]
                temp_term = temp_term + ' <= 0'
            
                f_data_set.write(temp_term + '\n')
                
                current_index = current_index + 1
                temp_term = 'c' + str(current_index) + ': '
                temp_term = temp_term + original_data['processlist']['Name'][i] + '_' + original_data['processlist']['Variable2'][i]
                temp_term = temp_term + ' - ' + str(original_data['processlist']['Fmax_v2'][i]) + ' ' + original_data['processlist']['Name'][i] + '_y'
                temp_term = temp_term + ' <= 0'

                f_data_set.write(temp_term + '\n \n')

    f_data_set.write('\n')
                
###############################################################################################################################################################################################
    ##Writing the terms affected by bilinear relationships for utilities 
    f_data_set.write('\\\\ Writing the terms affected by bilinear relationships for utilities \n \n')

    dim_dual_v_c_util_bilin_new = linearized_list['dual_v_c_util_bilin_new'].shape 
    
    if dim_dual_v_c_util_bilin_new[0] > 0:

        ##Writing all the constraints for the Fmin and Fmax for each bilinear sub term         
        for i in range (0, dim_dual_v_c_util_bilin_new[0]):
            
            current_index = current_index + 1
            temp_term = 'c' + str(current_index) + ': '
            temp_term = temp_term + str(linearized_list['dual_v_c_util_bilin_new']['Fmin_v1'][i]) + ' ' +  linearized_list['dual_v_c_util_bilin_new']['Name'][i] + '_y'
            temp_term = temp_term + ' - '  + linearized_list['dual_v_c_util_bilin_new']['Name'][i]
            temp_term = temp_term + ' <= 0'

            f_data_set.write(temp_term + '\n')
            
            current_index = current_index + 1            
            temp_term = 'c' + str(current_index) + ': '
            temp_term = temp_term + linearized_list['dual_v_c_util_bilin_new']['Name'][i]
            temp_term = temp_term + ' - ' + str(linearized_list['dual_v_c_util_bilin_new']['Fmax_v1'][i]) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][i] + '_y'
            temp_term = temp_term + ' <= 0'
            
            f_data_set.write(temp_term + '\n')
            
        ##Making sure that only 1 of the bilinear sub units are selected
        start_index = 0
        
        for i in range (0, dim_dual_v_c_util_bilin_new[0]):
            
            ##Preparing the starting terms
            if start_index <= 1:
                
                if linearized_list['dual_v_c_util_bilin_new']['Variable'][i] == 'u':
                    temp_term_u = ''
                    current_index = current_index + 1
                    temp_term_u = temp_term_u + 'c' + str(current_index) + ': '
                    temp_term_u = temp_term_u + linearized_list['dual_v_c_util_bilin_new']['Name'][i] + '_y + '
                    start_index = start_index + 1
                    
                elif linearized_list['dual_v_c_util_bilin_new']['Variable'][i] == 'v':
                    temp_term_v = ''
                    current_index = current_index + 1
                    temp_term_v = temp_term_v + 'c' + str(current_index) + ': '
                    temp_term_v = temp_term_v + linearized_list['dual_v_c_util_bilin_new']['Name'][i] + '_y + '
                    start_index = start_index + 1
            
            ##Adding in the subsequent terms and the final term 
            elif (start_index > 1) and (start_index < (2 * bilinear_pieces)):
                
                if (linearized_list['dual_v_c_util_bilin_new']['Variable'][i] == 'u'):
                    if start_index < (2 * bilinear_pieces - 2):
                        temp_term_u = temp_term_u + linearized_list['dual_v_c_util_bilin_new']['Name'][i] + '_y + '
                    else:
                        temp_term_u = temp_term_u + linearized_list['dual_v_c_util_bilin_new']['Name'][i] + '_y'
                        temp_term_u = temp_term_u + ' <= 1'
                        f_data_set.write(temp_term_u + '\n')
                    start_index = start_index + 1
                    
                elif (linearized_list['dual_v_c_util_bilin_new']['Variable'][i] == 'v'):
                    if start_index < (2 * bilinear_pieces - 1):
                        temp_term_v = temp_term_v + linearized_list['dual_v_c_util_bilin_new']['Name'][i] + '_y + '
                    else:
                        temp_term_v = temp_term_v + linearized_list['dual_v_c_util_bilin_new']['Name'][i] + '_y'
                        temp_term_v = temp_term_v + ' <= 1'
                        f_data_set.write(temp_term_v + '\n')
                        start_index = -1
                    start_index = start_index + 1
                    
        ##Making sure that if the main unit is switched off, all sub units are switched off correspondingly 
        start_index = 0
        
        for i in range (0, dim_dual_v_c_util_bilin_new[0]):
            ##Preparing the starting term 
            if start_index == 0:
                current_index = current_index + 1
                temp_term = ''
                temp_term = temp_term + 'c' + str(current_index) + ': '
                temp_term = temp_term + linearized_list['dual_v_c_util_bilin_new']['Name'][i] + '_y + '
                start_index = start_index + 1
            
            ##These are the subsequent terms 
            elif start_index < (2 * bilinear_pieces - 1):
                temp_term = temp_term + linearized_list['dual_v_c_util_bilin_new']['Name'][i] + '_y + '
                start_index = start_index + 1
            
            ##This is the ending term 
            else:
                temp_term = temp_term + linearized_list['dual_v_c_util_bilin_new']['Name'][i] + '_y - '
                temp_term = temp_term + '2 ' + linearized_list['dual_v_c_util_bilin_new']['Name_parent'][i] + '_y'
                temp_term = temp_term + ' = 0'
                f_data_set.write(temp_term + '\n')
                start_index = 0
            
        ##Making sure that u and v are in sync with x and y correspondingly 
        start_index = 0
        
        for i in range (0, dim_dual_v_c_util_bilin_new[0]):
            ##Preparing the starting terms 
            if start_index <= 1:
                
                if linearized_list['dual_v_c_util_bilin_new']['Variable'][i] == 'u':
                    temp_term_u = ''
                    current_index = current_index + 1
                    temp_term_u = temp_term_u + 'c' + str(current_index) + ': ' + linearized_list['dual_v_c_util_bilin_new']['Name'][i]    
                    start_index = start_index + 1
                    
                elif linearized_list['dual_v_c_util_bilin_new']['Variable'][i] == 'v':
                    temp_term_v = ''
                    current_index = current_index + 1
                    temp_term_v = temp_term_v + 'c' + str(current_index) + ': ' + linearized_list['dual_v_c_util_bilin_new']['Name'][i]   
                    start_index = start_index + 1   
                    
            ##Adding subsequent terms and the final term         
            elif (start_index > 1) and (start_index < (2 * bilinear_pieces)):
                
                if (linearized_list['dual_v_c_util_bilin_new']['Variable'][i] == 'u'):
                    if start_index < (2 * bilinear_pieces - 2):
                        temp_term_u = temp_term_u + ' + ' + linearized_list['dual_v_c_util_bilin_new']['Name'][i]    
                    
                    else:
                        temp_term_u = temp_term_u + ' + ' + linearized_list['dual_v_c_util_bilin_new']['Name'][i]
                        temp_term_u = temp_term_u + ' - ' + linearized_list['dual_v_c_util_bilin_new']['Name_parent'][i] + '_' + linearized_list['dual_v_c_util_bilin_new']['Variable1_parent'][i] 
                        temp_term_u = temp_term_u + ' - ' + linearized_list['dual_v_c_util_bilin_new']['Name_parent'][i] + '_' + linearized_list['dual_v_c_util_bilin_new']['Variable2_parent'][i]
                        temp_term_u = temp_term_u + ' = 0'
                        f_data_set.write(temp_term_u + '\n')
                        
                    start_index = start_index + 1
                
                elif (linearized_list['dual_v_c_util_bilin_new']['Variable'][i] == 'v'):
                    if start_index < (2 * bilinear_pieces - 1):                    
                        temp_term_v = temp_term_v + ' + ' + linearized_list['dual_v_c_util_bilin_new']['Name'][i]
                        
                    else:
                        temp_term_v = temp_term_v + ' + ' + linearized_list['dual_v_c_util_bilin_new']['Name'][i]
                        temp_term_v = temp_term_v + ' - ' + linearized_list['dual_v_c_util_bilin_new']['Name_parent'][i] + '_' + linearized_list['dual_v_c_util_bilin_new']['Variable1_parent'][i] 
                        temp_term_v = temp_term_v + ' + ' + linearized_list['dual_v_c_util_bilin_new']['Name_parent'][i] + '_' + linearized_list['dual_v_c_util_bilin_new']['Variable2_parent'][i]
                        temp_term_v = temp_term_v + ' = 0'
                        f_data_set.write(temp_term_v + '\n')
                        start_index = -1                        

                    start_index = start_index + 1 
                    
        ##Making sure that the master unit does not exceed bilinear constraints 
        ##First we need to extract the limits 
        dim_dual_variable_constraint_utility_bilinear = sorted_terms['dual_variable_constraint_utility_bilinear'].shape

        matrix_row = 0

        for i in range (0, dim_dual_variable_constraint_utility_bilinear[0]):
            
            ##Extracted values 
            fmin = sorted_terms['dual_variable_constraint_utility_bilinear']['Fmin'][i]
            fmax = sorted_terms['dual_variable_constraint_utility_bilinear']['Fmax'][i]
            v1_coeff = sorted_terms['dual_variable_constraint_utility_bilinear']['Coeff_v1_1'][i]
            v2_coeff = sorted_terms['dual_variable_constraint_utility_bilinear']['Coeff_v2_1'][i]
            v1v2_coeff = sorted_terms['dual_variable_constraint_utility_bilinear']['Coeff_v1_v2'][i]
            cst_coeff = sorted_terms['dual_variable_constraint_utility_bilinear']['Coeff_cst'][i]
            
            start_index = 0
            ##Preparing variable terms
            for j in range (matrix_row, matrix_row + (bilinear_pieces * 2)):
                ##Preparing the starting term   
                if start_index == 0:   
                    var_temp1 = ''
                    var_temp2 = ''
                    term1 = v1v2_coeff * linearized_list['dual_v_c_util_bilin_new']['Coeff'][j]
                    term2 = v1v2_coeff * linearized_list['dual_v_c_util_bilin_new']['Intercept'][j]

                    ##For the first equation Fmin y1 - term <= 0
                    var_temp1 = var_temp1 + str(-1 * term1) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][j] + ' + '
                    var_temp1 = var_temp1 + str(-1 * term2) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][j]+ '_y'
                    
                    
                    ##For the second equation term - Fmax y1 <= 0
                    var_temp2 = var_temp2 + str(term1) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][j] + ' + '
                    var_temp2 = var_temp2 + str(term2) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][j]+ '_y'
                    
                    start_index = start_index + 1
                
                ##These are the subsequent and the last term  
                elif start_index <= (2 * bilinear_pieces - 1):
                
                    if linearized_list['dual_v_c_util_bilin_new']['Variable'][j] == 'u':
                        term1 = v1v2_coeff * linearized_list['dual_v_c_util_bilin_new']['Coeff'][j]
                        term2 = v1v2_coeff * linearized_list['dual_v_c_util_bilin_new']['Intercept'][j]

                        ##For the first equation Fmin y1 - term <= 0
                        var_temp1 = var_temp1 + ' + ' +  str(-1 * term1) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][j] + ' + '
                        var_temp1 = var_temp1 + str(-1 * term2) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][j]+ '_y'
                        
                        ##For the second equation term - Fmax y1 <= 0
                        var_temp2 = var_temp2 + ' + ' +  str(term1) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][j] + ' + '
                        var_temp2 = var_temp2 + str(term2) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][j]+ '_y'                     

                    elif linearized_list['dual_v_c_util_bilin_new']['Variable'][j] == 'v':
                        term1 = v1v2_coeff * linearized_list['dual_v_c_util_bilin_new']['Coeff'][j]
                        term2 = v1v2_coeff * linearized_list['dual_v_c_util_bilin_new']['Intercept'][j]

                        ##For the first equation Fmin y1 - term <= 0
                        var_temp1 = var_temp1 + ' + ' + str(term1) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][j] + ' + '
                        var_temp1 = var_temp1 + str(term2) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][j]+ '_y'
                        
                        ##For the second equation term - Fmax y1 <= 0                        
                        var_temp2 = var_temp2 + ' - ' + str(term1) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][j] + ' - '
                        var_temp2 = var_temp2 + str(term2) + ' ' + linearized_list['dual_v_c_util_bilin_new']['Name'][j]+ '_y'
                    
                    start_index = start_index + 1
            
            ##Changing the matrix row values         
            matrix_row = matrix_row + (2 * bilinear_pieces)
            
            ##Writing the first part of the constraint
            y1_composite_coeff = fmin - cst_coeff
            current_index = current_index + 1
            temp_term_1 = ''
            temp_term_1 = temp_term_1 + 'c' + str(current_index) + ': '
            temp_term_1 = temp_term_1 + str(-v1_coeff) + ' ' + sorted_terms['dual_variable_constraint_utility_bilinear']['Name'][i] + '_' + sorted_terms['dual_variable_constraint_utility_bilinear']['Variable1'][i]
            temp_term_1 = temp_term_1 + ' + ' + str(-v2_coeff) + ' ' + sorted_terms['dual_variable_constraint_utility_bilinear']['Name'][i] + '_' + sorted_terms['dual_variable_constraint_utility_bilinear']['Variable2'][i]
            temp_term_1 = temp_term_1 + ' + ' + var_temp1 + ' + '
            temp_term_1 = temp_term_1 + str(y1_composite_coeff) + ' ' + sorted_terms['dual_variable_constraint_utility_bilinear']['Name'][i] + '_y'
            temp_term_1 = temp_term_1 + ' <= 0'
            f_data_set.write(temp_term_1 + '\n')

            ##Writing the second part of the constraint
            y2_composite_coeff = cst_coeff - fmax
            current_index = current_index + 1
            temp_term_2 = ''
            temp_term_2 = temp_term_2 + 'c' + str(current_index) + ': '
            temp_term_2 = temp_term_2 + str(v1_coeff) + ' ' + sorted_terms['dual_variable_constraint_utility_bilinear']['Name'][i] + '_' + sorted_terms['dual_variable_constraint_utility_bilinear']['Variable1'][i]
            temp_term_2 = temp_term_2 + ' + ' + str(v2_coeff) + ' ' + sorted_terms['dual_variable_constraint_utility_bilinear']['Name'][i] + '_' + sorted_terms['dual_variable_constraint_utility_bilinear']['Variable2'][i]
            temp_term_2 = temp_term_2 + ' + ' + var_temp2 + ' + '
            temp_term_2 = temp_term_2 + str(y2_composite_coeff) + ' ' + sorted_terms['dual_variable_constraint_utility_bilinear']['Name'][i] + '_y'
            temp_term_2 = temp_term_2 + ' <= 0'
            f_data_set.write(temp_term_2 + '\n')  
            
    f_data_set.write('\n')
###############################################################################################################################################################################################
    ##Writing the terms affected by bilinear relationships for processes
    f_data_set.write('\\\\ Writing the terms affected by bilinear relationships for processes \n \n')

    dim_dual_v_c_proc_bilin_new = linearized_list['dual_v_c_proc_bilin_new'].shape
         
    if dim_dual_v_c_proc_bilin_new[0] > 0:       
        
        ##Writing all the constraints for the Fmin and Fmax for each bilinear sub term         
        for i in range (0, dim_dual_v_c_proc_bilin_new[0]):
            
            current_index = current_index + 1
            temp_term = 'c' + str(current_index) + ': '
            temp_term = temp_term + str(linearized_list['dual_v_c_proc_bilin_new']['Fmin_v1'][i]) + ' ' +  linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + '_y'
            temp_term = temp_term + ' - '  + linearized_list['dual_v_c_proc_bilin_new']['Name'][i]
            temp_term = temp_term + ' <= 0'

            f_data_set.write(temp_term + '\n')
            
            current_index = current_index + 1            
            temp_term = 'c' + str(current_index) + ': '
            temp_term = temp_term + linearized_list['dual_v_c_proc_bilin_new']['Name'][i]
            temp_term = temp_term + ' - ' + str(linearized_list['dual_v_c_proc_bilin_new']['Fmax_v1'][i]) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + '_y'
            temp_term = temp_term + ' <= 0'
            
            f_data_set.write(temp_term + '\n')
            
        ##Making sure that only 1 of the bilinear sub units are selected
        start_index = 0
        
        for i in range (0, dim_dual_v_c_proc_bilin_new[0]):
            
            ##Preparing the starting terms
            if start_index <= 1:
                
                if linearized_list['dual_v_c_proc_bilin_new']['Variable'][i] == 'u':
                    temp_term_u = ''
                    current_index = current_index + 1
                    temp_term_u = temp_term_u + 'c' + str(current_index) + ': '
                    temp_term_u = temp_term_u + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + '_y + '
                    start_index = start_index + 1
                    
                elif linearized_list['dual_v_c_proc_bilin_new']['Variable'][i] == 'v':
                    temp_term_v = ''
                    current_index = current_index + 1
                    temp_term_v = temp_term_v + 'c' + str(current_index) + ': '
                    temp_term_v = temp_term_v + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + '_y + '
                    start_index = start_index + 1
            
            ##Adding in the subsequent terms and the final term 
            elif (start_index > 1) and (start_index < (2 * bilinear_pieces)):
                
                if (linearized_list['dual_v_c_proc_bilin_new']['Variable'][i] == 'u'):
                    if start_index < (2 * bilinear_pieces - 2):
                        temp_term_u = temp_term_u + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + '_y + '
                    else:
                        temp_term_u = temp_term_u + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + '_y'
                        temp_term_u = temp_term_u + ' <= 1'
                        f_data_set.write(temp_term_u + '\n')
                    start_index = start_index + 1
                    
                elif (linearized_list['dual_v_c_proc_bilin_new']['Variable'][i] == 'v'):
                    if start_index < (2 * bilinear_pieces - 1):
                        temp_term_v = temp_term_v + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + '_y + '
                    else:
                        temp_term_v = temp_term_v + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + '_y'
                        temp_term_v = temp_term_v + ' <= 1'
                        f_data_set.write(temp_term_v + '\n')
                        start_index = -1
                    start_index = start_index + 1
                    
        ##Making sure that if the main unit is switched off, all sub units are switched off correspondingly 
        start_index = 0
        
        for i in range (0, dim_dual_v_c_proc_bilin_new[0]):
            ##Preparing the starting term 
            if start_index == 0:
                current_index = current_index + 1
                temp_term = ''
                temp_term = temp_term + 'c' + str(current_index) + ': '
                temp_term = temp_term + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + '_y + '
                start_index = start_index + 1
            
            ##These are the subsequent terms 
            elif start_index < (2 * bilinear_pieces - 1):
                temp_term = temp_term + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + '_y + '
                start_index = start_index + 1
            
            ##This is the ending term 
            else:
                temp_term = temp_term + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + '_y - '
                temp_term = temp_term + '2 ' + linearized_list['dual_v_c_proc_bilin_new']['Name_parent'][i] + '_y'
                temp_term = temp_term + ' = 0'
                f_data_set.write(temp_term + '\n')
                start_index = 0
                
        ##Making sure that u and v are in sync with x and y correspondingly 
        start_index = 0
        
        for i in range (0, dim_dual_v_c_proc_bilin_new[0]):
            ##Preparing the starting terms 
            if start_index <= 1:
                
                if linearized_list['dual_v_c_proc_bilin_new']['Variable'][i] == 'u':
                    temp_term_u = ''
                    current_index = current_index + 1
                    temp_term_u = temp_term_u + 'c' + str(current_index) + ': ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][i]
                    start_index = start_index + 1
                    
                elif linearized_list['dual_v_c_proc_bilin_new']['Variable'][i] == 'v':
                    temp_term_v = ''
                    current_index = current_index + 1
                    temp_term_v = temp_term_v + 'c' + str(current_index) + ': ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][i]
                    start_index = start_index + 1   
                    
            ##Adding subsequent terms and the final term         
            elif (start_index > 1) and (start_index < (2 * bilinear_pieces)):
                
                if (linearized_list['dual_v_c_proc_bilin_new']['Variable'][i] == 'u'):
                    if start_index < (2 * bilinear_pieces - 2):
                        temp_term_u = temp_term_u + ' + ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][i]
                    
                    else:
                        temp_term_u = temp_term_u + ' + ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + ' + '
                        temp_term_u = temp_term_u + ' - ' + linearized_list['dual_v_c_proc_bilin_new']['Name_parent'][i] + '_' + linearized_list['dual_v_c_proc_bilin_new']['Variable1_parent'][i] 
                        temp_term_u = temp_term_u + ' - ' + linearized_list['dual_v_c_proc_bilin_new']['Name_parent'][i] + '_' + linearized_list['dual_v_c_proc_bilin_new']['Variable2_parent'][i]
                        temp_term_u = temp_term_u + ' = 0'
                        f_data_set.write(temp_term_u + '\n')
                        
                    start_index = start_index + 1
                
                elif (linearized_list['dual_v_c_proc_bilin_new']['Variable'][i] == 'v'):
                    if start_index < (2 * bilinear_pieces - 1):                    
                        temp_term_v = ' + ' + temp_term_v + linearized_list['dual_v_c_proc_bilin_new']['Name'][i]
                        
                    else:
                        temp_term_v = temp_term_v + ' + ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + ' + '
                        temp_term_v = temp_term_v + ' - ' + linearized_list['dual_v_c_proc_bilin_new']['Name_parent'][i] + '_' + linearized_list['dual_v_c_proc_bilin_new']['Variable1_parent'][i] 
                        temp_term_v = temp_term_v + ' + ' + linearized_list['dual_v_c_proc_bilin_new']['Name_parent'][i] + '_' + linearized_list['dual_v_c_proc_bilin_new']['Variable2_parent'][i]
                        temp_term_v = temp_term_v + ' = 0'
                        f_data_set.write(temp_term_v + '\n')
                        start_index = -1                        

                    start_index = start_index + 1 
                    
        ##Making sure that the master unit does not exceed bilinear constraints 
        ##First we need to extract the limits 
        dim_dual_variable_constraint_process_bilinear = sorted_terms['dual_variable_constraint_process_bilinear'].shape

        matrix_row = 0

        for i in range (0, dim_dual_variable_constraint_process_bilinear[0]):
            
            ##Extracted values 
            fmin = sorted_terms['dual_variable_constraint_process_bilinear']['Fmin'][i]
            fmax = sorted_terms['dual_variable_constraint_process_bilinear']['Fmax'][i]
            v1_coeff = sorted_terms['dual_variable_constraint_process_bilinear']['Coeff_v1_1'][i]
            v2_coeff = sorted_terms['dual_variable_constraint_process_bilinear']['Coeff_v2_1'][i]
            v1v2_coeff = sorted_terms['dual_variable_constraint_process_bilinear']['Coeff_v1_v2'][i]
            cst_coeff = sorted_terms['dual_variable_constraint_process_bilinear']['Coeff_cst'][i]
            
            start_index = 0
            ##Preparing variable terms
            for j in range (matrix_row, matrix_row + (bilinear_pieces * 2)):
                ##Preparing the starting term   
                if start_index == 0:   
                    var_temp1 = ''
                    var_temp2 = ''
                    term1 = v1v2_coeff * linearized_list['dual_v_c_proc_bilin_new']['Coeff'][j]
                    term2 = v1v2_coeff * linearized_list['dual_v_c_proc_bilin_new']['Intercept'][j]

                    ##For the first equation Fmin y1 - term <= 0
                    var_temp1 = var_temp1 + str(-1 * term1) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][j] + ' + '
                    var_temp1 = var_temp1 + str(-1 * term2) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][j]+ '_y'
                    
                    
                    ##For the second equation term - Fmax y1 <= 0
                    var_temp2 = var_temp2 + str(term1) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][j] + ' + '
                    var_temp2 = var_temp2 + str(term2) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][j]+ '_y'
                    
                    start_index = start_index + 1
                
                ##These are the subsequent and the last term  
                elif start_index <= (2 * bilinear_pieces - 1):
                
                    if linearized_list['dual_v_c_proc_bilin_new']['Variable'][j] == 'u':
                        term1 = v1v2_coeff * linearized_list['dual_v_c_proc_bilin_new']['Coeff'][j]
                        term2 = v1v2_coeff * linearized_list['dual_v_c_proc_bilin_new']['Intercept'][j]

                        ##For the first equation Fmin y1 - term <= 0
                        var_temp1 = var_temp1 + ' + ' +  str(-1 * term1) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][j] + ' + '
                        var_temp1 = var_temp1 + str(-1 * term2) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][j]+ '_y'
                        
                        ##For the second equation term - Fmax y1 <= 0
                        var_temp2 = var_temp2 + ' + ' +  str(term1) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][j] + ' + '
                        var_temp2 = var_temp2 + str(term2) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][j]+ '_y'                     

                    elif linearized_list['dual_v_c_proc_bilin_new']['Variable'][j] == 'v':
                        term1 = v1v2_coeff * linearized_list['dual_v_c_proc_bilin_new']['Coeff'][j]
                        term2 = v1v2_coeff * linearized_list['dual_v_c_proc_bilin_new']['Intercept'][j]

                        ##For the first equation Fmin y1 - term <= 0
                        var_temp1 = var_temp1 + ' + ' + str(term1) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][j] + ' + '
                        var_temp1 = var_temp1 + str(term2) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][j]+ '_y'
                        
                        ##For the second equation term - Fmax y1 <= 0                        
                        var_temp2 = var_temp2 + ' - ' + str(term1) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][j] + ' - '
                        var_temp2 = var_temp2 + str(term2) + ' ' + linearized_list['dual_v_c_proc_bilin_new']['Name'][j]+ '_y'
                    
                    start_index = start_index + 1
            
            ##Changing the matrix row values         
            matrix_row = matrix_row + (2 * bilinear_pieces)
            
            ##Writing the first part of the constraint
            y1_composite_coeff = fmin - cst_coeff
            current_index = current_index + 1
            temp_term_1 = ''
            temp_term_1 = temp_term_1 + 'c' + str(current_index) + ': '
            temp_term_1 = temp_term_1 + str(-v1_coeff) + ' ' + sorted_terms['dual_variable_constraint_process_bilinear']['Name'][i] + '_' + sorted_terms['dual_variable_constraint_process_bilinear']['Variable1'][i]
            temp_term_1 = temp_term_1 + ' + ' + str(-v2_coeff) + ' ' + sorted_terms['dual_variable_constraint_process_bilinear']['Name'][i] + '_' + sorted_terms['dual_variable_constraint_process_bilinear']['Variable2'][i]
            temp_term_1 = temp_term_1 + ' + ' + var_temp1 + ' + '
            temp_term_1 = temp_term_1 + str(y1_composite_coeff) + ' ' + sorted_terms['dual_variable_constraint_process_bilinear']['Name'][i] + '_y'
            temp_term_1 = temp_term_1 + ' <= 0'
            f_data_set.write(temp_term_1 + '\n')

            ##Writing the second part of the constraint
            y2_composite_coeff = cst_coeff - fmax
            current_index = current_index + 1
            temp_term_2 = ''
            temp_term_2 = temp_term_2 + 'c' + str(current_index) + ': '
            temp_term_2 = temp_term_2 + str(v1_coeff) + ' ' + sorted_terms['dual_variable_constraint_process_bilinear']['Name'][i] + '_' + sorted_terms['dual_variable_constraint_process_bilinear']['Variable1'][i]
            temp_term_2 = temp_term_2 + ' + ' + str(v2_coeff) + ' ' + sorted_terms['dual_variable_constraint_process_bilinear']['Name'][i] + '_' + sorted_terms['dual_variable_constraint_process_bilinear']['Variable2'][i]
            temp_term_2 = temp_term_2 + ' + ' + var_temp2 + ' + '
            temp_term_2 = temp_term_2 + str(y2_composite_coeff) + ' ' + sorted_terms['dual_variable_constraint_process_bilinear']['Name'][i] + '_y'
            temp_term_2 = temp_term_2 + ' <= 0'
            f_data_set.write(temp_term_2 + '\n')  
            
        f_data_set.write('\n')
###############################################################################################################################################################################################
    f_data_set.write('\\\\ Writing the streams constraints \n \n')

    dim_layerslist = original_data['layerslist'].shape
    dim_streams_lin = sorted_terms['streams_linear'].shape
    dim_streams_bilin = sorted_terms['streams_bilinear'].shape
    dim_streams_bilin_terms = linearized_list['streams_bilin_new'].shape

    f_data_set.write('\\\\ Writing the streams_type: balancing_only \n \n')
    for i in range (0, dim_layerslist[0]):
        ##L.H.S list, handle it as it is  
        lhs_terms = ''
        ##R.H.S list, these terms need to be multiplied by -1  
        rhs_terms = ''                                      
        
        ##Handling balancing only terms first 
        if original_data['layerslist']['Type'][i] == 'balancing_only':
            ##Writing the streams linear terms             
            for j in range (0, dim_streams_lin[0]):                                                                                         ##Handling strictly linear terms first                                                        
                
                if sorted_terms['streams_linear']['Layer'][j] == original_data['layerslist']['Name'][i]:
                    
                    if sorted_terms['streams_linear']['InOut'][j] == 'out':
                        if not lhs_terms:                                                                                                 ##Checking if this is the first term or not 
                            lhs_terms = str(sorted_terms['streams_linear']['Stream_coeff_v1_1'][j]) + ' ' 
                            lhs_terms = lhs_terms + sorted_terms['streams_linear']['Parent'][j] + '_' + sorted_terms['streams_linear']['Parent_v1_name'][j]
                            if sorted_terms['streams_linear']['Parent_v2_name'][j] != '-':
                                lhs_terms = lhs_terms + ' + ' + str(sorted_terms['streams_linear']['Stream_coeff_v2_1'][j]) + ' '
                                lhs_terms = lhs_terms + sorted_terms['streams_linear']['Parent'][j] + '_' + sorted_terms['streams_linear']['Parent_v2_name'][j]
                            lhs_terms = lhs_terms + ' + ' + str(sorted_terms['streams_linear']['Stream_coeff_cst'][j]) + ' ' + sorted_terms['streams_linear']['Parent'][j] + '_y'
                        else:
                            lhs_terms = lhs_terms + ' + ' + str(sorted_terms['streams_linear']['Stream_coeff_v1_1'][j]) + ' '
                            lhs_terms = lhs_terms + sorted_terms['streams_linear']['Parent'][j] + '_' + sorted_terms['streams_linear']['Parent_v1_name'][j]
                            if sorted_terms['streams_linear']['Parent_v2_name'][j] != '-':
                                lhs_terms = lhs_terms + ' + ' + str(sorted_terms['streams_linear']['Stream_coeff_v2_1'][j]) + ' '
                                lhs_terms = lhs_terms + sorted_terms['streams_linear']['Parent'][j] + '_' + sorted_terms['streams_linear']['Parent_v2_name'][j]
                            lhs_terms = lhs_terms + ' + ' + str(sorted_terms['streams_linear']['Stream_coeff_cst'][j]) + ' ' + sorted_terms['streams_linear']['Parent'][j] + '_y'                                                
                    elif sorted_terms['streams_linear']['InOut'][j] == 'in':
                        if not rhs_terms:
                            rhs_terms = str(-1 * sorted_terms['streams_linear']['Stream_coeff_v1_1'][j]) + ' ' 
                            rhs_terms = rhs_terms + sorted_terms['streams_linear']['Parent'][j] + '_' + sorted_terms['streams_linear']['Parent_v1_name'][j]
                            if sorted_terms['streams_linear']['Parent_v2_name'][j] != '-':
                                rhs_terms = rhs_terms + ' - ' + str(sorted_terms['streams_linear']['Stream_coeff_v2_1'][j]) + ' '
                                rhs_terms = rhs_terms + sorted_terms['streams_linear']['Parent'][j] + '_' + sorted_terms['streams_linear']['Parent_v2_name'][j]
                            rhs_terms = rhs_terms + ' - ' + str(sorted_terms['streams_linear']['Stream_coeff_cst'][j]) + ' ' + sorted_terms['streams_linear']['Parent'][j] + '_y'
                        else:
                            rhs_terms = rhs_terms + ' + ' + str(-1 * sorted_terms['streams_linear']['Stream_coeff_v1_1'][j]) + ' '
                            rhs_terms = rhs_terms + sorted_terms['streams_linear']['Parent'][j] + '_' + sorted_terms['streams_linear']['Parent_v1_name'][j]
                            if sorted_terms['streams_linear']['Parent_v2_name'][j] != '-':
                                rhs_terms = rhs_terms + ' - ' + str(sorted_terms['streams_linear']['Stream_coeff_v2_1'][j]) + ' '
                                rhs_terms = rhs_terms + sorted_terms['streams_linear']['Parent'][j] + '_' + sorted_terms['streams_linear']['Parent_v2_name'][j]
                            rhs_terms = rhs_terms + ' - ' + str(sorted_terms['streams_linear']['Stream_coeff_cst'][j]) + ' ' + sorted_terms['streams_linear']['Parent'][j] + '_y'
    
            for j in range (0, dim_streams_bilin[0]):                                                                                       ##Handling the bilinear terms now
              
                if sorted_terms['streams_bilinear']['Layer'][j] == original_data['layerslist']['Name'][i]:
                    
                    #Coefficients  
                    coeff_v1 = sorted_terms['streams_bilinear']['Stream_coeff_v1_1'][j]
                    coeff_v2 = sorted_terms['streams_bilinear']['Stream_coeff_v2_1'][j]
                    coeff_v1v2 = sorted_terms['streams_bilinear']['Stream_coeff_v1_v2'][j]
                    coeff_cst = sorted_terms['streams_bilinear']['Stream_coeff_cst'][j]
                   
                    if sorted_terms['streams_bilinear']['InOut'][j] == 'out':                                                               ##Akin to the lhs term
                        start_index = 0
                        temp_term_s = ''
                        for k in range (0, dim_streams_bilin_terms[0]):                                                                     ##Assembiling the linearized portion
                            if linearized_list['streams_bilin_new']['Name_parent'][k] == sorted_terms['streams_bilinear']['Name'][j]:       ##Making sure that the parent equations are matched
                                if start_index == 0:
                                    temp_term_s = temp_term_s + str(coeff_v1v2 * linearized_list['streams_bilin_new']['Coeff'][k]) + ' '
                                    temp_term_s = temp_term_s + linearized_list['streams_bilin_new']['Name'][k] + ' + '
                                    temp_term_s = temp_term_s + str(coeff_v1v2 * linearized_list['streams_bilin_new']['Intercept'][k]) + ' ' 
                                    temp_term_s = temp_term_s + linearized_list['streams_bilin_new']['Name'][k] + '_y'
                                    start_index = start_index + 1
                                elif (start_index > 0) and (start_index < (2 * bilinear_pieces)):
                                    if linearized_list['streams_bilin_new']['Variable'][k] == 'u':
                                        temp_term_s = temp_term_s + ' + ' + str(coeff_v1v2 * linearized_list['streams_bilin_new']['Coeff'][k]) + ' '
                                        temp_term_s = temp_term_s + linearized_list['streams_bilin_new']['Name'][k] + ' + ' 
                                        temp_term_s = temp_term_s + str(coeff_v1v2 * linearized_list['streams_bilin_new']['Intercept'][k]) + ' ' 
                                        temp_term_s = temp_term_s + linearized_list['streams_bilin_new']['Name'][k] + '_y'
                                        start_index = start_index + 1   
                                    elif linearized_list['streams_bilin_new']['Variable'][k] == 'v':
                                        temp_term_s = temp_term_s + ' - ' + str(coeff_v1v2 * linearized_list['streams_bilin_new']['Coeff'][k]) + ' '
                                        temp_term_s = temp_term_s + linearized_list['streams_bilin_new']['Name'][k] + ' - '
                                        temp_term_s = temp_term_s + str(coeff_v1v2 * linearized_list['streams_bilin_new']['Intercept'][k]) + ' ' 
                                        temp_term_s = temp_term_s + linearized_list['streams_bilin_new']['Name'][k] + '_y'
                                        start_index = start_index + 1                                       
                            if start_index == (2 * bilinear_pieces):
                                break
                        ##Adding in the other terms 
                        full_term = ''
                        full_term = full_term + str(coeff_v1) + ' ' + sorted_terms['streams_bilinear']['Parent'][j] + '_' + sorted_terms['streams_bilinear']['Parent_v1_name'][j]
                        full_term = full_term + ' + ' + str(coeff_v2) + ' ' + sorted_terms['streams_bilinear']['Parent'][j] + '_' + sorted_terms['streams_bilinear']['Parent_v2_name'][j]
                        full_term = full_term + ' + ' + temp_term_s
                        full_term = full_term + ' + ' + str(coeff_cst) + ' ' + sorted_terms['streams_bilinear']['Parent'][j] + '_y'
                        
                        ##Appending the lhs_terms
                        if not lhs_terms:
                            lhs_terms = full_term 
                        else:
                            lhs_terms = lhs_terms + ' + ' + full_term
                            
                    elif sorted_terms['streams_bilinear']['InOut'][j] == 'in':
                        start_index = 0
                        temp_term_s = ''
                        for k in range (0, dim_streams_bilin_terms[0]):                                                             ##Assembiling the linearized portion
                            if linearized_list['streams_bilin_new']['Name_parent'][k] == sorted_terms['streams_bilinear'][j]:       ##Making sure that the parent equations are matched
                                if start_index == 0:
                                    temp_term_s = temp_term_s + str(-1* coeff_v1v2 * linearized_list['streams_bilin_new']['Coeff'][k]) + ' '
                                    temp_term_s = temp_term_s + linearized_list['streams_bilin_new']['Name'][k] + ' - '
                                    temp_term_s = temp_term_s + str(coeff_v1v2 * linearized_list['streams_bilin_new']['Intercept'][k]) + ' ' 
                                    temp_term_s = temp_term_s + linearized_list['streams_bilin_new']['Name'][k] + '_y'
                                    start_index = start_index + 1
                                elif (start_index > 0) and (start_index < (2 * bilinear_pieces)):
                                    if linearized_list['streams_bilin_new']['Variable'][k] == 'u':
                                        temp_term_s = temp_term_s + ' - '  + str(coeff_v1v2 * linearized_list['streams_bilin_new']['Coeff'][k]) + ' '
                                        temp_term_s = temp_term_s + linearized_list['streams_bilin_new']['Name'][k] + ' - '
                                        temp_term_s = temp_term_s + str(coeff_v1v2 * linearized_list['streams_bilin_new']['Intercept'][k]) + ' ' 
                                        temp_term_s = temp_term_s + linearized_list['streams_bilin_new']['Name'][k] + '_y'
                                        start_index = start_index + 1   
                                    elif linearized_list['streams_bilin_new']['Variable'][k] == 'v':
                                        temp_term_s = temp_term_s + ' + ' + str(coeff_v1v2 * linearized_list['streams_bilin_new']['Coeff'][k]) + ' '
                                        temp_term_s = temp_term_s + linearized_list['streams_bilin_new']['Name'][k] + ' + '
                                        temp_term_s = temp_term_s + str(coeff_v1v2 * linearized_list['streams_bilin_new']['Intercept'][k]) + ' ' 
                                        temp_term_s = temp_term_s + linearized_list['streams_bilin_new']['Name'][k] + '_y'
                                        start_index = start_index + 1  
                            if start_index == (2 * bilinear_pieces):
                                break                        
                        ##Adding in the other terms 
                        full_term = ''
                        full_term = full_term + str(coeff_v1) + ' ' + sorted_terms['streams_bilinear']['Parent'][j] + '_' + sorted_terms['streams_bilinear']['Parent_v1_name'][j]
                        full_term = full_term + ' + ' + str(-1 * coeff_v2) + ' ' + sorted_terms['streams_bilinear']['Parent'][j] + '_' + sorted_terms['streams_bilinear']['Parent_v2_name'][j]
                        full_term = full_term + ' + ' + temp_term_s
                        full_term = full_term + ' - ' + str(coeff_cst) + ' ' + sorted_terms['streams_bilinear']['Parent'][j] + '_y' 

                        ##Appending the rhs terms 
                        if not rhs_terms:
                            rhs_terms =  full_term 
                        else:
                            rhs_terms = rhs_terms + ' + ' + full_term                        
            
            ##Wrting the formulated equation 
            current_index = current_index + 1
            written_eqn = ''             
            written_eqn = written_eqn + 'c' + str(current_index) + ': '
            written_eqn = written_eqn + lhs_terms + ' + ' + rhs_terms + ' = 0' 
            f_data_set.write(written_eqn + '\n')
            
    ##Writing additional constraints for bilinear terms only appearing in the streams
    f_data_set.write('\n')
    f_data_set.write('\\\\ Writing additional streams bilinear constraints \n \n')  
    
    ##The procedure is as follows: 
    #Scan through the dual variable bilinear for utilities and processes, if the term exist, do not do anything 
    
    dim_1 = sorted_terms['objective_function_utility_bilinear'].shape
    dim_2 = sorted_terms['dual_variable_constraint_utility_bilinear'].shape   
    dim_3 = sorted_terms['objective_function_process_bilinear'].shape
    dim_4 = sorted_terms['dual_variable_constraint_process_bilinear'].shape

    for i in range (0, dim_streams_bilin[0]):
        ##Checking if terms are in utilities and processes
        check1 = 0
        check2 = 0
        check3 = 0
        check4 = 0
        if dim_1[0] > 0:
            for j in range (0, dim_1[0]):
                if sorted_terms['objective_function_utility_bilinear']['Name'][j] == sorted_terms['streams_bilinear']['Parent'][i]:
                    check1 = 1
                    break
        if dim_2[0] > 0:
            for j in range (0, dim_2[0]):
                if sorted_terms['dual_variable_constraint_utility_bilinear']['Name'][j] == sorted_terms['streams_bilinear']['Parent'][i]: 
                    check2 = 1
                    break
        if dim_3[0] > 0:
            for j in range (0, dim_3[0]):
                if sorted_terms['objective_function_process_bilinear']['Name'][j] == sorted_terms['streams_bilinear']['Parent'][i]: 
                    check3 = 1
                    break 
        if dim_4[0] > 0:
            for j in range (0, dim_4[0]):
                if sorted_terms['dual_variable_constraint_process_bilinear']['Name'][j] == sorted_terms['streams_bilinear']['Parent'][i]: 
                    check4 = 1
                    break 
        
        final_check = check1 + check2 + check3 + check4
        
        if final_check == 0:
            ##Writing the bilinear constraints
            
            ##Writing the upper and lower limits
            start_index = 0
            for j in range (0, dim_streams_bilin_terms[0]):
                if linearized_list['streams_bilin_new']['Name_parent'][j] == sorted_terms['streams_bilinear']['Name'][i]:                       #Making sure that stream names match 
                    ##Writing the Fmin constraint 
                    temp_term = ''
                    temp_term = temp_term + str(linearized_list['streams_bilin_new']['Fmin_v1'][j]) + ' ' + linearized_list['streams_bilin_new']['Name'][j] + '_y'
                    temp_term = temp_term + ' - ' + linearized_list['streams_bilin_new']['Name'][j] 
                    temp_term = temp_term + ' <= 0'
                    current_index = current_index + 1
                    temp_term = 'c' + str(current_index) + ': ' + temp_term 
                    f_data_set.write(temp_term + '\n')     
                    ##Writing the Fmax constraint
                    temp_term = ''
                    temp_term = temp_term + linearized_list['streams_bilin_new']['Name'][j] 
                    temp_term = temp_term + ' - ' + str(linearized_list['streams_bilin_new']['Fmax_v1'][j]) + ' ' + linearized_list['streams_bilin_new']['Name'][j] + '_y'
                    temp_term = temp_term + ' <= 0'
                    current_index = current_index + 1
                    temp_term = 'c' + str(current_index) + ': ' + temp_term 
                    f_data_set.write(temp_term + '\n')
                    
                    start_index = start_index + 1
                    
                if start_index == (2 * bilinear_pieces):
                    break 
            
            ##Making sure that only 1 u and 1 v are selected at each point in time
            start_index = 0
            temp_term_u = ''
            temp_term_v = ''
            for j in range (0, dim_streams_bilin_terms[0]):
                if linearized_list['streams_bilin_new']['Name_parent'][j] == sorted_terms['streams_bilinear']['Name'][i]:                       #Making sure that stream names match 
                    ##Checking if it is u or v 
                    if linearized_list['streams_bilin_new']['Variable'][j] == 'u':
                        if not temp_term_u:
                            temp_term_u = linearized_list['streams_bilin_new']['Name'][j] + '_y'
                            start_index = start_index + 1
                        else:
                            temp_term_u = temp_term_u + ' + ' + linearized_list['streams_bilin_new']['Name'][j] + '_y'
                            start_index = start_index + 1
                    if linearized_list['streams_bilin_new']['Variable'][j] == 'v':
                        if not temp_term_v:
                            temp_term_v = linearized_list['streams_bilin_new']['Name'][j] + '_y'
                            start_index = start_index + 1                            
                        else:
                            temp_term_v = temp_term_v + ' + ' + linearized_list['streams_bilin_new']['Name'][j] + '_y'
                            start_index = start_index + 1                    
                if start_index == (2 * bilinear_pieces):
                    break
            current_index = current_index + 1
            temp_term_u1 = temp_term_u + ' <= 1'
            temp_term_u1 = 'c' + str(current_index) + ': ' + temp_term_u1
            f_data_set.write(temp_term_u1 + '\n')
            current_index = current_index + 1
            temp_term_v1 = temp_term_v + ' <= 1'
            temp_term_v1 = 'c' + str(current_index) + ': ' + temp_term_v1
            f_data_set.write(temp_term_v1 + '\n')
                    
            ##Making sure that if the master is switched off, all u and vs are switched off also
            current_index = current_index + 1
            temp_term_uv = temp_term_u + ' + ' + temp_term_v
            temp_term_uv = temp_term_uv + ' - 2 ' + sorted_terms['streams_bilinear']['Parent'][i] + '_y = 0'
            temp_term_uv = 'c' + str(current_index) + ': ' + temp_term_uv
            f_data_set.write(temp_term_uv + '\n') 
            
            ##Making sure that u and v are in sync with x and y 
            temp_term_u_full = ''
            temp_term_v_full = ''
            start_index = 0
            for j in range (0, dim_streams_bilin_terms[0]):
                if linearized_list['streams_bilin_new']['Name_parent'][j] == sorted_terms['streams_bilinear']['Name'][i]:                       #Making sure that stream names match 
                ##Checking if it is u or v 
                    if linearized_list['streams_bilin_new']['Variable'][j] == 'u':
                        if not temp_term_u_full:
                            temp_term_u_full = linearized_list['streams_bilin_new']['Name'][j]
                            start_index = start_index + 1 
                        else:
                            temp_term_u_full = temp_term_u_full + ' + ' + linearized_list['streams_bilin_new']['Name'][j]
                            start_index = start_index + 1
                    if linearized_list['streams_bilin_new']['Variable'][j] == 'v':
                        if not temp_term_v_full:
                            temp_term_v_full = linearized_list['streams_bilin_new']['Name'][j]
                            start_index = start_index + 1 
                        else:
                            temp_term_v_full = temp_term_v_full + ' + ' + linearized_list['streams_bilin_new']['Name'][j]
                            start_index = start_index + 1
                            
                if start_index == (2 * bilinear_pieces):
                    break
            
            ##Writing the x + y term
            current_index = current_index + 1
            temp_term = 'c' + str(current_index) + ': ' + temp_term_u_full
            temp_term = temp_term + ' - ' + sorted_terms['streams_bilinear']['Parent'][i] + '_' + sorted_terms['streams_bilinear']['Parent_v1_name'][i]
            temp_term = temp_term + ' - ' + sorted_terms['streams_bilinear']['Parent'][i] + '_' + sorted_terms['streams_bilinear']['Parent_v2_name'][i]
            temp_term = temp_term + ' = 0'
            f_data_set.write(temp_term + '\n')

            ##Writing the x - y term 
            current_index = current_index + 1
            temp_term = 'c' + str(current_index) + ': ' + temp_term_v_full       
            temp_term = temp_term + ' - ' + sorted_terms['streams_bilinear']['Parent'][i] + '_' + sorted_terms['streams_bilinear']['Parent_v1_name'][i]
            temp_term = temp_term + ' + ' + sorted_terms['streams_bilinear']['Parent'][i] + '_' + sorted_terms['streams_bilinear']['Parent_v2_name'][i]
            temp_term = temp_term + ' = 0'
            f_data_set.write(temp_term + '\n')    
 
    f_data_set.write('\n')
###############################################################################################################################################################################################

    f_data_set.write('\\\\ Writing the streams_type: network_parallel \n \n')

    dim_streams_bilin_contbin_new = streams_bilin_contbin_new.shape
    
    if dim_streams_bilin_contbin_new[0] > 0:
        ##Writing the representative 'x' component for the binary x continuous representation with the assumption that there are no additional bilinear terms embedded
        for i in range (0, dim_streams_bilin_contbin_new[0]):
            if streams_bilin_contbin_new['InOut'][i] == 'out':
                current_index = current_index + 1
                temp_term = ''
                temp_term = temp_term + 'c' + str(current_index) + ': '
                temp_term = temp_term + str(streams_bilin_contbin_new['Stream_coeff_v1_1'][i]) + ' '
                temp_term = temp_term + streams_bilin_contbin_new['Parent'][i] + '_' + streams_bilin_contbin_new['Parent_v1_name'][i]
                if streams_bilin_contbin_new['Parent_v2_name'][i] != '-':
                    temp_term = temp_term + ' + ' + str(streams_bilin_contbin_new['Stream_coeff_v2_1'][i]) + ' '
                    temp_term = temp_term + streams_bilin_contbin_new['Parent'][i] + '_' + streams_bilin_contbin_new['Parent_v2_name'][i]
                temp_term = temp_term + ' + ' + str(streams_bilin_contbin_new['Stream_coeff_cst'][i]) + ' ' 
                temp_term = temp_term + streams_bilin_contbin_new['Parent'][i] + '_y'
                temp_term = temp_term + ' - ' + streams_bilin_contbin_new['Temp_name'][i] + ' = 0'
                f_data_set.write(temp_term + '\n')
                
        ##Selecting the largest one will involve exponentially large number of constraints 
        for i in range (0, dim_layerslist[0]):
            ##Identifying the specific parallel network layer name 
            if original_data['layerslist']['Type'][i] == 'network_parallel':
                layer_name = original_data['layerslist']['Name'][i]
                ##Scanning through the parallel network list to identify those with the same network name 
                ##Setting a temporary dataframe to store the possible combinations 
                cont_binary_combinations = pd.DataFrame(columns = ['Y_name', 'X1_name', 'X2_name', 'X1X2_name', 'Z_name_new', 'Fmin_X1X2', 'Fmax_X1X2'])
                for j in range (0, dim_streams_bilin_contbin_new[0]):
                    if streams_bilin_contbin_new['Layer'][j] == layer_name:
                        if streams_bilin_contbin_new['InOut'][j] == 'out': 
                            Y_name = streams_bilin_contbin_new['Temp_name'][j] + '_y'
                            X1_name = streams_bilin_contbin_new['Temp_name'][j]
                            FminX1 = streams_bilin_contbin_new['Stream_coeff_v1_1'][j] * streams_bilin_contbin_new['P_fmin_v1'][j]
                            FmaxX1 = streams_bilin_contbin_new['Stream_coeff_v1_1'][j] * streams_bilin_contbin_new['P_fmax_v1'][j]
                            if streams_bilin_contbin_new['Parent_v2_name'][j] != '-':
                                FminX1 = FminX1 + (streams_bilin_contbin_new['Stream_coeff_v2_1'][j] * streams_bilin_contbin_new['P_fmin_v2'][j])
                                FmaxX1 = FmaxX1 + (streams_bilin_contbin_new['Stream_coeff_v2_1'][j] * streams_bilin_contbin_new['P_fmax_v2'][j])
                            FminX1 = FminX1 + (streams_bilin_contbin_new['Stream_coeff_cst'][j])
                            FmaxX1 = FmaxX1 + (streams_bilin_contbin_new['Stream_coeff_cst'][j])
                            ##Scanning through the list again to find possible combinations 
                            for k in range (0, dim_streams_bilin_contbin_new[0]):
                                if streams_bilin_contbin_new['Layer'][j] == layer_name:
                                    ##To avoid self combination 
                                    if k != j:
                                        if streams_bilin_contbin_new['InOut'][k] == 'out':
                                            X2_name = streams_bilin_contbin_new['Temp_name'][k]
                                            X1X2_name = streams_bilin_contbin_new['Temp_name'][j] + '_' + streams_bilin_contbin_new['Parent'][k]
                                            Z_name_new = X1X2_name + '_z'
                                            
                                            FminX2 = streams_bilin_contbin_new['Stream_coeff_v1_1'][k] * streams_bilin_contbin_new['P_fmin_v1'][k]
                                            FmaxX2 = streams_bilin_contbin_new['Stream_coeff_v1_1'][k] * streams_bilin_contbin_new['P_fmax_v1'][k]
                                            if streams_bilin_contbin_new['Parent_v2_name'][k] != '-':
                                                FminX2 = FminX2 + (streams_bilin_contbin_new['Stream_coeff_v2_1'][k] * streams_bilin_contbin_new['P_fmin_v2'][k])
                                                FmaxX2 = FmaxX2 + (streams_bilin_contbin_new['Stream_coeff_v2_1'][k] * streams_bilin_contbin_new['P_fmax_v2'][k])
                                            FminX2 = FminX2 + (streams_bilin_contbin_new['Stream_coeff_cst'][k])
                                            FmaxX2 = FmaxX2 + (streams_bilin_contbin_new['Stream_coeff_cst'][k])
                                            
                                            FminX1X2 = FminX1 - FmaxX2
                                            FmaxX1X2 = FmaxX1 - FminX2
                                            
                                            temp_data = [Y_name, X1_name, X2_name, X1X2_name, Z_name_new, FminX1X2, FmaxX1X2]
                                            temp_datadf = pd.DataFrame(data = [temp_data], columns = ['Y_name', 'X1_name', 'X2_name', 'X1X2_name', 'Z_name_new', 'Fmin_X1X2', 'Fmax_X1X2'])
                                            cont_binary_combinations = cont_binary_combinations.append(temp_datadf, ignore_index = True)

        ##Writing the expanded constraints 
        dim_cont_binary_combination = cont_binary_combinations.shape
        
        for i in range (0, dim_cont_binary_combination[0]):
            ##Writing the equlivance constraint 
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': ' 
            temp_term = temp_term + cont_binary_combinations['X1_name'][i] + ' - ' + cont_binary_combinations['X2_name'][i] + ' - ' + cont_binary_combinations['X1X2_name'][i] + ' = 0'
            f_data_set.write(temp_term + '\n')
            
            ##This section writes the linearized form constraints 
            
            ##Constraint 1: Fmin y - z <= 0
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + str(cont_binary_combinations['Fmin_X1X2'][i]) + ' ' + cont_binary_combinations['Y_name'][i]
            temp_term = temp_term + ' - ' + cont_binary_combinations['Z_name_new'][i] + ' <= 0'
            f_data_set.write(temp_term + '\n')    
            
            ##Constraint 2: z - Fmax y <= 0
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + cont_binary_combinations['Z_name_new'][i] + ' - '
            temp_term = temp_term + str(cont_binary_combinations['Fmax_X1X2'][i]) + ' ' + cont_binary_combinations['Y_name'][i]
            temp_term = temp_term + ' <= 0'
            f_data_set.write(temp_term + '\n')

            ##Constraint 3: x + Fmax y - z <= Fmax
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + cont_binary_combinations['X1X2_name'][i]
            temp_term = temp_term + ' + ' + str(cont_binary_combinations['Fmax_X1X2'][i]) + ' ' + cont_binary_combinations['Y_name'][i]
            temp_term = temp_term + ' - ' + cont_binary_combinations['Z_name_new'][i]
            temp_term = temp_term + ' <= ' + str(cont_binary_combinations['Fmax_X1X2'][i])
            f_data_set.write(temp_term + '\n')
            
            ##Constraint 4: z - x - Fmin y <= - Fmin 
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + cont_binary_combinations['Z_name_new'][i] + ' - ' 
            temp_term = temp_term + cont_binary_combinations['X1X2_name'][i] + ' - '
            temp_term = temp_term + str(cont_binary_combinations['Fmin_X1X2'][i]) + ' ' + cont_binary_combinations['Y_name'][i]
            temp_term = temp_term + ' <= ' + str(-1 * cont_binary_combinations['Fmin_X1X2'][i])
            f_data_set.write(temp_term + '\n')

            ##Constraint 5: z - x + Fmax y <= Fmax
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '
            temp_term = temp_term + cont_binary_combinations['Z_name_new'][i] + ' - '
            temp_term = temp_term + cont_binary_combinations['X1X2_name'][i] + ' + '
            temp_term = temp_term + str(cont_binary_combinations['Fmax_X1X2'][i]) + ' ' + cont_binary_combinations['Y_name'][i]
            temp_term = temp_term + ' <= ' + str(cont_binary_combinations['Fmax_X1X2'][i])
            f_data_set.write(temp_term + '\n')

        ##Writing the constraing for which only 1 y can be selected
        lhs_term = ''
        for i in range (0, dim_cont_binary_combination[0]):
            if not lhs_term: 
                lhs_term = lhs_term + cont_binary_combinations['Y_name'][i]
            else:
                lhs_term = lhs_term + ' + ' + cont_binary_combinations['Y_name'][i]

        current_index = current_index + 1
        total_term = 'c' + str(current_index) + ': '
        total_term = total_term + lhs_term + ' <= 1'
    
        ##Writing the stream balancing constraint
        lhs_lhs_term = ''
        for i in range (0, dim_streams_bilin_contbin_new[0]):
            if streams_bilin_contbin_new['InOut'][i] == 'in':
                layer_name = streams_bilin_contbin_new['Layer'][i]
                lhs_rhs_term = ''
                lhs_rhs_term = lhs_rhs_term + str(streams_bilin_contbin_new['Stream_coeff_v1_1'][i]) + ' ' 
                lhs_rhs_term = lhs_rhs_term + streams_bilin_contbin_new['Parent'][i] + '_' + streams_bilin_contbin_new['Parent_v1_name'][i]
                if streams_bilin_contbin_new['Parent_v2_name'][i] != '-':
                    lhs_rhs_term = lhs_rhs_term + ' - ' + str(streams_bilin_contbin_new['Stream_coeff_v2_1'][i]) + ' ' 
                    lhs_rhs_term = lhs_rhs_term + streams_bilin_contbin_new['Parent'][i] + '_' + streams_bilin_contbin_new['Parent_v2_name'][i]                   
                for j in range (0, dim_streams_bilin_contbin_new[0]):
                    if streams_bilin_contbin_new['InOut'][j] == 'out':                    
                        if streams_bilin_contbin_new['Layer'][j] == layer_name:
                            ##Determining the limits of each out stream belonging to the same layer 
                            Fmin_1 = streams_bilin_contbin_new['Stream_coeff_v1_1'][j] * streams_bilin_contbin_new['P_fmin_v1'][j]
                            Fmax_1 = streams_bilin_contbin_new['Stream_coeff_v1_1'][j] * streams_bilin_contbin_new['P_fmax_v1'][j]
                            if streams_bilin_contbin_new['Parent_v2_name'][j] != '-':
                                Fmin_1 = Fmin_1 + streams_bilin_contbin_new['Stream_coeff_v2_1'][j] * streams_bilin_contbin_new['P_fmin_v2'][j]
                                Fmax_1 = Fmax_1 + streams_bilin_contbin_new['Stream_coeff_v2_1'][j] * streams_bilin_contbin_new['P_fmax_v2'][j]     
                            Fmin_1 = Fmin_1 + streams_bilin_contbin_new['Stream_coeff_cst'][j]
                            Fmax_1 = Fmax_1 + streams_bilin_contbin_new['Stream_coeff_cst'][j]                                

                            ##Constraint 1: Fmin y - z <= 0
                            current_index = current_index + 1
                            temp_term = ''
                            temp_term = temp_term + 'c' + str(current_index) + ': '
                            temp_term = temp_term + str(Fmin_1) + ' ' + streams_bilin_contbin_new['Temp_name'][j] + '_y'
                            temp_term = temp_term + ' - ' + streams_bilin_contbin_new['Temp_name'][j] + '_z'
                            temp_term = temp_term + ' <= 0'
                            f_data_set.write(temp_term + '\n')

                            ##Constraint 2: z - Fmax y <= 0                            
                            current_index = current_index + 1
                            temp_term = ''
                            temp_term = temp_term + 'c' + str(current_index) + ': '
                            temp_term = temp_term + streams_bilin_contbin_new['Temp_name'][j] + '_z'
                            temp_term = temp_term + ' - ' + str(Fmax_1) + ' ' + streams_bilin_contbin_new['Temp_name'][j] + '_y'
                            temp_term = temp_term + ' <= 0'
                            f_data_set.write(temp_term + '\n')

                            ##Constraint 3: x + Fmax y - z <= Fmax
                            current_index = current_index + 1
                            temp_term = ''
                            temp_term = temp_term + 'c' + str(current_index) + ': '
                            temp_term = temp_term + streams_bilin_contbin_new['Temp_name'][j] 
                            temp_term = temp_term + ' + ' + str(Fmax_1) + ' ' +  streams_bilin_contbin_new['Temp_name'][j] + '_y'
                            temp_term = temp_term + ' - ' + streams_bilin_contbin_new['Temp_name'][j] + '_z'
                            temp_term = temp_term + ' <= ' + str(Fmax_1)
                            f_data_set.write(temp_term + '\n')

                            ##Constraint 4: z - x - Fmin y <= - Fmin
                            current_index = current_index + 1
                            temp_term = ''
                            temp_term = temp_term + 'c' + str(current_index) + ': '
                            temp_term = temp_term + streams_bilin_contbin_new['Temp_name'][j] + '_z'
                            temp_term = temp_term + ' - ' + streams_bilin_contbin_new['Temp_name'][j]
                            temp_term = temp_term + ' - ' + str(Fmin_1) + ' ' +  streams_bilin_contbin_new['Temp_name'][j] + '_y'
                            temp_term = temp_term + ' <= ' + str(-1 * Fmin_1)
                            f_data_set.write(temp_term + '\n')
                
                            ##Constraint 5: z - x + Fmax y <= Fmax                                                                               
                            current_index = current_index + 1
                            temp_term = ''
                            temp_term = temp_term + 'c' + str(current_index) + ': '
                            temp_term = temp_term + streams_bilin_contbin_new['Temp_name'][j] + '_z'
                            temp_term = temp_term + ' - ' + streams_bilin_contbin_new['Temp_name'][j]
                            temp_term = temp_term + ' + ' + str(Fmax_1) + ' ' + streams_bilin_contbin_new['Temp_name'][j] + '_y'
                            temp_term = temp_term + ' <= ' + str(Fmax_1)
                            f_data_set.write(temp_term + '\n')

                            if not lhs_lhs_term: 
                                lhs_lhs_term = lhs_lhs_term + streams_bilin_contbin_new['Temp_name'][j] + '_z'
                            else:
                                lhs_lhs_term = lhs_lhs_term + ' + ' + streams_bilin_contbin_new['Temp_name'][j] + '_z'
            
                current_index = current_index + 1
                temp_term = ''
                temp_term = temp_term + 'c' + str(current_index) + ': '
                temp_term = temp_term + lhs_lhs_term + ' - ' + lhs_rhs_term 
                temp_term = temp_term + ' = 0'
                f_data_set.write(temp_term + '\n')  
            
    f_data_set.write('\n')            

###############################################################################################################################################################################################
    ##Writing the additional constraints 

    f_data_set.write('\\\\ Writing additional constraints terms \n \n')
    
    dim_cons_eqns = original_data['cons_eqns'].shape
    dim_cons_eqn_terms = original_data['cons_eqns_terms'].shape
    dim_cons_eqn_terms_bilinear = sorted_terms['cons_eqn_terms_bilinear'].shape
    dim_cons_eqn_terms_linear = sorted_terms['cons_eqn_terms_linear'].shape            
    dim_cons_eqn_terms_bilin_new = linearized_list['cons_eqn_terms_bilin_new'].shape  

    ##Merging the dual_variable_constraint lists of both the utility and the process for easy scanning 
    combined_dual_variable_constraint_bilinear = pd.DataFrame(columns = ['Name', 'Variable1', 'Variable2', 'Fmin_v1', 'Fmax_v1', 'Fmin_v2', 'Fmax_v2', 'Coeff_v1_2', 'Coeff_v1_1', 
                                                                'Coeff_v2_2', 'Coeff_v2_1', 'Coeff_v1_v2', 'Coeff_cst', 'Fmin', 'Fmax', 'Cost_v1_2', 'Cost_v1_1', 'Cost_v2_2', 
                                                                'Cost_v2_1', 'Cost_v1_v2', 'Cost_cst', 'Cinv_v1_2', 'Cinv_v1_1', 'Cinv_v2_2', 'Cinv_v2_1', 'Cinv_v1_v2', 
                                                                'Cinv_cst', 'Power_v1_2', 'Power_v1_1', 'Power_v2_2', 'Power_v2_1', 'Power_v1_v2', 'Power_cst', 'Impact_v1_2', 
                                                                'Impact_v1_1', 'Impact_v2_2', 'Impact_v2_1', 'Impact_v1_v2', 'Impact_cst'])
    combined_dual_variable_constraint_bilinear = combined_dual_variable_constraint_bilinear.append(sorted_terms['dual_variable_constraint_utility_bilinear'], ignore_index = True)
    combined_dual_variable_constraint_bilinear = combined_dual_variable_constraint_bilinear.append(sorted_terms['dual_variable_constraint_process_bilinear'], ignore_index = True)
    dim_combined_dual_variable_constraint_bilinear = combined_dual_variable_constraint_bilinear.shape
    
    f_data_set.write('\\\\ Writing additional constraints terms: unit_link \n \n')
    
    for i in range (0, dim_cons_eqns[0]):
        
        if original_data['cons_eqns']['Type'][i] == 'unit_link':
            
            temp_term = ''
            rhs_value = original_data['cons_eqns']['RHS_value'][i]
            
            ##Determining the sign
            if original_data['cons_eqns']['Sign'][i] == 'equal_to':
                sign = '='
            elif original_data['cons_eqns']['Sign'][i] == 'less_than_equal_to':
                sign = '<='
            elif original_data['cons_eqns']['Sign'][i] == 'greater_than_equal_to':
                sign = '>='
                
            ##Searching through the linear terms first
            for j in range (0, dim_cons_eqn_terms_linear[0]):
                if sorted_terms['cons_eqn_terms_linear']['Parent_eqn'][j] == original_data['cons_eqns']['Name'][i]:
                    ##Checking the meaning of individual terms 
                    if sorted_terms['cons_eqn_terms_linear']['Coeff_v1_1'][j] == 1:
                        ##Checking if it is the first term 
                        if not temp_term:
                            temp_term = temp_term + str(sorted_terms['cons_eqn_terms_linear']['Coefficient'][j]) + ' ' 
                            temp_term = temp_term + sorted_terms['cons_eqn_terms_linear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_linear']['Parent_v1_name'][j]
                        else:
                            temp_term = temp_term + ' + ' + str(sorted_terms['cons_eqn_terms_linear']['Coefficient'][j]) + ' '
                            temp_term = temp_term + temp_term + sorted_terms['cons_eqn_terms_linear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_linear']['Parent_v1_name'][j]
                    elif sorted_terms['cons_eqn_terms_linear']['Coeff_v2_1'][j] == 1:
                        ##Checking if it is the first term 
                        if not temp_term:
                            temp_term = temp_term + str(sorted_terms['cons_eqn_terms_linear']['Coefficient'][j]) + ' ' 
                            temp_term = temp_term + sorted_terms['cons_eqn_terms_linear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_linear']['Parent_v2_name'][j]
                        else:
                            temp_term = temp_term + ' + ' + str(sorted_terms['cons_eqn_terms_linear']['Coefficient'][j]) + ' '
                            temp_term = temp_term + temp_term + sorted_terms['cons_eqn_terms_linear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_linear']['Parent_v2_name'][j]
            
            ##Searching through the bilinear terms
            for j in range (0, dim_cons_eqn_terms_bilinear[0]):
                if sorted_terms['cons_eqn_terms_bilinear']['Parent_eqn'][j] == original_data['cons_eqns']['Name'][i]: 
                    ##Checking the meaning of individual terms 
                    if sorted_terms['cons_eqn_terms_bilinear']['Coeff_v1_1'][j] == 1:
                        ##Checking if it is the first term 
                        if not temp_term:
                            temp_term = temp_term + str(sorted_terms['cons_eqn_terms_bilinear']['Coefficient'][j]) + ' ' 
                            temp_term = temp_term + sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_bilinear']['Parent_v1_name'][j]
                        else:
                            temp_term = temp_term + ' + ' + str(sorted_terms['cons_eqn_terms_bilinear']['Coefficient'][j]) + ' '
                            temp_term = temp_term + temp_term + sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_bilinear']['Parent_v1_name'][j]
                    elif sorted_terms['cons_eqn_terms_bilinear']['Coeff_v2_1'][j] == 1:
                        ##Checking if it is the first term 
                        if not temp_term:
                            temp_term = temp_term + str(sorted_terms['cons_eqn_terms_bilinear']['Coefficient'][j]) + ' ' 
                            temp_term = temp_term + sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_bilinear']['Parent_v2_name'][j]
                        else:
                            temp_term = temp_term + ' + ' + str(sorted_terms['cons_eqn_terms_bilinear']['Coefficient'][j]) + ' '
                            temp_term = temp_term + temp_term + sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_bilinear']['Parent_v2_name'][j]
                    elif sorted_terms['cons_eqn_terms_bilinear']['Coeff_v1v2'][j] == 1:
                        ##Scanning through the dual variable constraints for relevant information 
                        multiplier = sorted_terms['cons_eqn_terms_bilinear']['Coefficient'][j]
                        for k in range (0, dim_combined_dual_variable_constraint_bilinear[0]):
                            if combined_dual_variable_constraint_bilinear['Name'][k] == sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j]:                                
                                ##Checking if it is the first term 
                                if not temp_term:
                                    temp_term = temp_term + str(multiplier * combined_dual_variable_constraint_bilinear['Coeff_v1_1'][k]) + ' ' 
                                    temp_term = temp_term + combined_dual_variable_constraint_bilinear['Name'][k] + '_' + combined_dual_variable_constraint_bilinear['Variable1'][k]
                                    
                                    ##Checking if the second term exists 
                                    if combined_dual_variable_constraint_bilinear['Variable2'][k] != '-':
                                        temp_term = temp_term + ' + ' + str(multiplier * combined_dual_variable_constraint_bilinear['Coeff_v2_1'][k]) + ' '
                                        temp_term = temp_term + combined_dual_variable_constraint_bilinear['Name'][k] + '_' + combined_dual_variable_constraint_bilinear['Variable2'][k]
                                
                                else:
                                    temp_term = temp_term + ' + ' + str(multiplier * combined_dual_variable_constraint_bilinear['Coeff_v1_1'][k]) + ' ' 
                                    temp_term = temp_term + combined_dual_variable_constraint_bilinear['Name'][k] + '_' + combined_dual_variable_constraint_bilinear['Variable1'][k]

                                    ##Checking if the second term exists 
                                    if combined_dual_variable_constraint_bilinear['Variable2'][k] != '-':                                    
                                        temp_term = temp_term + ' + ' + str(multiplier * combined_dual_variable_constraint_bilinear['Coeff_v2_1'][k]) + ' '
                                        temp_term = temp_term + combined_dual_variable_constraint_bilinear['Name'][k] + '_' + combined_dual_variable_constraint_bilinear['Variable2'][k]     
                                
                                bilin_multiplier =  combined_dual_variable_constraint_bilinear['Coeff_v1_v2'][k]
                                ##Getting ready the additional terms of u and v
                                start_index = 0
                                bilin_terms = ''
                                for l in range (0, dim_cons_eqn_terms_bilin_new[0]):
                                    if linearized_list['cons_eqn_terms_bilin_new']['Name_parent'][l] == sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j]:
                                        if linearized_list['cons_eqn_terms_bilin_new']['Variable'][l] == 'u':
                                            ##Chekcing if it is the first term
                                            if not bilin_terms:
                                                bilin_terms = bilin_terms + str(multiplier * bilin_multiplier * linearized_list['cons_eqn_terms_bilin_new']['Coeff'][l]) + ' '
                                                bilin_terms = bilin_terms + linearized_list['cons_eqn_terms_bilin_new']['Name'][l]
                                                bilin_terms = bilin_terms + ' + ' + str(multiplier * bilin_multiplier * linearized_list['cons_eqn_terms_bilin_new']['Intercept'][l]) + ' '
                                                bilin_terms = bilin_terms + linearized_list['cons_eqn_terms_bilin_new']['Name'][l] + '_y'
                                                start_index = start_index + 1
                                            else:
                                                bilin_terms = bilin_terms + ' + ' + str(multiplier * bilin_multiplier * linearized_list['cons_eqn_terms_bilin_new']['Coeff'][l]) + ' '
                                                bilin_terms = bilin_terms + linearized_list['cons_eqn_terms_bilin_new']['Name'][l]
                                                bilin_terms = bilin_terms + ' + ' + str(multiplier * bilin_multiplier * linearized_list['cons_eqn_terms_bilin_new']['Intercept'][l]) + ' '
                                                bilin_terms = bilin_terms + linearized_list['cons_eqn_terms_bilin_new']['Name'][l] + '_y' 
                                                start_index = start_index + 1
                                        elif linearized_list['cons_eqn_terms_bilin_new']['Variable'][l] == 'v':
                                            bilin_terms = bilin_terms + ' - ' + str(multiplier * bilin_multiplier * linearized_list['cons_eqn_terms_bilin_new']['Coeff'][l]) + ' '
                                            bilin_terms = bilin_terms + linearized_list['cons_eqn_terms_bilin_new']['Name'][l]
                                            bilin_terms = bilin_terms + ' - ' + str(multiplier * bilin_multiplier * linearized_list['cons_eqn_terms_bilin_new']['Intercept'][l]) + ' '
                                            bilin_terms = bilin_terms + linearized_list['cons_eqn_terms_bilin_new']['Name'][l] + '_y' 
                                            start_index = start_index + 1 
                                            
                                    if start_index == (2 * bilinear_pieces):
                                        break
                                    
                                temp_term = temp_term + ' + ' + bilin_terms 
                                temp_term = temp_term + ' + ' + str(multiplier * combined_dual_variable_constraint_bilinear['Coeff_cst'][k]) 
                                temp_term = temp_term + ' ' + combined_dual_variable_constraint_bilinear['Name'][k] + '_y'

            ##Writing the constraint
            current_index = current_index + 1
            temp_term = 'c' + str(current_index) + ': ' + temp_term + ' ' + sign + ' ' + str(rhs_value)
            f_data_set.write(temp_term + '\n')

    f_data_set.write('\n')                                
    f_data_set.write('\\\\ Writing additional constraints terms: unit_binary \n \n')
    
    for i in range (0, dim_cons_eqns[0]):
        
        if original_data['cons_eqns']['Type'][i] == 'unit_binary':
            
            rhs_value = original_data['cons_eqns']['RHS_value'][i]
            
            ##Determining the sign
            if original_data['cons_eqns']['Sign'][i] == 'equal_to':
                sign = '='
            elif original_data['cons_eqns']['Sign'][i] == 'less_than_equal_to':
                sign = '<='
            elif original_data['cons_eqns']['Sign'][i] == 'greater_than_equal_to':
                sign = '>='
            
            ##Assembling the LHS of the equation
            lhs_term = ''
            for j in range (0, dim_cons_eqn_terms[0]):
                if original_data['cons_eqns_terms']['Parent_eqn'][j] == original_data['cons_eqns']['Name'][i]:
                    ##Checking if it is the first term 
                    if not lhs_term:
                        lhs_term = lhs_term + str(original_data['cons_eqns_terms']['Coefficient'][j]) + ' '
                        lhs_term = lhs_term + original_data['cons_eqns_terms']['Parent_unit'][j] + '_y'
                    else:
                        lhs_term = lhs_term + ' + ' + str(original_data['cons_eqns_terms']['Coefficient'][j]) + ' '
                        lhs_term = lhs_term + original_data['cons_eqns_terms']['Parent_unit'][j] + '_y'

            ##Writing the constraint 
            current_index = current_index + 1
            temp_term = 'c' + str(current_index) + ': ' + lhs_term 
            temp_term = temp_term + ' ' + sign + ' ' + str(rhs_value) 
            f_data_set.write(temp_term + '\n')                                   
    
    f_data_set.write('\n')
    f_data_set.write('\\\\ Writing additional constraints terms: stream_limit_modified \n \n')

    for i in range (0, dim_cons_eqns[0]):
        
        if original_data['cons_eqns']['Type'][i] == 'stream_limit_modified':  
            
            rhs_value = original_data['cons_eqns']['RHS_value'][i]
            
            ##Determining the sign
            if original_data['cons_eqns']['Sign'][i] == 'equal_to':
                sign = '='
            elif original_data['cons_eqns']['Sign'][i] == 'less_than_equal_to':
                sign = '<='
            elif original_data['cons_eqns']['Sign'][i] == 'greater_than_equal_to':
                sign = '>='
            
            ##Assembling the LHS of the equation
            
            ##Checking the linear equations first
            lhs_term = ''
            for j in range (0, dim_cons_eqn_terms_linear[0]):
                
                if sorted_terms['cons_eqn_terms_linear']['Parent_eqn'][j] == original_data['cons_eqns']['Name'][i]:
                    ##Checking if it is the first term 
                    if not lhs_term:
                        lhs_term = lhs_term + str(sorted_terms['cons_eqn_terms_linear']['Coeff_v1_1'][j]) + ' ' 
                        lhs_term = lhs_term + sorted_terms['cons_eqn_terms_linear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_linear']['Parent_v1_name'][j]
                        lhs_term = lhs_term + ' + ' + str(sorted_terms['cons_eqn_terms_linear']['Coeff_v2_1'][j]) + ' '
                        lhs_term = lhs_term + sorted_terms['cons_eqn_terms_linear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_linear']['Parent_v2_name'][j]
                        lhs_term = lhs_term + ' + ' + str(sorted_terms['cons_eqn_terms_linear']['Coeff_cst'][j]) + ' '
                        lhs_term = lhs_term + sorted_terms['cons_eqn_terms_linear']['Parent_unit'][j] + '_y'
                    else:
                        lhs_term = ' + ' + lhs_term + str(sorted_terms['cons_eqn_terms_linear']['Coeff_v1_1'][j]) + ' ' 
                        lhs_term = lhs_term + sorted_terms['cons_eqn_terms_linear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_linear']['Parent_v1_name'][j]
                        lhs_term = lhs_term + ' + ' + str(sorted_terms['cons_eqn_terms_linear']['Coeff_v2_1'][j]) + ' '
                        lhs_term = lhs_term + sorted_terms['cons_eqn_terms_linear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_linear']['Parent_v2_name'][j]
                        lhs_term = lhs_term + ' + ' + str(sorted_terms['cons_eqn_terms_linear']['Coeff_cst'][j]) + ' '
                        lhs_term = lhs_term + sorted_terms['cons_eqn_terms_linear']['Parent_unit'][j] + '_y'      

            for j in range (0, dim_cons_eqn_terms_bilinear[0]):
                
                if sorted_terms['cons_eqn_terms_bilinear']['Parent_eqn'][j] == original_data['cons_eqns']['Name'][i]:
                    ##Assembling the bilinear terms 
                    multiplier = sorted_terms['cons_eqn_terms_bilinear']['Coeff_v1v2'][j]
                    bilin_terms = ''
                    start_index = 0
                    for k in range (0, dim_cons_eqn_terms_bilin_new[0]):
                        if linearized_list['cons_eqn_terms_bilin_new']['Name_parent'][k] == sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j]:
                            ##Checking if it is the first term 
                            if not bilin_terms:
                                bilin_terms = bilin_terms + str(multiplier * linearized_list['cons_eqn_terms_bilin_new']['Coeff'][k]) + ' ' 
                                bilin_terms = bilin_terms + linearized_list['cons_eqn_terms_bilin_new']['Name'][k]
                                bilin_terms = bilin_terms + ' + ' + str(multiplier * linearized_list['cons_eqn_terms_bilin_new']['Intercept'][k]) + ' '
                                bilin_terms = bilin_terms + linearized_list['cons_eqn_terms_bilin_new']['Name'][k] + '_y'
                                start_index = start_index + 1
                            else:
                                if linearized_list['cons_eqn_terms_bilin_new']['Variable'][k] == 'u':
                                    bilin_terms = bilin_terms + ' + ' + str(multiplier * linearized_list['cons_eqn_terms_bilin_new']['Coeff'][k]) + ' ' 
                                    bilin_terms = bilin_terms + linearized_list['cons_eqn_terms_bilin_new']['Name'][k]
                                    bilin_terms = bilin_terms + ' + ' + str(multiplier * linearized_list['cons_eqn_terms_bilin_new']['Intercept'][k]) + ' '
                                    bilin_terms = bilin_terms + linearized_list['cons_eqn_terms_bilin_new']['Name'][k] + '_y'
                                    start_index = start_index + 1       
                                elif linearized_list['cons_eqn_terms_bilin_new']['Variable'][k] == 'v':
                                    bilin_terms = bilin_terms + ' - ' + str(multiplier * linearized_list['cons_eqn_terms_bilin_new']['Coeff'][k]) + ' ' 
                                    bilin_terms = bilin_terms + linearized_list['cons_eqn_terms_bilin_new']['Name'][k]
                                    bilin_terms = bilin_terms + ' - ' + str(multiplier * linearized_list['cons_eqn_terms_bilin_new']['Intercept'][k]) + ' '
                                    bilin_terms = bilin_terms + linearized_list['cons_eqn_terms_bilin_new']['Name'][k] + '_y'
                                    start_index = start_index + 1  
                        if start_index == (2 * bilinear_pieces):
                            break
                    ##Checking if it is the first term 
                    if not lhs_term:
                        lhs_term = lhs_term + str(sorted_terms['cons_eqn_terms_bilinear']['Coeff_v1_1'][j]) + ' ' 
                        lhs_term = lhs_term + sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_bilinear']['Parent_v1_name'][j]
                        lhs_term = lhs_term + ' + ' + str(sorted_terms['cons_eqn_terms_bilinear']['Coeff_v2_1'][j]) + ' '
                        lhs_term = lhs_term + sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_bilinear']['Parent_v2_name'][j]
                        lhs_term = lhs_term + ' + ' +  bilin_terms 
                        lhs_term = lhs_term + ' + ' + str(sorted_terms['cons_eqn_terms_bilinear']['Coeff_cst'][j])
                        lhs_term = lhs_term + ' ' + sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j] + '_y'
                    else:
                        lhs_term = ' + ' + lhs_term + str(sorted_terms['cons_eqn_terms_bilinear']['Coeff_v1_1'][j]) + ' ' 
                        lhs_term = lhs_term + sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_bilinear']['Parent_v1_name'][j]
                        lhs_term = lhs_term + ' + ' + str(sorted_terms['cons_eqn_terms_bilinear']['Coeff_v2_1'][j]) + ' '
                        lhs_term = lhs_term + sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j] + '_' + sorted_terms['cons_eqn_terms_bilinear']['Parent_v2_name'][j]
                        lhs_term = lhs_term + ' + ' +  bilin_terms 
                        lhs_term = lhs_term + ' + ' + str(sorted_terms['cons_eqn_terms_bilinear']['Coeff_cst'][j])
                        lhs_term = lhs_term + ' ' + sorted_terms['cons_eqn_terms_bilinear']['Parent_unit'][j] + '_y'     

            temp_term = ''
            current_index = current_index + 1
            temp_term = temp_term + 'c' + str(current_index) + ': ' + lhs_term 
            temp_term = temp_term + ' ' + sign + ' ' + str(rhs_value)

            f_data_set.write(temp_term + '\n')
            
###############################################################################################################################################################################################    
###############################################################################################################################################################################################
###############################################################################################################################################################################################
    ##Bounds section 
    f_data_set.write('\n')
    f_data_set.write('Bounds \n \n')
    
    ##Writing the bounds of variables in the utilitylist 
    f_data_set.write('\\\ Writing bounds for utility variables \n \n')
    dim_utilitylist = original_data['utilitylist'].shape 
    
    for i in range (0, dim_utilitylist[0]):
        temp_term = '' 
        temp_term = temp_term + str(original_data['utilitylist']['Fmin_v1'][i]) + ' <= '
        temp_term = temp_term + original_data['utilitylist']['Name'][i] + '_' + original_data['utilitylist']['Variable1'][i] + ' <= '
        temp_term = temp_term + str(original_data['utilitylist']['Fmax_v1'][i])
        f_data_set.write(temp_term + '\n')

        if original_data['utilitylist']['Variable2'][i] != '-':
            temp_term = '' 
            temp_term = temp_term + str(original_data['utilitylist']['Fmin_v2'][i]) + ' <= '
            temp_term = temp_term + original_data['utilitylist']['Name'][i] + '_' + original_data['utilitylist']['Variable2'][i] + ' <= '
            temp_term = temp_term + str(original_data['utilitylist']['Fmax_v2'][i])
            f_data_set.write(temp_term + '\n')
            
    f_data_set.write('\n')
    
    ##Writing the bounds of additional bilinear variables in the utilitylist 
    f_data_set.write('\\\ Writing bounds for bilinear variables in the utilitylist \n \n')
    dim_obj_func_u_bilin_new = linearized_list['obj_func_u_bilin_new'].shape
    dim_dual_v_c_util_bilin_new = linearized_list['dual_v_c_util_bilin_new'].shape
    
    ##Writing bounds for bilinear terms in the utility objective function first 
    if dim_obj_func_u_bilin_new[0] > 0:
        for i in range (0, dim_obj_func_u_bilin_new[0]):
            temp_term = ''
            temp_term = temp_term + str(linearized_list['obj_func_u_bilin_new']['Fmin_v1'][i]) + ' <= '
            temp_term = temp_term + linearized_list['obj_func_u_bilin_new']['Name'][i] 
            temp_term = temp_term + ' <= ' + str(linearized_list['obj_func_u_bilin_new']['Fmax_v1'][i])
            f_data_set.write(temp_term + '\n')
    ##Writing bounds for bilinear terms in the utility dual variable constraint
    if dim_dual_v_c_util_bilin_new[0] > 0:
        for i in range (0, dim_dual_v_c_util_bilin_new[0]):
            ##Scanning through the objective function list to check that the variable has not already been written
            check = 0
            if dim_obj_func_u_bilin_new[0] > 0:
                for j in range (0, dim_obj_func_u_bilin_new[0]):
                    if linearized_list['obj_func_u_bilin_new']['Name'][j] == linearized_list['dual_v_c_util_bilin_new']['Name'][i]:
                        check = 1
                        break
            
            ##If the term does not exist, write it
            if check == 0:
                temp_term = ''
                temp_term = temp_term + str(linearized_list['dual_v_c_util_bilin_new']['Fmin_v1'][i]) + ' <= '
                temp_term = temp_term + linearized_list['dual_v_c_util_bilin_new']['Name'][i] 
                temp_term = temp_term + ' <= ' + str(linearized_list['dual_v_c_util_bilin_new']['Fmax_v1'][i])
                f_data_set.write(temp_term + '\n')    
    
        f_data_set.write('\n') 
    
    ##Writing the bounds of variables in the processlist 
    f_data_set.write('\\\ Writing bounds for process variables \n \n')
    dim_processlist = original_data['processlist'].shape

    for i in range (0, dim_processlist[0]):
        temp_term = ''
        temp_term = temp_term + str(original_data['processlist']['Fmin_v1'][i]) + ' <= '
        temp_term = temp_term + original_data['processlist']['Name'][i] + '_' + original_data['processlist']['Variable1'][i] + ' <= '
        temp_term = temp_term + str(original_data['processlist']['Fmax_v1'][i])
        f_data_set.write(temp_term + '\n')
        
        if original_data['processlist']['Variable2'][i] != '-':
            temp_term = '' 
            temp_term = temp_term + str(original_data['processlist']['Fmin_v2'][i]) + ' <= '
            temp_term = temp_term + original_data['processlist']['Name'][i] + '_' + original_data['processlist']['Variable2'][i] + ' <= '
            temp_term = temp_term + str(original_data['processlist']['Fmax_v2'][i])
            f_data_set.write(temp_term + '\n')

    f_data_set.write('\n') 
            
    ##Writing the bounds of the bilinear variables in the processlist 
    f_data_set.write('\\\ Writing bounds for bilinear variables in the processlist \n \n')
    dim_obj_func_p_bilin_new = linearized_list['obj_func_p_bilin_new'].shape
    dim_dual_v_c_proc_bilin_new = linearized_list['dual_v_c_proc_bilin_new'].shape
    
    if dim_obj_func_p_bilin_new[0] > 0:
        for i in range (0, dim_obj_func_p_bilin_new[0]):
            temp_term = ''
            temp_term = temp_term + str(linearized_list['obj_func_p_bilin_new']['Fmin_v1'][i]) + ' <= '
            temp_term = temp_term + linearized_list['obj_func_p_bilin_new']['Name'][i] 
            temp_term = temp_term + ' <= ' + str(linearized_list['obj_func_p_bilin_new']['Fmax_v1'][i])
            f_data_set.write(temp_term + '\n')      
            
    ##Writing the bounds of the bilinear variables in the process dual variable constraint 
    if dim_dual_v_c_proc_bilin_new[0] > 0:
        for i in range (0, dim_dual_v_c_proc_bilin_new[0]):
            ##Scanning through the objective function list to check that the variable has not already been written
            check = 0
            for j in range (0, dim_dual_v_c_proc_bilin_new[0]):            
                if dim_obj_func_p_bilin_new[0] > 0:
                    for j in range (0, dim_obj_func_p_bilin_new[0]):
                        if linearized_list['obj_func_p_bilin_new']['Name'][j] == linearized_list['dual_v_c_proc_bilin_new']['Name'][i]:
                            check = 1
                            break
            
                ##If the term does not exist, write it
                if check == 0:
                    temp_term = ''
                    temp_term = temp_term + str(linearized_list['dual_v_c_proc_bilin_new']['Fmin_v1'][i]) + ' <= '
                    temp_term = temp_term + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] 
                    temp_term = temp_term + ' <= ' + str(linearized_list['dual_v_c_proc_bilin_new']['Fmax_v1'][i])
                    f_data_set.write(temp_term + '\n')    
    
        f_data_set.write('\n')             
    
    ##Writing the bounds for variables in the streams list 
    f_data_set.write('\\\ Writing bounds for variables in the streams \n \n')

    ##Writing bilinear variables which are unique only to the streams 
    f_data_set.write('\\\ Writing bounds for bilinear variables in the streams \n \n')
    dim_streams_bilin_new = linearized_list['streams_bilin_new'].shape
    dim_streams_bilin_contbin_new = streams_bilin_contbin_new.shape
    
    if dim_streams_bilin_new[0] > 0:
        for i in range (0, dim_streams_bilin_new[0]):
            check = 0
            ##Making sure that the bounds of the variable has not already been written 
            if dim_obj_func_u_bilin_new[0] > 0:
                for j in range (0, dim_obj_func_u_bilin_new[0]):
                    if linearized_list['obj_func_u_bilin_new']['Name'][j] == linearized_list['streams_bilin_new']['Name'][i]:
                        check = 1
                        break 
            if dim_dual_v_c_util_bilin_new[0] > 0:
                for j in range (0, dim_dual_v_c_util_bilin_new[0]):
                    if linearized_list['dual_v_c_util_bilin_new']['Name'][j] == linearized_list['streams_bilin_new']['Name'][i]:
                        check = 1
                        break
            if dim_obj_func_p_bilin_new[0] > 0:
                for j in range (0, dim_obj_func_p_bilin_new[0]):
                    if linearized_list['obj_func_p_bilin_new']['Name'][j] == linearized_list['streams_bilin_new']['Name'][i]:
                        check = 1
                        break  
            if dim_dual_v_c_proc_bilin_new[0] > 0:
                for j in range (0, dim_dual_v_c_proc_bilin_new[0]):
                    if linearized_list['dual_v_c_proc_bilin_new']['Name'][j] == linearized_list['streams_bilin_new']['Name'][i]:
                        check = 1
                        break       
            
            ##If it is not already written, write it 
            if check == 0:
                temp_term = ''
                temp_term = temp_term + str(linearized_list['streams_bilin_new']['Fmin_v1'][i]) + ' <= '
                temp_term = temp_term + linearized_list['streams_bilin_new']['Name'][i] 
                temp_term = temp_term + ' <= ' + str(linearized_list['streams_bilin_new']['Fmax_v1'][i])
                f_data_set.write(temp_term + '\n')  
                
        f_data_set.write('\n')  
    
    f_data_set.write('\\\ Writing bounds for bilinear variables in the streams_type: network_parallel \n \n')    
    if dim_streams_bilin_contbin_new[0]  > 0:
        for i in range (0, dim_streams_bilin_contbin_new[0]):
            if streams_bilin_contbin_new['InOut'][i] == 'out':
                ##Writing the bounds for the 'x' and 'z' terms 
                fmin = streams_bilin_contbin_new['P_fmin_v1'][i] * streams_bilin_contbin_new['Stream_coeff_v1_1'][i]
                fmax = streams_bilin_contbin_new['P_fmax_v1'][i] * streams_bilin_contbin_new['Stream_coeff_v1_1'][i]

                ##Checking if the second term exists
                if streams_bilin_contbin_new['Parent_v2_name'][i] != '-':
                    fmin = fmin + streams_bilin_contbin_new['P_fmin_v2'][i] * streams_bilin_contbin_new['Stream_coeff_v2_1'][i]
                    fmax = fmax + streams_bilin_contbin_new['P_fmax_v2'][i] * streams_bilin_contbin_new['Stream_coeff_v2_1'][i]
                
                temp_term = ''
                temp_term = temp_term + str(fmin) + ' <= ' 
                temp_term = temp_term + streams_bilin_contbin_new['Temp_name'][i]
                temp_term = temp_term + ' <= ' + str(fmax)
                f_data_set.write(temp_term + '\n')                    
                    
                temp_term = ''
                temp_term = temp_term + str(fmin) + ' <= ' 
                temp_term = temp_term + streams_bilin_contbin_new['Temp_name'][i] + '_z'
                temp_term = temp_term + ' <= ' + str(fmax)
                f_data_set.write(temp_term + '\n')    
                
        f_data_set.write('\n')    


    ##Writing the bounds for variables in the cons_eqns 
    ##There is nothing to write 
    
    f_data_set.write('Binary \n \n')    
    
    ##Writing the binary variables in the utilitylist 
    f_data_set.write('\\\ Writing the binary variables in the utilitylist \n \n')
    dim_utilitylist = original_data['utilitylist'].shape
    for i in range (0, dim_utilitylist[0]):    
        temp_term = ''
        temp_term = temp_term + original_data['utilitylist']['Name'][i] + '_y'
        f_data_set.write(temp_term + '\n')
    f_data_set.write('\n')
    ##Writing the binary variables in the processlist 
    f_data_set.write('\\\ Writing the binary variables in the processlist \n \n')
    dim_processlist = original_data['processlist'].shape
    for i in range (0, dim_processlist[0]):
        temp_term = ''
        temp_term = temp_term + original_data['processlist']['Name'][i] + '_y'
        f_data_set.write(temp_term + '\n')     
    f_data_set.write('\n')
    ##Writing the bilinear binary variables for utilities 
    f_data_set.write('\\\ Writing the bilinear binary variables for utilities \n \n')
    dim_obj_func_u_bilin_new = linearized_list['obj_func_u_bilin_new'].shape
    if dim_obj_func_u_bilin_new[0] > 0:
        for i in range (0, dim_obj_func_u_bilin_new[0]):  
            temp_term = ''
            temp_term = temp_term + linearized_list['obj_func_u_bilin_new']['Name'][i] + '_y'               
            f_data_set.write(temp_term + '\n') 
        f_data_set.write('\n')    
    dim_dual_v_c_util_bilin_new = linearized_list['dual_v_c_util_bilin_new'].shape
    if dim_dual_v_c_util_bilin_new[0] > 0:
        for i in range (0, dim_dual_v_c_util_bilin_new[0]):
            check = 0
            if dim_obj_func_u_bilin_new[0] > 0:
                for j in range (0, dim_obj_func_u_bilin_new[0]):
                    if linearized_list['obj_func_u_bilin_new']['Name'][j] == linearized_list['dual_v_c_util_bilin_new']['Name'][i]:
                        check = 1
                        break
                if check == 0:
                    temp_term = ''
                    temp_term = temp_term + linearized_list['dual_v_c_util_bilin_new']['Name'][i] + '_y'               
                    f_data_set.write(temp_term + '\n') 
    
        f_data_set.write('\n')     
                
    ##Writing the bilinear binary variables for processes
    f_data_set.write('\\\ Writing the bilinear binary variables for processes \n \n')
    dim_obj_func_p_bilin_new = linearized_list['obj_func_p_bilin_new'].shape
    if dim_obj_func_p_bilin_new[0] > 0:
        for i in range (0, dim_obj_func_p_bilin_new[0]):  
            temp_term = ''
            temp_term = temp_term + linearized_list['obj_func_p_bilin_new']['Name'][i] + '_y'               
            f_data_set.write(temp_term + '\n') 
        f_data_set.write('\n')    
    dim_dual_v_c_proc_bilin_new = linearized_list['dual_v_c_proc_bilin_new'].shape
    if dim_dual_v_c_proc_bilin_new[0] > 0:
        for i in range (0, dim_dual_v_c_proc_bilin_new[0]):
            check = 0
            if dim_obj_func_p_bilin_new[0] > 0:
                for j in range (0, dim_obj_func_p_bilin_new[0]):
                    if linearized_list['obj_func_p_bilin_new']['Name'][j] == linearized_list['dual_v_c_proc_bilin_new']['Name'][i]:
                        check = 1
                        break
                if check == 0:
                    temp_term = ''
                    temp_term = temp_term + linearized_list['dual_v_c_proc_bilin_new']['Name'][i] + '_y'               
                    f_data_set.write(temp_term + '\n')             
        f_data_set.write('\n')       

    ##Writing bilinear binary variables for streams 
    dim_streams_bilin_new = linearized_list['streams_bilin_new'].shape
    f_data_set.write('\\\ Writing the bilinear binary variables for streams \n \n')
    if dim_streams_bilin_new[0] > 0:
        for i in range (0, dim_streams_bilin_new[0]):
            check = 0
            if dim_obj_func_u_bilin_new[0] > 0:
                for j in range (0, dim_obj_func_u_bilin_new[0]):
                    if linearized_list['obj_func_u_bilin_new']['Name'][j] ==  linearized_list['streams_bilin_new']['Name'][i]:
                        check = 1
                        break 
            if dim_dual_v_c_util_bilin_new[0] > 0:
                for j in range (0, dim_dual_v_c_util_bilin_new[0]):
                    if linearized_list['dual_v_c_util_bilin_new']['Name'][j] ==  linearized_list['streams_bilin_new']['Name'][i]:
                        check = 1
                        break    
            if dim_obj_func_p_bilin_new[0] > 0:
                for j in range (0, dim_obj_func_p_bilin_new[0]):
                    if linearized_list['obj_func_p_bilin_new']['Name'][j] ==  linearized_list['streams_bilin_new']['Name'][i]:
                        check = 1
                        break        
            if dim_dual_v_c_proc_bilin_new[0] > 0:
                for j in range (0, dim_dual_v_c_proc_bilin_new[0]):
                    if linearized_list['dual_v_c_proc_bilin_new']['Name'][j] ==  linearized_list['streams_bilin_new']['Name'][i]:
                        check = 1
                        break
            if check == 0:
                temp_term = ''
                temp_term = temp_term + linearized_list['streams_bilin_new']['Name'][i] + '_y'               
                f_data_set.write(temp_term + '\n')   
        f_data_set.write('\n')     
        
    ##Writing bilinear binary variables for stream type: network parallel 
    f_data_set.write('\\\ Writing bilinear binary variables for stream type: network parallel  \n \n')    
    if dim_streams_bilin_contbin_new[0] > 0:
        for i in range (0, dim_streams_bilin_contbin_new[0]):
            if streams_bilin_contbin_new['InOut'][i] == 'out':
                temp_term = ''
                temp_term = temp_term + streams_bilin_contbin_new['Temp_name'][i] + '_y'
                f_data_set.write(temp_term + '\n')  
        f_data_set.write('\n')
        
###############################################################################################################################################################################################    
###############################################################################################################################################################################################
###############################################################################################################################################################################################
    ##Wrapping up 
    f_data_set.write('End \n')    
    f_data_set.close
    return 
    
    