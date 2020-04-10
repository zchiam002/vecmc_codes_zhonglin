##This is a sub-script of the chiller model 

def optimaluv_chiller_cond_gen_script_lpformat (Qc_real, bilin_pieces_list_cond, Tin_cond, mcond, mcond_t, org_var_bounds):
    import sys 
    sys.path.append('C:\\Optimization_zlc\\slave_convex_handlers\\auxillary\\')
    from single_sign_string import single_sign_string
    import pandas as pd
    
    ##Preparing the optimization script in LP format 
    file_save_directory = 'C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\sub_scripts\\result_holder\\chiller_cond_bilin.lp'
    
    f_data_set = open(file_save_directory, 'w')

######################################################################################################################################################
######################################################################################################################################################
    
    ##Writing the objective function 
    f_data_set.write('Minimize \n')
    f_data_set.write('\n') 
    f_data_set.write('obj: error \n \n')
    
######################################################################################################################################################
######################################################################################################################################################
    
    ##Writing the constraints 
    f_data_set.write('Subject To \n \n')
    current_index = 0

######################################################################################################################################################
    
    ##Writing the absolute error constraint 
    f_data_set.write('\\\Absolute error constraint \n \n')
    
    ##Converting all flow to kg/s 
    mcond = (mcond * 998.2) / 3600
    mcond_t = (mcond_t * 998.2) / 3600
    ##Converting all temperature into K
    Tin_cond = Tin_cond + 273.15
    
    a1 = mcond_t * 4.2                              ##Deals with the bilinear terms 
    a2 = mcond_t * 4.2 * Tin_cond                   ##Deals with the x term 
    a3 = Qc_real                                    ##Deals with the constant term 
    
    ##Fixing the value of the x term
    if mcond_t != 0:
        mcond_perc = mcond / mcond_t
    else:
        mcond_perc = 0

        
    ##Establishing the constant terms
    lhs_value = (mcond * 4.2 * Tin_cond) + Qc_real 
    bilin_coeff_external = mcond_t * 4.2
    
    ##Building tables of ui and vi separately 
    dim_bilin_pieces_list_cond = bilin_pieces_list_cond.shape 
    
    u_values = pd.DataFrame(columns = ['u_min', 'u_max', 'u_grad', 'u_int'])
    v_values = pd.DataFrame(columns = ['v_min', 'v_max', 'v_grad', 'v_int'])
    
    for i in range (0, dim_bilin_pieces_list_cond[0]):
        u_values_data = [bilin_pieces_list_cond['u_min'][i], bilin_pieces_list_cond['u_max'][i], bilin_pieces_list_cond['u_grad'][i], bilin_pieces_list_cond['u_int'][i]]
        u_values_temp = pd.DataFrame(data = [u_values_data], columns = ['u_min', 'u_max', 'u_grad', 'u_int'])
        u_values = u_values.append(u_values_temp, ignore_index = True)
        v_values_data = [bilin_pieces_list_cond['v_min'][i], bilin_pieces_list_cond['v_max'][i], bilin_pieces_list_cond['v_grad'][i], bilin_pieces_list_cond['v_int'][i]]
        v_values_temp = pd.DataFrame(data = [v_values_data], columns = ['v_min', 'v_max', 'v_grad', 'v_int'])
        v_values = v_values.append(v_values_temp, ignore_index = True)
        
    ##Writing the bilinear terms 
    dim_u_values = u_values.shape 
    dim_v_values = v_values.shape
    
    bilin_terms = ''
    for i in range (0, dim_u_values[0]):
        sub_script_u = 'u' + str(i)
        for j in range (0, dim_v_values[0]):
            sub_script = sub_script_u + 'v' + str(j)
            temp_grad = bilin_coeff_external * (u_values['u_grad'][i] + v_values['v_grad'][j])
            temp_int = bilin_coeff_external * ((u_values['u_grad'][i] * mcond_perc) + u_values['u_int'][i] - (v_values['v_grad'][j] * mcond_perc) - v_values['v_int'][j])
            var_temp = 'Tcond_out_' + sub_script
            if not bilin_terms:
                bilin_terms = bilin_terms + str(temp_grad) + ' ' + var_temp
                bilin_terms = bilin_terms + single_sign_string(temp_int, '+') + ' ' + var_temp + '_y'
            else:
                bilin_terms = bilin_terms + single_sign_string(temp_grad, '+') + ' ' + var_temp
                bilin_terms = bilin_terms + single_sign_string(temp_int, '+') + ' ' + var_temp + '_y'
    
    current_index = current_index + 1
    temp_term = ''
    temp_term = temp_term + 'c' + str(current_index) + ': '
    temp_term = temp_term + bilin_terms + ' - error <= ' + str(lhs_value)
    f_data_set.write(temp_term + ' \n')
    
    current_index = current_index + 1
    temp_term = ''
    temp_term = temp_term + 'c' + str(current_index) + ': '
    temp_term = temp_term + bilin_terms + ' + error >= ' + str(lhs_value)
    f_data_set.write(temp_term + ' \n')  
    
    f_data_set.write('\n') 
    
