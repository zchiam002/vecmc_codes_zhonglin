##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def dist_nwk_pump_compute (dist_np_dc, dist_np_table, dist_np_pres_table):
    
    import numpy as np 
    import pandas as pd
    
    ##list of input values 
    
    ##dist_np_dc = np.zeros((2,1))
    ##dist_np_dc[0,0] = dist_np_nwk_choice
    ##dist_np_dc[1,0] = dist_np_steps
    
    ##dist_np_table --- a dataframe containing all possible pump combinations for the distribution network
    ##dist_np_pres_table --- a dataframe containing all the corresponding pressure curves for the pump combinations 
    
    ##Forming the table of choices according to the associated distribution network choice 
    
    ##Intializing a table to holde the associated pump parameters and values 
    dist_np_possible_choices = pd.DataFrame(columns = ['p1_m_coeff', 'p1_p_coeff', 'p1_cst', 'p1_max_m', 'p1_max_p', 'p2_m_coeff', 'p2_p_coeff', 'p2_cst', 'p2_max_m', 
                                                       'p2_max_p', 'p3_m_coeff', 'p3_p_coeff', 'p3_cst', 'p3_max_m', 'p3_max_p', 'p1_c0', 'p1_c1', 'p1_c2'])
    
    ##The values to be copied according to the associated network choice
        ##The first value is the starting index, the second is the number of iterations, and the third represents the number of activated pumps at a given time
    starting_values_chosen = [34, 7, 1]
        
    start = int(starting_values_chosen[0])
    end = int(starting_values_chosen[0] + starting_values_chosen[1])
    
    for i in range (start, end):
        temp_data = [dist_np_table['p1_m_coeff'][i], dist_np_table['p1_p_coeff'][i], dist_np_table['p1_cst'][i], dist_np_table['p1_max_m'][i],
                     dist_np_table['p1_max_p'][i], dist_np_pres_table['p1_c0'][i], dist_np_pres_table['p1_c1'][i], dist_np_pres_table['p1_c2'][i]]
        
        temp_df = pd.DataFrame(data = [temp_data], columns = ['p1_m_coeff', 'p1_p_coeff', 'p1_cst', 'p1_max_m', 'p1_max_p', 'p1_c0', 'p1_c1', 'p1_c2'])
        dist_np_possible_choices = dist_np_possible_choices.append(temp_df, ignore_index = True)
    
    ##Asembling the dataframe of return values
    ret_values_pump = piecewise_dist_np_ret_values (dist_np_possible_choices, starting_values_chosen, dist_np_dc)

    return ret_values_pump

########################################################################################################################################################################
##Additional functions 

def piecewise_dist_np_ret_values (dist_np_possible_choices, starting_values_chosen, dist_np_dc):
    
    import pandas as pd 
    import numpy as np
    
    ##dist_np_possible_choices --- associated dataframe pump details 
    ##starting_values_chosen --- the associated values of the chosen network (starting index, number of combinations, number of activated pumps)
    ##dist_np_dc --- decision values from the main script 

    dim_dist_np_possible_choices = dist_np_possible_choices.shape   
    
    ret_values_pump = pd.DataFrame(columns = ['grad', 'int' ,'lb' ,'ub', 'combi', 'm_coeff', 'p_coeff', 'cst', 'max_m', 'max_p', 'step']) 
        
    for i in range (0, dim_dist_np_possible_choices[0]):
       
        curr_c0_p1 = dist_np_possible_choices['p1_c0'][i]
        curr_c1_p1 = dist_np_possible_choices['p1_c1'][i]
        curr_c2_p1 = dist_np_possible_choices['p1_c2'][i]
        curr_max_m_p1 = dist_np_possible_choices['p1_max_m'][i]
        
        curr_steps = dist_np_dc[1,0]              
        
        ##Determining the step size 
        step_size = 1 / curr_steps            
        
        for j in range (0, int(curr_steps)):
            
            lb = j * step_size
            ub = (j + 1) * step_size 
            
            flow_lb = lb * curr_max_m_p1
            flow_ub = ub * curr_max_m_p1
            
            delp_lb = (curr_c0_p1 * pow(flow_lb, 2)) + (curr_c1_p1 * flow_lb) + (curr_c2_p1)    ##This is a downward sloping graph
            delp_ub = (curr_c0_p1 * pow(flow_ub, 2)) + (curr_c1_p1 * flow_ub) + (curr_c2_p1)        
            
            grad_temp = (delp_ub - delp_lb) / (flow_ub - flow_lb)
            int_temp = delp_ub - (grad_temp * flow_ub)
            
            temp_data = [grad_temp, int_temp, lb, ub, i, dist_np_possible_choices['p1_m_coeff'][i], dist_np_possible_choices['p1_p_coeff'][i], 
                         dist_np_possible_choices['p1_cst'][i], dist_np_possible_choices['p1_max_m'][i], dist_np_possible_choices['p1_max_p'][i], j]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['grad', 'int' ,'lb' ,'ub', 'combi', 'm_coeff', 'p_coeff', 'cst', 'max_m', 'max_p', 'step']) 
            ret_values_pump = ret_values_pump.append(temp_df, ignore_index = True)
                
    return ret_values_pump
