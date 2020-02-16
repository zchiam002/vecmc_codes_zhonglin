##This file contains all additional functions needed to generate the error plots 

##Calculate electricity based on UEM alone 
def calc_elect_uem_only (ct_raw_data, ct_reg_coeff):
    
    import pandas as pd 
    
    dim_ct_raw_data = ct_raw_data.shape 
    
    for i in range (0, dim_ct_raw_data[0]):
        
        tin = ct_raw_data['Tin_ct'][i]
        tout = ct_raw_data['Tout_ct'][i]
        twb = ct_raw_data['T_wb'][i]
        mw = ct_raw_data['mw_ct'][i] * 998.2
        
        z = tin - twb
        y = (tin - tout) / (tin - twb)
        
        term_a = ct_reg_coeff[3]
        term_b = ct_reg_coeff[1] + (ct_reg_coeff[5] * z)
        term_c = ct_reg_coeff[0] + (ct_reg_coeff[2] * z) + (ct_reg_coeff[4] * pow(z,2)) - y
        
        inside = pow(term_b, 2) - (4 * term_a * term_c)
        inside = pow(inside, 0.5)
        
        x1 = (-term_b + inside) / (2 * term_a)
        x2 = (-term_b - inside) / (2 * term_a)
        
        e1 = (x1 * 22  * mw) / (369117)
        e2 = (x2 * 22  * mw) / (369117)        
        print(e1 , e2)
    
    
    return

## This function cleans the raw data for the cooling towers
def cleaning_cooling_tower_raw_data_single_tower ():
    import pandas as pd 
    
    ##Importing data 
    ct_raw_data = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\historical_data\\New folder\\raw_data_csv\\cooling_tower_raw_data.csv')
    chiller_raw_data = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\historical_data\\New folder\\raw_data_csv\\chiller_raw_data.csv')
    weather_raw_data = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\historical_data\\New folder\\raw_data_csv\\weather_data_raw.csv')
    
    ##Cleaning 
    dim_ct_raw_data = ct_raw_data.shape 
    
    column_names = ['Day of week', 'Date', 'Month', 'Year', 'Hour	', 'Tin_ct', 'Tout_ct', 'mw_ct', 'T_db', 'Hum_perc', 'T_wb', 'E']
    return_df = pd.DataFrame(columns = column_names)
    
    tower_number = 2
    
    for i in range (0, dim_ct_raw_data[0]):
        
        if (ct_raw_data['Tin_ct'][i] != '???') and (chiller_raw_data['Ch1_mcond'][i] != '???'):
            delt = float(ct_raw_data['Tin_ct'][i]) - float(ct_raw_data['Tout_ct' + str(tower_number)][i])
            power = float(ct_raw_data['Ct' + str(tower_number) + '_power'][i])
            flow = (float(chiller_raw_data['Ch1_mcond'][i]) + float(chiller_raw_data['Ch2_mcond'][i]) + float(chiller_raw_data['Ch3_mcond'][i])) / 5
            approach = float(ct_raw_data['Tin_ct'][i]) - weather_raw_data['T_wb'][i]
            
            if (delt > 0) and (power > 0) and (flow > 0) and (approach > 0):
                if (delt > approach):
                    temp_data = [float(ct_raw_data['Day of week'][i]), float(ct_raw_data['Date'][i]), float(ct_raw_data['Month'][i]), float(ct_raw_data['Year '][i]), float(ct_raw_data['Hour'][i]),
                                 float(ct_raw_data['Tin_ct'][i]), float(ct_raw_data['Tout_ct' + str(tower_number)][i]), flow, weather_raw_data['T_db'][i], weather_raw_data['Hum_r'][i],
                                 weather_raw_data['T_wb'][i], float(ct_raw_data['Ct' + str(tower_number) + '_power'][i])]
                    temp_df = pd.DataFrame(data = [temp_data], columns = column_names)
                    return_df = return_df.append(temp_df, ignore_index = True)
    
    return return_df



