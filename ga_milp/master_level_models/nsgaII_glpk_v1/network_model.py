##This is the network script.
##It will be converted into a function later 

def network_model(nwk_var):
    from network_initial_feasibility_check import network_initial_feasibility_check
    from dist_network import dist_network 
    from evap_network import evap_network
    from cond_network import cond_network 
    
    ##Decision variables 
    
    ##Evaporator flowrates
    evap_ch1 = nwk_var[0]
    evap_ch2 = nwk_var[2]
    evap_ch3 = nwk_var[4]
    
    ##Condenser flowrates 
    cond_ch1 = nwk_var[1]
    cond_ch2 = nwk_var[3]
    cond_ch3 = nwk_var[5]

    ##Distribution split ratios
    split_cp = nwk_var[6]
    split_gv2 = nwk_var[7]  
    split_hsb = nwk_var[8]
    split_pfa = nwk_var[9]
    split_ser = nwk_var[10]
    split_fir = nwk_var[11]

    ##Selected distribution network
    dist_option1 = int(nwk_var[15])
    dist_option2 = int(nwk_var[16])
    dist_option3 = int(nwk_var[17])
    dist_option4 = int(nwk_var[18])

    ##Selected distribution pump 
    pumpaf1_1 = int(nwk_var[19])
    pumpaf1_2 = int(nwk_var[20])
    pumpaf2_1 = int(nwk_var[21])
    pumpaf2_2 = int(nwk_var[22])
    pumpaf3_1 = int(nwk_var[23])
    pumpaf3_2 = int(nwk_var[24])
    pumpaf3_3 = int(nwk_var[25])

    ##Initiating feasibility check to determine if the selected variables fall within the feasible region
    greenlight = network_initial_feasibility_check(nwk_var)
    
    #print(greenlight)
    if greenlight == 1:
        
        ##Handling the distribution network
        select = []
        select.append(dist_option1)
        select.append(dist_option2)
        select.append(dist_option3)
        select.append(dist_option4)
        
        perc_split = []
        perc_split.append(split_cp)
        perc_split.append(split_gv2)
        perc_split.append(split_hsb)
        perc_split.append(split_pfa)
        perc_split.append(split_ser)
        perc_split.append(split_fir)
        
        dist_pump = []
        dist_pump.append(pumpaf1_1)
        dist_pump.append(pumpaf1_2)
        dist_pump.append(pumpaf2_1)
        dist_pump.append(pumpaf2_2)
        dist_pump.append(pumpaf3_1)
        dist_pump.append(pumpaf3_2)
        dist_pump.append(pumpaf3_3)
        
        total_flow = evap_ch1 + evap_ch2 + evap_ch3
        feasibility_dist, power_dist = dist_network(select, perc_split, total_flow, dist_pump)
        #print('feasibility_dist ' + str(feasibility_dist))
        
        ##Handling the evaporator network 
        evap_total_flow = evap_ch1 + evap_ch2 + evap_ch3
        
        if evap_total_flow > 0:
            evap_flow_ratio = []
            evap_flow_ratio.append(evap_ch1/evap_total_flow)
            evap_flow_ratio.append(evap_ch2/evap_total_flow)
            evap_flow_ratio.append(evap_ch3/evap_total_flow)
        else:
            evap_flow_ratio = []
            evap_flow_ratio.append(0)
            evap_flow_ratio.append(0)
            evap_flow_ratio.append(0)
        
        feasibility_evap, power_evap = evap_network(evap_flow_ratio, evap_total_flow)
        #print('feasibility_evap ' + str(feasibility_evap))
        
        ##Handling the condensation network 
        cond_total_flow = cond_ch1 + cond_ch2 + cond_ch3
        
        if cond_total_flow > 0:
            cond_flow_ratio = []
            cond_flow_ratio.append(cond_ch1/cond_total_flow)
            cond_flow_ratio.append(cond_ch2/cond_total_flow)
            cond_flow_ratio.append(cond_ch3/cond_total_flow)
        else:
            cond_flow_ratio = []
            cond_flow_ratio.append(0)
            cond_flow_ratio.append(0)
            cond_flow_ratio.append(0)

        feasibility_cond, power_cond = cond_network(cond_flow_ratio, cond_total_flow)   
        #print('feasibility_cond ' + str(feasibility_cond)) 
        
        ##Evaluating the overall feasibility and the total power        
        if (feasibility_dist == 1) and (feasibility_evap == 1) and (feasibility_cond == 1):
            total_power = power_dist + power_evap + power_cond
        else:
            total_power = -1000

        return total_power
        
    else:
        total_power = -1000   
        
        return total_power


