##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def evap_nwk_compute (enwk_dc):
    
    import numpy as np 
    import pandas as pd
    
    ##list of input values 
    ##enwk_dc = np.zeros((3,1))
    
    ##enwk_dc[0,0] = enwk_com_coeff
    ##enwk_dc[1,0] = enwk_max_flow
    ##enwk_dc[2,0] = enwk_steps


    ##Initializing an array to store the return values 
    enwk_calc = pd.DataFrame(columns = ['grad', 'int' ,'lb' ,'ub'])
    
    ##Determining the step size 
    step_size = 1 / enwk_dc[2,0]
    
    for i in range (0, int(enwk_dc[2,0])):
        lb = i * step_size
        ub = (i + 1) * step_size 
        
        flow_lb = lb * enwk_dc[1,0]
        flow_ub = ub * enwk_dc[1,0]
        
        delp_lb = enwk_dc[0,0] * pow(flow_lb, 1.852) 
        delp_ub = enwk_dc[0,0] * pow(flow_ub, 1.852)
        
        grad_temp = (delp_ub - delp_lb) / (flow_ub - flow_lb)
        int_temp = delp_ub - (grad_temp * flow_ub)
        
        temp_data = [grad_temp, int_temp, lb, ub]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['grad', 'int' ,'lb' ,'ub'])
        
        enwk_calc = enwk_calc.append(temp_df, ignore_index = True)

    return enwk_calc