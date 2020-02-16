##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def cond_nwk_compute (cnwk_dc):
    
    import numpy as np 
    import pandas as pd
    
    ##list of input values 
    ##cnwk_dc = np.zeros((3,1))
    
    ##cnwk_dc[0,0] = cnwk_com_coeff
    ##cnwk_dc[1,0] = cnwk_max_flow
    ##cnwk_dc[2,0] = cnwk_steps


    ##Initializing an array to store the return values 
    cnwk_calc = pd.DataFrame(columns = ['grad', 'int' ,'lb' ,'ub'])
    
    ##Determining the step size 
    step_size = 1 / cnwk_dc[2,0]
    
    for i in range (0, int(cnwk_dc[2,0])):
        lb = i * step_size
        ub = (i + 1) * step_size 
        
        flow_lb = lb * cnwk_dc[1,0]
        flow_ub = ub * cnwk_dc[1,0]
        
        delp_lb = cnwk_dc[0,0] * pow(flow_lb, 1.852) 
        delp_ub = cnwk_dc[0,0] * pow(flow_ub, 1.852)
        
        grad_temp = (delp_ub - delp_lb) / (flow_ub - flow_lb)
        int_temp = delp_ub - (grad_temp * flow_ub)
        
        temp_data = [grad_temp, int_temp, lb, ub]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['grad', 'int' ,'lb' ,'ub'])
        
        cnwk_calc = cnwk_calc.append(temp_df, ignore_index = True)

    return cnwk_calc