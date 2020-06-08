##This function enumerates every possible pump and network combination and records the flowrate, pressure, constant term and maximum
##flowrate for each combination 

def prepare_dist_nwk_lin_coeff ():
    import os
    current_directory = os.path.dirname(__file__)[:-73] + '//'     
    import sys 
    sys.path.append(current_directory + 'master_level_models\\chiller_optimization_dist_nwk_pg_master_level_models\\add_ons\\')
    from convert_to_quadratic import convert_to_quadratic 
    from solve_quad_simul_eqns import solve_quad_simul_eqns
    from sklearn import linear_model 
    import pandas as pd
    import numpy as np
    from convert_dist_nwk_pump_choice import convert_dist_nwk_pump_choice
    from dist_nwk_lower_limits_model import dist_nwk_lower_limits_model
    
    
    ##Enumerating all possible pump and network combination for the distribution network 
    all_pump_nwk_combi = convert_dist_nwk_pump_choice()
    dim_all_pump_nwk_combi = all_pump_nwk_combi.shape
    
    ##Enumerating the lowest pressure drop limit for each distribution network combinations 
    all_lower_limit_dist_nwk = dist_nwk_lower_limits_model()
    dim_all_lower_limit_dist_nwk = all_lower_limit_dist_nwk.shape
    
    ##Pump parameters for pressure drop and electricity 
    ##The pressure drop curves will be in the quadratic form while the electricity curve will be in the cubic form 
    ##The coefficients are arranged in the form of x3, x2, x and the constant 
    ice_1 = [-0.0001037875, 0.0324647918, 46.1796318122]
    ice_2 = [-0.0000242521, 0.0132106447, 50.3198893609]
    tro_1 = [-0.0000151451, 0.0119236210, 58.2250275059]
    tro_2 = [-0.0000036319, 0.0002190621, 73.1928514998]
    fir_1 = [-0.0001095722, 0.0228923489, 35.2618445622]
    fir_2 = [-0.0000220090, 0.0091939614, 34.0585340963]
    fir_3 = [-0.0000220090, 0.0091939614, 34.0585340963]
    
    ice_1_p_max = 50
    ice_2_p_max = 55
    tro_1_p_max = 65
    tro_2_p_max = 75
    fir_1_p_max = 40
    fir_2_p_max = 40
    fir_3_p_max = 40
    
    ice_1_e = [0, -0.0000456328, 0.1072050404, 22.7694786782]
    ice_2_e = [0, 0.0000095593, 0.0548196056, 53.1923042054]
    tro_1_e = [0, -0.0000055276, 0.0771653808, 106.7867892025]
    tro_2_e = [0, -0.0000123489, 0.0845123896, 240.8517560062]
    fir_1_e = [0, -0.0000372609, 0.0745145187, 13.8059958033]
    fir_2_e =[0, -0.0000077383, 0.0506120010, 37.8841630174]
    fir_3_e =[0, -0.0000077383, 0.0506120010, 37.8841630174]
    
    ##Running through every possible combination and 
    ##Initiate a Dataframe to hold the results 
    all_combi_dist_pump_lin_coeff = pd.DataFrame(columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3', 'p1_m_coeff',
                                                            'p1_p_coeff', 'p1_cst', 'p1_max_m', 'p1_max_p', 'p2_m_coeff', 'p2_p_coeff', 'p2_cst', 'p2_max_m', 
                                                            'p2_max_p', 'p3_m_coeff', 'p3_p_coeff', 'p3_cst', 'p3_max_m', 'p3_max_p'])
    all_combi_dist_pump_press_coeff = pd.DataFrame(columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3', 'p1_c0', 'p1_c1', 'p1_c2',
                                                              'p2_c0', 'p2_c1', 'p2_c2', 'p3_c0', 'p3_c1', 'p3_c2'])
    
    limit = int(dim_all_pump_nwk_combi[0])
    for i in range (0, limit):
        ##There are 4 network choices, dist pump ordering will always be assigned in the order of ice, tro and fir 
    
    #############################################################################################################################################################################
    #############################################################################################################################################################################
    #############################################################################################################################################################################
        
        if all_pump_nwk_combi['nwk_choice'][i] == 0:
            ##Extracting the relevant network coefficients 
            ice_lower_limit_0 = [all_lower_limit_dist_nwk['x2_coeff'][0], all_lower_limit_dist_nwk['x_coeff'][0], 0]
            tro_lower_limit_0 = [all_lower_limit_dist_nwk['x2_coeff'][1], all_lower_limit_dist_nwk['x_coeff'][1], 0]
            fir_lower_limit_0 = [all_lower_limit_dist_nwk['x2_coeff'][2], all_lower_limit_dist_nwk['x_coeff'][2], 0]
            ##For each of the selected pumps, we would like to find the associated regression based values
            ##The procedure will be as follows:
                ##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case 
                ##Evaluating the maximum electricity consumption at the intersection point 
                ##Assume that the variable speed correlates linearly with the electrical consumption 
                ##We aim to express E = A1m + A2p + cst, hence regression analysis is needed
                ##To do that, we take 20 points for each of the flowrate interval for different pressure drops and electricity consumptions 
                
            if all_pump_nwk_combi['ice_1'][i] == 1:
                ice_1_flow_max = solve_quad_simul_eqns(ice_1, ice_lower_limit_0)
                ice_1_e_max = ice_1_e[0]*pow(ice_1_flow_max[0], 3) + ice_1_e[1]*pow(ice_1_flow_max[0], 2) + ice_1_e[2]*ice_1_flow_max[0] + ice_1_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = ice_1_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                ice_1_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                ice_1_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_lower_limit_0[0]*pow(c_fr, 2) + ice_lower_limit_0[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = ice_1[0]*pow(c_fr, 2) + ice_1[1]*c_fr + ice_1[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (ice_1_e_max / ice_1_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = ice_1_e[0]*pow(c_fr, 3) + ice_1_e[1]*pow(c_fr, 2) + ice_1_e[2]*c_fr + ice_1_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        ice_1_table_X[j*delp_interval+k, 0] = c_fr
                        ice_1_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        ice_1_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(ice_1_table_X, ice_1_table_Y)
                result = clf.score(ice_1_table_X, ice_1_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = ice_1_flow_max[0]
                p1_max_p = ice_1_p_max
                
                p1_c0 = ice_1[0]
                p1_c1 = ice_1[1]
                p1_c2 = ice_1[2]
                
            if all_pump_nwk_combi['ice_2'][i] == 1:
                ice_2_flow_max = solve_quad_simul_eqns(ice_2, ice_lower_limit_0)
                ice_2_e_max = ice_2_e[0]*pow(ice_2_flow_max[0], 3) + ice_2_e[1]*pow(ice_2_flow_max[0], 2) + ice_2_e[2]*ice_2_flow_max[0] + ice_2_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = ice_2_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                ice_2_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                ice_2_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_lower_limit_0[0]*pow(c_fr, 2) + ice_lower_limit_0[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = ice_2[0]*pow(c_fr, 2) + ice_2[1]*c_fr + ice_2[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (ice_2_e_max / ice_2_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = ice_2_e[0]*pow(c_fr, 3) + ice_2_e[1]*pow(c_fr, 2) + ice_2_e[2]*c_fr + ice_2_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        ice_2_table_X[j*delp_interval+k, 0] = c_fr
                        ice_2_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        ice_2_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(ice_2_table_X, ice_2_table_Y)
                result = clf.score(ice_2_table_X, ice_2_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = ice_2_flow_max[0]            
                p1_max_p = ice_2_p_max
                
                p1_c0 = ice_2[0]
                p1_c1 = ice_2[1]
                p1_c2 = ice_2[2]
                 
            if all_pump_nwk_combi['tro_1'][i] == 1:
                tro_1_flow_max = solve_quad_simul_eqns(tro_1, tro_lower_limit_0)
                tro_1_e_max = tro_1_e[0]*pow(tro_1_flow_max[0], 3) + tro_1_e[1]*pow(tro_1_flow_max[0], 2) + tro_1_e[2]*tro_1_flow_max[0] + tro_1_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = tro_1_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                tro_1_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                tro_1_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = tro_lower_limit_0[0]*pow(c_fr, 2) + tro_lower_limit_0[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = tro_1[0]*pow(c_fr, 2) + tro_1[1]*c_fr + tro_1[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (tro_1_e_max / tro_1_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = tro_1_e[0]*pow(c_fr, 3) + tro_1_e[1]*pow(c_fr, 2) + tro_1_e[2]*c_fr + tro_1_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        tro_1_table_X[j*delp_interval+k, 0] = c_fr
                        tro_1_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        tro_1_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(tro_1_table_X, tro_1_table_Y)
                result = clf.score(tro_1_table_X, tro_1_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p2_m_coef = lin_coeff[0,0]
                p2_p_coeff = lin_coeff[0,1]
                p2_cst = int_lin[0]
                p2_max_m = tro_1_flow_max[0]  
                p2_max_p = tro_1_p_max

                p2_c0 = tro_1[0]
                p2_c1 = tro_1[1]
                p2_c2 = tro_1[2]
    
            if all_pump_nwk_combi['tro_2'][i] == 1:
                tro_2_flow_max = solve_quad_simul_eqns(tro_2, tro_lower_limit_0)
                tro_2_e_max = tro_2_e[0]*pow(tro_2_flow_max[0], 3) + tro_2_e[1]*pow(tro_2_flow_max[0], 2) + tro_2_e[2]*tro_2_flow_max[0] + tro_2_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = tro_2_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                tro_2_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                tro_2_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = tro_lower_limit_0[0]*pow(c_fr, 2) + tro_lower_limit_0[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = tro_2[0]*pow(c_fr, 2) + tro_2[1]*c_fr + tro_2[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (tro_2_e_max / tro_2_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = tro_2_e[0]*pow(c_fr, 3) + tro_2_e[1]*pow(c_fr, 2) + tro_2_e[2]*c_fr + tro_2_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        tro_2_table_X[j*delp_interval+k, 0] = c_fr
                        tro_2_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        tro_2_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(tro_2_table_X, tro_2_table_Y)
                result = clf.score(tro_2_table_X, tro_2_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p2_m_coef = lin_coeff[0,0]
                p2_p_coeff = lin_coeff[0,1]
                p2_cst = int_lin[0]
                p2_max_m = tro_2_flow_max[0] 
                p2_max_p = tro_2_p_max
                
                p2_c0 = tro_2[0]
                p2_c1 = tro_2[1]
                p2_c2 = tro_2[2]
    
            if all_pump_nwk_combi['fir_1'][i] == 1:
                fir_1_flow_max = solve_quad_simul_eqns(fir_1, fir_lower_limit_0)
                fir_1_e_max = fir_1_e[0]*pow(fir_1_flow_max[0], 3) + fir_1_e[1]*pow(fir_1_flow_max[0], 2) + fir_1_e[2]*fir_1_flow_max[0] + fir_1_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = fir_1_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                fir_1_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                fir_1_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = fir_lower_limit_0[0]*pow(c_fr, 2) + fir_lower_limit_0[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = fir_1[0]*pow(c_fr, 2) + fir_1[1]*c_fr + fir_1[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (fir_1_e_max / fir_1_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = fir_1_e[0]*pow(c_fr, 3) + fir_1_e[1]*pow(c_fr, 2) + fir_1_e[2]*c_fr + fir_1_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        fir_1_table_X[j*delp_interval+k, 0] = c_fr
                        fir_1_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        fir_1_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(fir_1_table_X, fir_1_table_Y)
                result = clf.score(fir_1_table_X, fir_1_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p3_m_coef = lin_coeff[0,0]
                p3_p_coeff = lin_coeff[0,1]
                p3_cst = int_lin[0]
                p3_max_m = fir_1_flow_max[0]
                p3_max_p = fir_1_p_max
                
                p3_c0 = fir_1[0]
                p3_c1 = fir_1[1]
                p3_c2 = fir_1[2]
    
            if all_pump_nwk_combi['fir_2'][i] == 1:
                fir_2_flow_max = solve_quad_simul_eqns(fir_2, fir_lower_limit_0)
                fir_2_e_max = fir_2_e[0]*pow(fir_2_flow_max[0], 3) + fir_2_e[1]*pow(fir_2_flow_max[0], 2) + fir_2_e[2]*fir_2_flow_max[0] + fir_2_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = fir_2_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                fir_2_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                fir_2_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = fir_lower_limit_0[0]*pow(c_fr, 2) + fir_lower_limit_0[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = fir_2[0]*pow(c_fr, 2) + fir_2[1]*c_fr + fir_2[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (fir_2_e_max / fir_2_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = fir_2_e[0]*pow(c_fr, 3) + fir_2_e[1]*pow(c_fr, 2) + fir_2_e[2]*c_fr + fir_2_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        fir_2_table_X[j*delp_interval+k, 0] = c_fr
                        fir_2_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        fir_2_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(fir_2_table_X, fir_2_table_Y)
                result = clf.score(fir_2_table_X, fir_2_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p3_m_coef = lin_coeff[0,0]
                p3_p_coeff = lin_coeff[0,1]
                p3_cst = int_lin[0]
                p3_max_m = fir_2_flow_max[0]
                p3_max_p = fir_2_p_max
                
                p3_c0 = fir_2[0]
                p3_c1 = fir_2[1]
                p3_c2 = fir_2[2]
    
            if all_pump_nwk_combi['fir_3'][i] == 1:
                fir_3_flow_max = solve_quad_simul_eqns(fir_3, fir_lower_limit_0)
                fir_3_e_max = fir_3_e[0]*pow(fir_3_flow_max[0], 3) + fir_3_e[1]*pow(fir_3_flow_max[0], 2) + fir_3_e[2]*fir_3_flow_max[0] + fir_3_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = fir_3_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                fir_3_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                fir_3_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = fir_lower_limit_0[0]*pow(c_fr, 2) + fir_lower_limit_0[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = fir_3[0]*pow(c_fr, 2) + fir_3[1]*c_fr + fir_3[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (fir_3_e_max / fir_3_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = fir_3_e[0]*pow(c_fr, 3) + fir_3_e[1]*pow(c_fr, 2) + fir_3_e[2]*c_fr + fir_3_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        fir_3_table_X[j*delp_interval+k, 0] = c_fr
                        fir_3_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        fir_3_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(fir_3_table_X, fir_3_table_Y)
                result = clf.score(fir_3_table_X, fir_3_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p3_m_coef = lin_coeff[0,0]
                p3_p_coeff = lin_coeff[0,1]
                p3_cst = int_lin[0]
                p3_max_m = fir_3_flow_max[0]
                p3_max_p = fir_3_p_max
                
                p3_c0 = fir_3[0]
                p3_c1 = fir_3[1]
                p3_c2 = fir_3[2]
            
            temp_data = [all_pump_nwk_combi['nwk_choice'][i], all_pump_nwk_combi['ice_1'][i], all_pump_nwk_combi['ice_2'][i], all_pump_nwk_combi['tro_1'][i],
                         all_pump_nwk_combi['tro_2'][i], all_pump_nwk_combi['fir_1'][i], all_pump_nwk_combi['fir_2'][i], all_pump_nwk_combi['fir_3'][i],
                         p1_m_coef, p1_p_coeff, p1_cst, p1_max_m, p1_max_p, p2_m_coef, p2_p_coeff, p2_cst, p2_max_m, p2_max_p, p3_m_coef, p3_p_coeff, p3_cst, p3_max_m, p3_max_p]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3', 'p1_m_coeff', 'p1_p_coeff', 
                                                                       'p1_cst', 'p1_max_m', 'p1_max_p', 'p2_m_coeff', 'p2_p_coeff', 'p2_cst', 'p2_max_m', 'p2_max_p', 'p3_m_coeff', 
                                                                       'p3_p_coeff', 'p3_cst', 'p3_max_m', 'p3_max_p'])
            all_combi_dist_pump_lin_coeff = all_combi_dist_pump_lin_coeff.append(temp_data_df, ignore_index=True)  

            temp_data = [all_pump_nwk_combi['nwk_choice'][i], all_pump_nwk_combi['ice_1'][i], all_pump_nwk_combi['ice_2'][i], all_pump_nwk_combi['tro_1'][i],
                         all_pump_nwk_combi['tro_2'][i], all_pump_nwk_combi['fir_1'][i], all_pump_nwk_combi['fir_2'][i], all_pump_nwk_combi['fir_3'][i],
                         p1_c0, p1_c1, p1_c2, p2_c0, p2_c1, p2_c2, p3_c0, p3_c1, p3_c2]  
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3', 'p1_c0', 'p1_c1', 'p1_c2',
                                                                       'p2_c0', 'p2_c1', 'p2_c2', 'p3_c0', 'p3_c1', 'p3_c2'])       
            all_combi_dist_pump_press_coeff = all_combi_dist_pump_press_coeff.append(temp_data_df, ignore_index=True)              
    
    #############################################################################################################################################################################
    #############################################################################################################################################################################
    #############################################################################################################################################################################
    
        elif all_pump_nwk_combi['nwk_choice'][i] == 1:
            ##Extracting the relevant network coefficients 
            ice_tro_lower_limit_1 = [all_lower_limit_dist_nwk['x2_coeff'][3], all_lower_limit_dist_nwk['x_coeff'][3], 0]
            fir_lower_limit_1 = [all_lower_limit_dist_nwk['x2_coeff'][4], all_lower_limit_dist_nwk['x_coeff'][4], 0]
            ##For each of the selected pumps, we would like to find the associated regression based values
            ##The procedure will be as follows:
                ##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case 
                ##Evaluating the maximum electricity consumption at the intersection point 
                ##Assume that the variable speed correlates linearly with the electrical consumption 
                ##We aim to express E = A1m + A2p + cst, hence regression analysis is needed
                ##To do that, we take 20 points for each of the flowrate interval for different pressure drops and electricity consumptions 
                
            if all_pump_nwk_combi['ice_1'][i] == 1:
                ice_1_flow_max = solve_quad_simul_eqns(ice_1, ice_tro_lower_limit_1)
                ice_1_e_max = ice_1_e[0]*pow(ice_1_flow_max[0], 3) + ice_1_e[1]*pow(ice_1_flow_max[0], 2) + ice_1_e[2]*ice_1_flow_max[0] + ice_1_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = ice_1_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                ice_1_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                ice_1_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_tro_lower_limit_1[0]*pow(c_fr, 2) + ice_tro_lower_limit_1[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = ice_1[0]*pow(c_fr, 2) + ice_1[1]*c_fr + ice_1[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (ice_1_e_max / ice_1_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = ice_1_e[0]*pow(c_fr, 3) + ice_1_e[1]*pow(c_fr, 2) + ice_1_e[2]*c_fr + ice_1_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        ice_1_table_X[j*delp_interval+k, 0] = c_fr
                        ice_1_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        ice_1_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(ice_1_table_X, ice_1_table_Y)
                result = clf.score(ice_1_table_X, ice_1_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = ice_1_flow_max[0]
                p1_max_p = ice_1_p_max
                
                p1_c0 = ice_1[0]
                p1_c1 = ice_1[1]
                p1_c2 = ice_1[2]
                
            if all_pump_nwk_combi['ice_2'][i] == 1:
                ice_2_flow_max = solve_quad_simul_eqns(ice_2, ice_tro_lower_limit_1)
                ice_2_e_max = ice_2_e[0]*pow(ice_2_flow_max[0], 3) + ice_2_e[1]*pow(ice_2_flow_max[0], 2) + ice_2_e[2]*ice_2_flow_max[0] + ice_2_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = ice_2_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                ice_2_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                ice_2_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_tro_lower_limit_1[0]*pow(c_fr, 2) + ice_tro_lower_limit_1[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = ice_2[0]*pow(c_fr, 2) + ice_2[1]*c_fr + ice_2[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (ice_2_e_max / ice_2_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = ice_2_e[0]*pow(c_fr, 3) + ice_2_e[1]*pow(c_fr, 2) + ice_2_e[2]*c_fr + ice_2_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        ice_2_table_X[j*delp_interval+k, 0] = c_fr
                        ice_2_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        ice_2_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(ice_2_table_X, ice_2_table_Y)
                result = clf.score(ice_2_table_X, ice_2_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = ice_2_flow_max[0]            
                p1_max_p = ice_2_p_max
                
                p1_c0 = ice_2[0]
                p1_c1 = ice_2[1]
                p1_c2 = ice_2[2]
                
            if all_pump_nwk_combi['tro_1'][i] == 1:
                tro_1_flow_max = solve_quad_simul_eqns(tro_1, ice_tro_lower_limit_1)
                tro_1_e_max = tro_1_e[0]*pow(tro_1_flow_max[0], 3) + tro_1_e[1]*pow(tro_1_flow_max[0], 2) + tro_1_e[2]*tro_1_flow_max[0] + tro_1_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = tro_1_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                tro_1_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                tro_1_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_tro_lower_limit_1[0]*pow(c_fr, 2) + ice_tro_lower_limit_1[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = tro_1[0]*pow(c_fr, 2) + tro_1[1]*c_fr + tro_1[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (tro_1_e_max / tro_1_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = tro_1_e[0]*pow(c_fr, 3) + tro_1_e[1]*pow(c_fr, 2) + tro_1_e[2]*c_fr + tro_1_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        tro_1_table_X[j*delp_interval+k, 0] = c_fr
                        tro_1_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        tro_1_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(tro_1_table_X, tro_1_table_Y)
                result = clf.score(tro_1_table_X, tro_1_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = tro_1_flow_max[0] 
                p1_max_p = tro_1_p_max
                
                p1_c0 = tro_1[0]
                p1_c1 = tro_1[1]
                p1_c2 = tro_1[2]
    
            if all_pump_nwk_combi['tro_2'][i] == 1:
                tro_2_flow_max = solve_quad_simul_eqns(tro_2, ice_tro_lower_limit_1)
                tro_2_e_max = tro_2_e[0]*pow(tro_2_flow_max[0], 3) + tro_2_e[1]*pow(tro_2_flow_max[0], 2) + tro_2_e[2]*tro_2_flow_max[0] + tro_2_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = tro_2_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                tro_2_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                tro_2_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_tro_lower_limit_1[0]*pow(c_fr, 2) + ice_tro_lower_limit_1[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = tro_2[0]*pow(c_fr, 2) + tro_2[1]*c_fr + tro_2[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (tro_2_e_max / tro_2_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = tro_2_e[0]*pow(c_fr, 3) + tro_2_e[1]*pow(c_fr, 2) + tro_2_e[2]*c_fr + tro_2_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        tro_2_table_X[j*delp_interval+k, 0] = c_fr
                        tro_2_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        tro_2_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(tro_2_table_X, tro_2_table_Y)
                result = clf.score(tro_2_table_X, tro_2_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = tro_2_flow_max[0] 
                p1_max_p = tro_2_p_max
                
                p1_c0 = tro_2[0]
                p1_c1 = tro_2[1]
                p1_c2 = tro_2[2]
    
            if all_pump_nwk_combi['fir_1'][i] == 1:
                fir_1_flow_max = solve_quad_simul_eqns(fir_1, fir_lower_limit_1)
                fir_1_e_max = fir_1_e[0]*pow(fir_1_flow_max[0], 3) + fir_1_e[1]*pow(fir_1_flow_max[0], 2) + fir_1_e[2]*fir_1_flow_max[0] + fir_1_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = fir_1_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                fir_1_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                fir_1_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = fir_lower_limit_1[0]*pow(c_fr, 2) + fir_lower_limit_1[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = fir_1[0]*pow(c_fr, 2) + fir_1[1]*c_fr + fir_1[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (fir_1_e_max / fir_1_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = fir_1_e[0]*pow(c_fr, 3) + fir_1_e[1]*pow(c_fr, 2) + fir_1_e[2]*c_fr + fir_1_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        fir_1_table_X[j*delp_interval+k, 0] = c_fr
                        fir_1_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        fir_1_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(fir_1_table_X, fir_1_table_Y)
                result = clf.score(fir_1_table_X, fir_1_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p2_m_coef = lin_coeff[0,0]
                p2_p_coeff = lin_coeff[0,1]
                p2_cst = int_lin[0]
                p2_max_m = fir_1_flow_max[0]
                p2_max_p = fir_1_p_max
                
                p2_c0 = fir_1[0]
                p2_c1 = fir_1[1]
                p2_c2 = fir_1[2]
    
            if all_pump_nwk_combi['fir_2'][i] == 1:
                fir_2_flow_max = solve_quad_simul_eqns(fir_2, fir_lower_limit_1)
                fir_2_e_max = fir_2_e[0]*pow(fir_2_flow_max[0], 3) + fir_2_e[1]*pow(fir_2_flow_max[0], 2) + fir_2_e[2]*fir_2_flow_max[0] + fir_2_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = fir_2_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                fir_2_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                fir_2_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = fir_lower_limit_1[0]*pow(c_fr, 2) + fir_lower_limit_1[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = fir_2[0]*pow(c_fr, 2) + fir_2[1]*c_fr + fir_2[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (fir_2_e_max / fir_2_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = fir_2_e[0]*pow(c_fr, 3) + fir_2_e[1]*pow(c_fr, 2) + fir_2_e[2]*c_fr + fir_2_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        fir_2_table_X[j*delp_interval+k, 0] = c_fr
                        fir_2_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        fir_2_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(fir_2_table_X, fir_2_table_Y)
                result = clf.score(fir_2_table_X, fir_2_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p2_m_coef = lin_coeff[0,0]
                p2_p_coeff = lin_coeff[0,1]
                p2_cst = int_lin[0]
                p2_max_m = fir_2_flow_max[0]
                p2_max_p = fir_2_p_max
                
                p2_c0 = fir_2[0]
                p2_c1 = fir_2[1]
                p2_c2 = fir_2[2]
    
            if all_pump_nwk_combi['fir_3'][i] == 1:
                fir_3_flow_max = solve_quad_simul_eqns(fir_3, fir_lower_limit_1)
                fir_3_e_max = fir_3_e[0]*pow(fir_3_flow_max[0], 3) + fir_3_e[1]*pow(fir_3_flow_max[0], 2) + fir_3_e[2]*fir_3_flow_max[0] + fir_3_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = fir_3_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                fir_3_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                fir_3_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = fir_lower_limit_1[0]*pow(c_fr, 2) + fir_lower_limit_1[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = fir_3[0]*pow(c_fr, 2) + fir_3[1]*c_fr + fir_3[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (fir_3_e_max / fir_3_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = fir_3_e[0]*pow(c_fr, 3) + fir_3_e[1]*pow(c_fr, 2) + fir_3_e[2]*c_fr + fir_3_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        fir_3_table_X[j*delp_interval+k, 0] = c_fr
                        fir_3_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        fir_3_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(fir_3_table_X, fir_3_table_Y)
                result = clf.score(fir_3_table_X, fir_3_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p2_m_coef = lin_coeff[0,0]
                p2_p_coeff = lin_coeff[0,1]
                p2_cst = int_lin[0]
                p2_max_m = fir_3_flow_max[0]
                p2_max_p = fir_3_p_max
                
                p2_c0 = fir_3[0]
                p2_c1 = fir_3[1]
                p2_c2 = fir_3[2]
    
            temp_data = [all_pump_nwk_combi['nwk_choice'][i], all_pump_nwk_combi['ice_1'][i], all_pump_nwk_combi['ice_2'][i], all_pump_nwk_combi['tro_1'][i],
                         all_pump_nwk_combi['tro_2'][i], all_pump_nwk_combi['fir_1'][i], all_pump_nwk_combi['fir_2'][i], all_pump_nwk_combi['fir_3'][i],
                         p1_m_coef, p1_p_coeff, p1_cst, p1_max_m, p1_max_p, p2_m_coef, p2_p_coeff, p2_cst, p2_max_m, p2_max_p, 0, 0, 0, 0, 0]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3', 'p1_m_coeff', 'p1_p_coeff', 
                                                                       'p1_cst', 'p1_max_m', 'p1_max_p', 'p2_m_coeff', 'p2_p_coeff', 'p2_cst', 'p2_max_m', 'p2_max_p', 'p3_m_coeff', 
                                                                       'p3_p_coeff', 'p3_cst', 'p3_max_m', 'p3_max_p'])
            all_combi_dist_pump_lin_coeff = all_combi_dist_pump_lin_coeff.append(temp_data_df, ignore_index=True)    

            temp_data = [all_pump_nwk_combi['nwk_choice'][i], all_pump_nwk_combi['ice_1'][i], all_pump_nwk_combi['ice_2'][i], all_pump_nwk_combi['tro_1'][i],
                         all_pump_nwk_combi['tro_2'][i], all_pump_nwk_combi['fir_1'][i], all_pump_nwk_combi['fir_2'][i], all_pump_nwk_combi['fir_3'][i],
                         p1_c0, p1_c1, p1_c2, p2_c0, p2_c1, p2_c2, 0, 0, 0]  
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3', 'p1_c0', 'p1_c1', 'p1_c2',
                                                                       'p2_c0', 'p2_c1', 'p2_c2', 'p3_c0', 'p3_c1', 'p3_c2'])       
            all_combi_dist_pump_press_coeff = all_combi_dist_pump_press_coeff.append(temp_data_df, ignore_index=True)                         
    
    ############################################################################################################################################################################
    ############################################################################################################################################################################
    ############################################################################################################################################################################
            
        elif all_pump_nwk_combi['nwk_choice'][i] == 2:
            ##Extracting the relevant network coefficients:
            ice_lower_limit_2 = [all_lower_limit_dist_nwk['x2_coeff'][5], all_lower_limit_dist_nwk['x_coeff'][5], 0]
            tro_fir_lower_limit_2 = [all_lower_limit_dist_nwk['x2_coeff'][6], all_lower_limit_dist_nwk['x_coeff'][6], 0]
            ##For each of the selected pumps, we would like to find the associated regression based values
            ##The procedure will be as follows:
                ##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case 
                ##Evaluating the maximum electricity consumption at the intersection point 
                ##Assume that the variable speed correlates linearly with the electrical consumption 
                ##We aim to express E = A1m + A2p + cst, hence regression analysis is needed
                ##To do that, we take 20 points for each of the flowrate interval for different pressure drops and electricity consumptions 
                
            if all_pump_nwk_combi['ice_1'][i] == 1:
                ice_1_flow_max = solve_quad_simul_eqns(ice_1, ice_lower_limit_2)
                ice_1_e_max = ice_1_e[0]*pow(ice_1_flow_max[0], 3) + ice_1_e[1]*pow(ice_1_flow_max[0], 2) + ice_1_e[2]*ice_1_flow_max[0] + ice_1_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = ice_1_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                ice_1_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                ice_1_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_lower_limit_2[0]*pow(c_fr, 2) + ice_lower_limit_2[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = ice_1[0]*pow(c_fr, 2) + ice_1[1]*c_fr + ice_1[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (ice_1_e_max / ice_1_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = ice_1_e[0]*pow(c_fr, 3) + ice_1_e[1]*pow(c_fr, 2) + ice_1_e[2]*c_fr + ice_1_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        ice_1_table_X[j*delp_interval+k, 0] = c_fr
                        ice_1_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        ice_1_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(ice_1_table_X, ice_1_table_Y)
                result = clf.score(ice_1_table_X, ice_1_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = ice_1_flow_max[0]
                p1_max_p = ice_1_p_max
                
                p1_c0 = ice_1[0]
                p1_c1 = ice_1[1]
                p1_c2 = ice_1[2]
                
            if all_pump_nwk_combi['ice_2'][i] == 1:
                ice_2_flow_max = solve_quad_simul_eqns(ice_2, ice_lower_limit_2)
                ice_2_e_max = ice_2_e[0]*pow(ice_2_flow_max[0], 3) + ice_2_e[1]*pow(ice_2_flow_max[0], 2) + ice_2_e[2]*ice_2_flow_max[0] + ice_2_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = ice_2_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                ice_2_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                ice_2_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_lower_limit_2[0]*pow(c_fr, 2) + ice_lower_limit_2[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = ice_2[0]*pow(c_fr, 2) + ice_2[1]*c_fr + ice_2[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (ice_2_e_max / ice_2_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = ice_2_e[0]*pow(c_fr, 3) + ice_2_e[1]*pow(c_fr, 2) + ice_2_e[2]*c_fr + ice_2_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        ice_2_table_X[j*delp_interval+k, 0] = c_fr
                        ice_2_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        ice_2_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(ice_2_table_X, ice_2_table_Y)
                result = clf.score(ice_2_table_X, ice_2_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = ice_2_flow_max[0]            
                p1_max_p = ice_2_p_max
                
                p1_c0 = ice_2[0]
                p1_c1 = ice_2[1]
                p1_c2 = ice_2[2]
                
            if all_pump_nwk_combi['tro_1'][i] == 1:
                tro_1_flow_max = solve_quad_simul_eqns(tro_1, tro_fir_lower_limit_2)
                tro_1_e_max = tro_1_e[0]*pow(tro_1_flow_max[0], 3) + tro_1_e[1]*pow(tro_1_flow_max[0], 2) + tro_1_e[2]*tro_1_flow_max[0] + tro_1_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = tro_1_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                tro_1_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                tro_1_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = tro_fir_lower_limit_2[0]*pow(c_fr, 2) + tro_fir_lower_limit_2[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = tro_1[0]*pow(c_fr, 2) + tro_1[1]*c_fr + tro_1[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (tro_1_e_max / tro_1_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = tro_1_e[0]*pow(c_fr, 3) + tro_1_e[1]*pow(c_fr, 2) + tro_1_e[2]*c_fr + tro_1_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        tro_1_table_X[j*delp_interval+k, 0] = c_fr
                        tro_1_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        tro_1_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(tro_1_table_X, tro_1_table_Y)
                result = clf.score(tro_1_table_X, tro_1_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p2_m_coef = lin_coeff[0,0]
                p2_p_coeff = lin_coeff[0,1]
                p2_cst = int_lin[0]
                p2_max_m = tro_1_flow_max[0] 
                p2_max_p = tro_1_p_max
                
                p2_c0 = tro_1[0]
                p2_c1 = tro_1[1]
                p2_c2 = tro_1[2]
    
            if all_pump_nwk_combi['tro_2'][i] == 1:
                tro_2_flow_max = solve_quad_simul_eqns(tro_2, tro_fir_lower_limit_2)
                tro_2_e_max = tro_2_e[0]*pow(tro_2_flow_max[0], 3) + tro_2_e[1]*pow(tro_2_flow_max[0], 2) + tro_2_e[2]*tro_2_flow_max[0] + tro_2_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = tro_2_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                tro_2_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                tro_2_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = tro_fir_lower_limit_2[0]*pow(c_fr, 2) + tro_fir_lower_limit_2[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = tro_2[0]*pow(c_fr, 2) + tro_2[1]*c_fr + tro_2[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (tro_2_e_max / tro_2_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = tro_2_e[0]*pow(c_fr, 3) + tro_2_e[1]*pow(c_fr, 2) + tro_2_e[2]*c_fr + tro_2_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        tro_2_table_X[j*delp_interval+k, 0] = c_fr
                        tro_2_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        tro_2_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(tro_2_table_X, tro_2_table_Y)
                result = clf.score(tro_2_table_X, tro_2_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p2_m_coef = lin_coeff[0,0]
                p2_p_coeff = lin_coeff[0,1]
                p2_cst = int_lin[0]
                p2_max_m = tro_2_flow_max[0]  
                p2_max_p = tro_2_p_max
                
                p2_c0 = tro_2[0]
                p2_c1 = tro_2[1]
                p2_c2 = tro_2[2]
    
            if all_pump_nwk_combi['fir_1'][i] == 1:
                fir_1_flow_max = solve_quad_simul_eqns(fir_1, tro_fir_lower_limit_2)
                fir_1_e_max = fir_1_e[0]*pow(fir_1_flow_max[0], 3) + fir_1_e[1]*pow(fir_1_flow_max[0], 2) + fir_1_e[2]*fir_1_flow_max[0] + fir_1_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = fir_1_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                fir_1_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                fir_1_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = tro_fir_lower_limit_2[0]*pow(c_fr, 2) + tro_fir_lower_limit_2[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = fir_1[0]*pow(c_fr, 2) + fir_1[1]*c_fr + fir_1[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (fir_1_e_max / fir_1_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = fir_1_e[0]*pow(c_fr, 3) + fir_1_e[1]*pow(c_fr, 2) + fir_1_e[2]*c_fr + fir_1_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        fir_1_table_X[j*delp_interval+k, 0] = c_fr
                        fir_1_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        fir_1_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(fir_1_table_X, fir_1_table_Y)
                result = clf.score(fir_1_table_X, fir_1_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p2_m_coef = lin_coeff[0,0]
                p2_p_coeff = lin_coeff[0,1]
                p2_cst = int_lin[0]
                p2_max_m = fir_1_flow_max[0]
                p2_max_p = fir_1_p_max
                
                p2_c0 = fir_1[0]
                p2_c1 = fir_1[1]
                p2_c2 = fir_1[2]
    
            if all_pump_nwk_combi['fir_2'][i] == 1:
                fir_2_flow_max = solve_quad_simul_eqns(fir_2, tro_fir_lower_limit_2)
                fir_2_e_max = fir_2_e[0]*pow(fir_2_flow_max[0], 3) + fir_2_e[1]*pow(fir_2_flow_max[0], 2) + fir_2_e[2]*fir_2_flow_max[0] + fir_2_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = fir_2_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                fir_2_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                fir_2_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = tro_fir_lower_limit_2[0]*pow(c_fr, 2) + tro_fir_lower_limit_2[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = fir_2[0]*pow(c_fr, 2) + fir_2[1]*c_fr + fir_2[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (fir_2_e_max / fir_2_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = fir_2_e[0]*pow(c_fr, 3) + fir_2_e[1]*pow(c_fr, 2) + fir_2_e[2]*c_fr + fir_2_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        fir_2_table_X[j*delp_interval+k, 0] = c_fr
                        fir_2_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        fir_2_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(fir_2_table_X, fir_2_table_Y)
                result = clf.score(fir_2_table_X, fir_2_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p2_m_coef = lin_coeff[0,0]
                p2_p_coeff = lin_coeff[0,1]
                p2_cst = int_lin[0]
                p2_max_m = fir_2_flow_max[0]
                p2_max_p = fir_2_p_max
                
                p2_c0 = fir_2[0]
                p2_c1 = fir_2[1]
                p2_c2 = fir_2[2]
    
            if all_pump_nwk_combi['fir_3'][i] == 1:
                fir_3_flow_max = solve_quad_simul_eqns(fir_3, tro_fir_lower_limit_2)
                fir_3_e_max = fir_3_e[0]*pow(fir_3_flow_max[0], 3) + fir_3_e[1]*pow(fir_3_flow_max[0], 2) + fir_3_e[2]*fir_3_flow_max[0] + fir_3_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = fir_3_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                fir_3_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                fir_3_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = tro_fir_lower_limit_2[0]*pow(c_fr, 2) + tro_fir_lower_limit_2[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = fir_3[0]*pow(c_fr, 2) + fir_3[1]*c_fr + fir_3[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (fir_3_e_max / fir_3_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = fir_3_e[0]*pow(c_fr, 3) + fir_3_e[1]*pow(c_fr, 2) + fir_3_e[2]*c_fr + fir_3_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        fir_3_table_X[j*delp_interval+k, 0] = c_fr
                        fir_3_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        fir_3_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(fir_3_table_X, fir_3_table_Y)
                result = clf.score(fir_3_table_X, fir_3_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p2_m_coef = lin_coeff[0,0]
                p2_p_coeff = lin_coeff[0,1]
                p2_cst = int_lin[0]
                p2_max_m = fir_3_flow_max[0]
                p2_max_p = fir_3_p_max
                
                p2_c0 = fir_3[0]
                p2_c1 = fir_3[1]
                p2_c2 = fir_3[2]
    
            temp_data = [all_pump_nwk_combi['nwk_choice'][i], all_pump_nwk_combi['ice_1'][i], all_pump_nwk_combi['ice_2'][i], all_pump_nwk_combi['tro_1'][i],
                         all_pump_nwk_combi['tro_2'][i], all_pump_nwk_combi['fir_1'][i], all_pump_nwk_combi['fir_2'][i], all_pump_nwk_combi['fir_3'][i],
                         p1_m_coef, p1_p_coeff, p1_cst, p1_max_m, p1_max_p, p2_m_coef, p2_p_coeff, p2_cst, p2_max_m, p2_max_p, 0, 0, 0, 0, 0]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3', 'p1_m_coeff', 'p1_p_coeff', 
                                                                       'p1_cst', 'p1_max_m', 'p1_max_p', 'p2_m_coeff', 'p2_p_coeff', 'p2_cst', 'p2_max_m', 'p2_max_p', 'p3_m_coeff', 
                                                                       'p3_p_coeff', 'p3_cst', 'p3_max_m', 'p3_max_p'])
            all_combi_dist_pump_lin_coeff = all_combi_dist_pump_lin_coeff.append(temp_data_df, ignore_index=True) 
            
            temp_data = [all_pump_nwk_combi['nwk_choice'][i], all_pump_nwk_combi['ice_1'][i], all_pump_nwk_combi['ice_2'][i], all_pump_nwk_combi['tro_1'][i],
                         all_pump_nwk_combi['tro_2'][i], all_pump_nwk_combi['fir_1'][i], all_pump_nwk_combi['fir_2'][i], all_pump_nwk_combi['fir_3'][i],
                         p1_c0, p1_c1, p1_c2, p2_c0, p2_c1, p2_c2, 0, 0, 0]  
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3', 'p1_c0', 'p1_c1', 'p1_c2',
                                                                       'p2_c0', 'p2_c1', 'p2_c2', 'p3_c0', 'p3_c1', 'p3_c2'])       
            all_combi_dist_pump_press_coeff = all_combi_dist_pump_press_coeff.append(temp_data_df, ignore_index=True)
    
    ############################################################################################################################################################################
    ############################################################################################################################################################################
    ############################################################################################################################################################################
                            
        else:
            ##Extracting the relevant network coefficients:
            ice_tro_fir_lower_limit_3 = [all_lower_limit_dist_nwk['x2_coeff'][7], all_lower_limit_dist_nwk['x_coeff'][7], 0]
            ##For each of the selected pumps, we would like to find the associated regression based values
            ##The procedure will be as follows:
                ##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case 
                ##Evaluating the maximum electricity consumption at the intersection point 
                ##Assume that the variable speed correlates linearly with the electrical consumption 
                ##We aim to express E = A1m + A2p + cst, hence regression analysis is needed
                ##To do that, we take 20 points for each of the flowrate interval for different pressure drops and electricity consumptions 
                
            if all_pump_nwk_combi['ice_1'][i] == 1:
                ice_1_flow_max = solve_quad_simul_eqns(ice_1, ice_tro_fir_lower_limit_3)
                ice_1_e_max = ice_1_e[0]*pow(ice_1_flow_max[0], 3) + ice_1_e[1]*pow(ice_1_flow_max[0], 2) + ice_1_e[2]*ice_1_flow_max[0] + ice_1_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = ice_1_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                ice_1_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                ice_1_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_tro_fir_lower_limit_3[0]*pow(c_fr, 2) + ice_tro_fir_lower_limit_3[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = ice_1[0]*pow(c_fr, 2) + ice_1[1]*c_fr + ice_1[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (ice_1_e_max / ice_1_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = ice_1_e[0]*pow(c_fr, 3) + ice_1_e[1]*pow(c_fr, 2) + ice_1_e[2]*c_fr + ice_1_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        ice_1_table_X[j*delp_interval+k, 0] = c_fr
                        ice_1_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        ice_1_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(ice_1_table_X, ice_1_table_Y)
                result = clf.score(ice_1_table_X, ice_1_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = ice_1_flow_max[0]
                p1_max_p = ice_1_p_max
            
                p1_c0 = ice_1[0]
                p1_c1 = ice_1[1]
                p1_c2 = ice_1[2]
                
            if all_pump_nwk_combi['ice_2'][i] == 1:
                ice_2_flow_max = solve_quad_simul_eqns(ice_2, ice_tro_fir_lower_limit_3)
                ice_2_e_max = ice_2_e[0]*pow(ice_2_flow_max[0], 3) + ice_2_e[1]*pow(ice_2_flow_max[0], 2) + ice_2_e[2]*ice_2_flow_max[0] + ice_2_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = ice_2_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                ice_2_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                ice_2_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_tro_fir_lower_limit_3[0]*pow(c_fr, 2) + ice_tro_fir_lower_limit_3[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = ice_2[0]*pow(c_fr, 2) + ice_2[1]*c_fr + ice_2[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (ice_2_e_max / ice_2_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = ice_2_e[0]*pow(c_fr, 3) + ice_2_e[1]*pow(c_fr, 2) + ice_2_e[2]*c_fr + ice_2_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        ice_2_table_X[j*delp_interval+k, 0] = c_fr
                        ice_2_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        ice_2_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(ice_2_table_X, ice_2_table_Y)
                result = clf.score(ice_2_table_X, ice_2_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = ice_2_flow_max[0]            
                p1_max_p = ice_2_p_max
                
                p1_c0 = ice_2[0]
                p1_c1 = ice_2[1]
                p1_c2 = ice_2[2]
                
            if all_pump_nwk_combi['tro_1'][i] == 1:
                tro_1_flow_max = solve_quad_simul_eqns(tro_1, ice_tro_fir_lower_limit_3)
                tro_1_e_max = tro_1_e[0]*pow(tro_1_flow_max[0], 3) + tro_1_e[1]*pow(tro_1_flow_max[0], 2) + tro_1_e[2]*tro_1_flow_max[0] + tro_1_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = tro_1_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                tro_1_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                tro_1_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_tro_fir_lower_limit_3[0]*pow(c_fr, 2) + ice_tro_fir_lower_limit_3[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = tro_1[0]*pow(c_fr, 2) + tro_1[1]*c_fr + tro_1[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (tro_1_e_max / tro_1_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = tro_1_e[0]*pow(c_fr, 3) + tro_1_e[1]*pow(c_fr, 2) + tro_1_e[2]*c_fr + tro_1_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        tro_1_table_X[j*delp_interval+k, 0] = c_fr
                        tro_1_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        tro_1_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(tro_1_table_X, tro_1_table_Y)
                result = clf.score(tro_1_table_X, tro_1_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = tro_1_flow_max[0]  
                p1_max_p = tro_1_p_max
                
                p1_c0 = tro_1[0]
                p1_c1 = tro_1[1]
                p1_c2 = tro_1[2]
    
            if all_pump_nwk_combi['tro_2'][i] == 1:
                tro_2_flow_max = solve_quad_simul_eqns(tro_2, ice_tro_fir_lower_limit_3)
                tro_2_e_max = tro_2_e[0]*pow(tro_2_flow_max[0], 3) + tro_2_e[1]*pow(tro_2_flow_max[0], 2) + tro_2_e[2]*tro_2_flow_max[0] + tro_2_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = tro_2_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                tro_2_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                tro_2_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_tro_fir_lower_limit_3[0]*pow(c_fr, 2) + ice_tro_fir_lower_limit_3[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = tro_2[0]*pow(c_fr, 2) + tro_2[1]*c_fr + tro_2[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (tro_2_e_max / tro_2_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = tro_2_e[0]*pow(c_fr, 3) + tro_2_e[1]*pow(c_fr, 2) + tro_2_e[2]*c_fr + tro_2_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        tro_2_table_X[j*delp_interval+k, 0] = c_fr
                        tro_2_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        tro_2_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(tro_2_table_X, tro_2_table_Y)
                result = clf.score(tro_2_table_X, tro_2_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = tro_2_flow_max[0]  
                p1_max_p = tro_2_p_max
                
                p1_c0 = tro_2[0]
                p1_c1 = tro_2[1]
                p1_c2 = tro_2[2]
    
            if all_pump_nwk_combi['fir_1'][i] == 1:
                fir_1_flow_max = solve_quad_simul_eqns(fir_1, ice_tro_fir_lower_limit_3)
                fir_1_e_max = fir_1_e[0]*pow(fir_1_flow_max[0], 3) + fir_1_e[1]*pow(fir_1_flow_max[0], 2) + fir_1_e[2]*fir_1_flow_max[0] + fir_1_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = fir_1_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                fir_1_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                fir_1_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_tro_fir_lower_limit_3[0]*pow(c_fr, 2) + ice_tro_fir_lower_limit_3[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = fir_1[0]*pow(c_fr, 2) + fir_1[1]*c_fr + fir_1[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (fir_1_e_max / fir_1_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = fir_1_e[0]*pow(c_fr, 3) + fir_1_e[1]*pow(c_fr, 2) + fir_1_e[2]*c_fr + fir_1_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        fir_1_table_X[j*delp_interval+k, 0] = c_fr
                        fir_1_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        fir_1_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(fir_1_table_X, fir_1_table_Y)
                result = clf.score(fir_1_table_X, fir_1_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = fir_1_flow_max[0]
                p1_max_p = fir_1_p_max
                
                p1_c0 = fir_1[0]
                p1_c1 = fir_1[1]
                p1_c2 = fir_1[2]
    
            if all_pump_nwk_combi['fir_2'][i] == 1:
                fir_2_flow_max = solve_quad_simul_eqns(fir_2, ice_tro_fir_lower_limit_3)
                fir_2_e_max = fir_2_e[0]*pow(fir_2_flow_max[0], 3) + fir_2_e[1]*pow(fir_2_flow_max[0], 2) + fir_2_e[2]*fir_2_flow_max[0] + fir_2_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = fir_2_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                fir_2_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                fir_2_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_tro_fir_lower_limit_3[0]*pow(c_fr, 2) + ice_tro_fir_lower_limit_3[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = fir_2[0]*pow(c_fr, 2) + fir_2[1]*c_fr + fir_2[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (fir_2_e_max / fir_2_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = fir_2_e[0]*pow(c_fr, 3) + fir_2_e[1]*pow(c_fr, 2) + fir_2_e[2]*c_fr + fir_2_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        fir_2_table_X[j*delp_interval+k, 0] = c_fr
                        fir_2_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        fir_2_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(fir_2_table_X, fir_2_table_Y)
                result = clf.score(fir_2_table_X, fir_2_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = fir_2_flow_max[0]
                p1_max_p = fir_2_p_max
                
                p1_c0 = fir_2[0]
                p1_c1 = fir_2[1]
                p1_c2 = fir_2[2]
    
            if all_pump_nwk_combi['fir_3'][i] == 1:
                fir_3_flow_max = solve_quad_simul_eqns(fir_3, ice_tro_fir_lower_limit_3)
                fir_3_e_max = fir_3_e[0]*pow(fir_3_flow_max[0], 3) + fir_3_e[1]*pow(fir_3_flow_max[0], 2) + fir_3_e[2]*fir_3_flow_max[0] + fir_3_e[3]
                
                delp_interval = 20
                flowrate_interval = 50
                flowrate_step = fir_3_flow_max[0] / flowrate_interval 
                ##Initiate a matrix to hold all the values 
                ##Column 1 will be flowrate 
                ##Column 2 will be pressure drop 
                ##Column 3 will be electricity consumed
                fir_3_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
                fir_3_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))     
                
                for j in range (0, flowrate_interval+1):
                    ##current flowrate 
                    c_fr = j * flowrate_step 
                    ##minimum pressure drop comes from the system curve 
                    min_p = ice_tro_fir_lower_limit_3[0]*pow(c_fr, 2) + ice_tro_fir_lower_limit_3[1]*c_fr
                    ##maximum pressure drop comes from the pump curve 
                    max_p = fir_3[0]*pow(c_fr, 2) + fir_3[1]*c_fr + fir_3[2]
                    ##minimum electricity consumption comes from the linear assumption curve 
                    min_e = c_fr * (fir_3_e_max / fir_3_flow_max[0])
                    ##maximum electricity consumption comes from the electricity curve 
                    max_e = fir_3_e[0]*pow(c_fr, 3) + fir_3_e[1]*pow(c_fr, 2) + fir_3_e[2]*c_fr + fir_3_e[3]
                    ##recording the maximum and minimums 
                    temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
                    temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)
            
                    for k in range (0, delp_interval):
                        fir_3_table_X[j*delp_interval+k, 0] = c_fr
                        fir_3_table_X[j*delp_interval+k, 1] = temp_pressure_rec[k]
                        fir_3_table_Y[j*delp_interval+k, 0] = temp_elec_rec[k]
                
                ##Performing regression analysis
                clf = linear_model.LinearRegression(fit_intercept = True)
                clf.fit(fir_3_table_X, fir_3_table_Y)
                result = clf.score(fir_3_table_X, fir_3_table_Y, sample_weight=None)
                lin_coeff = clf.coef_
                int_lin = clf.intercept_
        
                ##Assembling the DataFrame 
                p1_m_coef = lin_coeff[0,0]
                p1_p_coeff = lin_coeff[0,1]
                p1_cst = int_lin[0]
                p1_max_m = fir_3_flow_max[0]
                p1_max_p = fir_3_p_max
                
                p1_c0 = fir_3[0]
                p1_c1 = fir_3[1]
                p1_c2 = fir_3[2]
    
            temp_data = [all_pump_nwk_combi['nwk_choice'][i], all_pump_nwk_combi['ice_1'][i], all_pump_nwk_combi['ice_2'][i], all_pump_nwk_combi['tro_1'][i],
                         all_pump_nwk_combi['tro_2'][i], all_pump_nwk_combi['fir_1'][i], all_pump_nwk_combi['fir_2'][i], all_pump_nwk_combi['fir_3'][i],
                         p1_m_coef, p1_p_coeff, p1_cst, p1_max_m, p1_max_p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3', 'p1_m_coeff', 'p1_p_coeff', 
                                                                       'p1_cst', 'p1_max_m', 'p1_max_p', 'p2_m_coeff', 'p2_p_coeff', 'p2_cst', 'p2_max_m', 'p2_max_p', 'p3_m_coeff', 
                                                                       'p3_p_coeff', 'p3_cst', 'p3_max_m', 'p3_max_p'])
            all_combi_dist_pump_lin_coeff = all_combi_dist_pump_lin_coeff.append(temp_data_df, ignore_index=True)
            
            temp_data = [all_pump_nwk_combi['nwk_choice'][i], all_pump_nwk_combi['ice_1'][i], all_pump_nwk_combi['ice_2'][i], all_pump_nwk_combi['tro_1'][i],
                         all_pump_nwk_combi['tro_2'][i], all_pump_nwk_combi['fir_1'][i], all_pump_nwk_combi['fir_2'][i], all_pump_nwk_combi['fir_3'][i],
                         p1_c0, p1_c1, p1_c2, 0, 0, 0, 0, 0, 0]  
            temp_data_df = pd.DataFrame(data = [temp_data], columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3', 'p1_c0', 'p1_c1', 'p1_c2',
                                                                       'p2_c0', 'p2_c1', 'p2_c2', 'p3_c0', 'p3_c1', 'p3_c2'])       
            all_combi_dist_pump_press_coeff = all_combi_dist_pump_press_coeff.append(temp_data_df, ignore_index=True)
            
    all_combi_dist_pump_lin_coeff.to_csv(current_directory + 'master_level_models\\\chiller_optimization_dist_nwk_ga_nb_master_level_models\\look_up_tables\\dist_pump_lincoeff.csv')
    all_combi_dist_pump_press_coeff.to_csv(current_directory + 'master_level_models\\\chiller_optimization_dist_nwk_ga_nb_master_level_models\\look_up_tables\\dist_pump_presscoeff.csv')
    return 

#########################################################################################################################################################################
##Running the extraction algorithm  
#if __name__ == '__main__':
#    prepare_dist_nwk_lin_coeff ()

#print(all_combi_dist_pump_lin_coeff)
#print(dim_all_pump_nwk_combi[0])
#print(all_pump_nwk_combi)
#
#print(dim_all_lower_limit_dist_nwk[0])
#print(all_lower_limit_dist_nwk)
