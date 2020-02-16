##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def cond_pump1_compute (cp1_dc):
    
    import numpy as np 
    import pandas as pd
    
    ##list of input values 
    ##cp1_dc = np.zeros((5,1))
    
    ##cp1_dc[0,0] = cp1_c0
    ##cp1_dc[1,0] = cp1_c1
    ##cp1_dc[2,0] = cp1_c2
    ##cp1_dc[3,0] = cp1_max_m
    ##cp1_dc[4,0] = cp1_steps

    ##Initializing an array to store the return values 
    cp1_calc = pd.DataFrame(columns = ['grad', 'int' ,'lb' ,'ub'])
    
    ##Determining the step size 
    step_size = 1 / cp1_dc[4,0]
    
    for i in range (0, int(cp1_dc[4,0])):
        lb = i * step_size
        ub = (i + 1) * step_size 
        
        flow_lb = lb * cp1_dc[3,0]
        flow_ub = ub * cp1_dc[3,0]
        
        delp_lb = (cp1_dc[0,0] * pow(flow_lb, 2)) + (cp1_dc[1,0] * flow_lb) + (cp1_dc[2,0])    ##This is a downward sloping graph
        delp_ub = (cp1_dc[0,0] * pow(flow_ub, 2)) + (cp1_dc[1,0] * flow_ub) + (cp1_dc[2,0])        
        
        grad_temp = (delp_ub - delp_lb) / (flow_ub - flow_lb)
        int_temp = delp_ub - (grad_temp * flow_ub)
        
        temp_data = [grad_temp, int_temp, lb, ub]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['grad', 'int' ,'lb' ,'ub'])
        
        cp1_calc = cp1_calc.append(temp_df, ignore_index = True)

    return cp1_calc