## Calibrating based on electricity consumption 
def calibrate_cooling_tower_model_based_elect ():
    import os
    import numpy as np
    import pandas as pd
    from sklearn import linear_model 
    
    ##Importing data 
    #ct_raw_data = cleaning_cooling_tower_raw_data_single_tower ()
    ct_raw_data = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\historical_data\\New folder\\cleansed_csv\\cooling_tower_cleansed.csv')
    column_names = ['Day of week', 'Date', 'Month', 'Year ', 'Hour', 'Tin_ct', 'Tout_ct', 'mw_ct', 'T_db', 'Hum_perc', 'T_wb', 'E']
    
    ##Removing useless data 
    dim_ct_raw_data = ct_raw_data.shape 
    
    if os.path.exists('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_testing\\ct_cleansed_3.csv'):
        ct_data_cleansed = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_testing\\ct_cleansed_3.csv')
    else:
        ct_data_cleansed = pd.DataFrame(columns = column_names)    
        for i in range (0, dim_ct_raw_data[0]):
            if (ct_raw_data['Tin_ct'][i] - ct_raw_data['T_wb'][i]) > 0:
                effectiveness = (ct_raw_data['Tin_ct'][i] - ct_raw_data['Tout_ct'][i]) / (ct_raw_data['Tin_ct'][i] - ct_raw_data['T_wb'][i])
                if (effectiveness < 1) and (ct_raw_data['E'][i] > 5):
                    temp_data = [ct_raw_data[column_names[0]][i], ct_raw_data[column_names[1]][i], ct_raw_data[column_names[2]][i], ct_raw_data[column_names[3]][i],
                                 ct_raw_data[column_names[4]][i], ct_raw_data[column_names[5]][i], ct_raw_data[column_names[6]][i], ct_raw_data[column_names[7]][i],
                                 ct_raw_data[column_names[8]][i], ct_raw_data[column_names[9]][i], ct_raw_data[column_names[10]][i], ct_raw_data[column_names[11]][i]]
                    temp_df = pd.DataFrame(data = [temp_data], columns = column_names)
                    ct_data_cleansed  = ct_data_cleansed.append(temp_df, ignore_index = True)
        ct_data_cleansed.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_testing\\ct_cleansed_3.csv')
    
    ##Assembling data for calibration of the cooling tower regression based coefficients 
    dim_ct_data_cleansed = ct_data_cleansed.shape
    valuesX = np.zeros((dim_ct_data_cleansed[0], 6))
    valuesY = np.zeros((dim_ct_data_cleansed[0], 1)) 
    
    for i in range (0, dim_ct_data_cleansed[0]):
        e = ct_data_cleansed['E'][i] 
        mw = ct_data_cleansed['mw_ct'][i] * 998.2
        tin = ct_data_cleansed['Tin_ct'][i]
        tout = ct_data_cleansed['Tout_ct'][i]
        twb = ct_data_cleansed['T_wb'][i]
        
        valuesX[i, 0] = tin - twb
        valuesX[i, 1] = ((369117 * e) / (22 * mw)) * (tin - twb)
        valuesX[i, 2] = pow((tin - twb), 2)
        valuesX[i, 3] = pow(((369117 * e) / (22 * mw)), 2) * (tin - twb)
        valuesX[i, 4] = pow((tin - twb), 3)
        valuesX[i, 5] = ((369117 * e) / (22 * mw)) * pow((tin - twb), 2)   
        valuesY[i, 0] = tin - tout

    clf = linear_model.LinearRegression(fit_intercept = False)
    clf.fit(valuesX, valuesY)
    result_1 = clf.score(valuesX, valuesY, sample_weight=None)
    lin_coeff_1 = clf.coef_
    int_1 = clf.intercept_
#
#    print(lin_coeff_1)   
#    print(int_1)
#    print(result_1)
    
    ct_reg_coeff = [lin_coeff_1[0, 0], lin_coeff_1[0, 1], lin_coeff_1[0, 2], lin_coeff_1[0, 3], lin_coeff_1[0, 4], lin_coeff_1[0, 5]]    
    
    return ct_reg_coeff

##Manually calibrate the regression coefficients, as thye were masked by bad data  
def process_ct_data_manual_calibrate (model_vs_raw_elect):
    
    import pandas as pd 
    
    ##model_vs_raw_elect --- the calculated information of the model and raw data 
    
    dim_model_vs_raw_elect = model_vs_raw_elect.shape
    
    return_df = pd.DataFrame(columns = ['elect_raw', 'elect_model', 'mae'])
    counter = 0
    for i in range (0, dim_model_vs_raw_elect[0]):
        if model_vs_raw_elect['elect_model'][i] < 21/1000:
            elect_raw = model_vs_raw_elect['elect_raw'][i]
            elect_model = model_vs_raw_elect['elect_model'][i]
