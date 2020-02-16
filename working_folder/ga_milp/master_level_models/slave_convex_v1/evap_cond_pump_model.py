##This script contains the evaporator and condenser pump models 

def evap_pump_ch1 ():
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\add_ons\\')
    from convert_to_quadratic import convert_to_quadratic 
    from solve_quad_simul_eqns import solve_quad_simul_eqns
    from sklearn import linear_model 
    import numpy as np
    import matplotlib.pyplot as plt 
    
    ##Pump parameters, regarding pressure-drop
    pumpaf1_c0 = -0.0001266405
    pumpaf1_c1 = 0.0112272822
    pumpaf1_c2 = 12.3463827922
    
    ##Pump parameters, regarding electricity consumption at the maximum rpm 
    pumpaf1_e_c0 = -0.0000003355
    pumpaf1_e_c1 = 0.0001014045
    pumpaf1_e_c2 = 0.0053863673
    pumpaf1_e_c3 = 3.8221779914
    
    ##Network parameters 
    evap_network_A_val = 1.66667E-05
    ch1_evap_A_val = 0.000246472 + evap_network_A_val
    
    ##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case 
    ch1_evap_x2_coeff, ch1_evap_x_coeff = convert_to_quadratic(ch1_evap_A_val)
    ##ch1_eflow_max[0] - maximum flowrate for this given combination 
    ch1_eflow_max = solve_quad_simul_eqns([ch1_evap_x2_coeff, ch1_evap_x_coeff, 0], [pumpaf1_c0, pumpaf1_c1, pumpaf1_c2])
    ##The corresponding electricity consumption at the maximum flowrate and rpm is 
    ch1_e_max = pumpaf1_e_c0*pow(ch1_eflow_max[0], 3) + pumpaf1_e_c1*pow(ch1_eflow_max[0], 2) + pumpaf1_e_c2*ch1_eflow_max[0] + pumpaf1_e_c3
    ##From here onwards, variable speed of the pump will be assumed to linearly correlate with electrical consumption 
    ##We want to express E = A1m + A2p + cst, hence regression analysis is needed 
    ##To do that, we take 20 points for each of the flowrate interval for different pressure drops and electricity consumptions 
    delp_interval = 20 
    flowrate_interval = 50
    flowrate_step = ch1_eflow_max[0] / flowrate_interval 
    ##Initiate a matrix to hold all the values 
    ##Column 1 will be flowrate 
    ##Column 2 will be pressure drop 
    ##Column 3 will be electricity consumed 
    ch1_value_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
    ch1_value_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))

    for i in range (0, flowrate_interval+1):
        ##current flowrate 
        c_fr = i * flowrate_step 
        ##minimum pressure drop comes from the system curve 
        min_p = ch1_evap_x2_coeff*pow(c_fr, 2) + ch1_evap_x_coeff*c_fr
        ##maximum pressure drop comes from the pump curve 
        max_p = pumpaf1_c0*pow(c_fr, 2) + pumpaf1_c1*c_fr + pumpaf1_c2
        ##minimum electricity consumption comes from the linear assumption curve 
        min_e = c_fr * (ch1_e_max / ch1_eflow_max[0])
        ##maximum electricity consumption comes from the electricity curve 
        max_e = pumpaf1_e_c0*pow(c_fr, 3) + pumpaf1_e_c1*pow(c_fr, 2) + pumpaf1_e_c2*c_fr + pumpaf1_e_c3
        ##recording the maximum and minimums 
        temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
        temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)

        for j in range (0, delp_interval):
            ch1_value_table_X[i*delp_interval+j, 0] = c_fr
            ch1_value_table_X[i*delp_interval+j, 1] = temp_pressure_rec[j]
            ch1_value_table_Y[i*delp_interval+j, 0] = temp_elec_rec[j]
    
    ##Performing regression analysis
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(ch1_value_table_X, ch1_value_table_Y)
    result = clf.score(ch1_value_table_X, ch1_value_table_Y, sample_weight=None)
    lin_coeff = clf.coef_
    int_lin = clf.intercept_  
      
    ##print(result)
    ##print(lin_coeff)
    ##print(int_lin)

    ##Evaluating the electricity consumption using linear combination model 
    calc_Y = np.zeros(((delp_interval*(flowrate_interval+1) ,1)))
    for i in range (0, delp_interval*(flowrate_interval+1)):
        calc_Y[i,0] = lin_coeff[0,0]*ch1_value_table_X[i,0] + lin_coeff[0,1]*ch1_value_table_X[i,1] + int_lin
    
    ##Plotting the pressure drop and flowrate area
