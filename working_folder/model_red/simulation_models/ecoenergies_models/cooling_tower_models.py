##This script contains all the cooling tower models, the input and output of all the models should be the same 
##The each model has 5 cooling tower units 

##Model 1: Universal engineering cooling tower model 
##Model 2: Simplification using regression 
##Model 3: Impact of LP relaxation on the bilinear terms 

def cooling_tower_uem (perc_fan, total_water_flow_config, tw_in, twb):
    
    import pandas as pd 
    
    ##perc_fan[0] --- the percentage at which the cooling tower 1's fan is operated (0 - 100 %)
    ##perc_fan[1] --- the percentage at which the cooling tower 2's fan is operated (0 - 100 %)
    ##perc_fan[2] --- the percentage at which the cooling tower 3's fan is operated (0 - 100 %)
    ##perc_fan[3] --- the percentage at which the cooling tower 4's fan is operated (0 - 100 %)
    ##perc_fan[4] --- the percentage at which the cooling tower 5's fan is operated (0 - 100 %)
    ##total_water_flow_config --- the total flowrate of water into the configuration 
    ##tw_in --- the temperature of water into the cooling tower configuration 
    ##twb --- the ambient wet_bulb temperature 
    
    ##Cooling tower regression derived coefficients 
    b0 = 0.14029549639345207	
    b1 = 0.600266127023157	
    b2 = -0.0211475692653011	
    b3 = 0.2792094538127389	
    b4 = 9.294683422723725*pow(10, -4)
    b5 = 0.16052557022400754
    
    make_up_water_correct_coeff = 2.3294122
    
    ct_reg_coeff = [b0, b1, b2, b3, b4, b5]
    towers_in_config = 1
    flow_rate_to_each_tower = total_water_flow_config / towers_in_config 
    del_t_max = tw_in - twb
    
    ##Deriving the flowrate of air
    min_air_flow = 0            ##kg/h
    max_air_flow = 369117       ##kg/h
    ##Maximum electricity consumption by fan 
    elect_max_fan = 22          ##kWh
    
    return_values = {}
    return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    temp_values = pd.DataFrame(columns = ['Name', 'Value'])
    
    for i in range (0, towers_in_config):
        ct_id = 'ct' + str(i + 1)
        flow_ma_temp = perc_fan[i] * (max_air_flow - min_air_flow)
        constants_temp = [flow_rate_to_each_tower, twb]
        del_t_temp = delT_calc (ct_reg_coeff, flow_ma_temp, tw_in, constants_temp)
        if del_t_temp > del_t_max: 
            del_t_temp = del_t_max
        
        ##Calculating exit water temperature of unit 
        name_temp = ct_id + '_t_out'
        value = tw_in - del_t_temp
        data_temp = [name_temp, value]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
        temp_values = temp_values.append(temp_df, ignore_index = True)
        
        ##Calculating the electricity consumption of the fan 
        name_temp = ct_id + '_elect_fan'
        value = perc_fan[i] * elect_max_fan 
        data_temp = [name_temp, value]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
        temp_values = temp_values.append(temp_df, ignore_index = True)
        
        ##Calculating the make up water needed 
        name_temp = ct_id + '_water_cons'     
        value = (0.0027 + (0.01 * (del_t_temp/5.6))) * flow_rate_to_each_tower * make_up_water_correct_coeff
        data_temp = [name_temp, value]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
        temp_values = temp_values.append(temp_df, ignore_index = True)

    for i in range (0, towers_in_config):
        ##Writing values in a dictionary  
        return_values[temp_values['Name'][(i * 3) + 0]] = temp_values['Value'][(i * 3) + 0]
        return_values[temp_values['Name'][(i * 3) + 1]] = temp_values['Value'][(i * 3) + 1]
        return_values[temp_values['Name'][(i * 3) + 2]] = temp_values['Value'][(i * 3) + 2]
        ##Writing values in a dataframe 
        data_temp = [temp_values['Name'][(i * 3) + 0], temp_values['Value'][(i * 3) + 0], 'K']
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
        return_values_df = return_values_df.append(temp_df, ignore_index = True)
        
        data_temp = [temp_values['Name'][(i * 3) + 1], temp_values['Value'][(i * 3) + 1], 'kWh']
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
        return_values_df = return_values_df.append(temp_df, ignore_index = True)
        
        data_temp = [temp_values['Name'][(i * 3) + 2], temp_values['Value'][(i * 3) + 2], 'm3/h']
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
        return_values_df = return_values_df.append(temp_df, ignore_index = True)
        
    ##Computing the temperature of water exiting the configuration
    t_config_out = 0
    for i in range (0, towers_in_config):
        t_config_out = t_config_out + ((1 / towers_in_config) * temp_values['Value'][(i * 3) + 0])

    return_values['t_out_config'] = t_config_out
    data_temp = ['t_out_config', t_config_out, 'K']
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
    return_values_df = return_values_df.append(temp_df, ignore_index = True)
    
    
    return return_values, return_values_df
    
