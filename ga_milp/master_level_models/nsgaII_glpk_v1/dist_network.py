##This model handles the distribution network 

def dist_network(select, perc_split, total_flow, dist_pump):
    import numpy as np
    from dist_network_coeff import dist_network_coeff
    from convert_to_quadratic import convert_to_quadratic 
    from dist_pump_data import dist_pump_data 
    from solve_quad_simul_eqns import solve_quad_simul_eqns
    
    ##select[0] --- dist_option1
    ##select[1] --- dist_option2
    ##select[2] --- dist_option3
    ##select[3] --- dist_option4
    
    ##perc_split[0] --- split_cp
    ##perc_split[1] --- split_gv2   
    ##perc_split[2] --- split_hsb
    ##perc_split[3] --- split_pfa
    ##perc_split[4] --- split_ser
    ##perc_split[5] --- split_fir
    
    ##dist_pump -- allocation of pumps for the distribution network 
    
    
    if select[0] == 1:
            
        ##Retrieving the singular coefficient approximation
        ice_coeff, tro_coeff, fir_coeff = dist_network_coeff(select, perc_split, total_flow)
        sys_curve = np.zeros((3,3))
        
        ##Converting into quadratic form 
        x_2, x = convert_to_quadratic(ice_coeff)
        sys_curve[0,0] = x_2
        sys_curve[0,1] = x
        
        x_2, x = convert_to_quadratic(tro_coeff)
        sys_curve[1,0] = x_2
        sys_curve[1,1] = x
        
        x_2, x = convert_to_quadratic(fir_coeff)
        sys_curve[2,0] = x_2
        sys_curve[2,1] = x
        
        ##Gathering the relevant information for the selected pumps 
        pump_curve_data, pump_power_data = dist_pump_data(dist_pump)
        
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
            max_power[i] = (pump_power_data[i,0]*pow(flow,2)) + (pump_power_data[i,1]*flow) + pump_power_data[i,2]
        
        ##Evaluate the power consumption
        flow = np.zeros((3,1))
        flow[0,0] = (perc_split[1] + perc_split[2]) * total_flow
        flow[1,0] = (perc_split[3] + perc_split[4]) * total_flow
        flow[2,0] = perc_split[5] * total_flow
        
        power = 0
        for i in range (0,3):
            power = power + ((flow[i,0]/int_point[i,0])*max_power[i])
                    
        ##Check for flowrate feasibility
        feasibility = 1
        for i in range (0,3):
            if flow[i,0] > int_point[i,0]:
                feasibility = 0
                break
            
    elif select[1] == 1:

        ##Retrieving the singular coefficient approximation
        icetro_coeff, fir_coeff = dist_network_coeff(select, perc_split, total_flow)
        sys_curve = np.zeros((2,3))

        ##Converting into quadratic form             
        x_2, x = convert_to_quadratic(icetro_coeff)
        sys_curve[0,0] = x_2
        sys_curve[0,1] = x

        x_2, x = convert_to_quadratic(fir_coeff)
        sys_curve[1,0] = x_2
        sys_curve[1,1] = x 

        ##Gathering the relevant information for the selected pumps 
        pump_curve_data, pump_power_data = dist_pump_data(dist_pump)
        
        ##Finding the intersection point for each of the pump and system curves 
        int_point = np.zeros((2,2))##Flow(m3/h), Head(mH2O)
        
        for i in range (0,2):
            D = solve_quad_simul_eqns(pump_curve_data[i,:],sys_curve[i,:])
            int_point[i,0] = D[0]
            int_point[i,1] = D[1]
        
        ##Finding the maximum power consumption of each pump
        max_power = np.zeros((2,1))
        
        for i in range (0,2):
            flow = int_point[i,0]
            max_power[i] = (pump_power_data[i,0]*pow(flow,2)) + (pump_power_data[i,1]*flow) + pump_power_data[i,2]
        
        ##Evaluate the power consumption
        flow = np.zeros((2,1))
        flow[0,0] = (perc_split[1] + perc_split[2] + perc_split[3] + perc_split[4]) * total_flow
        flow[1,0] = perc_split[5] * total_flow
        
        power = 0
        for i in range (0,2):
            power = power + ((flow[i,0]/int_point[i,0])*max_power[i])
                    
        ##Check for flowrate feasibility
        feasibility = 1
        for i in range (0,2):
            if flow[i,0] > int_point[i,0]:
                feasibility = 0
                break
            
    elif select[2] == 1:

        ##Retrieving the singular coefficient approximation
        ice_coeff, trofir_coeff = dist_network_coeff(select, perc_split, total_flow)
        sys_curve = np.zeros((2,3))
        
        ##Converting into quadratic form 
        x_2, x = convert_to_quadratic(ice_coeff)
        sys_curve[0,0] = x_2
        sys_curve[0,1] = x  
        
        ##Converting into quadratic form 
        x_2, x = convert_to_quadratic(trofir_coeff)
        sys_curve[1,0] = x_2
        sys_curve[1,1] = x

        ##Gathering the relevant information for the selected pumps 
        pump_curve_data, pump_power_data = dist_pump_data(dist_pump)
        
        ##Finding the intersection point for each of the pump and system curves 
        int_point = np.zeros((2,2))##Flow(m3/h), Head(mH2O)
        
        for i in range (0,2):
            D = solve_quad_simul_eqns(pump_curve_data[i,:],sys_curve[i,:])
            int_point[i,0] = D[0]
            int_point[i,1] = D[1]
        
        ##Finding the maximum power consumption of each pump
        max_power = np.zeros((2,1))
        
        for i in range (0,2):
            flow = int_point[i,0]
            max_power[i] = (pump_power_data[i,0]*pow(flow,2)) + (pump_power_data[i,1]*flow) + pump_power_data[i,2]
        
        ##Evaluate the power consumption
        flow = np.zeros((2,1))
        flow[0,0] = (perc_split[1] + perc_split[2]) * total_flow
        flow[1,0] = (perc_split[3] + perc_split[4] + perc_split[5]) * total_flow
        
        power = 0
        for i in range (0,2):
            power = power + ((flow[i,0]/int_point[i,0])*max_power[i])
                    
        ##Check for flowrate feasibility
        feasibility = 1
        for i in range (0,2):
            if flow[i,0] > int_point[i,0]:
                feasibility = 0
                break
            
    elif select[3] == 1:
        
        ##Retrieving the singular coefficient approximation 
        icetrofir_coeff = dist_network_coeff(select, perc_split, total_flow)
        sys_curve = np.zeros((1,3))
        
        ##Converting into quadratic form 
        x_2, x = convert_to_quadratic(icetrofir_coeff)
        sys_curve[0,0] = x_2
        sys_curve[0,1] = x  

        ##Gathering the relevant information for the selected pumps 
        pump_curve_data, pump_power_data = dist_pump_data(dist_pump)
        
        ##Finding the intersection point for each of the pump and system curves 
        int_point = np.zeros((1,2))##Flow(m3/h), Head(mH2O)
        
        for i in range (0,1):
            D = solve_quad_simul_eqns(pump_curve_data[i,:],sys_curve[i,:])
            int_point[i,0] = D[0]
            int_point[i,1] = D[1]
        
        ##Finding the maximum power consumption of each pump
        max_power = np.zeros((1,1))
        
        for i in range (0,1):
            flow = int_point[i,0]
            max_power[i] = (pump_power_data[i,0]*pow(flow,2)) + (pump_power_data[i,1]*flow) + pump_power_data[i,2]
        
        ##Evaluate the power consumption
        flow = np.zeros((1,1))
        flow[0,0] = (perc_split[1] + perc_split[2] + perc_split[3] + perc_split[4] + perc_split[5] ) * total_flow
        
        power = 0
        for i in range (0,1):
            power = power + ((flow[i,0]/int_point[i,0])*max_power[i])
                    
        ##Check for flowrate feasibility
        feasibility = 1
        for i in range (0,1):
            if flow[i,0] > int_point[i,0]:
                feasibility = 0
                break
        
    return feasibility, power
