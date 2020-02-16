##Processing input data 

def extract_temp (wd):
    import pandas as pd 
    all_temp = pd.read_csv(wd)
    
    return all_temp
    
def extract_demand (dd):
    import pandas as pd 
    all_demand = pd.read_csv(dd)
    
    return all_demand

def extract_weather_and_ct_coefficients (file_loc, demand_type, allocated_hour):
    
    import pandas as pd
    
    ##file_loc --- the file location of the look up table 
    ##demand_type --- high, mid, low, needed to select the right file
    ##allocated_hour --- the row which the data is needed
    
    ##Processing the weather data and the coefficients for the cooling towers
    if demand_type == 'high':
        weather_and_ct_coeff_loc = file_loc + 'ct_hl_coeff.csv'
    elif demand_type == 'mid':
        weather_and_ct_coeff_loc = file_loc + 'ct_ml_coeff.csv' 
    elif demand_type == 'low': 
        weather_and_ct_coeff_loc = file_loc + 'ct_ll_coeff.csv' 
    
    weather_and_ct_coeff = pd.read_csv(weather_and_ct_coeff_loc)
    
    ##Packaging the required return information 
    required_data = [weather_and_ct_coeff['T_DB'][allocated_hour], weather_and_ct_coeff['T_WB'][allocated_hour], 
                     weather_and_ct_coeff['f0_c0'][allocated_hour], weather_and_ct_coeff['f0_c1'][allocated_hour], weather_and_ct_coeff['f0_c2'][allocated_hour], weather_and_ct_coeff['f0_c3'][allocated_hour],
                     weather_and_ct_coeff['f1_c0'][allocated_hour], weather_and_ct_coeff['f1_c1'][allocated_hour], weather_and_ct_coeff['f1_c2'][allocated_hour], weather_and_ct_coeff['f1_c3'][allocated_hour], 
                     weather_and_ct_coeff['f2_c0'][allocated_hour], weather_and_ct_coeff['f2_c1'][allocated_hour], weather_and_ct_coeff['f2_c2'][allocated_hour], weather_and_ct_coeff['f2_c3'][allocated_hour], 
                     weather_and_ct_coeff['f3_c0'][allocated_hour], weather_and_ct_coeff['f3_c1'][allocated_hour], weather_and_ct_coeff['f3_c2'][allocated_hour], weather_and_ct_coeff['f3_c3'][allocated_hour],
                     weather_and_ct_coeff['f4_c0'][allocated_hour], weather_and_ct_coeff['f4_c1'][allocated_hour], weather_and_ct_coeff['f4_c2'][allocated_hour], weather_and_ct_coeff['f4_c3'][allocated_hour]]
    required_df = pd.DataFrame(data = [required_data], columns = ['T_DB', 'T_WB', 
                                                                  'f0_c0', 'f0_c1', 'f0_c2', 'f0_c3', 
                                                                  'f1_c0', 'f1_c1', 'f1_c2', 'f1_c3', 
                                                                  'f2_c0', 'f2_c1', 'f2_c2', 'f2_c3',	
                                                                  'f3_c0', 'f3_c1', 'f3_c2', 'f3_c3',	
                                                                  'f4_c0', 'f4_c1', 'f4_c2', 'f4_c3'])
    
    return required_df

def extract_elect_tariff (pricing_structure, hourly_data):
    import pandas as pd 
    
    ##pricing structure --- a dataframe containing the data about period and corresponding price 
    ##hourly_pricing --- the demand period and associated pricing pricing sturcture data 
    
    ##The objective of this functiong is to return the hourly_data with corresponding price
    
    ##Creating a return dataframe for the return values
    ret_val = pd.DataFrame(columns = ['Hour', 'Price'])
    
    dim_pricing_structure = pricing_structure.shape 
    dim_hourly_data = hourly_data.shape 
    
    for i in range (0, dim_hourly_data[0]):
        curr_tariff = hourly_data['Tariff'][i]
        curr_price = 'na'
        for j in range (0, dim_pricing_structure[0]):
            if curr_tariff == pricing_structure['Tariff'][j]:
                curr_price = pricing_structure['Price'][j]
                break
        if curr_price == 'na':
            import sys
            print('Error in Electricity Tariff Data')
            sys.exit()
        else:
            temp = [i, curr_price]
            temp_df = pd.DataFrame(data = [temp], columns = ['Hour', 'Price'])
            ret_val = ret_val.append(temp_df, ignore_index = True)
    
    return ret_val