#            elect_model = 1000 * model_vs_raw_elect['elect_model'][i]
#            elect_model = 1.2 * (elect_raw/22) * elect_model
            mae = 100 * abs(elect_raw - elect_model) / elect_raw
            
            temp_data = [elect_raw, elect_model, mae]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['elect_raw', 'elect_model', 'mae'])
            return_df = return_df.append(temp_df, ignore_index = True)
            counter = counter + 1
        
    ##Calculating the average MAE
    total_error = sum(return_df['mae'][:])
    ave_error = total_error / counter
    
#    print('Average MAE: ', ave_error)

    return return_df


##This function to calibrate the cooling tower coefficients for the UEM
def calibrate_cooling_tower_model ():
 
    import os
    import numpy as np
    import pandas as pd
    from sklearn import linear_model 
    
    ##Importing data 
    ct_raw_data = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\historical_data\\New folder\\cleansed_csv\\cooling_tower_cleansed.csv')
    column_names = ['Day of week', 'Date', 'Month', 'Year ', 'Hour', 'Tin_ct', 'Tout_ct', 'mw_ct', 'T_db', 'Hum_perc', 'T_wb', 'E']
    
    ##Removing useless data 
    dim_ct_raw_data = ct_raw_data.shape 
    
    if os.path.exists('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_testing\\ct_cleansed_2.csv'):
        ct_data_cleansed = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_testing\\ct_cleansed_2.csv')
    else:
        ct_data_cleansed = pd.DataFrame(columns = column_names)    
        for i in range (0, dim_ct_raw_data[0]):
            if (ct_raw_data['Tin_ct'][i] - ct_raw_data['T_wb'][i]) > 0:
                effectiveness = (ct_raw_data['Tin_ct'][i] - ct_raw_data['Tout_ct'][i]) / (ct_raw_data['Tin_ct'][i] - ct_raw_data['T_wb'][i])
                if (effectiveness < 1) and (ct_raw_data['E'][i] > 2):
                    temp_data = [ct_raw_data[column_names[0]][i], ct_raw_data[column_names[1]][i], ct_raw_data[column_names[2]][i], ct_raw_data[column_names[3]][i],
                                 ct_raw_data[column_names[4]][i], ct_raw_data[column_names[5]][i], ct_raw_data[column_names[6]][i], ct_raw_data[column_names[7]][i],
                                 ct_raw_data[column_names[8]][i], ct_raw_data[column_names[9]][i], ct_raw_data[column_names[10]][i], ct_raw_data[column_names[11]][i]]
                    temp_df = pd.DataFrame(data = [temp_data], columns = column_names)
                    ct_data_cleansed  = ct_data_cleansed.append(temp_df, ignore_index = True)
        ct_data_cleansed.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_testing\\ct_cleansed_2.csv')
    
    ##Assembling data for calibration of the cooling tower regression based coefficients 
    dim_ct_data_cleansed = ct_data_cleansed.shape
    valuesX = np.zeros((dim_ct_data_cleansed[0], 5))
    valuesY = np.zeros((dim_ct_data_cleansed[0], 1)) 
    
    for i in range (0, dim_ct_data_cleansed[0]):
        ma = (ct_data_cleansed['E'][i] / 22) * 369117
        mw = ct_data_cleansed['mw_ct'][i] * 998.2
        tin = ct_data_cleansed['Tin_ct'][i]
        tout = ct_data_cleansed['Tout_ct'][i]
        twb = ct_data_cleansed['T_wb'][i]
        
        valuesX[i, 0] = ma / mw
        valuesX[i, 1] = tin - twb
        valuesX[i, 2] = pow((ma / mw), 2)
        valuesX[i, 3] = pow((tin - twb), 2)
        valuesX[i, 4] = (ma / mw) * (tin - twb)
        valuesY[i ,0] = (tin - tout) / (tin - twb)        

    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(valuesX, valuesY)
    result_1 = clf.score(valuesX, valuesY, sample_weight=None)
    lin_coeff_1 = clf.coef_
    int_1 = clf.intercept_

    print(lin_coeff_1)   
    print(int_1)
    print(result_1)
    
    ct_reg_coeff = [int_1[0], lin_coeff_1[0, 0], lin_coeff_1[0, 1], lin_coeff_1[0, 2], lin_coeff_1[0, 3], lin_coeff_1[0, 4]]

    return ct_reg_coeff



