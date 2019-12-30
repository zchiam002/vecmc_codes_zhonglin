##This function enumerates all possible parameters of the system curves for the distribution network 

def dist_nwk_lower_limits_model ():
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\slave_convex_v1\\add_ons\\')
    from convert_to_quadratic import convert_to_quadratic 
    from sklearn import linear_model
    import numpy as np 
    import pandas as pd 
    import matplotlib.pyplot as plt 
    
    ##First we need to determine the pressure drop coefficients of the composite systems curves for the lowest delta p configuration
    ##That is when all of the valves are open 
    
    ##Choice 0 - all parallel networks are served by their own pumps 
    ##Choice 1 - ice and tro share pumps, fir served by its own pump 
    ##Choice 2 - ice served by its own pump, tro and fir share pumps
    ##Choice 3 - ice, tro and fir all share pumps 
    
    ##Initiate a DataFrame to store all the results 
    lowest_deltap_results = pd.DataFrame(columns = ['Choice', 'Network_gv2', 'Network_hsb', 'Network_pfa', 'Network_ser', 'Network_fir', 'x2_coeff', 'x_coeff'])
    
    ##Individual network pressure drop coefficients, they are all determined in the form of delp = A*m^1.852 
    ice_main_coeff = 0.00011627906976743445
    gv2_coeff = 0.00034883720930232456
    hsb_coeff = 0.05046511627906977
    tro_main_coeff = 0.001162790697674419
    pfa_coeff = 0.0029069767441860417
    ser_coeff = 0.00023255813953487953
    fir_coeff = 0.005697674418604649
    
    ##########################################################################################################################################################
    ##########################################################################################################################################################
    
    ##Choice 0 lowest pressure drop cases
    ##For the ice pump
    ##The maximum flowrate is set to 3200 m3/h
    
    ##Expressing hsb flowrate in terms of gv2 flowrate
    mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
    ##Expressing total flowrate as a function as gv2 flowrate
    mgv2_intermsof_mice_coeff = 1 + mhsb_intermsof_mgv2_coeff
    
    max_flow = 3200
    num_steps = 100
    flow_interval = max_flow / num_steps 
    temp_record_X = np.zeros((num_steps+1, 2))
    temp_record_Y = np.zeros((num_steps+1, 1))
    
    for i in range (0, num_steps+1):
        flow = i * flow_interval 
        gv2_flow = flow / mgv2_intermsof_mice_coeff
        pressure = ice_main_coeff*pow(flow, 1.852) +  gv2_coeff*pow(gv2_flow, 1.852)
        temp_record_X[i,0] = flow
        temp_record_X[i,1] = pow(flow, 2)
        temp_record_Y[i,0] = pressure 
    
    ##Finding the quadratic relationship between the lowest case presure drop for the ice network
    clf = linear_model.LinearRegression(fit_intercept = False)
    clf.fit(temp_record_X, temp_record_Y)
    result = clf.score(temp_record_X, temp_record_Y, sample_weight=None)
    quad_coeff = clf.coef_
    intercept = clf.intercept_
    
    choice = 0
    nwk_gv2 = 1
    nwk_hsb = 1
    nwk_pfa = 0
    nwk_ser = 0
    nwk_fir = 0
    x2_coeff = quad_coeff[0,1]
    x_coeff = quad_coeff[0,0]
    data_temp = [choice, nwk_gv2, nwk_hsb, nwk_pfa, nwk_ser, nwk_fir, x2_coeff, x_coeff]
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Choice', 'Network_gv2', 'Network_hsb', 'Network_pfa', 'Network_ser', 'Network_fir', 'x2_coeff', 'x_coeff'])
    lowest_deltap_results = lowest_deltap_results.append(data_temp_df, ignore_index=True)
    
    
    ##For the tro pump
    ##The maximum flowrate is set to 3200 m3/h
    ##Expressing ser flowrate in terms of pfa flowrate 
    mser_intermsof_mpfa_coeff = pow(pfa_coeff / ser_coeff, 1/1.852)
    ##Expressing total flowrate as a function as pfa flowrate
    mpfa_intermsof_mtro_coeff = 1 + mser_intermsof_mpfa_coeff
    
    max_flow = 3200
    num_steps = 100
    flow_interval = max_flow / num_steps 
    temp_record_X = np.zeros((num_steps+1, 2))
    temp_record_Y = np.zeros((num_steps+1, 1))
    
    for i in range (0, num_steps+1):
        flow = i * flow_interval 
        pfa_flow = flow / mpfa_intermsof_mtro_coeff
        pressure = tro_main_coeff*pow(flow, 1.852) +  pfa_coeff*pow(pfa_flow, 1.852)
        temp_record_X[i,0] = flow
        temp_record_X[i,1] = pow(flow, 2)
        temp_record_Y[i,0] = pressure 
    
    ##Finding the quadratic relationship between the lowest case presure drop for the tro network
    clf = linear_model.LinearRegression(fit_intercept = False)
    clf.fit(temp_record_X, temp_record_Y)
    result = clf.score(temp_record_X, temp_record_Y, sample_weight=None)
    quad_coeff = clf.coef_
    intercept = clf.intercept_
    
    choice = 0
    nwk_gv2 = 0
    nwk_hsb = 0
    nwk_pfa = 1
    nwk_ser = 1
    nwk_fir = 0
    x2_coeff = quad_coeff[0,1]
    x_coeff = quad_coeff[0,0]
    data_temp = [choice, nwk_gv2, nwk_hsb, nwk_pfa, nwk_ser, nwk_fir, x2_coeff, x_coeff]
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Choice', 'Network_gv2', 'Network_hsb', 'Network_pfa', 'Network_ser', 'Network_fir', 'x2_coeff', 'x_coeff'])
    lowest_deltap_results = lowest_deltap_results.append(data_temp_df, ignore_index=True)
    
    ##For the fir pump
    ##The maximum flowrate is set to 3200 m3/h
    ##Since this is a single circuit, just convert the single power into quadratic form
    
    coeff_x2, coeff_x = convert_to_quadratic(fir_coeff)
    
    choice = 0
    nwk_gv2 = 0
    nwk_hsb = 0
    nwk_pfa = 0
    nwk_ser = 0
    nwk_fir = 1
    x2_coeff = coeff_x2
    x_coeff = coeff_x
    data_temp = [choice, nwk_gv2, nwk_hsb, nwk_pfa, nwk_ser, nwk_fir, x2_coeff, x_coeff]
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Choice', 'Network_gv2', 'Network_hsb', 'Network_pfa', 'Network_ser', 'Network_fir', 'x2_coeff', 'x_coeff'])
    lowest_deltap_results = lowest_deltap_results.append(data_temp_df, ignore_index=True)
    
    ##########################################################################################################################################################
    ##########################################################################################################################################################
    
    ##Choice 1 lowest pressure drop cases
    ##For the ice and tro pump 
    ##The maximum flowrate is set to 3200 m3/h
    
    ##Expressing hsb flowrate in terms of gv2 flowrate
    mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
    ##Expressing pfa flowrate in terms of gv2 flowrate 
    term1 = pow(gv2_coeff/hsb_coeff, 1/1.852)
    term2 = ice_main_coeff*pow(1 + term1, 1.852) + gv2_coeff
    term3 = pow(pfa_coeff/ser_coeff, 1/1.852)
    term4 = tro_main_coeff*pow(1 + term3, 1.852) + pfa_coeff
    mpfa_intermaof_mgv2_coeff = pow(term2/term4, 1/1.852)
    ##Expressing ser flowrate in terms of gv2 flowrate 
    term5 = pow(ser_coeff/pfa_coeff, 1/1.852)
    term6 = tro_main_coeff*pow(1 + term5, 1.852) + ser_coeff
    mser_intermsof_mgv2_coeff = pow(term2/term6, 1/1.852)
    ##Expressing total flowrate as a function as gv2 flowrate
    mgv2_intermsof_miceandmtro_coeff = 1 + mhsb_intermsof_mgv2_coeff + mpfa_intermaof_mgv2_coeff + mser_intermsof_mgv2_coeff
    
    max_flow = 3200
    num_steps = 100
    flow_interval = max_flow / num_steps 
    temp_record_X = np.zeros((num_steps+1, 2))
    temp_record_Y = np.zeros((num_steps+1, 1))
    
    for i in range (0, num_steps+1):
        flow = i * flow_interval 
        gv2_flow = flow / mgv2_intermsof_miceandmtro_coeff
        ice_flow = gv2_flow + mhsb_intermsof_mgv2_coeff*gv2_flow
        pressure = ice_main_coeff*pow(ice_flow, 1.852) +  gv2_coeff*pow(gv2_flow, 1.852)
        temp_record_X[i,0] = flow
        temp_record_X[i,1] = pow(flow, 2)
        temp_record_Y[i,0] = pressure 
    
    ##Finding the quadratic relationship between the lowest case presure drop for the ice and tro network
    clf = linear_model.LinearRegression(fit_intercept = False)
    clf.fit(temp_record_X, temp_record_Y)
    result = clf.score(temp_record_X, temp_record_Y, sample_weight=None)
    quad_coeff = clf.coef_
    intercept = clf.intercept_
    
    choice = 1
    nwk_gv2 = 1
    nwk_hsb = 1
    nwk_pfa = 1
    nwk_ser = 1
    nwk_fir = 0
    x2_coeff = quad_coeff[0,1]
    x_coeff = quad_coeff[0,0]
    data_temp = [choice, nwk_gv2, nwk_hsb, nwk_pfa, nwk_ser, nwk_fir, x2_coeff, x_coeff]
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Choice', 'Network_gv2', 'Network_hsb', 'Network_pfa', 'Network_ser', 'Network_fir', 'x2_coeff', 'x_coeff'])
    lowest_deltap_results = lowest_deltap_results.append(data_temp_df, ignore_index=True)
    
    ##For the fir pump
    ##The maximum flowrate is set to 3200 m3/h
    ##Since this is a single circuit, just convert the single power into quadratic form
    
    coeff_x2, coeff_x = convert_to_quadratic(fir_coeff)
    
    choice = 1
    nwk_gv2 = 0
    nwk_hsb = 0
    nwk_pfa = 0
    nwk_ser = 0
    nwk_fir = 1
    x2_coeff = coeff_x2
    x_coeff = coeff_x
    data_temp = [choice, nwk_gv2, nwk_hsb, nwk_pfa, nwk_ser, nwk_fir, x2_coeff, x_coeff]
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Choice', 'Network_gv2', 'Network_hsb', 'Network_pfa', 'Network_ser', 'Network_fir', 'x2_coeff', 'x_coeff'])
    lowest_deltap_results = lowest_deltap_results.append(data_temp_df, ignore_index=True)
    
    ##########################################################################################################################################################
    ##########################################################################################################################################################
    
    ##Choice 2 lowest pressure drop cases
    ##For the ice pump
    ##The maximum flowrate is set to 3200 m3/h
    
    ##Expressing hsb flowrate in terms of gv2 flowrate
    mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
    ##Expressing total flowrate as a function as gv2 flowrate
    mgv2_intermsof_mice_coeff = 1 + mhsb_intermsof_mgv2_coeff
    
    max_flow = 3200
    num_steps = 100
    flow_interval = max_flow / num_steps 
    temp_record_X = np.zeros((num_steps+1, 2))
    temp_record_Y = np.zeros((num_steps+1, 1))
    
    for i in range (0, num_steps+1):
        flow = i * flow_interval 
        gv2_flow = flow / mgv2_intermsof_mice_coeff
        pressure = ice_main_coeff*pow(flow, 1.852) +  gv2_coeff*pow(gv2_flow, 1.852)
        temp_record_X[i,0] = flow
        temp_record_X[i,1] = pow(flow, 2)
        temp_record_Y[i,0] = pressure 
    
    ##Finding the quadratic relationship between the lowest case presure drop for the ice network
    clf = linear_model.LinearRegression(fit_intercept = False)
    clf.fit(temp_record_X, temp_record_Y)
    result = clf.score(temp_record_X, temp_record_Y, sample_weight=None)
    quad_coeff = clf.coef_
    intercept = clf.intercept_
    
    choice = 2
    nwk_gv2 = 1
    nwk_hsb = 1
    nwk_pfa = 0
    nwk_ser = 0
    nwk_fir = 0
    x2_coeff = quad_coeff[0,1]
    x_coeff = quad_coeff[0,0]
    data_temp = [choice, nwk_gv2, nwk_hsb, nwk_pfa, nwk_ser, nwk_fir, x2_coeff, x_coeff]
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Choice', 'Network_gv2', 'Network_hsb', 'Network_pfa', 'Network_ser', 'Network_fir', 'x2_coeff', 'x_coeff'])
    lowest_deltap_results = lowest_deltap_results.append(data_temp_df, ignore_index=True)
    
    ##For the tro and fir pump 
    ##The maximum flowrate is set to 3200 m3/h
    
    ##Expresing ser flowrate in terms of pfa flowrate 
    mser_intermsof_mpfa_coeff = pow(pfa_coeff / ser_coeff, 1/1.852)
    ##Expressing fir flowrate in terms of pfa flowrate 
    term1 = pow(pfa_coeff/ser_coeff, 1/1.852)
    term2 = tro_main_coeff*pow(1 + term1, 1.852) + pfa_coeff
    mfir_intermsof_mpfa_coeff = pow(term2/fir_coeff, 1/1.852)
    ##Expressing total flowrate as a function of pfa flowrate 
    mtrofir_intermsof_mpfa_coeff = 1 + mser_intermsof_mpfa_coeff + mfir_intermsof_mpfa_coeff
    
    max_flow = 3200
    num_steps = 100
    flow_interval = max_flow / num_steps 
    temp_record_X = np.zeros((num_steps+1, 2))
    temp_record_Y = np.zeros((num_steps+1, 1))
    
    for i in range (0, num_steps+1):
        flow = i * flow_interval 
        pfa_flow = flow / mtrofir_intermsof_mpfa_coeff
        ser_flow = pfa_flow * mser_intermsof_mpfa_coeff
        tro_flow = pfa_flow + ser_flow  
        pressure = tro_main_coeff*pow(tro_flow, 1.852) +  pfa_coeff*pow(pfa_flow, 1.852)
        temp_record_X[i,0] = flow
        temp_record_X[i,1] = pow(flow, 2)
        temp_record_Y[i,0] = pressure 
    
    ##Finding the quadratic relationship between the lowest case presure drop for the ice network
    clf = linear_model.LinearRegression(fit_intercept = False)
    clf.fit(temp_record_X, temp_record_Y)
    result = clf.score(temp_record_X, temp_record_Y, sample_weight=None)
    quad_coeff = clf.coef_
    intercept = clf.intercept_
    
    choice = 2
    nwk_gv2 = 0
    nwk_hsb = 0
    nwk_pfa = 1
    nwk_ser = 1
    nwk_fir = 1
    x2_coeff = quad_coeff[0,1]
    x_coeff = quad_coeff[0,0]
    data_temp = [choice, nwk_gv2, nwk_hsb, nwk_pfa, nwk_ser, nwk_fir, x2_coeff, x_coeff]
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Choice', 'Network_gv2', 'Network_hsb', 'Network_pfa', 'Network_ser', 'Network_fir', 'x2_coeff', 'x_coeff'])
    lowest_deltap_results = lowest_deltap_results.append(data_temp_df, ignore_index=True)
    
    ##########################################################################################################################################################
    ##########################################################################################################################################################
    
    ##Choice 3 lowest pressure drop cases
    ##For the ice, tro and fir pump
    ##The maximum flowrate is set to 3200 m3/h
    
    ##Expresing hsb flowrate in terms of gv2 flowrate
    mhsb_intermsof_mgv2_coeff = pow(gv2_coeff / hsb_coeff, 1/1.852)
    ##Expressing pfa flowrate in terms of gv2 flowrate 
    term1 = pow(gv2_coeff/hsb_coeff, 1/1.852)
    term2 = ice_main_coeff*pow(1 + term1, 1.852) + gv2_coeff
    term3 = pow(pfa_coeff/ser_coeff, 1/1.852)
    term4 = tro_main_coeff*pow(1 + term3, 1.852) + pfa_coeff
    mpfa_intermaof_mgv2_coeff = pow(term2/term4, 1/1.852)
    ##Expressing ser flowrate in terms of gv2 flowrate 
    term5 = pow(ser_coeff/pfa_coeff, 1/1.852)
    term6 = tro_main_coeff*pow(1 + term5, 1.852) + ser_coeff
    mser_intermsof_mgv2_coeff = pow(term2/term6, 1/1.852)
    ##Expressing fir flowrate in terms of gv2 flowrate 
    term7 = pow(gv2_coeff/hsb_coeff, 1/1.852)
    term8 = ice_main_coeff*pow(1 + term7, 1.852) + gv2_coeff
    mfir_intermsof_mgv2_coeff = pow(term8/fir_coeff, 1/1.852)
    ##Expressing total flowrate as a function of gv2 flowrate
    micetrofir_intermsof_mgv2_coeff = 1 + mhsb_intermsof_mgv2_coeff + mpfa_intermaof_mgv2_coeff + mser_intermsof_mgv2_coeff + mfir_intermsof_mgv2_coeff
    
    max_flow = 3200
    num_steps = 100
    flow_interval = max_flow / num_steps 
    temp_record_X = np.zeros((num_steps+1, 2))
    temp_record_Y = np.zeros((num_steps+1, 1))
    
    for i in range (0, num_steps+1):
        flow = i * flow_interval 
        gv2_flow = flow / micetrofir_intermsof_mgv2_coeff
        hsb_flow = gv2_flow * mhsb_intermsof_mgv2_coeff
        ice_flow = gv2_flow + hsb_flow
        pressure = ice_main_coeff*pow(ice_flow, 1.852) +  gv2_coeff*pow(gv2_flow, 1.852)
        temp_record_X[i,0] = flow
        temp_record_X[i,1] = pow(flow, 2)
        temp_record_Y[i,0] = pressure 
    
    ##Finding the quadratic relationship between the lowest case presure drop for the ice network
    clf = linear_model.LinearRegression(fit_intercept = False)
    clf.fit(temp_record_X, temp_record_Y)
    result = clf.score(temp_record_X, temp_record_Y, sample_weight=None)
    quad_coeff = clf.coef_
    intercept = clf.intercept_
    
    choice = 3
    nwk_gv2 = 1
    nwk_hsb = 1
    nwk_pfa = 1
    nwk_ser = 1
    nwk_fir = 1
    x2_coeff = quad_coeff[0,1]
    x_coeff = quad_coeff[0,0]
    data_temp = [choice, nwk_gv2, nwk_hsb, nwk_pfa, nwk_ser, nwk_fir, x2_coeff, x_coeff]
    data_temp_df = pd.DataFrame(data = [data_temp], columns = ['Choice', 'Network_gv2', 'Network_hsb', 'Network_pfa', 'Network_ser', 'Network_fir', 'x2_coeff', 'x_coeff'])
    lowest_deltap_results = lowest_deltap_results.append(data_temp_df, ignore_index=True)
    
    return lowest_deltap_results

