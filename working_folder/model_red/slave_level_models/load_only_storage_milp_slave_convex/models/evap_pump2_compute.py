##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def evap_pump2_compute (ep2_dc):
    
    import numpy as np 
    import pandas as pd
    
    ##list of input values 
    ##ep2_dc = np.zeros((5,1))
    
    ##ep2_dc[0,0] = ep2_c0
    ##ep2_dc[1,0] = ep2_c1
    ##ep2_dc[2,0] = ep2_c2
    ##ep2_dc[3,0] = ep2_max_m
    ##ep2_dc[4,0] = ep2_steps

    ##Initializing an array to store the return values 
    ep2_calc = pd.DataFrame(columns = ['grad', 'int' ,'lb' ,'ub'])
    
    ##Determining the step size 
    step_size = 1 / ep2_dc[4,0]
    
    for i in range (0, int(ep2_dc[4,0])):
        lb = i * step_size
        ub = (i + 1) * step_size 
        
        flow_lb = lb * ep2_dc[3,0]
        flow_ub = ub * ep2_dc[3,0]
        
        delp_lb = (ep2_dc[0,0] * pow(flow_lb, 2)) + (ep2_dc[1,0] * flow_lb) + (ep2_dc[2,0])    ##This is a downward sloping graph
        delp_ub = (ep2_dc[0,0] * pow(flow_ub, 2)) + (ep2_dc[1,0] * flow_ub) + (ep2_dc[2,0])        
        
        grad_temp = (delp_ub - delp_lb) / (flow_ub - flow_lb)
        int_temp = delp_ub - (grad_temp * flow_ub)
        
        temp_data = [grad_temp, int_temp, lb, ub]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['grad', 'int' ,'lb' ,'ub'])
        
        ep2_calc = ep2_calc.append(temp_df, ignore_index = True)

    return ep2_calc