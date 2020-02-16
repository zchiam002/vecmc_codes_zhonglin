##The main script for the cooling tower testing 

def prepare_cooling_tower_coeff ():
    
    import numpy as np
    import pandas as pd
    
    ##Import the TWB data 
    weather_hl = pd.read_csv('C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\high_load\\high_demand_weather.csv')
    weather_ml = pd.read_csv('C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\mid_load\\mid_demand_weather.csv')    
    weather_ll = pd.read_csv('C:\\Optimization_zlc\\input_data\\paper_qe_testcase_input_data\\low_load\\low_demand_weather.csv')  
    
    dim_weather_hl = weather_hl.shape
    dim_weather_ml = weather_ml.shape
    dim_weather_ll = weather_ll.shape

    twb_array_hl = []
    twb_array_ml = []
    twb_array_ll = []
    
    for i in range (0, dim_weather_hl[0]):
        twb_array_hl.append(weather_hl['T_WB'][i])
        twb_array_ml.append(weather_ml['T_WB'][i])    
        twb_array_ll.append(weather_ll['T_WB'][i])
         
    flow = [407, 1476, 407+1476, 1476+1476, 407+1476+1476]    
    max_dt = 12
    steps = 2
    bilinear_pieces = 20
    
    ##The reference dataframe 
    cooling_tower_twb_coeff_hl = pd.DataFrame(columns = ['f0_twb', 'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 'f0_c4',
                                                         'f1_twb', 'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3', 'f1_c4',
                                                         'f2_twb', 'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3', 'f2_c4',
                                                         'f3_twb', 'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3', 'f3_c4',
                                                         'f4_twb', 'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3', 'f4_c4'])
    cooling_tower_twb_coeff_ml = pd.DataFrame(columns = ['f0_twb', 'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 'f0_c4',
                                                         'f1_twb', 'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3', 'f1_c4',
                                                         'f2_twb', 'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3', 'f2_c4',
                                                         'f3_twb', 'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3', 'f3_c4',
                                                         'f4_twb', 'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3', 'f4_c4'])    
    cooling_tower_twb_coeff_ll = pd.DataFrame(columns = ['f0_twb', 'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 'f0_c4',
                                                         'f1_twb', 'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3', 'f1_c4',
                                                         'f2_twb', 'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3', 'f2_c4',
                                                         'f3_twb', 'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3', 'f3_c4',
                                                         'f4_twb', 'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3', 'f4_c4'])    
    
    ##Dealing with high load data first 
    
    for i in range (0, dim_weather_hl[0]):
        
        print(i)
        temp_data = []
        for j in range (0, len(flow)):
            
            print(i, j)
            check = 0
            ##Finding the parameters which will not violate the conditions 
            twb = twb_array_hl[i] 
            
            while check == 0:
                print_dataframe_hl, del_t_coeff_temp = testing_one_cooling_tower (twb, max_dt, flow[j], steps, bilinear_pieces)
                check2 = 0
                for k in range (0, pow((steps + 1), 2)):
                    if print_dataframe_hl['ct1_water_cons'][k] < 0:
                        check2 = check2 + 1
                        twb = twb + 0.01
                if check2 == 0:
                    temp_data.append(twb)
                    temp_data.append(del_t_coeff_temp[0,0])                    
                    temp_data.append(del_t_coeff_temp[1,0]) 
                    temp_data.append(del_t_coeff_temp[2,0]) 
                    temp_data.append(del_t_coeff_temp[3,0]) 
                    temp_data.append(del_t_coeff_temp[4,0])                     
                    check = 1
            
        temp_df = pd.DataFrame(data = [temp_data], columns = ['f0_twb', 'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 'f0_c4',
                                                              'f1_twb', 'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3', 'f1_c4',
                                                              'f2_twb', 'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3', 'f2_c4',
                                                              'f3_twb', 'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3', 'f3_c4',
                                                              'f4_twb', 'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3', 'f4_c4'])
        cooling_tower_twb_coeff_hl = cooling_tower_twb_coeff_hl.append(temp_df, ignore_index = True)
        
    cooling_tower_twb_coeff_hl.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\ct_hl.csv')
    
    ##Dealing with the mid load 
    
    for i in range (0, dim_weather_ml[0]):
        
        print(i)
        temp_data = []
        for j in range (0, len(flow)):
            
            print(i, j)
            check = 0
            ##Finding the parameters which will not violate the conditions 
            twb = twb_array_ml[i] 
            
            while check == 0:
                print_dataframe_ml, del_t_coeff_temp = testing_one_cooling_tower (twb, max_dt, flow[j], steps, bilinear_pieces)
                check2 = 0
                for k in range (0, pow((steps + 1), 2)):
                    if print_dataframe_ml['ct1_water_cons'][k] < 0:
                        check2 = check2 + 1
                        twb = twb + 0.01
                if check2 == 0:
                    temp_data.append(twb)
                    temp_data.append(del_t_coeff_temp[0,0])                    
                    temp_data.append(del_t_coeff_temp[1,0]) 
                    temp_data.append(del_t_coeff_temp[2,0]) 
                    temp_data.append(del_t_coeff_temp[3,0]) 
                    temp_data.append(del_t_coeff_temp[4,0])                     
                    check = 1
            
        temp_df = pd.DataFrame(data = [temp_data], columns = ['f0_twb', 'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 'f0_c4',
                                                              'f1_twb', 'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3', 'f1_c4',
                                                              'f2_twb', 'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3', 'f2_c4',
                                                              'f3_twb', 'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3', 'f3_c4',
                                                              'f4_twb', 'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3', 'f4_c4'])
        cooling_tower_twb_coeff_ml = cooling_tower_twb_coeff_ml.append(temp_df, ignore_index = True)
        
    cooling_tower_twb_coeff_ml.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\ct_ml.csv')

    for i in range (0, dim_weather_ll[0]):
        
        print(i)
        temp_data = []
        for j in range (0, len(flow)):
            
            print(i, j)
            check = 0
            ##Finding the parameters which will not violate the conditions 
            twb = twb_array_ll[i] 
            
            while check == 0:
                print_dataframe_ll, del_t_coeff_temp = testing_one_cooling_tower (twb, max_dt, flow[j], steps, bilinear_pieces)
                check2 = 0
                for k in range (0, pow((steps + 1), 2)):
                    if print_dataframe_ll['ct1_water_cons'][k] < 0:
                        check2 = check2 + 1
                        twb = twb + 0.01
                if check2 == 0:
                    temp_data.append(twb)
                    temp_data.append(del_t_coeff_temp[0,0])                    
                    temp_data.append(del_t_coeff_temp[1,0]) 
                    temp_data.append(del_t_coeff_temp[2,0]) 
                    temp_data.append(del_t_coeff_temp[3,0]) 
                    temp_data.append(del_t_coeff_temp[4,0])                     
                    check = 1
            
        temp_df = pd.DataFrame(data = [temp_data], columns = ['f0_twb', 'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 'f0_c4',
                                                              'f1_twb', 'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3', 'f1_c4',
                                                              'f2_twb', 'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3', 'f2_c4',
                                                              'f3_twb', 'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3', 'f3_c4',
                                                              'f4_twb', 'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3', 'f4_c4'])
        cooling_tower_twb_coeff_ll = cooling_tower_twb_coeff_ll.append(temp_df, ignore_index = True)
        
    cooling_tower_twb_coeff_ll.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\ct_ll.csv')        
    return 

