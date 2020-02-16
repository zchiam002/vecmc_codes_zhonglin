def ct_uem_original (twb, m_ct, m_air, t_in, delt_max):
    
    import pandas as pd     
    
    ##twb --- the wetbulb temperature 
    ##m_ct --- flowrate through the cooling tower
    ##m_air --- air-flow through the cooling tower 
    ##t_in --- temperature of fluid entering the cooling tower 
    
    ##Cooling tower regression derived coefficients 
    
    b0 = 0.14029549639345207	
    b1 = 0.600266127023157	
    b2 = -0.0211475692653011	
    b3 = 0.2792094538127389	
    b4 = 9.294683422723725*pow(10, -4)
    b5 = 0.16052557022400754
#    b0 = 0.23382397 	
#    b1 = -0.03876029 	
#    b2 = -0.03298896 	
#    b3 = 0.00113387	
#    b4 = -0.00416801
#    b5 = 0.42846231
    
    ##Calculating the delta-T of the cooling tower 
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from cooling_tower_models import delT_calc
    
    delT_ct = delT_calc ([b0, b1, b2, b3, b4, b5], m_air, t_in, [m_ct, twb])
    if delT_ct > delt_max :
        delT_ct = delt_max
    elif delT_ct < 0:
        delT_ct = 0
    
    return delT_ct

def cooling_tower_uem_reg_lprelax (m_air, m_ct, tw_in, twb, bilinear_pieces, del_t_coeff_temp, ma_table, twi_table):
    
    import pandas as pd 
        
    ##Searching the bilinear pieces 
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from cooling_tower_models import search_bilin_table_for_values
    bilin_est = search_bilin_table_for_values (ma_table, twi_table, m_air, tw_in)
    
    del_t_temp = (del_t_coeff_temp[0,0] * m_air) + (del_t_coeff_temp[1,0] * tw_in) + (del_t_coeff_temp[2,0] * bilin_est) + del_t_coeff_temp[3,0]

    return del_t_temp