################################################################################################################################################################
################################################################################################################################################################

def cooling_tower_uem_reg (perc_fan, total_water_flow_config, tw_in, twb, twi_min, twi_max):
    import pandas as pd 
    
    ##perc_fan[0] --- the percentage at which the cooling tower 1's fan is operated (0 - 100 %)
    ##perc_fan[1] --- the percentage at which the cooling tower 2's fan is operated (0 - 100 %)
    ##perc_fan[2] --- the percentage at which the cooling tower 3's fan is operated (0 - 100 %)
    ##perc_fan[3] --- the percentage at which the cooling tower 4's fan is operated (0 - 100 %)
    ##perc_fan[4] --- the percentage at which the cooling tower 5's fan is operated (0 - 100 %)
    ##total_water_flow_config --- the total flowrate of water into the configuration 
    ##tw_in --- the temperature of water into the cooling tower configuration 
    ##twb --- the ambient wet_bulb temperature 
    
    ##Cooling tower regression derived coefficients 
#    b0 = 0.14029549639345207	
#    b1 = 0.600266127023157	
#    b2 = -0.0211475692653011	
#    b3 = 0.2792094538127389	
#    b4 = 9.294683422723725*pow(10, -4)
#    b5 = 0.16052557022400754
    
    b0 = 0.23382397 	
    b1 = -0.03876029 	
    b2 = -0.03298896 	
    b3 = 0.00113387	
    b4 = -0.00416801
    b5 = 0.42846231
    
    make_up_water_correct_coeff = 2.3294122
    
    ct_reg_coeff = [b0, b1, b2, b3, b4, b5]
    towers_in_config = 1
    flow_rate_to_each_tower = total_water_flow_config / towers_in_config 
    del_t_max = tw_in - twb
    
    ##Deriving the flowrate of air
    min_air_flow = 0            ##kg/h
    max_air_flow = 369117       ##kg/h
    ##Maximum electricity consumption by fan 
    elect_max_fan = 22          ##kWh
    
    return_values = {}
    return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    temp_values = pd.DataFrame(columns = ['Name', 'Value'])
    
    for i in range (0, towers_in_config):
        ct_id = 'ct' + str(i + 1)
        flow_ma_temp = perc_fan[i] * (max_air_flow - min_air_flow)
        del_t_coeff_temp = ct_reg_coeff_calc (ct_reg_coeff, twb, twi_min, twi_max, min_air_flow, max_air_flow, flow_rate_to_each_tower, elect_max_fan)
        del_t_temp = (del_t_coeff_temp[0,0] * flow_ma_temp) + (del_t_coeff_temp[1,0] * tw_in) + (del_t_coeff_temp[2,0] * flow_ma_temp * tw_in) + del_t_coeff_temp[3,0]
        if del_t_temp > del_t_max: 
            del_t_temp = del_t_max
        
        ##Calculating exit water temperature of unit 
        name_temp = ct_id + '_t_out'
        value = tw_in - del_t_temp
        data_temp = [name_temp, value]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
        temp_values = temp_values.append(temp_df, ignore_index = True)
        
        ##Calculating the electricity consumption of the fan 
        name_temp = ct_id + '_elect_fan'
        value = perc_fan[i] * elect_max_fan 
        data_temp = [name_temp, value]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
        temp_values = temp_values.append(temp_df, ignore_index = True)
        
        ##Calculating the make up water needed 
        name_temp = ct_id + '_water_cons'     
        value = (0.0027 + (0.01 * (del_t_temp/5.6))) * flow_rate_to_each_tower * make_up_water_correct_coeff
        data_temp = [name_temp, value]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
        temp_values = temp_values.append(temp_df, ignore_index = True)

    for i in range (0, towers_in_config):
        ##Writing values in a dictionary  
        return_values[temp_values['Name'][(i * 3) + 0]] = temp_values['Value'][(i * 3) + 0]
        return_values[temp_values['Name'][(i * 3) + 1]] = temp_values['Value'][(i * 3) + 1]
        return_values[temp_values['Name'][(i * 3) + 2]] = temp_values['Value'][(i * 3) + 2]
        ##Writing values in a dataframe 
        data_temp = [temp_values['Name'][(i * 3) + 0], temp_values['Value'][(i * 3) + 0], 'K']
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
        return_values_df = return_values_df.append(temp_df, ignore_index = True)
        
        data_temp = [temp_values['Name'][(i * 3) + 1], temp_values['Value'][(i * 3) + 1], 'kWh']
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
        return_values_df = return_values_df.append(temp_df, ignore_index = True)
        
        data_temp = [temp_values['Name'][(i * 3) + 2], temp_values['Value'][(i * 3) + 2], 'm3/h']
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
        return_values_df = return_values_df.append(temp_df, ignore_index = True)
        
    ##Computing the temperature of water exiting the configuration
    t_config_out = 0
    for i in range (0, towers_in_config):
        t_config_out = t_config_out + ((1 / towers_in_config) * temp_values['Value'][(i * 3) + 0])

    return_values['t_out_config'] = t_config_out
    data_temp = ['t_out_config', t_config_out, 'K']
    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
    return_values_df = return_values_df.append(temp_df, ignore_index = True)    
    
    return return_values, return_values_df, del_t_coeff_temp
    
