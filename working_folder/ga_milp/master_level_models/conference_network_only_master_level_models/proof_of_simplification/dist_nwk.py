##This is script contains functions which calculate the relevant values required for pumps 

def dist_nwk_system_bounds ():
    ##The coefficients of the network branches associated with pressure drop, for simplicity they are expressed in the form of 
    ##delp = A * pow(m, 1.852)
    ##The function then returns the upper and lower bounds of the system curve in their respective quadratic forms 
    
    from convert_to_quadratic import convert_to_quadratic
    
    A1_2 = 0.00011627906976743445
    A1 = 0.00034883720930232456
    A2 = 0.05046511627906977
    A3_4 = 0.001162790697674419
    A3 = 0.0029069767441860417
    A4 = 0.00023255813953487953
    A5 = 0.005697674418604649
    
    ##Forming ratio of other flowrates as that of m1, when all the valves are fully open 
    
    m2_coeff = pow(A1 / A2,1 / 1.852)
    
    m3_numer_1 = 1 + pow(A1 / A2, 1 / 1.852)
    m3_numer = (A1_2 * pow(m3_numer_1, 1.852)) + A1
    m3_denom_1 = 1 + pow(A3 / A4, 1 / 1.852)
    m3_denom = (A3_4 * pow(m3_denom_1, 1.852)) + A3
    m3_coeff = pow(m3_numer / m3_denom, 1 / 1.852)
    
    m4_numer_1 = 1 + pow(A1 / A2, 1 / 1.852)
    m4_numer = (A1_2 * pow(m4_numer_1, 1.852)) + A1
    m4_denom_1 = 1 + pow(A4 / A3, 1 / 1.852)
    m4_denom = (A3_4 * pow(m4_denom_1, 1.852)) + A4
    m4_coeff = pow(m4_numer / m4_denom, 1 / 1.852)
    
    m5_numer_1 = 1 + pow(A1 / A2, 1 / 1.852)
    m5_numer = (A1_2 * pow(m5_numer_1, 1.852)) + A1
    m5_denom = A5
    m5_coeff = pow(m5_numer / m5_denom, 1 / 1.852)
    
    ##Since the delta p in all parallel branches need to be equal, A1*pow(m1,1.852) = A_new*pow(m_total,1.852)
    ##Hence, the following is a new step to find A_new_lower
    
    A_new_lower_denom_1 = 1 + m2_coeff + m3_coeff + m4_coeff + m5_coeff 
    A_new_lower_denom = pow(A_new_lower_denom_1, 1.852)
    A_new_lower = A1 / A_new_lower_denom 
    
    ##The upper limit of the pressure drop occurs when all but 1 valve corresponding to the branch with the highest pressure
    ##drop coefficient 
    
    ##The obvious highest pressure drop is that of the HSB branch 
    
    B2 = A1_2 + A2
    
    A_new_upper = B2
    
    ##Regression analysis to return them in the respective quadratic forms 
    Al_2, Al_1 = convert_to_quadratic(A_new_lower)
    Au_2, Au_1 = convert_to_quadratic(A_new_upper)
    
    return Al_2, Al_1, Au_2, Au_1
    