#    plt.plot(ch1_value_table_X[:, 0], ch1_value_table_X[:, 1], 'o')
#    plt.show()
    ##Plotting the electricity consumption and flowrate area
#    plt.plot(ch1_value_table_X[:, 0], ch1_value_table_Y[:, 0], 'o')
#    plt.show()
    ##Plotting actual values and predicted values 
#    plt.plot(calc_Y, ch1_value_table_Y, 'o')
#    plt.show()
#    plt.plot(ch1_value_table_X[:, 0], calc_Y, 'o')
#    plt.show()
    
    ##Assembling the return values 
    ch1_evap_pump_m_coeff = lin_coeff[0,0]
    ch1_evap_pump_p_coeff = lin_coeff[0,1]
    ch1_evap_pump_cst = int_lin
    ch1_evap_pump_max_flow = ch1_eflow_max[0]
    ch1_evap_pump_regress_r2 = result
    
    ret_values = np.zeros((5,1))
    ret_values[0,0] = ch1_evap_pump_m_coeff
    ret_values[1,0] = ch1_evap_pump_p_coeff
    ret_values[2,0] = ch1_evap_pump_cst
    ret_values[3,0] = ch1_evap_pump_max_flow
    ret_values[4,0] = ch1_evap_pump_regress_r2

    return ret_values

