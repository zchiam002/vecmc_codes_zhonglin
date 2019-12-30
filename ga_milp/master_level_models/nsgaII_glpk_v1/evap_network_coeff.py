##This is the evaporator network model, it will return the pressure-drop coefficient each combination 

def evap_network_coeff (evap_flow_ratio, evap_total_flow):
    ##flow_ratio[0]     --- ch1 evapenser share 
    ##flow_ratio[1]     --- ch2 evapenser share 
    ##flow_ratio[2]     --- ch3 evapenser share
    ##total_flow (m3/h) --- the total flowrate through the evapensers
    
    ##The coefficients inclues the presure-drop associated with the evaporator at the chiller 
    ch1_evap_coeff = 0.00001 
    ch2_evap_coeff = 0.00001
    ch3_evap_coeff = 0.00001
    shared_coeff = 0.00001
    
    flow_ch1 = evap_flow_ratio[0]*evap_total_flow
    flow_ch2 = evap_flow_ratio[1]*evap_total_flow
    flow_ch3 = evap_flow_ratio[2]*evap_total_flow

    delp_ch1_evap_nwk = ch1_evap_coeff*pow(flow_ch1, 1.852) + shared_coeff*pow(evap_total_flow, 1.852)
    delp_ch2_evap_nwk = ch2_evap_coeff*pow(flow_ch2, 1.852) + shared_coeff*pow(evap_total_flow, 1.852)
    delp_ch3_evap_nwk = ch3_evap_coeff*pow(flow_ch3, 1.852) + shared_coeff*pow(evap_total_flow, 1.852)
    
    if flow_ch1 > 0:
        ch1_evap_nwk_coeff = delp_ch1_evap_nwk/pow(flow_ch1, 1.852)
    else:
        ch1_evap_nwk_coeff = 0
    
    if flow_ch2 > 0:
        ch2_evap_nwk_coeff = delp_ch2_evap_nwk/pow(flow_ch2, 1.852)
    else:
        ch2_evap_nwk_coeff = 0
    
    if flow_ch3 > 0:
        ch3_evap_nwk_coeff = delp_ch3_evap_nwk/pow(flow_ch3, 1.852)
    else:
        ch3_evap_nwk_coeff = 0
    
    return ch1_evap_nwk_coeff, ch2_evap_nwk_coeff, ch3_evap_nwk_coeff

