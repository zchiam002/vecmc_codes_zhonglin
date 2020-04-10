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
    
    total_nwk_flow = a1
    
    gv2_split = s1		
    hsb_split = s2
    pfa_split = s3
    ser_split = s4
    fir_split = s5
    
    perc_split = [gv2_split, hsb_split, pfa_split, ser_split, fir_split]
    
    nwk_pump_select = 37
    
    tin_dist_nwk = 273.15 + 6
    
    steps = 4
    
    tin_dist_nwk_max = 273.15 + 20
    
    
        
    
    
    
    ##Running model 1
    return_values_1, return_values_df_1 = dist_nwk_org(consumer_demand, total_nwk_flow, perc_split, nwk_pump_select, tin_dist_nwk, max_flow)
    return 

