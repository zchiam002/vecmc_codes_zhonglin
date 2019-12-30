##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def cond_pump2_compute (cp2_dc):
    
    import numpy as np 
    import pandas as pd
    
    ##list of input values 
    ##cp2_dc = np.zeros((5,1))
    
    ##cp2_dc[0,0] = cp2_c0
    ##cp2_dc[1,0] = cp2_c1
    ##cp2_dc[2,0] = cp2_c2
    ##cp2_dc[3,0] = cp2_max_m
    ##cp2_dc[4,0] = cp2_steps

    ##Initializing an array to store the return values 
    cp2_calc = pd.DataFrame(columns = ['grad', 'int' ,'lb' ,'ub'])
    
    ##Determining the step size 
    step_size = 1 / cp2_dc[4,0]
    
    for i in range (0, int(cp2_dc[4,0])):
        lb = i * step_size
        ub = (i + 1) * step_size 
        
        flow_lb = lb * cp2_dc[3,0]
        flow_ub = ub * cp2_dc[3,0]
        
        delp_lb = (cp2_dc[0,0] * pow(flow_lb, 2)) + (cp2_dc[1,0] * flow_lb) + (cp2_dc[2,0])    ##This is a downward sloping graph
        delp_ub = (cp2_dc[0,0] * pow(flow_ub, 2)) + (cp2_dc[1,0] * flow_ub) + (cp2_dc[2,0])        
        
        grad_temp = (delp_ub - delp_lb) / (flow_ub - flow_lb)
        int_temp = delp_ub - (grad_temp * flow_ub)
        
        temp_data = [grad_temp, int_temp, lb, ub]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['grad', 'int' ,'lb' ,'ub'])
        
        cp2_calc = cp2_calc.append(temp_df, ignore_index = True)

    return cp2_calc