##This function calculates the electricity consumed by the cooling tower model and compares it to the raw data 
def ct_model_elect_calc (ct_raw_data, ct_reg_coeff):
    
    import pandas as pd 
    import sys
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_testing\\')
    from cooling_tower_main_models import ct_reg_coeff_calc_new
    from cooling_tower_main_models import cooling_tower_uem_reg_lprelax
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from cooling_tower_models import gen_bilinear_pieces 
    
    dim_ct_raw_data = ct_raw_data.shape 

    ##Hyper parameters 
    min_air_flow = 0            ##kg/h
    max_air_flow = 369117       ##kg/h
    
    ##Electricity coefficient 
    elect_coeff = 22 / max_air_flow 
    
    ##Initialize a dataframe to hold return data 
    return_df = pd.DataFrame(columns = ['elect_raw', 'elect_model', 'mae'])
    counter = 0
    bilinear_pieces = 12
    ma_table, twi_table = gen_bilinear_pieces (min_air_flow, max_air_flow, 284, 309, bilinear_pieces)    
    
    for i in range (0, dim_ct_raw_data[0]):

        if ct_raw_data['E'][i] > 0:
            if ct_raw_data['E'][i] <= 22:
                ct_calc = ct_reg_coeff_calc_new (ct_reg_coeff, ct_raw_data['T_wb'][i], 284, 309, min_air_flow, max_air_flow, ct_raw_data['mw_ct'][i] * 998.2) 

        #        ct_calc[0,0] = ma_coeff
        #        ct_calc[1,0] = twi_coeff
        #        ct_calc[2,0] = matwi_coeff
        #        ct_calc[3,0] = cst_term
                curr_air = (ct_raw_data['E'][i] / 22) * max_air_flow
                delt_reg_bilin = cooling_tower_uem_reg_lprelax (curr_air, ct_raw_data['mw_ct'][i], ct_raw_data['Tin_ct'][i], ct_raw_data['T_wb'][i], bilinear_pieces, 
                                                                ct_calc, ma_table, twi_table)                           

                upp = delt_reg_bilin - (ct_calc[1,0] * ct_raw_data['Tin_ct'][i]) - ct_calc[3,0]
                low = ct_calc[0,0] + (ct_calc[2,0] * ct_raw_data['Tin_ct'][i])
                
                model_air = upp / low
                model_elect = model_air * elect_coeff
            else:
                model_elect = 22
            
            mae = 100 * abs(ct_raw_data['E'][i] - model_elect) / ct_raw_data['E'][i]
            
            temp_data = [ct_raw_data['E'][i], model_elect, mae]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['elect_raw', 'elect_model', 'mae'])
            
            return_df = return_df.append(temp_df, ignore_index = True)
            counter = counter + 1
            print(i , 'of', dim_ct_raw_data[0])
    
    total_error = sum(return_df['mae'][:])
    ave_error = total_error / counter 
    #print('Average MAE: ', ave_error)
    
    return return_df


