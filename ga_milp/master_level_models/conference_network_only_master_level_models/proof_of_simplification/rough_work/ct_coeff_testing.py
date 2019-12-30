##This script validates the coefficients of the which were geerated for the MILP process
##This script also validates the range at which the cooling tower is to be optimized

def ct_coeff_testing ():
    
    import numpy as np 
    import pandas as pd 
    
    #Importing data 
    high_load_coeff = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\ct_hl.csv')
    mid_load_coeff = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\ct_ml.csv')
    low_load_coeff = pd.read_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\look_up_tables\\ct_ll.csv')    
    
    dim_high_load_coeff = high_load_coeff.shape 
    
    flow_range = [407, 1476, 407+1476, 1476+1476, 407+1476+1476]  
    
    ##Assembling the datafrom he test 
    test_hl_results = pd.DataFrame(columns = ['flow', 'Hour', 'Twb', 'check_flow'])
    
    for i in range (0, 5):
        
        flow_curr = flow_range[i]
        
        ##Testing high load coefficients first 
        for j in range (0, dim_high_load_coeff[0]):
            
            print('hl', i, j)
            twb_curr = high_load_coeff['f' + str(i) + '_twb'][j]
            c0_curr = high_load_coeff['f' + str(i) + '_c0'][j]
            c1_curr = high_load_coeff['f' + str(i) + '_c1'][j]
            c2_curr = high_load_coeff['f' + str(i) + '_c2'][j]
            c3_curr = high_load_coeff['f' + str(i) + '_c3'][j]
            c4_curr = high_load_coeff['f' + str(i) + '_c4'][j]
            
            reduced_coefficients = [twb_curr, c0_curr, c1_curr, c2_curr, c3_curr, c4_curr]
            return_flow = test_cooling_tower_function(reduced_coefficients, flow_curr, j)
            test_hl_results = test_hl_results.append(return_flow, ignore_index = True)
        

    ##Saving the return results to csv format 
    test_hl_results.to_csv('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\proof_of_simplification\\rough_work\\hl_results.csv')
    
    return

#######################################################################################################################
##Additional functions 


def test_cooling_tower_function(reduced_coefficients, flow, hour):
    
    import sys 
    sys.path.append('C:\\Optimization_zlc\\master_level_models\\paper_qe_testcase_master_level_models\\')
    import pandas as pd 
    
    #testing_one_cooling_tower_modified (twb, max_dt, flow, steps, bilinear_pieces)
    #return print_dataframe, del_t_coeff_temp

    bilinear_pieces = 20 
    steps = 3
    max_dt = 12 
       
    twb = reduced_coefficients[0]
    print_dataframe, del_t_coeff_temp = testing_one_cooling_tower_modified (twb, max_dt, flow, steps, bilinear_pieces, reduced_coefficients)
    
    return_flow = pd.DataFrame(columns = ['flow', 'Hour', 'Twb', 'check_flow']) 
    for i in range (0, pow(steps+1,2)):
        check_flow_curr = print_dataframe['ct1_water_cons'][i]
        temp_data = [flow, hour, twb, check_flow_curr]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['flow', 'Hour', 'Twb', 'check_flow'])
        return_flow = return_flow.append(temp_df, ignore_index = True)
    
    return return_flow

##To test the performance of cooling tower with gicen reduced coefficients
def testing_one_cooling_tower_modified (twb, max_dt, flow, steps, bilinear_pieces, reduced_coefficients):
    
    import pandas as pd 
    import sys
    
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
            return_values_3, return_values_df_3, del_t_coeff_temp = cooling_tower_uem_reg_lprelax_modified (perc_fan, total_water_flow, tin_curr, twb1, twi_min, twi_max, bilinear_pieces, reduced_coefficients)
        
            #print(return_values_df_1)
            #print(return_values_df_2)
            #print(return_values_df_3)

            temp_data = [fan_perc_ct1, tin_curr - 273.15, return_values_df_3['Value'][0] - 273.15, return_values_df_3['Value'][1], return_values_df_3['Value'][2], twb1-273.15]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['fan_perc', 'twi', 'ct1_t_out', 'ct1_elect_fan', 'ct1_water_cons', 'twb'])
            print_dataframe = print_dataframe.append(temp_df, ignore_index = True)
            #print(return_values_df_3)
            #print(print_dataframe)
#            sys.exit()
    return print_dataframe, del_t_coeff_temp

##Single cooling tower script with reduced coefficients
def cooling_tower_uem_reg_lprelax_modified (perc_fan, total_water_flow_config, tw_in, twb, twi_min, twi_max, bilinear_pieces, reduced_coefficients):
    
    import pandas as pd 
    
    ##perc_fan[0] --- the percentage at which the cooling tower 1's fan is operated (0 - 100 %)
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
#    b0 = 0.14029549639345207	          ##GA determined
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
        del_t_coeff_temp = ct_reg_coeff_calc_modified (ct_reg_coeff, twb, twi_min, twi_max, min_air_flow, max_air_flow, flow_rate_to_each_tower, elect_max_fan, reduced_coefficients)
        ##Generating the bilinear pieces 
        ma_table, twi_table = gen_bilinear_pieces (min_air_flow, max_air_flow, twi_min, twi_max, bilinear_pieces)
        bilin_est = search_bilin_table_for_values (ma_table, twi_table, flow_ma_temp, tw_in)
#        print('del_t_coeff_temp', del_t_coeff_temp)
#        print('flow_ma_temp', flow_ma_temp)
#        print('tw_in', tw_in)
#        print('bilin_est', bilin_est)
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

##A function which returns the regression coefficients for a single tower
def ct_reg_coeff_calc_modified (ct_reg_coeff, twb, twi_min, twi_max, ma_min, ma_max, flow_mw_unit, fan_emax, reduced_coefficients):

    import numpy as np
    
    ##Initiating a matrix to hold the return values 
    
    ct_calc = np.zeros((5,1))
    
    ct_calc[0,0] = reduced_coefficients[1]                          #ma_coeff
    ct_calc[1,0] = reduced_coefficients[2]                          #twi_coeff
    ct_calc[2,0] = reduced_coefficients[3]                          #matwi_coeff
    ct_calc[3,0] = reduced_coefficients[4]                          #cst_term
    ct_calc[4,0] = reduced_coefficients[5]                          #lin_fan_coeff 

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
    ct_coeff_testing ()