def evap_pump_ch2 ():
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\add_ons\\')
    from convert_to_quadratic import convert_to_quadratic 
    from solve_quad_simul_eqns import solve_quad_simul_eqns
    from sklearn import linear_model 
    import numpy as np
    import matplotlib.pyplot as plt 
    
    ##Pump parameters, regarding pressure-drop
    pumpaf2_c0 = -0.0000136254
    pumpaf2_c1 = 0.0001647403
    pumpaf2_c2 = 21.4327511013
    
    ##Pump parameters, regarding electricity consumption at the maximum rpm 
    pumpaf2_e_c0 = 0
    pumpaf2_e_c1 = -0.0000106288
    pumpaf2_e_c2 = 0.0310754128
    pumpaf2_e_c3 = 18.9432666214
    
    ##Network parameters 
    evap_network_A_val = 1.66667E-05
    ch2_evap_A_val = 3.07492E-05 + evap_network_A_val
    
    ##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case 
    ch2_evap_x2_coeff, ch2_evap_x_coeff = convert_to_quadratic(ch2_evap_A_val)
    ##ch2_eflow_max[0] - maximum flowrate for this given combination 
    ch2_eflow_max = solve_quad_simul_eqns([ch2_evap_x2_coeff, ch2_evap_x_coeff, 0], [pumpaf2_c0, pumpaf2_c1, pumpaf2_c2])
    ##The corresponding electricity consumption at the maximum flowrate and rpm is 
    ch2_e_max = pumpaf2_e_c0*pow(ch2_eflow_max[0], 3) + pumpaf2_e_c1*pow(ch2_eflow_max[0], 2) + pumpaf2_e_c2*ch2_eflow_max[0] + pumpaf2_e_c3
    ##From here onwards, variable speed of the pump will be assumed to linearly correlate with electrical consumption 
    ##We want to express E = A1m + A2p + cst, hence regression analysis is needed 
    ##To do that, we take 20 points for each of the flowrate interval for different pressure drops and electricity consumptions 
    delp_interval = 20 
    flowrate_interval = 50
    flowrate_step = ch2_eflow_max[0] / flowrate_interval 
    ##Initiate a matrix to hold all the values 
    ##Column 1 will be flowrate 
    ##Column 2 will be pressure drop 
    ##Column 3 will be electricity consumed 
    ch2_value_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
    ch2_value_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))

    for i in range (0, flowrate_interval+1):
        ##current flowrate 
        c_fr = i * flowrate_step 
        ##minimum pressure drop comes from the system curve 
        min_p = ch2_evap_x2_coeff*pow(c_fr, 2) + ch2_evap_x_coeff*c_fr
        ##maximum pressure drop comes from the pump curve 
        max_p = pumpaf2_c0*pow(c_fr, 2) + pumpaf2_c1*c_fr + pumpaf2_c2
        ##minimum electricity consumption comes from the linear assumption curve 
        min_e = c_fr * (ch2_e_max / ch2_eflow_max[0])
        ##maximum electricity consumption comes from the electricity curve 
        max_e = pumpaf2_e_c0*pow(c_fr, 3) + pumpaf2_e_c1*pow(c_fr, 2) + pumpaf2_e_c2*c_fr + pumpaf2_e_c3
        ##recording the maximum and minimums 
        temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
        temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)

        for j in range (0, delp_interval):
            ch2_value_table_X[i*delp_interval+j, 0] = c_fr
            ch2_value_table_X[i*delp_interval+j, 1] = temp_pressure_rec[j]
            ch2_value_table_Y[i*delp_interval+j, 0] = temp_elec_rec[j]
    
    ##Performing regression analysis
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(ch2_value_table_X, ch2_value_table_Y)
    result = clf.score(ch2_value_table_X, ch2_value_table_Y, sample_weight=None)
    lin_coeff = clf.coef_
    int_lin = clf.intercept_  
      
    ##print(result)
    ##print(lin_coeff)
    ##print(int_lin)

    ##Evaluating the electricity consumption using linear combination model 
    calc_Y = np.zeros(((delp_interval*(flowrate_interval+1) ,1)))
    for i in range (0, delp_interval*(flowrate_interval+1)):
        calc_Y[i,0] = lin_coeff[0,0]*ch2_value_table_X[i,0] + lin_coeff[0,1]*ch2_value_table_X[i,1] + int_lin
    
    ##Plotting the pressure drop and flowrate area
    ##plt.plot(ch2_value_table_X[:, 0], ch2_value_table_X[:, 1], 'o')
    ##plt.show()
    ##Plotting the electricity consumption and flowrate area
    ##plt.plot(ch2_value_table_X[:, 0], ch2_value_table_Y[:, 0], 'o')
    ##plt.show()
    ##Plotting actual values and predicted values 
    ##plt.plot(calc_Y, ch2_value_table_Y, 'o')
    ##plt.show()
    ##plt.plot(ch2_value_table_X[:, 0], calc_Y, 'o')
    ##plt.show()
    
    ##Assembling the return values 
    ch2_evap_pump_m_coeff = lin_coeff[0,0]
    ch2_evap_pump_p_coeff = lin_coeff[0,1]
    ch2_evap_pump_cst = int_lin
    ch2_evap_pump_max_flow = ch2_eflow_max[0]
    ch2_evap_pump_regress_r2 = result
    
    ret_values = np.zeros((5,1))
    ret_values[0,0] = ch2_evap_pump_m_coeff
    ret_values[1,0] = ch2_evap_pump_p_coeff
    ret_values[2,0] = ch2_evap_pump_cst
    ret_values[3,0] = ch2_evap_pump_max_flow
    ret_values[4,0] = ch2_evap_pump_regress_r2
    
    return ret_values 
    