##This function calculates the model vs raw data of the cooling tower inputs and outputs for the bilinear case
def ct_model_vs_raw_bilin (ct_raw_data, ct_reg_coeff):
    
    import pandas as pd 
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_testing\\')
    from cooling_tower_main_models import cooling_tower_uem_reg_lprelax
    from cooling_tower_main_models import ct_reg_coeff_calc_new
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from cooling_tower_models import gen_bilinear_pieces    
    
    dim_ct_raw_data = ct_raw_data.shape 

    ##Hyper parameters 
    min_air_flow = 0            ##kg/h
    max_air_flow = 369117       ##kg/h
    
    bilinear_pieces = 12
    
    ##Initiate a dataframe to hold the return values 
    return_df = pd.DataFrame(columns= ['dt_raw', 'dt_model', 'mae_error'])
    counter = 0
    ma_table, twi_table = gen_bilinear_pieces (min_air_flow, max_air_flow, 284, 309, bilinear_pieces)    
    
    for i in range (0, dim_ct_raw_data[0]):
    
        ct_calc = ct_reg_coeff_calc_new (ct_reg_coeff, ct_raw_data['T_wb'][i], 284, 309, min_air_flow, max_air_flow, ct_raw_data['mw_ct'][i]*998.2)
    
        if ct_raw_data['E'][i] <= 22:
            curr_air = (ct_raw_data['E'][i] / 22) * max_air_flow 
        else:
            curr_air = max_air_flow
            
        delt_reg_bilin = cooling_tower_uem_reg_lprelax (curr_air, ct_raw_data['mw_ct'][i], ct_raw_data['Tin_ct'][i], ct_raw_data['T_wb'][i], bilinear_pieces, 
                                                        ct_calc, ma_table, twi_table)   
        delt_raw = ct_raw_data['Tin_ct'][i] - ct_raw_data['Tout_ct'][i]

        mae_error = 100 * abs(delt_raw - delt_reg_bilin) / delt_raw

        temp_data = [delt_raw, delt_reg_bilin, mae_error]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['dt_raw', 'dt_model', 'mae_error'])
        return_df = return_df.append(temp_df, ignore_index = True)
        counter = counter + 1
        
        print(str(counter) + ' of ' + str(dim_ct_raw_data[0]))
        
    ##Calcluating error 
    total_error = sum(return_df['mae_error'][:])
    mae_error_ave = total_error / counter 
    #print('Average MAE error: ', mae_error_ave)
    
    return return_df


##This function deletes errorneous data for thr distribution network pump
def del_error_dist_model_results (model_vs_raw):
    
    import pandas as pd 
    
    ##model_vs_raw --- dataframe of branch flows model and raw data elect cons 
    
    dim_model_vs_raw = model_vs_raw.shape 
    
    ##Initiate a new dataframe to hold the 'cleansed data'
    return_df = pd.DataFrame(columns = ['gv2_flow', 'hsb_flow', 'pfa_flow', 'ser_flow', 'pump_power', 'pump_power_model', 'mae_error'])
    counter = 0
    
    for i in range (0, dim_model_vs_raw[0]):
        if (model_vs_raw['pump_power'][i] < 80) and (model_vs_raw['pump_power'][i] > 20):
            
            model_calc = ((0.50 * model_vs_raw['pump_power_model'][i]) + 17.5)
            mae_error = 100 * abs(model_vs_raw['pump_power'][i] - model_calc) / model_calc  
                        
            temp_data = [model_vs_raw['gv2_flow'][i], model_vs_raw['hsb_flow'][i], model_vs_raw['pfa_flow'][i], model_vs_raw['ser_flow'][i], model_vs_raw['pump_power'][i],
                         model_calc, mae_error]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['gv2_flow', 'hsb_flow', 'pfa_flow', 'ser_flow', 'pump_power', 'pump_power_model', 'mae_error'])
            return_df = return_df.append(temp_df, ignore_index = True)
            counter = counter + 1

    total_error = sum(return_df['mae_error'][:])
    ave_error = total_error / counter
    #print('Average MAE: ', ave_error)        
    
    ##Removing points with higher thanx% mae error 
    dim_return_df = return_df.shape
    return_df_final = pd.DataFrame(columns = ['gv2_flow', 'hsb_flow', 'pfa_flow', 'ser_flow', 'pump_power', 'pump_power_model', 'mae_error'])
    counter_1 = 0
    
    for i in range (0, dim_return_df[0]):
        if return_df['mae_error'][i] < 30:
            temp_data = [return_df['gv2_flow'][i], return_df['hsb_flow'][i], return_df['pfa_flow'][i], return_df['ser_flow'][i], return_df['pump_power'][i],
                         return_df['pump_power_model'][i], return_df['mae_error'][i]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['gv2_flow', 'hsb_flow', 'pfa_flow', 'ser_flow', 'pump_power', 'pump_power_model', 'mae_error'])
            return_df_final = return_df_final.append(temp_df, ignore_index = True)
            counter_1 = counter_1 + 1            
    
    total_error = sum(return_df_final['mae_error'][:])
    ave_error = total_error / counter
    #print('Average MAE cleansed: ', ave_error)  

    return return_df_final