################################################################################################################################################################
################################################################################################################################################################

def cooling_tower_uem_reg_lprelax (perc_fan, total_water_flow_config, tw_in, twb, twi_min, twi_max, bilinear_pieces):
    
    import pandas as pd 
    
    ##perc_fan[0] --- the percentage at which the cooling tower 1's fan is operated (0 - 100 %)
    ##perc_fan[1] --- the percentage at which the cooling tower 2's fan is operated (0 - 100 %)
    ##perc_fan[2] --- the percentage at which the cooling tower 3's fan is operated (0 - 100 %)
    ##perc_fan[3] --- the percentage at which the cooling tower 4's fan is operated (0 - 100 %)
    ##perc_fan[4] --- the percentage at which the cooling tower 5's fan is operated (0 - 100 %)
    ##total_water_flow_config --- the total flowrate of water into the configuration 
    ##tw_in --- the temperature of water into the cooling tower configuration 
    ##twb --- the ambient wet_bulb temperature 
    
    ##Cooling tower regression derived coefficients
    
    b0 = 0.23382397 	
    b1 = -0.03876029 	
    b2 = -0.03298896 	
    b3 = 0.00113387	
    b4 = -0.00416801
    b5 = 0.42846231
#    b0 = 0.14029549639345207	
#    b1 = 0.600266127023157	
#    b2 = -0.0211475692653011	
#    b3 = 0.2792094538127389	
#    b4 = 9.294683422723725*pow(10, -4)
#    b5 = 0.16052557022400754
    
    make_up_water_correct_coeff = 2.3294122
    
    ct_reg_coeff = [b0, b1, b2, b3, b4, b5]
    towers_in_config = 1
    flow_rate_to_each_tower = total_water_flow_config / towers_in_config 
    del_t_max = tw_in - twb
    
    ##Deriving the flowrate of air
    min_air_flow = 0            ##kg/h
    max_air_flow = 369117       ##kg/h
    ##Maximum electricity consumption by fan 
    elect_max_fan = 22          ##kWh
    
    return_values = {}
    return_values_df = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    temp_values = pd.DataFrame(columns = ['Name', 'Value'])
    
    for i in range (0, towers_in_config):
        ct_id = 'ct' + str(i + 1)
        flow_ma_temp = perc_fan[i] * (max_air_flow - min_air_flow)
        del_t_coeff_temp = ct_reg_coeff_calc (ct_reg_coeff, twb, twi_min, twi_max, min_air_flow, max_air_flow, flow_rate_to_each_tower, elect_max_fan)
        ##Generating the bilinear pieces 
        ma_table, twi_table = gen_bilinear_pieces (min_air_flow, max_air_flow, twi_min, twi_max, bilinear_pieces)
        bilin_est = search_bilin_table_for_values (ma_table, twi_table, flow_ma_temp, tw_in)
        del_t_temp = (del_t_coeff_temp[0,0] * flow_ma_temp) + (del_t_coeff_temp[1,0] * tw_in) + (del_t_coeff_temp[2,0] * bilin_est) + del_t_coeff_temp[3,0]
        if del_t_temp > del_t_max: 
            del_t_temp = del_t_max
        
        ##Calculating exit water temperature of unit 
        name_temp = ct_id + '_t_out'
        value = tw_in - del_t_temp
        data_temp = [name_temp, value]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
        temp_values = temp_values.append(temp_df, ignore_index = True)
        
        ##Calculating the electricity consumption of the fan 
        name_temp = ct_id + '_elect_fan'
        value = perc_fan[i] * elect_max_fan 
        data_temp = [name_temp, value]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
        temp_values = temp_values.append(temp_df, ignore_index = True)
        
        ##Calculating the make up water needed 
        name_temp = ct_id + '_water_cons'     
        value = (0.0027 + (0.01 * (del_t_temp/5.6))) * flow_rate_to_each_tower * make_up_water_correct_coeff
        data_temp = [name_temp, value]
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value'])
        temp_values = temp_values.append(temp_df, ignore_index = True)

    for i in range (0, towers_in_config):
        ##Writing values in a dictionary  
        return_values[temp_values['Name'][(i * 3) + 0]] = temp_values['Value'][(i * 3) + 0]
        return_values[temp_values['Name'][(i * 3) + 1]] = temp_values['Value'][(i * 3) + 1]
        return_values[temp_values['Name'][(i * 3) + 2]] = temp_values['Value'][(i * 3) + 2]
        ##Writing values in a dataframe 
        data_temp = [temp_values['Name'][(i * 3) + 0], temp_values['Value'][(i * 3) + 0], 'K']
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
        return_values_df = return_values_df.append(temp_df, ignore_index = True)
        
        data_temp = [temp_values['Name'][(i * 3) + 1], temp_values['Value'][(i * 3) + 1], 'kWh']
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
        return_values_df = return_values_df.append(temp_df, ignore_index = True)
        
        data_temp = [temp_values['Name'][(i * 3) + 2], temp_values['Value'][(i * 3) + 2], 'm3/h']
        temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
        return_values_df = return_values_df.append(temp_df, ignore_index = True)
        
    ##Computing the temperature of water exiting the configuration