def evap_pump_ch3 ():
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\add_ons\\')
    from convert_to_quadratic import convert_to_quadratic 
    from solve_quad_simul_eqns import solve_quad_simul_eqns
    from sklearn import linear_model 
    import numpy as np
    import matplotlib.pyplot as plt 
    
    ##Pump parameters, regarding pressure-drop
    pumpaf3_c0 = -0.0000136254
    pumpaf3_c1 = 0.0001647403
    pumpaf3_c2 = 21.4327511013
    
    ##Pump parameters, regarding electricity consumption at the maximum rpm 
    pumpaf3_e_c0 = 0
    pumpaf3_e_c1 = -0.0000106288
    pumpaf3_e_c2 = 0.0310754128
    pumpaf3_e_c3 = 18.9432666214
    
    ##Network parameters 
    evap_network_A_val = 1.66667E-05
    ch3_evap_A_val = 3.07492E-05 + evap_network_A_val
    
    ##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case 
    ch3_evap_x2_coeff, ch3_evap_x_coeff = convert_to_quadratic(ch3_evap_A_val)
    ##ch3_eflow_max[0] - maximum flowrate for this given combination 
    ch3_eflow_max = solve_quad_simul_eqns([ch3_evap_x2_coeff, ch3_evap_x_coeff, 0], [pumpaf3_c0, pumpaf3_c1, pumpaf3_c2])
    ##The corresponding electricity consumption at the maximum flowrate and rpm is 
    ch3_e_max = pumpaf3_e_c0*pow(ch3_eflow_max[0], 3) + pumpaf3_e_c1*pow(ch3_eflow_max[0], 2) + pumpaf3_e_c2*ch3_eflow_max[0] + pumpaf3_e_c3
    ##From here onwards, variable speed of the pump will be assumed to linearly correlate with electrical consumption 
    ##We want to express E = A1m + A2p + cst, hence regression analysis is needed 
    ##To do that, we take 20 points for each of the flowrate interval for different pressure drops and electricity consumptions 
    delp_interval = 20 
    flowrate_interval = 50
    flowrate_step = ch3_eflow_max[0] / flowrate_interval 
    ##Initiate a matrix to hold all the values 
    ##Column 1 will be flowrate 
    ##Column 2 will be pressure drop 
    ##Column 3 will be electricity consumed 
    ch3_value_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
    ch3_value_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))

    for i in range (0, flowrate_interval+1):
        ##current flowrate 
        c_fr = i * flowrate_step 
        ##minimum pressure drop comes from the system curve 
        min_p = ch3_evap_x2_coeff*pow(c_fr, 2) + ch3_evap_x_coeff*c_fr
        ##maximum pressure drop comes from the pump curve 
        max_p = pumpaf3_c0*pow(c_fr, 2) + pumpaf3_c1*c_fr + pumpaf3_c2
        ##minimum electricity consumption comes from the linear assumption curve 
        min_e = c_fr * (ch3_e_max / ch3_eflow_max[0])
        ##maximum electricity consumption comes from the electricity curve 
        max_e = pumpaf3_e_c0*pow(c_fr, 3) + pumpaf3_e_c1*pow(c_fr, 2) + pumpaf3_e_c2*c_fr + pumpaf3_e_c3
        ##recording the maximum and minimums 
        temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
        temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)

        for j in range (0, delp_interval):
            ch3_value_table_X[i*delp_interval+j, 0] = c_fr
            ch3_value_table_X[i*delp_interval+j, 1] = temp_pressure_rec[j]
            ch3_value_table_Y[i*delp_interval+j, 0] = temp_elec_rec[j]
    
    ##Performing regression analysis
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(ch3_value_table_X, ch3_value_table_Y)
    result = clf.score(ch3_value_table_X, ch3_value_table_Y, sample_weight=None)
    lin_coeff = clf.coef_
    int_lin = clf.intercept_  
      
    ##print(result)
    ##print(lin_coeff)
    ##print(int_lin)

    ##Evaluating the electricity consumption using linear combination model 
    calc_Y = np.zeros(((delp_interval*(flowrate_interval+1) ,1)))
    for i in range (0, delp_interval*(flowrate_interval+1)):
        calc_Y[i,0] = lin_coeff[0,0]*ch3_value_table_X[i,0] + lin_coeff[0,1]*ch3_value_table_X[i,1] + int_lin
    
    ##Plotting the pressure drop and flowrate area
    ##plt.plot(ch3_value_table_X[:, 0], ch3_value_table_X[:, 1], 'o')
    ##plt.show()
    ##Plotting the electricity consumption and flowrate area
    ##plt.plot(ch3_value_table_X[:, 0], ch3_value_table_Y[:, 0], 'o')
    ##plt.show()
    ##Plotting actual values and predicted values 
    ##plt.plot(calc_Y, ch3_value_table_Y, 'o')
    ##plt.show()
    ##plt.plot(ch3_value_table_X[:, 0], calc_Y, 'o')
    ##plt.show()
    
    ##Assembling the return values 
    ch3_evap_pump_m_coeff = lin_coeff[0,0]
    ch3_evap_pump_p_coeff = lin_coeff[0,1]
    ch3_evap_pump_cst = int_lin
    ch3_evap_pump_max_flow = ch3_eflow_max[0]
    ch3_evap_pump_regress_r2 = result
    
    ret_values = np.zeros((5,1))
    ret_values[0,0] = ch3_evap_pump_m_coeff
    ret_values[1,0] = ch3_evap_pump_p_coeff
    ret_values[2,0] = ch3_evap_pump_cst
    ret_values[3,0] = ch3_evap_pump_max_flow
    ret_values[4,0] = ch3_evap_pump_regress_r2
    
    return ret_values
    