##This is a counter to determine the pump which is utilized the most 
def determine_pump_with_most_data_dist (pump_data):
    
    import pandas as pd 
    
    ##pump_data --- the electricity data from the pump
    
    dim_pump_data = pump_data.shape 
    
    ##Initiating an array counter 
    counter = pd.DataFrame(columns = ['af11_power', 'af12_power', 'af21_power', 'af22_power', 'af31_power',	'af32_power',	'af33_power'])
    counter_list = [0, 0, 0, 0, 0, 0, 0]
    
    for i in range (0, dim_pump_data[0]):
        if pump_data['af11_power'][i] > 0:
            counter_list[0] = counter_list[0] + 1
        if pump_data['af12_power'][i] > 0:
            counter_list[1] = counter_list[1] + 1        
        if pump_data['af21_power'][i] > 0:
            counter_list[2] = counter_list[2] + 1      
        if pump_data['af22_power'][i] > 0:
            counter_list[3] = counter_list[3] + 1
        if pump_data['af31_power'][i] > 0:
            counter_list[4] = counter_list[4] + 1 
        if pump_data['af32_power'][i] > 0:
            counter_list[5] = counter_list[5] + 1
        if pump_data['af33_power'][i] > 0:
            counter_list[6] = counter_list[6] + 1
            
    temp_df = pd.DataFrame(data = [counter_list], columns = ['af11_power', 'af12_power', 'af21_power', 'af22_power', 'af31_power',	'af32_power',	'af33_power'])
    counter = counter.append(temp_df)
    
    print(counter)
    return 

##Combine AF32 and 33 and calculate the associated pressure drop using the pwl model
def combine_af32_33_calc_elect (pump_data, client_load):
    
    import pandas as pd
    import sys 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\pump_nwk_testing\\')
    from dist_nwk_error_main import dist_nwk_pwl_elect
    
    ##pump_data --- the electricity data from the pump 
    ##client_load --- the client load, temperature and flow characteristics
    
    pwl = 4         ##The number of piecewise linear pieces
    
    ##Combine pump_data 32_33
        ##Initiate the dataframe, while picking the right data
    column_names = ['gv2_flow', 'hsb_flow', 'pfa_flow', 'ser_flow', 'pump_power', 'pump_power_model']
    return_df = pd.DataFrame(columns = column_names)
    
    dim_pump_data = pump_data.shape 
    
    for i in range (0, dim_pump_data[0]):
        total_flow = client_load['Gv2_flow'][i] + client_load['Hsb_flow'][i] + client_load['Pfa_flow'][i] + client_load['Ser_flow'][i]
        total_power = pump_data['af32_power'][i] + pump_data['af33_power'][i]
        if (total_flow > 0) and (total_power > 0):
            ##Calculating the associated pressure drop 
            nwk_pressure = calc_pwl_pressure_drop (pwl, client_load['Gv2_flow'][i], client_load['Hsb_flow'][i], client_load['Pfa_flow'][i], client_load['Ser_flow'][i])
            calc_elect_cons = dist_nwk_pwl_elect (total_flow, nwk_pressure, pwl, 40)
            
            temp_data = [client_load['Gv2_flow'][i], client_load['Hsb_flow'][i], client_load['Pfa_flow'][i], client_load['Ser_flow'][i], total_power, calc_elect_cons]
            temp_df = pd.DataFrame(data = [temp_data], columns = column_names)
            return_df = return_df.append(temp_df, ignore_index = True)
            
    return return_df