#    t_config_out = 0
#    for i in range (0, towers_in_config):
#        t_config_out = t_config_out + ((1 / towers_in_config) * temp_values['Value'][(i * 3) + 0])
#
#    return_values['t_out_config'] = t_config_out
#    data_temp = ['t_out_config', t_config_out, 'K']
#    temp_df = pd.DataFrame(data = [data_temp], columns = ['Name', 'Value', 'Unit'])   
#    return_values_df = return_values_df.append(temp_df, ignore_index = True)  
    
    return return_values, return_values_df, del_t_coeff_temp

################################################################################################################################################################
################################################################################################################################################################
##Add-on functions

##A function to calculate the delta t of a tower unit using the universal engineering model 
def delT_calc (ct_reg_coeff, ma, Twi, constants):
    ##Constants
    mw = constants[0]                      ##mw (m3/h)
    Twb = constants[1]                     ##Twb (K)
    
    ##Converting mw to kg/h
    mw = mw * 998.2    

    ##Calculated coefficients 
    b0 = ct_reg_coeff[0]	
    b1 = ct_reg_coeff[1]	
    b2 = ct_reg_coeff[2]	
    b3 = ct_reg_coeff[3]		
    b4 = ct_reg_coeff[4]	
    b5 = ct_reg_coeff[5]	 
    
    term1 = b0 * (Twi - Twb)
    if mw == 0:
        term2 = 0
        term4 = 0
        term6 = 0
    else:
        term2 = b1 * (ma / mw) * (Twi - Twb)
        term4 = b3 * pow((ma / mw), 2) * (Twi - Twb)
        term6 = b5 * (ma / mw) * pow((Twi - Twb), 2)
        
    term3 = b2 * pow((Twi - Twb), 2)
    term5 = b4 * pow((Twi - Twb), 3)
    
    delT_overall = term1 + term2 + term3 + term4 + term5 + term6

    return delT_overall
    
