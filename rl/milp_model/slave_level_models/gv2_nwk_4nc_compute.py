##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def gv2_nwk_4nc_compute (gv2_nwk_dc):
    
    import numpy as np 
    import pandas as pd
    
    ##list of input values 
    ##gv2_nwk_dc = np.zeros((4,1))
    
    ##gv2_nwk_dc[0,0] = gv2_nwk_tf
    ##gv2_nwk_dc[1,0] = gv2_nwk_coeff
    ##gv2_nwk_dc[2,0] = gv2_nwk_max_flow
    ##gv2_nwk_dc[3,0] = gv2_nwk_steps


    ##Initializing an array to store the return values 
    gv2_nwk_calc = pd.DataFrame(columns = ['grad', 'int' ,'lb' ,'ub'])
    
    ##Determining the step size 
    step_size = 1 / gv2_nwk_dc[3,0]
    
    for i in range (0, int(gv2_nwk_dc[3,0])):
        lb = i * step_size
        ub = (i + 1) * step_size 
        
        flow_lb = lb * gv2_nwk_dc[2,0]
        flow_ub = ub * gv2_nwk_dc[2,0]
        
        delp_lb = gv2_nwk_dc[1,0] * pow(flow_lb, 1.852)
        delp_ub = gv2_nwk_dc[1,0] * pow(flow_ub, 1.852)
        
        grad_temp = (delp_ub - delp_lb) / (flow_ub - flow_lb)
        int_temp = delp_ub - (grad_temp * flow_ub)
        
        temp_data = [grad_temp, int_temp, lb, ub]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['grad', 'int' ,'lb' ,'ub'])
        
        gv2_nwk_calc = gv2_nwk_calc.append(temp_df, ignore_index = True)

    return gv2_nwk_calc