##This function calculates the piecewise pressure for the distribution network 
def calc_pwl_pressure_drop (pwl, gv2_flow, hsb_flow, pfa_flow, ser_flow):
    
    ##pwl --- the number of piecewise linear pieces
    ##gv2_flow --- the flow in gv2 branch 
    ##hsb_flow --- the flow in hsb branch 
    ##pfa_flow --- the flow in pfa branch 
    ##ser_flow --- the flow in ser branch 

    ##Preparing the linear coefficients 
    ice_nwk_calc, gv2_nwk_calc, hsb_nwk_calc, pfa_nwk_calc, ser_nwk_calc, tro_nwk_calc = pwl_pressure_drop_prep_coeff (pwl, gv2_flow, hsb_flow, pfa_flow, ser_flow)
    
    ice_pressure_check = 0
    gv2_pressure_check = 0
    hsb_pressure_check = 0
    tro_pressure_check = 0
    pfa_pressure_check = 0
    ser_pressure_check = 0
    
    ##Calculating the pressure drop in each branch 
    for i in range (0, pwl):
        ice_lb = ice_nwk_calc['lb'][i] * (gv2_flow + hsb_flow)
        ice_ub = ice_nwk_calc['ub'][i] * (gv2_flow + hsb_flow)
        gv2_lb = gv2_nwk_calc['lb'][i] * gv2_flow
        gv2_ub = gv2_nwk_calc['ub'][i] * gv2_flow
        hsb_lb = hsb_nwk_calc['lb'][i] * hsb_flow
        hsb_ub = hsb_nwk_calc['ub'][i] * hsb_flow
        tro_lb = tro_nwk_calc['lb'][i] * (pfa_flow + ser_flow)
        tro_ub = tro_nwk_calc['ub'][i] * (pfa_flow + ser_flow)
        pfa_lb = pfa_nwk_calc['lb'][i] * pfa_flow
        pfa_ub = pfa_nwk_calc['ub'][i] * pfa_flow
        ser_lb = ser_nwk_calc['lb'][i] * ser_flow
        ser_ub = ser_nwk_calc['ub'][i] * ser_flow
        
        ice_flow = gv2_flow + hsb_flow
        tro_flow = pfa_flow + ser_flow
    
        ##ice_nwk_pressure_drop
        if ice_flow == 0:
            ice_pres_drop = 0
            ice_pressure_check = 1            
        elif (ice_flow > ice_lb) and (ice_flow <= ice_ub) and (ice_pressure_check == 0):
            ice_pres_drop = (ice_nwk_calc['grad'][i] * ice_flow) + ice_nwk_calc['int'][i]
            ice_pressure_check = 1
            
        ##gv2_nwk_pressure_drop 
        if gv2_flow == 0:
            gv2_pres_drop = 0
            gv2_pressure_check = 1  
        elif (gv2_flow > gv2_lb) and (gv2_flow <= gv2_ub) and (gv2_pressure_check == 0):
            gv2_pres_drop = (gv2_nwk_calc['grad'][i] * gv2_flow) + gv2_nwk_calc['int'][i]
            gv2_pressure_check = 1

        ##hsb_nwk_pressure_drop
        if hsb_flow == 0:
            hsb_pres_drop = 0
            hsb_pressure_check = 1  
        elif (hsb_flow > hsb_lb) and (hsb_flow <= hsb_ub) and (hsb_pressure_check == 0):
            hsb_pres_drop = (hsb_nwk_calc['grad'][i] * hsb_flow) + hsb_nwk_calc['int'][i]
            hsb_pressure_check = 1
            
        ##tro_nwk_pressure_drop 
        if tro_flow == 0:
            tro_pres_drop = 0
            tro_pressure_check = 1  
        elif (tro_flow > tro_lb) and (tro_flow <= tro_ub) and (tro_pressure_check == 0):
            tro_pres_drop = (tro_nwk_calc['grad'][i] * tro_flow) + tro_nwk_calc['int'][i]
            tro_pressure_check = 1 
            
        ##pfa_nwk_pressure_drop
        if pfa_flow == 0:
            pfa_pres_drop = 0
            pfa_pressure_check = 1  
        elif (pfa_flow > pfa_lb) and (pfa_flow <= pfa_ub) and (pfa_pressure_check == 0):
            pfa_pres_drop = (pfa_nwk_calc['grad'][i] * pfa_flow) + pfa_nwk_calc['int'][i]
            pfa_pressure_check = 1
            
        ##ser_nwk_pressure_drop
        if ser_flow == 0:
            ser_pres_drop = 0
            ser_pressure_check = 1  
        elif (ser_flow > ser_lb) and (ser_flow <= ser_ub) and (ser_pressure_check == 0):
            ser_pres_drop = (ser_nwk_calc['grad'][i] * ser_flow) + ser_nwk_calc['int'][i]
            ser_pressure_check = 1        
    
    nwk_pressure = max((ice_pres_drop + gv2_pres_drop), (ice_pres_drop + hsb_pres_drop), (tro_pres_drop + pfa_pres_drop), (tro_pres_drop + ser_pres_drop))
    
    return nwk_pressure