def cond_pump_ch1 ():
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\add_ons\\')
    from convert_to_quadratic import convert_to_quadratic 
    from solve_quad_simul_eqns import solve_quad_simul_eqns
    from sklearn import linear_model 
    import numpy as np
    import matplotlib.pyplot as plt 
    
    ##Pump parameters, regarding pressure-drop
    pumpar1_c0 = -0.0000552287
    pumpar1_c1 = 0.0127459461
    pumpar1_c2 = 28.8570326545
    
    ##Pump parameters, regarding electricity consumption at the maximum rpm 
    pumpar1_e_c0 = 0
    pumpar1_e_c1 = -0.0000218828
    pumpar1_e_c2 = 0.0599176697
    pumpar1_e_c3 = 22.8337836011
    
    ##Network parameters 
    cond_network_A_val = 6.62983425414365E-07
    ch1_cond_A_val = 0.000133743 + cond_network_A_val
    
    ##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case 
    ch1_cond_x2_coeff, ch1_cond_x_coeff = convert_to_quadratic(ch1_cond_A_val)
    ##ch1_eflow_max[0] - maximum flowrate for this given combination 
    ch1_eflow_max = solve_quad_simul_eqns([ch1_cond_x2_coeff, ch1_cond_x_coeff, 0], [pumpar1_c0, pumpar1_c1, pumpar1_c2])
    ##The corresponding electricity consumption at the maximum flowrate and rpm is 
    ch1_e_max = pumpar1_e_c0*pow(ch1_eflow_max[0], 3) + pumpar1_e_c1*pow(ch1_eflow_max[0], 2) + pumpar1_e_c2*ch1_eflow_max[0] + pumpar1_e_c3
    ##From here onwards, variable speed of the pump will be assumed to linearly correlate with electrical consumption 
    ##We want to express E = A1m + A2p + cst, hence regression analysis is needed 
    ##To do that, we take 20 points for each of the flowrate interval for different pressure drops and electricity consumptions 
    delp_interval = 20 
    flowrate_interval = 50
    flowrate_step = ch1_eflow_max[0] / flowrate_interval 
    ##Initiate a matrix to hold all the values 
    ##Column 1 will be flowrate 
    ##Column 2 will be pressure drop 
    ##Column 3 will be electricity consumed 
    ch1_value_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
    ch1_value_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))

    for i in range (0, flowrate_interval+1):
        ##current flowrate 
        c_fr = i * flowrate_step 
        ##minimum pressure drop comes from the system curve 
        min_p = ch1_cond_x2_coeff*pow(c_fr, 2) + ch1_cond_x_coeff*c_fr
        ##maximum pressure drop comes from the pump curve 
        max_p = pumpar1_c0*pow(c_fr, 2) + pumpar1_c1*c_fr + pumpar1_c2
        ##minimum electricity consumption comes from the linear assumption curve 
        min_e = c_fr * (ch1_e_max / ch1_eflow_max[0])
        ##maximum electricity consumption comes from the electricity curve 
        max_e = pumpar1_e_c0*pow(c_fr, 3) + pumpar1_e_c1*pow(c_fr, 2) + pumpar1_e_c2*c_fr + pumpar1_e_c3
        ##recording the maximum and minimums 
        temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
        temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)

        for j in range (0, delp_interval):
            ch1_value_table_X[i*delp_interval+j, 0] = c_fr
            ch1_value_table_X[i*delp_interval+j, 1] = temp_pressure_rec[j]
            ch1_value_table_Y[i*delp_interval+j, 0] = temp_elec_rec[j]
    
    ##Performing regression analysis
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(ch1_value_table_X, ch1_value_table_Y)
    result = clf.score(ch1_value_table_X, ch1_value_table_Y, sample_weight=None)
    lin_coeff = clf.coef_
    int_lin = clf.intercept_  
      
    ##print(result)
    ##print(lin_coeff)
    ##print(int_lin)

    ##Evaluating the electricity consumption using linear combination model 
    calc_Y = np.zeros(((delp_interval*(flowrate_interval+1) ,1)))
    for i in range (0, delp_interval*(flowrate_interval+1)):
        calc_Y[i,0] = lin_coeff[0,0]*ch1_value_table_X[i,0] + lin_coeff[0,1]*ch1_value_table_X[i,1] + int_lin
    
    ##Plotting the pressure drop and flowrate area
    ##plt.plot(ch1_value_table_X[:, 0], ch1_value_table_X[:, 1], 'o')
    ##plt.show()
    ##Plotting the electricity consumption and flowrate area
    ##plt.plot(ch1_value_table_X[:, 0], ch1_value_table_Y[:, 0], 'o')
    ##plt.show()
    ##Plotting actual values and predicted values 
    ##plt.plot(calc_Y, ch1_value_table_Y, 'o')
    ##plt.show()
    ##plt.plot(ch1_value_table_X[:, 0], calc_Y, 'o')
    ##plt.show()
    
    ##Assembling the return values 
    ch1_cond_pump_m_coeff = lin_coeff[0,0]
    ch1_cond_pump_p_coeff = lin_coeff[0,1]
    ch1_cond_pump_cst = int_lin
    ch1_cond_pump_max_flow = ch1_eflow_max[0]
    ch1_cond_pump_regress_r2 = result
    
    ret_values = np.zeros((5,1))
    ret_values[0,0] = ch1_cond_pump_m_coeff
    ret_values[1,0] = ch1_cond_pump_p_coeff
    ret_values[2,0] = ch1_cond_pump_cst
    ret_values[3,0] = ch1_cond_pump_max_flow
    ret_values[4,0] = ch1_cond_pump_regress_r2

    return ret_values
    
