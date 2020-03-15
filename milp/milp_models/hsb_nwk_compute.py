##This is the compute file 

##Note: Some of the implementations may be more accurate than others due to the dynamic step size 

def hsb_nwk_compute (hsb_nwk_dc):

    ##hsb_nwk_dc    --- list of input values 
    ##hsb_nwk_dc[0,0] = hsb_nwk_tf
    ##hsb_nwk_dc[1,0] = hsb_nwk_coeff
    ##hsb_nwk_dc[2,0] = hsb_nwk_max_flow
    ##hsb_nwk_dc[3,0] = hsb_nwk_steps
    
    import pandas as pd

    ##Initializing an array to store the return values 
    hsb_nwk_calc = pd.DataFrame(columns = ['grad', 'int' ,'lb' ,'ub'])
    
    ##Determining the step size 
    step_size = 1 / hsb_nwk_dc[3,0]
    
    for i in range (0, int(hsb_nwk_dc[3,0])):
        lb = i * step_size
        ub = (i + 1) * step_size 
        
        flow_lb = lb * hsb_nwk_dc[2,0]
        flow_ub = ub * hsb_nwk_dc[2,0]
        
        delp_lb = hsb_nwk_dc[1,0] * pow(flow_lb, 1.852)
        delp_ub = hsb_nwk_dc[1,0] * pow(flow_ub, 1.852)
        
        grad_temp = (delp_ub - delp_lb) / (flow_ub - flow_lb)
        int_temp = delp_ub - (grad_temp * flow_ub)
        
        temp_data = [grad_temp, int_temp, lb, ub]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['grad', 'int' ,'lb' ,'ub'])
        
        hsb_nwk_calc = hsb_nwk_calc.append(temp_df, ignore_index = True)

    return hsb_nwk_calc