######################################################################################################################################################

    ##Writing the constraint which makes sure that the selected variable falls within the bounds and that if binary is off, the continuous is also off
    f_data_set.write('\\\Fmin, Fmax and binary constraints \n \n')

    for i in range (0, dim_u_values[0]):    
        sub_script_u = 'u' + str(i)
        fmin_u = u_values['u_min'][i] - mcond_perc
        fmax_u = u_values['u_max'][i] - mcond_perc
        for j in range (0, dim_v_values[0]):
            sub_script = sub_script_u + 'v' + str(j)            
            var_temp = 'Tcond_out_' + sub_script
            fmin_v = -1 * (v_values['v_max'][j] - mcond_perc)
            fmax_v = -1 * (v_values['v_min'][j] - mcond_perc)
            
            fmin_term = max(fmin_u, fmin_v)
            fmax_term = min(fmax_u, fmax_v)
            
            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': '  
            temp_term = temp_term + str(fmin_term) + ' ' + var_temp + '_y'
            temp_term = temp_term + ' - ' + var_temp + ' <= 0'
            f_data_set.write(temp_term + ' \n') 

            current_index = current_index + 1
            temp_term = ''
            temp_term = temp_term + 'c' + str(current_index) + ': ' 
            temp_term = temp_term + var_temp 
            temp_term = temp_term + single_sign_string(fmax_term, '-') + ' ' + var_temp + '_y'
            temp_term = temp_term + ' <= 0'
            f_data_set.write(temp_term + ' \n')                         
    
    f_data_set.write('\n')     

######################################################################################################################################################

    ##Making sure that only 1 of the Tcond_out terms are picked at all times 
    f_data_set.write('\\\Making sure that only 1 Tcond_out_uivi is picked at all times \n \n')
    
    ##Assembling all the binary terms 
    binary_terms = ''
    
    for i in range (0, dim_u_values[0]):
        sub_script_u = 'u' + str(i)
        for j in range (0, dim_v_values[0]):
            sub_script = sub_script_u + 'v' + str(j)            
            var_temp = 'Tcond_out_' + sub_script + '_y'
            
            if not binary_terms:
                binary_terms = binary_terms + var_temp 
            else:
                binary_terms = binary_terms + ' + ' + var_temp 
                
    ##Writing the constraint 
    current_index = current_index + 1
    temp_term = ''
    temp_term = temp_term + 'c' + str(current_index) + ': ' 
    temp_term = temp_term + binary_terms + ' = 1'
    f_data_set.write(temp_term + ' \n')

    f_data_set.write('\n')

###################################################################################################################################################### 
######################################################################################################################################################

    ##Writing the bounds 
    f_data_set.write('Bounds \n \n')
    
######################################################################################################################################################
######################################################################################################################################################
    
    ##Writing the binary variables 
    f_data_set.write('Binary \n \n')
    
    for i in range (0, dim_u_values[0]):
        sub_script_u = 'u' + str(i)
        for j in range (0, dim_v_values[0]):
            sub_script = sub_script_u + 'v' + str(j)            
            var_temp = 'Tcond_out_' + sub_script + '_y'
            
            f_data_set.write(var_temp + ' \n')            
                
    f_data_set.write('\n') 
###################################################################################################################################################### 
######################################################################################################################################################    

    ##Wrapping up 
    f_data_set.write('End \n')    
    f_data_set.close
    
######################################################################################################################################################
######################################################################################################################################################

    ##Assembling the generated variable list 

    var_list = pd.DataFrame(columns = ['var_name'])
    
    for i in range (0, dim_u_values[0]):
        sub_script_u = 'u' + str(i)
        for j in range (0, dim_v_values[0]):
            sub_script = sub_script_u + 'v' + str(j)
            var_temp = 'Tcond_out_' + sub_script
            var_list_temp = pd.DataFrame(data = [var_temp], columns = ['var_name'])
            var_list = var_list.append(var_list_temp, ignore_index = True)
            
            var_temp_y = 'Tcond_out_' + sub_script + '_y'    
            var_list_temp = pd.DataFrame(data = [var_temp_y], columns = ['var_name'])
            var_list = var_list.append(var_list_temp, ignore_index = True) 
            
    var_list_temp = pd.DataFrame(data = ['error'], columns = ['var_name'])
    var_list = var_list.append(var_list_temp, ignore_index = True)    
         
    return var_list