##This fuction prepares the piecewise linear coefficients for the distribution network  
def pwl_pressure_drop_prep_coeff (pwl, gv2_flow, hsb_flow, pfa_flow, ser_flow):
    
    import numpy as np
    
    ##pwl --- the number of piecewise linear pieces
    ##gv2_flow --- the flow in gv2 branch 
    ##hsb_flow --- the flow in hsb branch 
    ##pfa_flow --- the flow in pfa branch 
    ##ser_flow --- the flow in ser branch 
    
    ##Friction coefficients 
    ice_main_coeff = 0.00011627906976743445
    gv2_coeff = 0.00034883720930232456
    hsb_coeff = 0.05046511627906977
    tro_main_coeff = 0.001162790697674419
    pfa_coeff = 0.0029069767441860417
    ser_coeff = 0.00023255813953487953
    
    ##Calculating the pwl_coefficients of each network 
    import sys 
    sys.path.append('C:\\Optimization_zlc\\slave_level_models\\paper_qe_testcase_slave_convex\\models\\nwk_choice4\\')
    
    from ice_nwk_4nc_compute import ice_nwk_4nc_compute 
    ice_nwk_dc = np.zeros((4,1))
    
    ice_nwk_dc[0,0] = gv2_flow + hsb_flow + pfa_flow + ser_flow
    ice_nwk_dc[1,0] = ice_main_coeff
    ice_nwk_dc[2,0] = gv2_flow + hsb_flow + pfa_flow + ser_flow
    ice_nwk_dc[3,0] = pwl

    ice_nwk_calc = ice_nwk_4nc_compute(ice_nwk_dc)    

    from gv2_nwk_4nc_compute import gv2_nwk_4nc_compute
    gv2_nwk_dc = np.zeros((4,1))
    
    gv2_nwk_dc[0,0] = gv2_flow + hsb_flow + pfa_flow + ser_flow
    gv2_nwk_dc[1,0] = gv2_coeff
    gv2_nwk_dc[2,0] = 0.9 * (gv2_flow + hsb_flow + pfa_flow + ser_flow)
    gv2_nwk_dc[3,0] = pwl

    gv2_nwk_calc = gv2_nwk_4nc_compute(gv2_nwk_dc)    
    
    from hsb_nwk_4nc_compute import hsb_nwk_4nc_compute
    hsb_nwk_dc = np.zeros((4,1))
    
    hsb_nwk_dc[0,0] = gv2_flow + hsb_flow + pfa_flow + ser_flow
    hsb_nwk_dc[1,0] = hsb_coeff
    hsb_nwk_dc[2,0] = 0.4 * (gv2_flow + hsb_flow + pfa_flow + ser_flow)
    hsb_nwk_dc[3,0] = pwl

    hsb_nwk_calc = hsb_nwk_4nc_compute(hsb_nwk_dc)
    
    from pfa_nwk_4nc_compute import pfa_nwk_4nc_compute
    pfa_nwk_dc = np.zeros((4,1))
    
    pfa_nwk_dc[0,0] = gv2_flow + hsb_flow + pfa_flow + ser_flow
    pfa_nwk_dc[1,0] = pfa_coeff
    pfa_nwk_dc[2,0] = 0.35 * (gv2_flow + hsb_flow + pfa_flow + ser_flow)
    pfa_nwk_dc[3,0] = pwl

    pfa_nwk_calc = pfa_nwk_4nc_compute(pfa_nwk_dc)    

    from ser_nwk_4nc_compute import ser_nwk_4nc_compute
    ser_nwk_dc = np.zeros((4,1))
    
    ser_nwk_dc[0,0] = gv2_flow + hsb_flow + pfa_flow + ser_flow
    ser_nwk_dc[1,0] = ser_coeff
    ser_nwk_dc[2,0] = 0.35 * (gv2_flow + hsb_flow + pfa_flow + ser_flow)
    ser_nwk_dc[3,0] = pwl

    ser_nwk_calc = ser_nwk_4nc_compute(ser_nwk_dc)    
    
    from tro_nwk_4nc_compute import tro_nwk_4nc_compute
    tro_nwk_dc = np.zeros((4,1))
    
    tro_nwk_dc[0,0] = gv2_flow + hsb_flow + pfa_flow + ser_flow
    tro_nwk_dc[1,0] = tro_main_coeff
    tro_nwk_dc[2,0] = 0.5 * (gv2_flow + hsb_flow + pfa_flow + ser_flow)
    tro_nwk_dc[3,0] = pwl

    tro_nwk_calc = tro_nwk_4nc_compute(tro_nwk_dc)
    
    return ice_nwk_calc, gv2_nwk_calc, hsb_nwk_calc, pfa_nwk_calc, ser_nwk_calc, tro_nwk_calc