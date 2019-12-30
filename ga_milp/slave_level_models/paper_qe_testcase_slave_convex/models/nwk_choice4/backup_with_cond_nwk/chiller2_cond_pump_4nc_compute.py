##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def chiller2_cond_pump_4nc_compute (ch2_cp_dc):
    
    import numpy as np 
    import pandas as pd
    
    ##list of input values 
    ##ch2_cp_dc = np.zeros((5,1))
    
    ##ch2_cp_dc[0,0] = ch2_cp_c0
    ##ch2_cp_dc[1,0] = ch2_cp_c1
    ##ch2_cp_dc[2,0] = ch2_cp_c2
    ##ch2_cp_dc[3,0] = ch2_cp_max_m
    ##ch2_cp_dc[4,0] = ch2_cp_steps

    ##Initializing an array to store the return values 
    ch2_cp_calc = pd.DataFrame(columns = ['grad', 'int' ,'lb' ,'ub'])
    
    ##Determining the step size 
    step_size = 1 / ch2_cp_dc[4,0]
    
    for i in range (0, int(ch2_cp_dc[4,0])):
        lb = i * step_size
        ub = (i + 1) * step_size 
        
        flow_lb = lb * ch2_cp_dc[3,0]
        flow_ub = ub * ch2_cp_dc[3,0]
        
        delp_lb = (ch2_cp_dc[0,0] * pow(flow_lb, 2)) + (ch2_cp_dc[1,0] * flow_lb) + (ch2_cp_dc[2,0])    ##This is a downward sloping graph
        delp_ub = (ch2_cp_dc[0,0] * pow(flow_ub, 2)) + (ch2_cp_dc[1,0] * flow_ub) + (ch2_cp_dc[2,0])        
        
        grad_temp = (delp_ub - delp_lb) / (flow_ub - flow_lb)
        int_temp = delp_ub - (grad_temp * flow_ub)
        
        temp_data = [grad_temp, int_temp, lb, ub]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['grad', 'int' ,'lb' ,'ub'])
        
        ch2_cp_calc = ch2_cp_calc.append(temp_df, ignore_index = True)

    return ch2_cp_calc