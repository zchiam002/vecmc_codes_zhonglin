##This is the distribution network selection model, it will return the pressure_drop coefficient for the selected network choice. 

def dist_network_coeff (select, perc_split, total_flow):
    ##select is an array of 4 elements
        ##select[0] == 1        --- each individual network is served by their own pumps 
        ##select[1] == 1        --- Fira is served by its own pump, Troncal and ICE share pumps 
        ##select[2] == 1        --- Fira and Troncal share pumps, ICE is served by its own pumps 
        ##select[3] == 1        --- All networks can share pumps
    ##perc_split is an array of 6 elements
        ##perc_split[0]         --- ratio of flowrate to common pipe 
        ##perc_split[1]         --- ratio of flowrate to gv2
        ##perc_split[2]         --- ratio of flowrate to hsb 
        ##perc_split[3]         --- ratio of flowrate to pfa
        ##perc_split[4]         --- ratio of flowrate to ser
        ##perc_split[5]         --- ratio of flowrate to fir
    ##total_flow (m3/h)    --- the total flowrate through the distribution networks
        
    ##The coefficients include the pressure-drop associated with the heat-exchanger at the substation and the return line.
    ice_main_coeff = 0.0000260567799112396
    gv2_coeff = 0.000183911797547263
    hsb_coeff = 0.018912221388394
    tro_main_coeff = 0.0010975270251404
    pfa_coeff = 0.000546263467870374
    ser_coeff = 0.00134239151150882
    fir_main_coeff = 0.00931240185493485
    
    flow_gv2 = perc_split[1]*total_flow
    flow_hsb = perc_split[2]*total_flow
    flow_pfa = perc_split[3]*total_flow
    flow_ser = perc_split[4]*total_flow
    flow_fir = perc_split[5]*total_flow

    delp_ice_main =  ice_main_coeff*pow((flow_gv2+flow_hsb),1.852)
    delp_gv2_br = gv2_coeff*pow(flow_gv2,1.852)
    delp_hsb_br = hsb_coeff*pow(flow_hsb,1.852)
    
    delp_tro_main = tro_main_coeff*pow((flow_pfa+flow_ser),1.852)
    delp_pfa_br = pfa_coeff*pow(flow_pfa,1.852)
    delp_ser_br = ser_coeff*pow(flow_ser,1.852)
    
    delp_fir = fir_main_coeff*pow(flow_fir,1.852)
    
    if select[0] == 1:
        ##Each individual network is served by their own pumps
        delp_ice = max ((delp_ice_main + delp_gv2_br), (delp_ice_main + delp_hsb_br))
        delp_tro = max((delp_tro_main + delp_pfa_br), (delp_tro_main + delp_ser_br))
        
        if (flow_gv2 + flow_hsb) > 0: 
            result_coeff_ice = delp_ice/pow((flow_gv2 + flow_hsb),1.852)
        else:
            result_coeff_ice = 0
            
        if (flow_pfa + flow_ser) > 0:
            result_coeff_tro = delp_tro/pow((flow_pfa + flow_ser),1.852)
        else:
            result_coeff_tro = 0
        
        return result_coeff_ice, result_coeff_tro, fir_main_coeff
        
    elif select[1] == 1:
        ##Fira is served by its own pump, Troncal and ICE share pumps 
        delp_icetro = max((delp_ice_main + delp_gv2_br), (delp_ice_main + delp_hsb_br), (delp_tro_main + delp_pfa_br), (delp_tro_main + delp_ser_br))
        
        if (flow_gv2 + flow_hsb + flow_pfa + flow_ser) > 0:
            result_coeff_icetro = delp_icetro/pow((flow_gv2 + flow_hsb + flow_pfa + flow_ser),1.852)
        else:
            result_coeff_icetro = 0
        
        return result_coeff_icetro, fir_main_coeff
    
    elif select[2] == 1:
        ##Fira and Troncal share pumps, ICE is served by its own pumps 
        delp_trofir = max((delp_tro_main + delp_pfa_br), (delp_tro_main + delp_ser_br), (delp_fir))
        delp_ice = max ((delp_ice_main + delp_gv2_br), (delp_ice_main + delp_hsb_br))
        
        if (flow_pfa + flow_ser  + flow_fir) > 0:
            result_coeff_trofir = delp_trofir/pow((flow_pfa + flow_ser  + flow_fir),1.852)
        else:
            result_coeff_trofir = 0
            
        if (flow_gv2 + flow_hsb) > 0:
            result_coeff_ice = delp_ice/pow((flow_gv2 + flow_hsb),1.852)
        else:
            result_coeff_ice = 0
        
        return result_coeff_ice, result_coeff_trofir
        
    elif select[3] == 1:
        ##All networks can share pumps
        delp_icetrofir = max((delp_ice_main + delp_gv2_br),(delp_ice_main + delp_hsb_br),(delp_tro_main + delp_pfa_br),(delp_tro_main + delp_ser_br),(delp_fir))
        
        if (flow_gv2 + flow_hsb + flow_pfa + flow_ser + flow_fir) > 0:
            result_coeff_icetrofir = delp_icetrofir/pow((flow_gv2 + flow_hsb + flow_pfa + flow_ser + flow_fir),1.852)
        else:
            result_coeff_icetrofir = 0
            
        return result_coeff_icetrofir

