##This model handles the evaporator network 

def evap_network(evap_flow_ratio, evap_total_flow):
    import numpy as np
    from evap_network_coeff import evap_network_coeff 
    from convert_to_quadratic import convert_to_quadratic 
    from evap_pump_data import evap_pump_data 
    from solve_quad_simul_eqns import solve_quad_simul_eqns 
    
    ##evap_flow_ratio[0] --- ch1 flow ratio
    ##evap_flow_ratio[1] --- ch2 flow ratio
    ##evap_flow_ratio[2] --- ch3 flow ratio
    
    ##Retrieving the singular coefficient approximation 
    ch1_evap_coeff, ch2_evap_coeff, ch3_evap_coeff = evap_network_coeff(evap_flow_ratio, evap_total_flow)
    sys_curve = np.zeros((3,3))
    
    ##Converting into quadratic form 
    x_2, x = convert_to_quadratic(ch1_evap_coeff)
    sys_curve[0,0] = x_2
    sys_curve[0,1] = x
    
    x_2, x = convert_to_quadratic(ch2_evap_coeff)
    sys_curve[1,0] = x_2
    sys_curve[1,1] = x

    x_2, x = convert_to_quadratic(ch3_evap_coeff)
    sys_curve[2,0] = x_2
    sys_curve[2,1] = x

    ##Gathering the relevant information for the selected pumps
    pump_curve_data, pump_power_data = evap_pump_data()
    
    ##Finding the intersection point for each of the pump and system curves 
    int_point = np.zeros((3,2))##Flow(m3/h), Head(mH2O)
    
    for i in range (0,3):
        D = solve_quad_simul_eqns(pump_curve_data[i,:],sys_curve[i,:])
        int_point[i,0] = D[0]
        int_point[i,1] = D[1]      

    ##Finding the maximum power consumption of each pump
    max_power = np.zeros((3,1))
    
    for i in range (0,3):
        flow = int_point[i,0]
        max_power[i] = (pump_power_data[i,0]*pow(flow,3)) + (pump_power_data[i,1]*pow(flow,2)) + (pump_power_data[i,2]*flow) + pump_power_data[i,3]

    ##Evaluate the power consumption 
    flow = np.zeros((3,1))
    flow[0,0] = evap_flow_ratio[0] * evap_total_flow
    flow[1,0] = evap_flow_ratio[1] * evap_total_flow
    flow[2,0] = evap_flow_ratio[2] * evap_total_flow

    power = 0
    for i in range (0,3):
        power = power + ((flow[i,0]/int_point[i,0])*max_power[i])
                
    ##Check for flowrate feasibility
    feasibility = 1
    for i in range (0,3):
        if flow[i,0] > int_point[i,0]:
            feasibility = 0
            break        
        
    return feasibility, power