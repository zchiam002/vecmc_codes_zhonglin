#This is the compute file 

def combined_substation_compute (cb_ss_dc):
    
    import numpy as np 
    
    ##list of input values 
    ##cb_ss_dc = np.zeros((5,1))                                 ##Initialize the list, note the number of constants 
    
    ##cb_ss_dc[0,0] = cb_ss_gv2_demand
    ##cb_ss_dc[1,0] = cb_ss_hsb_demand
    ##cb_ss_dc[2,0] = cb_ss_pfa_demand
    ##cb_ss_dc[3,0] = cb_ss_ser_demand
    ##cb_ss_dc[4,0] = cb_ss_all_ss    
    ##cb_ss_dc[5,0] = cb_ss_cp
    ##cb_ss_dc[6,0] = cb_ss_ice_coeff 
    ##cb_ss_dc[7,0] = cb_ss_tro_coeff
    ##cb_ss_dc[8,0] = cb_ss_gv2_coeff
    ##cb_ss_dc[9,0] = cb_ss_hsb_coeff 
    ##cb_ss_dc[10,0] = cb_ss_pfa_coeff 
    ##cb_ss_dc[11,0] = cb_ss_ser_coeff  
    
    ##Such a way of calculating the flowrate implicit assumes that there is no flow through the common pipe.
    ##For a fixed temperature difference, this will always be the optimal case.
    ##Calculating the flowrate from each entering each substation 
    cb_ss_gv2_flow = 3600 * (cb_ss_dc[0,0] / (cb_ss_dc[5,0] * cb_ss_dc[4,0])) / 998.2
    cb_ss_hsb_flow = 3600 * (cb_ss_dc[1,0] / (cb_ss_dc[5,0] * cb_ss_dc[4,0])) / 998.2
    cb_ss_pfa_flow = 3600 * (cb_ss_dc[2,0] / (cb_ss_dc[5,0] * cb_ss_dc[4,0])) / 998.2
    cb_ss_ser_flow = 3600 * (cb_ss_dc[3,0] / (cb_ss_dc[5,0] * cb_ss_dc[4,0])) / 998.2

    ##Calculating the pressure drop in each branch
        ##Flowrate/pressure drop in ice branch 
    cb_ss_ice_flow = cb_ss_gv2_flow + cb_ss_hsb_flow
    cb_ss_ice_delp = cb_ss_dc[6,0] * pow(cb_ss_ice_flow, 1.852)
        ##Flowrate/pressure drop in tro branch 
    cb_ss_tro_flow = cb_ss_pfa_flow + cb_ss_ser_flow
    cb_ss_tro_delp = cb_ss_dc[7,0] * pow(cb_ss_tro_flow, 1.852)

    cb_ss_gv2_delp = cb_ss_dc[8,0] * pow(cb_ss_gv2_flow, 1.852) + cb_ss_ice_delp
    cb_ss_hsb_delp = cb_ss_dc[7,0] * pow(cb_ss_hsb_flow, 1.852) + cb_ss_ice_delp
    cb_ss_pfa_delp = cb_ss_dc[10,0] * pow(cb_ss_pfa_flow, 1.852) + cb_ss_tro_delp
    cb_ss_ser_delp = cb_ss_dc[11,0] * pow(cb_ss_ser_flow, 1.852) + cb_ss_tro_delp
       
    ##Pressure drop of the entire network
    cb_ss_delp_dist_nwk = max(cb_ss_gv2_delp, cb_ss_hsb_delp, cb_ss_pfa_delp, cb_ss_ser_delp)
    
       
    ##Flowrate in the distribution network
    cb_ss_flow_dist_nwk = cb_ss_ice_flow + cb_ss_tro_flow
    
    ##Total demand calculation 
    cb_ss_total_demand = cb_ss_dc[0,0] + cb_ss_dc[1,0] + cb_ss_dc[2,0] + cb_ss_dc[3,0]
    
    
    ##Initiate a matrix to hold the return values 
    cb_ss_calc = np.zeros((3,1))
    
    cb_ss_calc[0,0] = cb_ss_flow_dist_nwk
    cb_ss_calc[1,0] = cb_ss_delp_dist_nwk
    cb_ss_calc[2,0] = cb_ss_total_demand

    return cb_ss_calc  

    

