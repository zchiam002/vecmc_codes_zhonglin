##This is the main script which runs the simulation model of the DCS 
def run_simulation_model ():

    from overall_model import overall_model
    
    ##Listing the decision variables (user defined)
    
        ##System-level variables
    chiller_evap_return_temperature = 286.89        ##chiller_evap_return_temperature (K)       lower bound: 274.15      upper bound: 288.15
    chiller_cond_inlet_temperature = 3.34           ##chiller_cond_inlet_temperature (range)    lower bound: 0           upper bound: 100            
    
        ##Chiller 1
    chiller1_onoff = 0                              ##chiller1_onoff (binary)                   lower bound: 0           upper bound: 1
    chiller1_mevap = 214.92                         ##chiller1_mevap (m3/h)                     lower bound: 109.195     upper bound: 218.390
    chiller1_evap_delt = 27.87                      ##chiller1_evap_delt (range)                lower bound: 0           upper bound: 100
    
        ##Chiller 2
    chiller2_onoff = 0                              ##chiller2_onoff (binary)                   lower bound: 0           upper bound: 1
    chiller2_mevap = 437.73                         ##chiller2_mevap (m3/h)                     lower bound: 410.226     upper bound: 820.453
    chiller2_evap_delt = 64.63                      ##chiller2_evap_delt (range)                lower bound: 0           upper bound: 100
    
        ##Chiller 3
    chiller3_onoff = 1                              ##chiller3_onoff (binary)                   lower bound: 0           upper bound: 1
    chiller3_mevap = 713.80                         ##chiller3_mevap (m3/h)                     lower bound: 410.226     upper bound: 820.453
    chiller3_evap_delt = 1.41                       ##chiller3_evap_delt (range)                lower bound: 0           upper bound: 100
    
        ##Distribution network
    dist_nwk_cp_split =  64.44                      ##dist_nwk_cp_split (range)                 lower bound: 0           upper bound: 100
    dist_nwk_pump_select = 1                        ##dist_nwk_pump_select (discrete 0-7)       lower bound: 1           upper bound: 7
    dist_nwk_gv2_split_perc = 55.12                 ##dist_nwk_gv2_split_perc (range)           lower bound: 0           upper bound: 100
    dist_nwk_hsb_split_perc = 66.05                 ##dist_nwk_hsb_split_perc (range)           lower bound: 0           upper bound: 100
    dist_nwk_pfa_split_perc = 44.94                 ##dist_nwk_pfa_split_perc (range)           lower bound: 0           upper bound: 100
    dist_nwk_ser_split_perc = 31.26                 ##dist_nwk_ser_split_perc (range)           lower bound: 0           upper bound: 100
    
        ##Cooling tower
    cooling_tower_1_air = 2.87                      ##cooling_tower_1_air (range)               lower bound: 0           upper bound: 100
    cooling_tower_2_air = 43.22                     ##cooling_tower_2_air (range)               lower bound: 0           upper bound: 100
    cooling_tower_3_air = 40.84                     ##cooling_tower_3_air (range)               lower bound: 0           upper bound: 100
    cooling_tower_4_air = 28.49                     ##cooling_tower_4_air (range)               lower bound: 0           upper bound: 100
    cooling_tower_5_air = 84.17                     ##cooling_tower_5_air (range)               lower bound: 0           upper bound: 100
        
    ##Initializing an array to hold the decision variables for the DCS simulation model 
    decision_variables = []
    
    decision_variables.append(chiller_evap_return_temperature)
    decision_variables.append(chiller_cond_inlet_temperature)    

    decision_variables.append(chiller1_onoff)    
    decision_variables.append(chiller1_mevap)
    decision_variables.append(chiller1_evap_delt)

    decision_variables.append(chiller2_onoff)
    decision_variables.append(chiller2_mevap)
    decision_variables.append(chiller2_evap_delt)

    decision_variables.append(chiller3_onoff)
    decision_variables.append(chiller3_mevap)
    decision_variables.append(chiller3_evap_delt)

    decision_variables.append(dist_nwk_cp_split)
    decision_variables.append(dist_nwk_pump_select)
    decision_variables.append(dist_nwk_gv2_split_perc)
    decision_variables.append(dist_nwk_hsb_split_perc)
    decision_variables.append(dist_nwk_pfa_split_perc)
    decision_variables.append(dist_nwk_ser_split_perc)

    decision_variables.append(cooling_tower_1_air)
    decision_variables.append(cooling_tower_2_air)
    decision_variables.append(cooling_tower_3_air)
    decision_variables.append(cooling_tower_4_air)
    decision_variables.append(cooling_tower_5_air)
    
    ##Running the model 
    total_elect_cons = overall_model (decision_variables)
    
    ##Printing the total electricity consumption 
    print(total_elect_cons)
    
    return 

########################################################################################################################################################################
########################################################################################################################################################################
##Running the script 
if __name__ == '__main__':
    
    run_simulation_model ()
    
    
    
    