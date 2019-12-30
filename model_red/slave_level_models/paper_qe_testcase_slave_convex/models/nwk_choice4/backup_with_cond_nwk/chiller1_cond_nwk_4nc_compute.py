##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def chiller1_cond_nwk_4nc_compute (ch1_cnwk_dc):
    
    import numpy as np 
    import pandas as pd
    
    ##list of input values 
    ##ch1_cnwk_dc = np.zeros((5,1))
    
    ##ch1_cnwk_dc[0,0] = ch1_cnwk_tf
    ##ch1_cnwk_dc[1,0] = ch1_cnwk_coeff
    ##ch1_cnwk_dc[2,0] = ch1_cnwk_com_coeff
    ##ch1_cnwk_dc[3,0] = ch1_cnwk_max_flow
    ##ch1_cnwk_dc[4,0] = ch1_cnwk_steps


    ##Initializing an array to store the return values 
    ch1_cnwk_calc = pd.DataFrame(columns = ['grad', 'int' ,'lb' ,'ub'])
    
    ##Determining the step size 
    step_size = 1 / ch1_cnwk_dc[4,0]
    
    for i in range (0, int(ch1_cnwk_dc[4,0])):
        lb = i * step_size
        ub = (i + 1) * step_size 
        
        flow_lb = lb * ch1_cnwk_dc[3,0]
        flow_ub = ub * ch1_cnwk_dc[3,0]
        
        delp_lb = (ch1_cnwk_dc[1,0] * pow(flow_lb, 1.852)) + (ch1_cnwk_dc[2,0] * pow(ch1_cnwk_dc[0,0], 1.852))
        delp_ub = (ch1_cnwk_dc[1,0] * pow(flow_ub, 1.852)) + (ch1_cnwk_dc[2,0] * pow(ch1_cnwk_dc[0,0], 1.852))
        
        grad_temp = (delp_ub - delp_lb) / (flow_ub - flow_lb)
        int_temp = delp_ub - (grad_temp * flow_ub)
        
        temp_data = [grad_temp, int_temp, lb, ub]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['grad', 'int' ,'lb' ,'ub'])
        
        ch1_cnwk_calc = ch1_cnwk_calc.append(temp_df, ignore_index = True)

    return ch1_cnwk_calc