#This is the compute file 

def cooling_tower5_4nc_compute (ct5_4nc_dc):
     
    import pandas as pd
    import numpy as np
    
    ##List of input values
    ##ct5_4nc_dc = np.zeros((11, 1))   
    
    ##ct5_4nc_dc[0,0] = ct5_4nc_twb
    ##ct5_4nc_dc[1,0] = ct5_4nc_twi_range
    ##ct5_4nc_dc[2,0] = ct5_4nc_min_approach
    ##ct5_4nc_dc[3,0] = ct5_4nc_make_up_water_correct_coeff     
    ##ct5_4nc_dc[4,0] = ct5_4nc_tcnwkflow   
    ##ct5_4nc_dc[5,0] = ct5_4nc_num_towers_config  
    ##ct5_4nc_dc[6,0] = ct5_4nc_max_ma_flow 
    ##ct5_4nc_dc[7,0] = ct5_4nc_c0 
    ##ct5_4nc_dc[8,0] = ct5_4nc_c1 
    ##ct5_4nc_dc[9,0] = ct5_4nc_c2 
    ##ct5_4nc_dc[10,0] = ct5_4nc_c3 

    ##Determining the min and max of twi                    
    twi_min = ct5_4nc_dc[0,0] + ct5_4nc_dc[2,0]         ##The units are in K
    twi_max = twi_min + ct5_4nc_dc[1,0]
    
    ##Determining the delta t coefficients in terms of %ma and %twi
    ma_perc_coeff = (ct5_4nc_dc[7,0] * ct5_4nc_dc[6,0]) + (ct5_4nc_dc[9,0] * ct5_4nc_dc[6,0] * twi_min)
    twi_perc_coeff = ct5_4nc_dc[8,0] * (twi_max - twi_min) 
    ma_twi_perc_coeff = ct5_4nc_dc[9,0] * ct5_4nc_dc[6,0] * (twi_max - twi_min)
    cst_term = ct5_4nc_dc[10,0] + (ct5_4nc_dc[8,0] * twi_min)
    
    ##Determining the minimum outlet temperature with respect to the flowratio
    tout_min_frac = twi_min / ct5_4nc_dc[5,0]
    
    ##Determining the make up water coefficients 
    flow_to_tower = ct5_4nc_dc[4,0] / ct5_4nc_dc[5,0]
    
    water_coeff1 = 0.0027 * flow_to_tower * ct5_4nc_dc[3,0]
    water_coeff2 = (0.01 / 5.6) * flow_to_tower * ct5_4nc_dc[3,0]
    
    ma_perc_coeff_water = water_coeff2 * ma_perc_coeff
    twi_perc_coeff_water = water_coeff2 * twi_perc_coeff
    ma_twi_perc_coeff_water = water_coeff2 * ma_twi_perc_coeff
    cst_term_water = water_coeff1 * (water_coeff2 * cst_term)
    
    ##Assembling a numpy array to hold the return values 
    
    ret_vals = np.zeros((11,1))
    
    ret_vals[0,0] = twi_min
    ret_vals[1,0] = twi_max    
    ret_vals[2,0] = ma_perc_coeff
    ret_vals[3,0] = twi_perc_coeff
    ret_vals[4,0] = ma_twi_perc_coeff
    ret_vals[5,0] = cst_term
    ret_vals[6,0] = tout_min_frac
    ret_vals[7,0] = ma_perc_coeff_water
    ret_vals[8,0] = twi_perc_coeff_water
    ret_vals[9,0] = ma_twi_perc_coeff_water
    ret_vals[10,0] = cst_term_water
 
    return ret_vals  