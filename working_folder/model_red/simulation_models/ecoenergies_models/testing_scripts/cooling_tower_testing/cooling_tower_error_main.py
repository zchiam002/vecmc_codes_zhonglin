##This function test for the abstracted error pertaining to the cooling tower model 

def cooling_tower_error_main ():
    
    import pandas as pd 
    from cooling_tower_main_models import ct_uem_original
    from cooling_tower_main_models import cooling_tower_uem_reg_lprelax    
    from cooling_tower_main_models import cooling_tower_uem_reg_lprelax_pwl_twi
    from cooling_tower_main_models import ct_reg_coeff_calc_new_pwl   
    ##Determining the parameters 
    twb = 30 + 273.15
    m_w = 407
    
    bilinear_pieces = 20
    pwl = 10
    
    delt_max = 7000
    
    ##Cooling tower coefficients 
    b0 = 0.14029549639345207	
    b1 = 0.600266127023157	
    b2 = -0.0211475692653011	
    b3 = 0.2792094538127389	
    b4 = 9.294683422723725*pow(10, -4)
    b5 = 0.16052557022400754
    ct_reg_coeff = [b0, b1, b2, b3, b4, b5]
    
    ##Determining the range of variables 
    tin_ct_min = twb + 3
    tin_ct_max = tin_ct_min + 10
    step_tin = 20
    interval_tin = (tin_ct_max - tin_ct_min) / step_tin
    
    
    ##Initializing a dataframe to store the return values
    delT_values = pd.DataFrame(columns = ['twb', 'flow','air', 'tin', 'delt_org', 'delt_reg_bilin', 'delt_reg_bilin_pwl', 'error_reg_bilin', 'error_reg_bilin_pwl', 'mae'])
    
    ##Deriving the flowrate of air
    min_air_flow = 0            ##kg/h
    max_air_flow = 369117       ##kg/h
    step_air = 20
    interval_air = (max_air_flow - min_air_flow) / step_air
    
    ##Finding the regression based coefficients
    from cooling_tower_main_models import ct_reg_coeff_calc_new
    #ct_calc = ct_reg_coeff_calc_new (ct_reg_coeff, twb, tin_ct_min, tin_ct_max, min_air_flow, max_air_flow, m_w)
    
    ##Creating the look up tables for the bilinear portion
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from cooling_tower_models import gen_bilinear_pieces
    #ma_table, twi_table = gen_bilinear_pieces (min_air_flow, max_air_flow, tin_ct_min, tin_ct_max, bilinear_pieces)
    
    ##Determine max and min twb
    min_twb = 20 + 273.15
    max_twb = 30 + 273.15
    step_twb = 10
    interval_twb = (max_twb - min_twb) / step_twb
    
    ##Determine the parameters for flow variation 
    flow = [407, 1476, 407+1476, 1476+1476, 407+1476+1476]
    step_flow = len(flow)
    
    counter = 0
    for ii in range (0, step_flow):
        curr_m_w = flow[ii]
        for iii in range (0, step_twb):
            curr_twb = (iii * interval_twb) + min_twb
            ct_calc = ct_reg_coeff_calc_new (ct_reg_coeff, curr_twb, tin_ct_min, tin_ct_max, min_air_flow, max_air_flow, curr_m_w)
            del_t_coeff_temp_dict = ct_reg_coeff_calc_new_pwl (ct_reg_coeff, curr_twb, tin_ct_min, tin_ct_max, min_air_flow, max_air_flow, curr_m_w, pwl)
            ma_table, twi_table = gen_bilinear_pieces (min_air_flow, max_air_flow, tin_ct_min, tin_ct_max, bilinear_pieces)   
    
            for i in range (0, step_tin+1):
                curr_tin = (i * interval_tin) + tin_ct_min
                for j in range (0, step_air+1):
                    curr_air = (j * interval_air)
                    delt_org = ct_uem_original(curr_twb, curr_m_w, curr_air, curr_tin, delt_max)
                    delt_reg_bilin = cooling_tower_uem_reg_lprelax (curr_air, curr_m_w, curr_tin, curr_twb, bilinear_pieces, ct_calc, ma_table, twi_table)
                    delt_reg_bilin_pwl = cooling_tower_uem_reg_lprelax_pwl_twi (curr_air, curr_m_w, curr_tin, curr_twb, bilinear_pieces, del_t_coeff_temp_dict, ma_table, twi_table, pwl, tin_ct_min, tin_ct_max)
                    
                    
                    error_reg_bilin = pow(100*((delt_org - delt_reg_bilin)/delt_org), 2)
                    error_reg_bilin_pwl = pow(100*((delt_org - delt_reg_bilin_pwl)/delt_org), 2)
                    mae = 100*((delt_org - delt_reg_bilin)/delt_org)
                    
                    temp_df = pd.DataFrame(data = [[curr_twb, curr_m_w, curr_air, curr_tin, delt_org, delt_reg_bilin, delt_reg_bilin_pwl, error_reg_bilin, error_reg_bilin_pwl, mae]], 
                                           columns = ['twb', 'flow', 'air', 'tin', 'delt_org', 'delt_reg_bilin', 'delt_reg_bilin_pwl', 'error_reg_bilin', 'error_reg_bilin_pwl', 'mae'])
                    delT_values = delT_values.append(temp_df, ignore_index = True)
                    counter = counter + 1
                    print('Iteration: ' + str(counter) + ' of ' + str((step_tin+1) * step_twb * step_flow * (step_tin+1)))
                    print(delt_org, delt_reg_bilin_pwl[0], error_reg_bilin_pwl[0])
    
    
    
    
    import matplotlib.pyplot as plt
    plt.plot(delT_values['delt_org'][:], delT_values['delt_reg_bilin'][:], '.')
    
    import numpy as np
    lims = [
    np.min([plt.axes().get_xlim(), plt.axes().get_ylim()]),  # min of both axes
    np.max([plt.axes().get_xlim(), plt.axes().get_ylim()]),  # max of both axes
    ]
    # now plot both limits against eachother
    plt.axes().plot(lims, lims, 'k-', alpha=0.75, zorder=0, label = 'y = x')
    plt.axes().set_xlim(lims)
    plt.axes().set_ylim(lims)
    plt.show()
    
    ##Calculating the error 
    total_error = sum(delT_values['error_reg_bilin'][:])
    total_error = total_error / counter 
    final_error = pow(total_error, 0.5)
    
    total_error_pwl = sum(delT_values['error_reg_bilin_pwl'][:])
    total_error_pwl = total_error_pwl / counter 
    final_error_pwl = pow(total_error_pwl, 0.5) 
    
    total_mae = sum(delT_values['mae'][:])
    mae = total_mae / counter
    
    print(final_error)
    print(final_error_pwl)
    print(mae)

    
    return 

####################################################################################################################################################################################
##Additional functions 

##this function performs piecewise linearization by delt
def pwl_by_tin_ct_model (pwl, m_air, m_ct, tw_in, twb, twi_min, twi_max, bilinear_pieces):
    
    
    return delt
    
###################################################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    cooling_tower_error_main ()