def cond_pump_ch2 ():
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\add_ons\\')
    from convert_to_quadratic import convert_to_quadratic 
    from solve_quad_simul_eqns import solve_quad_simul_eqns
    from sklearn import linear_model 
    import numpy as np
    import matplotlib.pyplot as plt 
    
    ##Pump parameters, regarding pressure-drop
    pumpar2_c0 = -0.0000090818
    pumpar2_c1 = 0.0029568794
    pumpar2_c2 = 45.1880038403
    
    ##Pump parameters, regarding electricity consumption at the maximum rpm 
    pumpar2_e_c0 = 0
    pumpar2_e_c1 = -0.0000228942
    pumpar2_e_c2 = 0.0721558792
    pumpar2_e_c3 = 76.4863706961
    
    ##Network parameters 
    cond_network_A_val = 6.62983425414365E-07
    ch2_cond_A_val = 1.78251E-05 + cond_network_A_val
    
    ##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case 
    ch2_cond_x2_coeff, ch2_cond_x_coeff = convert_to_quadratic(ch2_cond_A_val)
    ##ch2_eflow_max[0] - maximum flowrate for this given combination 
    ch2_eflow_max = solve_quad_simul_eqns([ch2_cond_x2_coeff, ch2_cond_x_coeff, 0], [pumpar2_c0, pumpar2_c1, pumpar2_c2])
    ##The corresponding electricity consumption at the maximum flowrate and rpm is 
    ch2_e_max = pumpar2_e_c0*pow(ch2_eflow_max[0], 3) + pumpar2_e_c1*pow(ch2_eflow_max[0], 2) + pumpar2_e_c2*ch2_eflow_max[0] + pumpar2_e_c3
    ##From here onwards, variable speed of the pump will be assumed to linearly correlate with electrical consumption 
    ##We want to express E = A1m + A2p + cst, hence regression analysis is needed 
    ##To do that, we take 20 points for each of the flowrate interval for different pressure drops and electricity consumptions 
    delp_interval = 20 
    flowrate_interval = 50
    flowrate_step = ch2_eflow_max[0] / flowrate_interval 
    ##Initiate a matrix to hold all the values 
    ##Column 1 will be flowrate 
    ##Column 2 will be pressure drop 
    ##Column 3 will be electricity consumed 
    ch2_value_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
    ch2_value_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))

    for i in range (0, flowrate_interval+1):
        ##current flowrate 
        c_fr = i * flowrate_step 
        ##minimum pressure drop comes from the system curve 
        min_p = ch2_cond_x2_coeff*pow(c_fr, 2) + ch2_cond_x_coeff*c_fr
        ##maximum pressure drop comes from the pump curve 
        max_p = pumpar2_c0*pow(c_fr, 2) + pumpar2_c1*c_fr + pumpar2_c2
        ##minimum electricity consumption comes from the linear assumption curve 
        min_e = c_fr * (ch2_e_max / ch2_eflow_max[0])
        ##maximum electricity consumption comes from the electricity curve 
        max_e = pumpar2_e_c0*pow(c_fr, 3) + pumpar2_e_c1*pow(c_fr, 2) + pumpar2_e_c2*c_fr + pumpar2_e_c3
        ##recording the maximum and minimums 
        temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
        temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)

        for j in range (0, delp_interval):
            ch2_value_table_X[i*delp_interval+j, 0] = c_fr
            ch2_value_table_X[i*delp_interval+j, 1] = temp_pressure_rec[j]
            ch2_value_table_Y[i*delp_interval+j, 0] = temp_elec_rec[j]
    
    ##Performing regression analysis
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(ch2_value_table_X, ch2_value_table_Y)
    result = clf.score(ch2_value_table_X, ch2_value_table_Y, sample_weight=None)
    lin_coeff = clf.coef_
    int_lin = clf.intercept_  
      
    ##print(result)
    ##print(lin_coeff)
    ##print(int_lin)

    ##Evaluating the electricity consumption using linear combination model 
    calc_Y = np.zeros(((delp_interval*(flowrate_interval+1) ,1)))
    for i in range (0, delp_interval*(flowrate_interval+1)):
        calc_Y[i,0] = lin_coeff[0,0]*ch2_value_table_X[i,0] + lin_coeff[0,1]*ch2_value_table_X[i,1] + int_lin
    
    ##Plotting the pressure drop and flowrate area
    ##plt.plot(ch2_value_table_X[:, 0], ch2_value_table_X[:, 1], 'o')
    ##plt.show()
    ##Plotting the electricity consumption and flowrate area
    ##plt.plot(ch2_value_table_X[:, 0], ch2_value_table_Y[:, 0], 'o')
    ##plt.show()
    ##Plotting actual values and predicted values 
    ##plt.plot(calc_Y, ch2_value_table_Y, 'o')
    ##plt.show()
    ##plt.plot(ch2_value_table_X[:, 0], calc_Y, 'o')
    ##plt.show()
    
    ##Assembling the return values 
    ch2_cond_pump_m_coeff = lin_coeff[0,0]
    ch2_cond_pump_p_coeff = lin_coeff[0,1]
    ch2_cond_pump_cst = int_lin
    ch2_cond_pump_max_flow = ch2_eflow_max[0]
    ch2_cond_pump_regress_r2 = result
    
    ret_values = np.zeros((5,1))
    ret_values[0,0] = ch2_cond_pump_m_coeff
    ret_values[1,0] = ch2_cond_pump_p_coeff
    ret_values[2,0] = ch2_cond_pump_cst
    ret_values[3,0] = ch2_cond_pump_max_flow
    ret_values[4,0] = ch2_cond_pump_regress_r2
    
    return ret_values
    
