##This script is dedicated to running the standalone models for the evaporator network 
def run_evaporator_network_model_main ():
    
    import pandas as pd 
    from evap_network_models import evap_nwk_org
    from evap_network_models import evap_nwk_piecewise_pressure
    from evap_network_models import evap_nwk_piecewise_pressure_reg_pumpnwk
    from evap_network_models import evap_nwk_piecewise_pressure_reg_pumpnwk_bilinear_temp
    
    ###########################################################################
    ##Testing the evaporator network models
    ###########################################################################
    ##There are 4 models in this section 
        ##1. Original evaporator network model, formulated using first principles.  
        ##2. Piecewise linearization of pressure drop.  
        ##3. Regression of pump and network electricity consumption.
        ##4. Linearization of bilinear temperature and flowrate variables.
        
    ##Setting up the parameters for the evaporator network which is connected to 3 chillers.  
    param = {}
    param['ch1_nwk_coeff'] = 0.000246472                                             ##Pipe friction coefficients 'A' , where delta P = A * flowrate^(1.852)
    param['ch2_nwk_coeff'] = 3.07492E-05
    param['ch3_nwk_coeff'] = 3.07492E-05
    param['common_nwk_coeff'] = 1.66667E-05
    ##Pump parameters 
    param['evap_pump_1_delp'] = [-0.0001266405, 0.0112272822, 12.3463827922]         ##Listed in terms of x2, x and cst coeff. Coefficients of the nominal pump curve.
    param['evap_pump_2_delp'] = [-0.0000136254, 0.0001647403, 21.4327511013]
    param['evap_pump_3_delp'] = [-0.0000136254, 0.0001647403, 21.4327511013]

    ##This is the linear form, better confidence with extrapolation 
    param['evap_pump_1_elect'] = [0, 0, 0.0087224764, 4.0804382340]                  ##Listed in terms of x3, x2, x and cst coeff. Pump electricity curve.
    param['evap_pump_2_elect'] = [0, 0, 0.0209871245, 20.3919751419]
    param['evap_pump_3_elect'] = [0, 0, 0.0209871245, 20.3919751419]

    ##Flow limits 
    param['ch1_evap_nwk_flow_limit'] = 250                                           ##Flowrate limits (m3/h) of each pump. Determined using the intersection between the pump
    param['ch2_evap_nwk_flow_limit'] = 850                                           ##and network curve.
    param['ch3_evap_nwk_flow_limit'] = 850
    
    steps = 4                               ##The number of linear pieces for linearizing the pressure curves.
    bilinear_pieces = 20                    ##The number of pieces used to linearize the temperature and flowrate variables.
    tevap_in = 15 + 273.15                  ##Evaporator return temperature. Functions as a upper limit for linearization.
    
    ##Variables for the evaporator network model 
    
    ch1_flow = 0                                            ##Flowrate through chiller 1 (m3/h)
    ch1_temp = 278.15                                       ##Chiller 1 supply temperature (K)
    ch2_flow = 820.4531779                                  ##Flowrate through chiller 2 (m3/h)
    ch2_temp = 280.15                                       ##Chiller 2 supply temperature (K)
    ch3_flow = 0                                            ##Flowrate through chiller 3(m3/h)
    ch3_temp = 281.15                                       ##Chiller 3 supply temperature (K)
    split_to_dist_nwk = 70                                  ##Percentage of the total flowrate which goes to the distribution network (%)
    split_to_common_pipe = 100 - split_to_dist_nwk          ##Percentage of the total flowrate which goes to the common pipe (%)
    
    ##Placing the values into a dataframe 
    chiller_input = pd.DataFrame(columns = ['Name', 'Value'])
    data_temp = ['chiller_1_flow', ch1_flow]
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
    chiller_input = chiller_input.append(temp_df, ignore_index = True)
    data_temp = ['chiller_1_supply_temperature', ch1_temp]
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
    chiller_input = chiller_input.append(temp_df, ignore_index = True)
    data_temp = ['chiller_2_flow', ch2_flow]
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
    chiller_input = chiller_input.append(temp_df, ignore_index = True)
    data_temp = ['chiller_2_supply_temperature', ch2_temp]
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
    chiller_input = chiller_input.append(temp_df, ignore_index = True)
    data_temp = ['chiller_3_flow', ch3_flow]
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
    chiller_input = chiller_input.append(temp_df, ignore_index = True)
    data_temp = ['chiller_3_supply_temperature', ch3_temp]
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
    chiller_input = chiller_input.append(temp_df, ignore_index = True)

    cp_dist_nwk_split = [split_to_dist_nwk, split_to_common_pipe]
    
    ##Running model 1
    return_values_1_dict, return_values_1_df = evap_nwk_org(chiller_input, cp_dist_nwk_split, param)
    ##Running model 2
    return_values_2_dict, return_values_2_df = evap_nwk_piecewise_pressure(chiller_input, cp_dist_nwk_split, steps, param)
    ##Running model 3
    return_values_3_dict, return_values_3_df = evap_nwk_piecewise_pressure_reg_pumpnwk(chiller_input, cp_dist_nwk_split, steps, param)
    ##Running model 4
    return_values_4_dict, return_values_4_df = evap_nwk_piecewise_pressure_reg_pumpnwk_bilinear_temp(chiller_input, cp_dist_nwk_split, steps, tevap_in, bilinear_pieces, param)
    
    ##Printing the results 
    print('Evaporator network model 1')
    print(return_values_1_df)
    print('Evaporator network model 2')
    print(return_values_2_df)   
    print('Evaporator network model 3')
    print(return_values_3_df)    
    print('Evaporator network model 4')
    print(return_values_4_df)
    
    return 

