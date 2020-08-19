##This script is dedicated to running the standalone models for the distribution network 
def run_distribution_network_model_main ():
    
    from dist_network_models import dist_nwk_org
    from dist_network_models import dist_nwk_piecewise_pressure
    from dist_network_models import dist_nwk_piecewise_pressure_reg_pumpnwk
    from dist_network_models import dist_nwk_piecewise_pressure_reg_pumpnwk_bilinear_temp

    ###########################################################################
    ##Testing the distribution network models
    ###########################################################################
    ##There are 4 models in this section 
        ##1. Original evaporator network model, formulated using first principles.  
        ##2. Piecewise linearization of pressure drop.  
        ##3. Regression of pump and network electricity consumption.
        ##4. Linearization of bilinear temperature and flowrate variables.
    
    ##Setting up the parameters for the distribution network which is connected to 5 customers.
        ##Pipe friction coefficients 'A' , where delta P = A * flowrate^(1.852)
    param = {}
    param['ice_main_coeff'] = 0.00011627906976743445                ##For the pipe which connects gv2 and hsb
    param['gv2_coeff'] = 0.00034883720930232456                     ##For the pipe which is connected to gv2 
    param['hsb_coeff'] = 0.05046511627906977                        ##For the pipe which is connected to hsb 
    param['tro_main_coeff'] = 0.001162790697674419                  ##For the pipe which connects pfa and ser
    param['pfa_coeff'] = 0.0029069767441860417                      ##For the pipe which is connected to pfa 
    param['ser_coeff'] = 0.00023255813953487953                     ##For the pipe which is connected to ser
    param['fir_coeff'] = 0.005697674418604649                       ##For the pipe which is connected to fir 
        
    max_flow = 3200                                                 ##Determined using the intersection point with the pump and network curves
    steps = 4                                                       ##For the linearization of the pressure curves
    bilinear_pieces = 20                                            ##For the linearization of the bilinear variables 
    
    ##Variables for the distribution network model 
    gv2_demand = 1000                                               ##Cooling demands for the varib
    hsb_demand = 400
    pfa_demand = 500
    ser_demand = 900
    fir_demand = 1000
    
    consumer_demand = [gv2_demand, hsb_demand, pfa_demand, ser_demand, fir_demand]
    
    total_nwk_flow = 46.57022822
    
    gv2_split = 0.113613471		
    hsb_split = 0.460964295
    pfa_split = 0.425422234
    ser_split = 0
    fir_split = 0
    
    perc_split = [gv2_split, hsb_split, pfa_split, ser_split, fir_split]
    
    nwk_pump_select = 37
    
    tin_dist_nwk = 273.15 + 6
    
    steps = 4
    
    tin_dist_nwk_max = 273.15 + 20
    
    ##Running model 1
    return_values_1, return_values_1_df = dist_nwk_org(consumer_demand, total_nwk_flow, perc_split, nwk_pump_select, tin_dist_nwk, param, max_flow)
    ##Running model 2
    return_values_1, return_values_2_df = dist_nwk_piecewise_pressure (consumer_demand, total_nwk_flow, perc_split, nwk_pump_select, tin_dist_nwk, steps)
    ##Running model 3
    return_values_1, return_values_3_df = dist_nwk_piecewise_pressure_reg_pumpnwk(consumer_demand, total_nwk_flow, perc_split, nwk_pump_select, tin_dist_nwk, steps)
    ##Running model 4 
    return_values_1, return_values_4_df = dist_nwk_piecewise_pressure_reg_pumpnwk_bilinear_temp(consumer_demand, total_nwk_flow, perc_split, nwk_pump_select, tin_dist_nwk, 
                                                                                                steps, tin_dist_nwk_max, bilinear_pieces)
    
    ##Printing the results 
    print('Distribution network model 1')
    print(return_values_1_df)
    print('Distribution network model 2')
    print(return_values_2_df)   
    print('Distribution network model 3')
    print(return_values_3_df)    
    print('Distribution network model 4')
    print(return_values_4_df)
    return 

