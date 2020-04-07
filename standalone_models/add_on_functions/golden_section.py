##This is the golden section function 

def golden_section_dist (func, func_bounds, sys_coeff, pump_coeffs):
    
    import sys 
    
    ##func contains the function which will evaluate the dependent variable
    ##func_bounds determine the maximum and minimum values of inputs into the function func 
    
    ##func[0] --- lb of the independent variable 
    ##func[1] --- ub of the independent variable 
    
    ##sys_coeff --- system presure drop coefficient 
    ##pump_coeffs --- the pump delp coefficients 
    
    gr = ((pow(5, 0.5)) - 1) / 2
    iteration = 0
    d = gr * (func_bounds[1] - func_bounds[0])
    x1 = func_bounds[0] + d
    x2 = func_bounds[1] - d

    xl = func_bounds[0]
    xu = func_bounds[1]

    eps = sys.float_info.epsilon

    while (abs(abs(xu)- abs(xl))) > 0.0001:
        
        iteration = iteration + 1
        fx1 = func(sys_coeff, pump_coeffs, x1)
        fx2 = func(sys_coeff, pump_coeffs, x2)
        
        if fx1 < fx2:
            xl = x2
            x2 = x1
            d = gr * (xu - xl)
            x1 = xl + d
            
        else:
            
            xu = x1
            x1 = x2
            d = gr * (xu - xl)
            x2 = xu - d

    value = (xl + xu) / 2
    
    return value 
    
def golden_section_evap_cond (func, func_bounds, sys_coeff, pump_coeffs, sys_offset):
    
    import sys 
    
    ##func contains the function which will evaluate the dependent variable
    ##func_bounds determine the maximum and minimum values of inputs into the function func 
    
    ##func[0] --- lb of the independent variable 
    ##func[1] --- ub of the independent variable 
    
    ##sys_coeff --- system presure drop coefficient 
    ##pump_coeffs --- the pump delp coefficients 
    ##sys_offset --- the extra pressure component of the systems 
    
    gr = ((pow(5, 0.5)) - 1) / 2
    iteration = 0
    d = gr * (func_bounds[1] - func_bounds[0])
    x1 = func_bounds[0] + d
    x2 = func_bounds[1] - d

    xl = func_bounds[0]
    xu = func_bounds[1]

    eps = sys.float_info.epsilon

    while (abs(abs(xu)- abs(xl))) > 0.0001:
        
        iteration = iteration + 1
        fx1 = func(sys_coeff, pump_coeffs, sys_offset, x1)
        fx2 = func(sys_coeff, pump_coeffs, sys_offset, x2)
        
        if fx1 < fx2:
            xl = x2
            x2 = x1
            d = gr * (xu - xl)
            x1 = xl + d
            
        else:
            
            xu = x1
            x1 = x2
            d = gr * (xu - xl)
            x2 = xu - d

    value = (xl + xu) / 2
    
    return value 
    
def golden_section_evap_cond_regress (func, func_bounds, sys_coeff, pump_coeffs):
    
    import sys 
    
    ##func contains the function which will evaluate the dependent variable
    ##func_bounds determine the maximum and minimum values of inputs into the function func 
    
    ##func[0] --- lb of the independent variable 
    ##func[1] --- ub of the independent variable 
    
    ##sys_coeff --- system presure drop coefficient 
    ##pump_coeffs --- the pump delp coefficients 
    
    gr = ((pow(5, 0.5)) - 1) / 2
    iteration = 0
    d = gr * (func_bounds[1] - func_bounds[0])
    x1 = func_bounds[0] + d
    x2 = func_bounds[1] - d

    xl = func_bounds[0]
    xu = func_bounds[1]

    eps = sys.float_info.epsilon

    while (abs(abs(xu)- abs(xl))) > 0.0001:
        
        iteration = iteration + 1
        fx1 = func(sys_coeff, pump_coeffs, x1)
        fx2 = func(sys_coeff, pump_coeffs, x2)
        
        if fx1 < fx2:
            xl = x2
            x2 = x1
            d = gr * (xu - xl)
            x1 = xl + d
            
        else:
            
            xu = x1
            x1 = x2
            d = gr * (xu - xl)
            x2 = xu - d

    value = (xl + xu) / 2
    
    return value 