def cond_pump_ch3 ():
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\add_ons\\')
    from convert_to_quadratic import convert_to_quadratic 
    from solve_quad_simul_eqns import solve_quad_simul_eqns
    from sklearn import linear_model 
    import numpy as np
    import matplotlib.pyplot as plt 
    
    ##Pump parameters, regarding pressure-drop
    pumpar3_c0 = -0.0000090818
    pumpar3_c1 = 0.0029568794
    pumpar3_c2 = 45.1880038403
    
    ##Pump parameters, regarding electricity consumption at the maximum rpm 
    pumpar3_e_c0 = 0
    pumpar3_e_c1 = -0.0000228942
    pumpar3_e_c2 = 0.0721558792
    pumpar3_e_c3 = 76.4863706961
    
    ##Network parameters 
    cond_network_A_val = 6.62983425414365E-07
    ch3_cond_A_val = 1.78251E-05 + cond_network_A_val
    
    ##Evaluating the intersection points for the pump and system curves for the lowest pressure drop case 
    ch3_cond_x2_coeff, ch3_cond_x_coeff = convert_to_quadratic(ch3_cond_A_val)
    ##ch3_eflow_max[0] - maximum flowrate for this given combination 
    ch3_eflow_max = solve_quad_simul_eqns([ch3_cond_x2_coeff, ch3_cond_x_coeff, 0], [pumpar3_c0, pumpar3_c1, pumpar3_c2])
    ##The corresponding electricity consumption at the maximum flowrate and rpm is 
    ch3_e_max = pumpar3_e_c0*pow(ch3_eflow_max[0], 3) + pumpar3_e_c1*pow(ch3_eflow_max[0], 2) + pumpar3_e_c2*ch3_eflow_max[0] + pumpar3_e_c3
    ##From here onwards, variable speed of the pump will be assumed to linearly correlate with electrical consumption 
    ##We want to express E = A1m + A2p + cst, hence regression analysis is needed 
    ##To do that, we take 20 points for each of the flowrate interval for different pressure drops and electricity consumptions 
    delp_interval = 20 
    flowrate_interval = 50
    flowrate_step = ch3_eflow_max[0] / flowrate_interval 
    ##Initiate a matrix to hold all the values 
    ##Column 1 will be flowrate 
    ##Column 2 will be pressure drop 
    ##Column 3 will be electricity consumed 
    ch3_value_table_X = np.zeros((delp_interval*(flowrate_interval+1) ,2))
    ch3_value_table_Y = np.zeros((delp_interval*(flowrate_interval+1) ,1))

    for i in range (0, flowrate_interval+1):
        ##current flowrate 
        c_fr = i * flowrate_step 
        ##minimum pressure drop comes from the system curve 
        min_p = ch3_cond_x2_coeff*pow(c_fr, 2) + ch3_cond_x_coeff*c_fr
        ##maximum pressure drop comes from the pump curve 
        max_p = pumpar3_c0*pow(c_fr, 2) + pumpar3_c1*c_fr + pumpar3_c2
        ##minimum electricity consumption comes from the linear assumption curve 
        min_e = c_fr * (ch3_e_max / ch3_eflow_max[0])
        ##maximum electricity consumption comes from the electricity curve 
        max_e = pumpar3_e_c0*pow(c_fr, 3) + pumpar3_e_c1*pow(c_fr, 2) + pumpar3_e_c2*c_fr + pumpar3_e_c3
        ##recording the maximum and minimums 
        temp_pressure_rec = np.linspace(min_p, max_p, delp_interval, endpoint = True)
        temp_elec_rec = np.linspace(min_e, max_e, delp_interval, endpoint = True)

        for j in range (0, delp_interval):
            ch3_value_table_X[i*delp_interval+j, 0] = c_fr
            ch3_value_table_X[i*delp_interval+j, 1] = temp_pressure_rec[j]
            ch3_value_table_Y[i*delp_interval+j, 0] = temp_elec_rec[j]
    
    ##Performing regression analysis
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(ch3_value_table_X, ch3_value_table_Y)
    result = clf.score(ch3_value_table_X, ch3_value_table_Y, sample_weight=None)
    lin_coeff = clf.coef_
    int_lin = clf.intercept_  
      
    ##print(result)
    ##print(lin_coeff)
    ##print(int_lin)

    ##Evaluating the electricity consumption using linear combination model 
    calc_Y = np.zeros(((delp_interval*(flowrate_interval+1) ,1)))
    for i in range (0, delp_interval*(flowrate_interval+1)):
        calc_Y[i,0] = lin_coeff[0,0]*ch3_value_table_X[i,0] + lin_coeff[0,1]*ch3_value_table_X[i,1] + int_lin
    
    ##Plotting the pressure drop and flowrate area
    ##plt.plot(ch3_value_table_X[:, 0], ch3_value_table_X[:, 1], 'o')
    ##plt.show()
    ##Plotting the electricity consumption and flowrate area
    ##plt.plot(ch3_value_table_X[:, 0], ch3_value_table_Y[:, 0], 'o')
    ##plt.show()
    ##Plotting actual values and predicted values 
    ##plt.plot(calc_Y, ch3_value_table_Y, 'o')
    ##plt.show()
    ##plt.plot(ch3_value_table_X[:, 0], calc_Y, 'o')
    ##plt.show()
    
    ##Assembling the return values 
    ch3_cond_pump_m_coeff = lin_coeff[0,0]
    ch3_cond_pump_p_coeff = lin_coeff[0,1]
    ch3_cond_pump_cst = int_lin
    ch3_cond_pump_max_flow = ch3_eflow_max[0]
    ch3_cond_pump_regress_r2 = result
    
    ret_values = np.zeros((5,1))
    ret_values[0,0] = ch3_cond_pump_m_coeff
    ret_values[1,0] = ch3_cond_pump_p_coeff
    ret_values[2,0] = ch3_cond_pump_cst
    ret_values[3,0] = ch3_cond_pump_max_flow
    ret_values[4,0] = ch3_cond_pump_regress_r2

    return ret_values 

cond_pump_ch1 ()
cond_pump_ch2 ()