##A function which returns the regression coefficients for a single tower
def ct_reg_coeff_calc (ct_reg_coeff, twb, twi_min, twi_max, ma_min, ma_max, flow_mw_unit, fan_emax):

    import numpy as np 
    from sklearn import linear_model 
    
        
    ##To employ multi-variate regression analysis to find the relationship between variables
    ma_steps = 200 
    ma_interval = (ma_max - ma_min) / ma_steps  

    twi_steps = 200
    twi_interval = (twi_max - twi_min) / twi_steps

    mf_water = flow_mw_unit
    T_wetbulb = twb
    constants = [mf_water, T_wetbulb]
    
    valuesX = np.zeros((ma_steps * twi_steps, 5))
    valuesY = np.zeros((ma_steps * twi_steps, 1))
    
    row = 0
    for i in range (0,ma_steps):
        for j in range (0, twi_steps):
            valuesX[row, 0] = 0 #pow(ma_min + (i * ma_interval), 2)
            valuesX[row, 1] = ma_min + (i * ma_interval)
            valuesX[row, 2] = 0 #pow(twi_min + (j * twi_interval) , 2)
            valuesX[row, 3] = twi_min + (j * twi_interval)
            valuesX[row, 4] = (ma_min + (i * ma_interval)) + (twi_min + (j * twi_interval))
            valuesY[row ,0] = delT_calc(ct_reg_coeff, valuesX[row, 1], valuesX[row, 3], constants)
            row = row + 1
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(valuesX, valuesY)
    result_1 = clf.score(valuesX, valuesY, sample_weight=None)
    lin_coeff_1 = clf.coef_
    int_1 = clf.intercept_

    ##Since the idea is to express delta T as a function of Twi, ma and Twi * ma 
    ma_coeff = lin_coeff_1[0,1]
    twi_coeff = lin_coeff_1[0,3]
    matwi_coeff = lin_coeff_1[0,4]
    cst_term = int_1
    
    ##Determining the value for can coefficient 
    lin_fan_coeff = fan_emax / ma_max
    
    ##Initiating a matrix to hold the return values 
    
    ct_calc = np.zeros((5,1))
    
    ct_calc[0,0] = ma_coeff
    ct_calc[1,0] = twi_coeff
    ct_calc[2,0] = matwi_coeff
    ct_calc[3,0] = cst_term
    ct_calc[4,0] = lin_fan_coeff 
    
    return ct_calc
    
##A function to generate a lookup table of bilinear pieces 
def gen_bilinear_pieces (x_min, x_max, y_min, y_max, bilinear_pieces):
    import pandas as pd 
    u_table = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int'])
    v_table = pd.DataFrame(columns = ['lb', 'ub', 'grad', 'int']) 
    
    ##u_bounds 
    u_overall_min = x_min + y_min 
    u_overall_max = x_max + y_max
    ##y_bounds 
    v_overall_min = x_min - y_max
    v_overall_max = x_max - y_min 
    ##step_increment 
    u_step = (u_overall_max - u_overall_min) / bilinear_pieces
    v_step = (v_overall_max - v_overall_min) / bilinear_pieces

    for i in range (0, bilinear_pieces):
        ##Handling u values first 
        u_min = (i * u_step) + u_overall_min
        u_max = ((i + 1) * u_step) + u_overall_min
        fu_min = 0.25 * pow(u_min, 2)
        fu_max = 0.25 * pow(u_max, 2)
        u_grad = (fu_max - fu_min) / (u_max - u_min)
        u_int = fu_max - (u_grad * u_max)
        u_data = [u_min, u_max, u_grad, u_int]
        u_df = pd.DataFrame(data = [u_data], columns = ['lb', 'ub', 'grad', 'int'])
        u_table = u_table.append(u_df, ignore_index = True)
        ##Handling v values next 
        v_min = (i * v_step) + v_overall_min
        v_max = ((i + 1) * v_step) + v_overall_min
        fv_min = 0.25 * pow(v_min, 2)
        fv_max = 0.25 * pow(v_max, 2)
        v_grad = (fv_max - fv_min) / (v_max - v_min)
        v_int = fv_max - (v_grad * v_max)
        v_data = [v_min, v_max, v_grad, v_int]
        v_df = pd.DataFrame(data = [v_data], columns = ['lb', 'ub', 'grad', 'int'])
        v_table = v_table.append(v_df, ignore_index = True)        
        
    return u_table, v_table 
    
##A function to determine the estimated values of using bilinear pieces 
def search_bilin_table_for_values (u_table, v_table, x_actual, y_actual):
    
    ##Computing the actual values 
    u_actual = x_actual + y_actual 
    v_actual = x_actual - y_actual 
    ##Computing the number of iterations 
    dim_u_table = u_table.shape 
    dim_v_table = v_table.shape 
    
    for i in range (0, dim_u_table[0]):
        if (u_actual >= u_table['lb'][i]) and (u_actual <= u_table['ub'][i]):
            fu_calc = (u_actual * u_table['grad'][i]) + u_table['int'][i]
            break
    for i in range (0, dim_v_table[0]):
         if (v_actual >= v_table['lb'][i]) and (v_actual <= v_table['ub'][i]):
            fv_calc = (v_actual * v_table['grad'][i]) + v_table['int'][i]
            break       
        
    bilin_est = fu_calc - fv_calc

    return bilin_est