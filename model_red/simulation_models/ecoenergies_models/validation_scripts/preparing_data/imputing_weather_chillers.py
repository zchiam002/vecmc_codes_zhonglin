##Filling in the temperature data for the chillers 

import pandas as pd 

##Preparing the raw data 

raw = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\cleansed_data\\ch1_data.csv')
weather = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\cleansed_data\\barcelona_weather_2016.csv')
raw_new = pd.DataFrame(columns=['Day', 'Date', 'Month', 'Year', 'Hour', 'Tin_cond', 'Tout_cond', 'mcond', 'Tin_evap', 'Tout_evap', 'mevap', 'Qe', 'Qc', 'T_DB', 'T_WB'])

dim_raw = raw.shape
dim_weather = weather.shape 

for i in range (0, dim_raw[0]):
    for j in range (0, dim_weather[0]):
        if (weather['Day'][j] == raw['Day'][i]) and (weather['Date'][j] == raw['Date'][i]) and (weather['Month'][j] == raw['Month'][i]) and (weather['Year'][j] == raw['Year'][i]) and (weather['Hour'][j] == raw['Hour'][i]):
            t_db = weather['T_DB'][j]
            t_wb = weather['T_WB'][j]
            data_temp = [raw['Day'][i], raw['Date'][i], raw['Month'][i], raw['Year'][i], raw['Hour'][i], raw['Tin_cond'][i], raw['Tout_cond'][i], raw['mcond'][i], raw['Tin_evap'][i], raw['Tout_evap'][i], raw['mevap'][i], raw['Qe'][i], raw['Qc'][i], t_db, t_wb]
            temp_df = pd.DataFrame(data = [data_temp], columns = ['Day', 'Date', 'Month', 'Year', 'Hour', 'Tin_cond', 'Tout_cond', 'mcond', 'Tin_evap', 'Tout_evap', 'mevap', 'Qe', 'Qc', 'T_DB', 'T_WB']) 
            raw_new = raw_new.append(temp_df, ignore_index = True)
            break
            
raw_new.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\cleansed_data\\raw_new.csv')