##Network model initial feasibility check 
##The purpose of this is to check is the combinations of decision variables are even feasible to begin with 

def network_initial_feasibility_check (nwk_var):
    
    ##Distribution split ratios
    split_cp = nwk_var[6]
    split_gv2 = nwk_var[7]  
    split_hsb = nwk_var[8]
    split_pfa = nwk_var[9]
    split_ser = nwk_var[10]
    split_fir = nwk_var[11]

    ##Selected distribution network
    dist_option1 = nwk_var[15]
    dist_option2 = nwk_var[16]
    dist_option3 = nwk_var[17]
    dist_option4 = nwk_var[18]

    ##Selected distribution pump 
    pumpaf1_1 = nwk_var[19]
    pumpaf1_2 = nwk_var[20]
    pumpaf2_1 = nwk_var[21]
    pumpaf2_2 = nwk_var[22]
    pumpaf3_1 = nwk_var[23]
    pumpaf3_2 = nwk_var[24]
    pumpaf3_3 = nwk_var[25]
        
    greenlight = 1
        
    ##Checking for the split ratios
    
    total_ratio = split_cp + split_gv2 + split_hsb + split_pfa + split_ser + split_fir

    if total_ratio != 1:
        greenlight = 0
        return greenlight 
    
    ##Checking for pump selection based on selected distribution network 
    
    total_dist_option = dist_option1 + dist_option2 + dist_option3 + dist_option4
    total_dist_option = int(round(total_dist_option))   
    
    if total_dist_option != 1:
        greenlight = 0
        return greenlight 
    
    ##Checking for the selected pump based on dist_option[i]
    if dist_option1 == 1:                                                       ##This case is where 3 networks are individualized 
        ice_pump = pumpaf1_1 + pumpaf1_2
        tro_pump = pumpaf2_1 + pumpaf2_2
        fir_pump = pumpaf3_1 + pumpaf3_2 + pumpaf3_3
        
        if ice_pump != 1:
            greenlight = 0
            return greenlight
        elif tro_pump != 1:
            greenlight = 0
            return greenlight
        elif fir_pump != 1:
            greenlight = 0
            return greenlight
             
    elif dist_option2 == 1:                                                     ##Only Fira is individualized 
        icetro_pump = pumpaf1_1 + pumpaf1_2 + pumpaf2_1 + pumpaf2_2
        fir_pump = pumpaf3_1 + pumpaf3_2 + pumpaf3_3
        
        if icetro_pump != 1:
            greenlight = 0
            return greenlight
        elif fir_pump != 1:
            greenlight = 0
            return greenlight
            
    elif dist_option3 == 1:                                                     ##Only ICE is individualized 
        ice_pump = pumpaf1_1 + pumpaf1_2
        trofir_pump = pumpaf2_1 + pumpaf2_2 + pumpaf3_1 + pumpaf3_2 + pumpaf3_3

        if ice_pump != 1:
            greenlight = 0
            return greenlight        
        elif trofir_pump != 1:
            greenlight = 0
            return greenlight
            
    elif dist_option4 == 1:                                                     ##All networks are shared 
        icetrofir_pump = pumpaf1_1 + pumpaf1_2 + pumpaf2_1 + pumpaf2_2 + pumpaf3_1 + pumpaf3_2 + pumpaf3_3
        
        if icetrofir_pump != 1:
            greenlight = 0
            return greenlight
    
    return greenlight