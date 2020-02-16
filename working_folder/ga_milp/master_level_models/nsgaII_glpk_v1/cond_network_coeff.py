##This is the condensation network model, it will return the pressure-drop coefficient each combination 

def cond_network_coeff (cond_flow_ratio, cond_total_flow):
    ##cond_flow_ratio[0]     --- ch1 condenser share 
    ##cond_flow_ratio[1]     --- ch2 condenser share 
    ##cond_flow_ratio[2]     --- ch3 condenser share
    ##cond_total_flow (m3/h) --- the total flowrate through the condensers
    
    
    ch1_cond_coeff = 0.00001 
    ch2_cond_coeff = 0.00001
    ch3_cond_coeff = 0.00001
    shared_coeff = 0.000001
    
    flow_ch1 = cond_flow_ratio[0]*cond_total_flow
    flow_ch2 = cond_flow_ratio[1]*cond_total_flow
    flow_ch3 = cond_flow_ratio[2]*cond_total_flow

    delp_ch1_cond_nwk = ch1_cond_coeff*pow(flow_ch1, 1.852) + shared_coeff*pow(cond_total_flow, 1.852)
    delp_ch2_cond_nwk = ch2_cond_coeff*pow(flow_ch2, 1.852) + shared_coeff*pow(cond_total_flow, 1.852)
    delp_ch3_cond_nwk = ch3_cond_coeff*pow(flow_ch3, 1.852) + shared_coeff*pow(cond_total_flow, 1.852)
    
#    ch1_cond_nwk_coeff = delp_ch1_cond_nwk/pow(flow_ch1, 1.852)
#    ch2_cond_nwk_coeff = delp_ch2_cond_nwk/pow(flow_ch2, 1.852)
#    ch3_cond_nwk_coeff = delp_ch3_cond_nwk/pow(flow_ch3, 1.852)

    if flow_ch1 > 0:
        ch1_cond_nwk_coeff = delp_ch1_cond_nwk/pow(flow_ch1, 1.852)
    else:
        ch1_cond_nwk_coeff = 0
    
    if flow_ch2 > 0:
        ch2_cond_nwk_coeff = delp_ch2_cond_nwk/pow(flow_ch2, 1.852)
    else:
        ch2_cond_nwk_coeff = 0
    
    if flow_ch3 > 0:
        ch3_cond_nwk_coeff = delp_ch3_cond_nwk/pow(flow_ch3, 1.852)
    else:
        ch3_cond_nwk_coeff = 0
    
    return ch1_cond_nwk_coeff, ch2_cond_nwk_coeff, ch3_cond_nwk_coeff