###########################################################################################################################################################
##Additional functions 

##To test the performance of cooling tower 
def testing_one_cooling_tower (twb, max_dt, flow, steps, bilinear_pieces):
    
    import pandas as pd 
    
    ##Assembling the return dataframe 
    print_dataframe = pd.DataFrame(columns = ['fan_perc', 'twi', 'ct1_t_out', 'ct1_elect_fan', 'ct1_water_cons', 'twb']) 
    
    for i in range (0, steps+1):
        ##Determining the step size for the fan
        fan_min = 0.05
        fan_max = 1
        fan_perc_ct1 = (i * (1/steps) * (fan_max - fan_min)) + fan_min
        
        for j in range (0, steps+1):
            ##Determining the step size for tin
            
            if twb > 15:
                tin_min = twb + 3
                tin_max = tin_min + max_dt 
                tin_curr = ((j * (1/steps) * (tin_max - tin_min)) + tin_min) + 273.15
                
                twi_min = 273.15 + tin_min       ##(Sensitive parameters, need to be taken care off...)
                twi_max = 273.15 + tin_max
            
            else:
                tin_min = 18 
                tin_max = 35 
                tin_curr = ((j * (1/steps) * (tin_max - tin_min)) + tin_min) + 273.15  
                
                twi_min = 273.15 + tin_min       ##(Sensitive parameters, need to be taken care off...)
                twi_max = 273.15 + tin_max
                
            perc_fan = [fan_perc_ct1, 0, 0, 0, 0]
            total_water_flow = flow
            twb1 = 273.15 + twb
        
            #return_values_1, return_values_df_1 = cooling_tower_uem (perc_fan, total_water_flow, tin_curr, twb1)
            #return_values_3, return_values_df_3, del_t_coeff_temp = cooling_tower_uem_reg(perc_fan, total_water_flow, tin_curr, twb1, twi_min, twi_max)
            return_values_3, return_values_df_3, del_t_coeff_temp = cooling_tower_uem_reg_lprelax (perc_fan, total_water_flow, tin_curr, twb1, twi_min, twi_max, bilinear_pieces)
        
            #print(return_values_df_1)
            #print(return_values_df_2)
            #print(return_values_df_3)

            temp_data = [fan_perc_ct1, tin_curr - 273.15, return_values_df_3['Value'][0] - 273.15, return_values_df_3['Value'][1], return_values_df_3['Value'][2], twb1-273.15]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['fan_perc', 'twi', 'ct1_t_out', 'ct1_elect_fan', 'ct1_water_cons', 'twb'])
            print_dataframe = print_dataframe.append(temp_df, ignore_index = True)
   
    return print_dataframe, del_t_coeff_temp

##Single cooling tower script
def cooling_tower_uem_reg_lprelax (perc_fan, total_water_flow_config, tw_in, twb, twi_min, twi_max, bilinear_pieces):
    
    import pandas as pd 
    
    ##perc_fan[0] --- the percentage at which the cooling tower 1's fan is operated (0 - 100 %)
    ##total_water_flow_config --- the total flowrate of water into the configuration 
    ##tw_in --- the temperature of water into the cooling tower configuration 
    ##twb --- the ambient wet_bulb temperature 
    
    ##Cooling tower regression derived coefficients
    
#    b0 = 0.23382397 	
#    b1 = -0.03876029 	
#    b2 = -0.03298896 	
#    b3 = 0.00113387	
#    b4 = -0.00416801
#    b5 = 0.42846231
    b0 = 0.14029549639345207	          ##GA determined
    b1 = 0.600266127023157	
    b2 = -0.0211475692653011	
    b3 = 0.2792094538127389	
    b4 = 9.294683422723725*pow(10, -4)
    b5 = 0.16052557022400754
    
    make_up_water_correct_coeff = 2.3294122
    
    ct_reg_coeff = [b0, b1, b2, b3, b4, b5]
    towers_in_config = 1
    flow_rate_to_each_tower = total_water_flow_config / 5
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

###########################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    prepare_cooling_tower_coeff ()
