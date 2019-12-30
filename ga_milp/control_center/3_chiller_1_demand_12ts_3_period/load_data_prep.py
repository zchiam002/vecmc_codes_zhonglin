##This script prepares the 3-12 hrs time period which is to be used as input data for the optimization excercise  

def define_load_periods():
    
    import pandas as pd
    import matplotlib.pyplot as plt 
    
    
    ##Loading the files into the dataframes
    weather_data = pd.read_csv('C:\\Optimization_zlc\\input_data\\3_chiller_1_demand_12ts_3_period_input_data\\2016_demand\\weather_data_raw.csv')
    client_load_data = pd.read_csv('C:\\Optimization_zlc\\input_data\\3_chiller_1_demand_12ts_3_period_input_data\\2016_demand\\client_load_data.csv')
    
    ##Determining the savefile locations 
    hl_loc = 'C:\\Optimization_zlc\\input_data\\3_chiller_1_demand_12ts_3_period_input_data\\high_load\\'
    ml_loc = 'C:\\Optimization_zlc\\input_data\\3_chiller_1_demand_12ts_3_period_input_data\\mid_load\\'
    ll_loc = 'C:\\Optimization_zlc\\input_data\\3_chiller_1_demand_12ts_3_period_input_data\\low_load\\'
    note_loc = 'C:\\Optimization_zlc\\input_data\\3_chiller_1_demand_12ts_3_period_input_data\\'
    
    ##3 12 hour time periods should be selected of the year. They will be representation of high, mid and low loads respectively 
    ##These 12 hour time periods will be determined from 0800 to 2000 hrs 
    high_load = pd.DataFrame(columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])
    high_load_weather = pd.DataFrame(columns = ['T_DB', 'T_WB'])
    
    mid_load = pd.DataFrame(columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])
    mid_load_weather = pd.DataFrame(columns = ['T_DB', 'T_WB'])
    
    low_load = pd.DataFrame(columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])
    low_load_weather = pd.DataFrame(columns = ['T_DB', 'T_WB'])    
    
    ##High load period is defined from july to september
    high_load_date = pd.DataFrame(data = [[17, 8, 2016]], columns = ['Date', 'Month', 'Year'])
    ##Mid load period is defined as jun and october 
    mid_load_date = pd.DataFrame(data = [[15, 6, 2016]], columns = ['Date', 'Month', 'Year'])
    ##Low load period is defined as november to may 
    low_load_date = pd.DataFrame(data = [[17, 2, 2016]], columns = ['Date', 'Month', 'Year'])
    
    hour = 0 ##The starting hour (0 - 23)
    duration = 24 ##The duration of the period 
    
    
    dim_client_load_data = client_load_data.shape
    
    for i in range (0, dim_client_load_data[0]):
        hl_count = 0
        ml_count = 0
        ll_count = 0
        
        ##Handling high load data 
        if (client_load_data['Date'][i] == high_load_date['Date'][0]) and (client_load_data['Month'][i] == high_load_date['Month'][0]) and (client_load_data['Year'][i] == high_load_date['Year'][0]):
            if (client_load_data['Hour'][i] >= hour) and (hl_count <= duration):
                temp_data = [client_load_data['Gv2_load'][i], client_load_data['Hsb_load'][i], client_load_data['Pfa_load'][i], client_load_data['Ser_load'][i], client_load_data['Fir_load'][i]]
                temp_df = pd.DataFrame(data = [temp_data], columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])
                high_load = high_load.append(temp_df, ignore_index = True)
                
                temp_data = [weather_data['T_db'][i], weather_data['T_wb'][i]]
                temp_df = pd.DataFrame(data = [temp_data], columns = ['T_DB', 'T_WB'])
                high_load_weather = high_load_weather.append(temp_df, ignore_index = True)    
                
                hl_count = hl_count + 1

        ##Handling mid load data 
        if (client_load_data['Date'][i] == mid_load_date['Date'][0]) and (client_load_data['Month'][i] == mid_load_date['Month'][0]) and (client_load_data['Year'][i] == mid_load_date['Year'][0]):
            if (client_load_data['Hour'][i] >= hour) and (ml_count <= duration):
                temp_data = [client_load_data['Gv2_load'][i], client_load_data['Hsb_load'][i], client_load_data['Pfa_load'][i], client_load_data['Ser_load'][i], client_load_data['Fir_load'][i]]
                temp_df = pd.DataFrame(data = [temp_data], columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])
                mid_load = mid_load.append(temp_df, ignore_index = True)
                
                temp_data = [weather_data['T_db'][i], weather_data['T_wb'][i]]
                temp_df = pd.DataFrame(data = [temp_data], columns = ['T_DB', 'T_WB'])
                mid_load_weather = mid_load_weather.append(temp_df, ignore_index = True)  
                
                ml_count = ml_count + 1

        ##Handling low load data 
        if (client_load_data['Date'][i] == low_load_date['Date'][0]) and (client_load_data['Month'][i] == low_load_date['Month'][0]) and (client_load_data['Year'][i] == low_load_date['Year'][0]):
            if (client_load_data['Hour'][i] >= hour) and (ll_count <= duration):
                temp_data = [client_load_data['Gv2_load'][i], client_load_data['Hsb_load'][i], client_load_data['Pfa_load'][i], client_load_data['Ser_load'][i], client_load_data['Fir_load'][i]]
                temp_df = pd.DataFrame(data = [temp_data], columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])
                low_load = low_load.append(temp_df, ignore_index = True)
                
                temp_data = [weather_data['T_db'][i], weather_data['T_wb'][i]]
                temp_df = pd.DataFrame(data = [temp_data], columns = ['T_DB', 'T_WB'])
                low_load_weather = low_load_weather.append(temp_df, ignore_index = True)  
                
                ll_count = ll_count + 1
                
        ##Breaking when necessary 
        if (hl_count > duration) and (ml_count > duration) and (ll_count > duration):
            break 
        
    ##Placing the dataframes into a csv file for reading by the master models 
    high_load.to_csv(hl_loc + 'high_demand.csv')
    high_load_weather.to_csv(hl_loc + 'high_demand_weather.csv')
    
    mid_load.to_csv(ml_loc + 'mid_demand.csv')
    mid_load_weather.to_csv(ml_loc + 'mid_demand_weather.csv') 

    low_load.to_csv(ll_loc + 'low_demand.csv')
    low_load_weather.to_csv(ll_loc + 'low_demand_weather.csv')
    
    ##Writing a notepad 
    
    f_data_set = open(note_loc + 'input_data_readme.txt', 'w')
    st_time = hour_in_military_format (hour)
    f_data_set.write('Starting hour of period = ' + st_time + 'hrs \n \n')
    f_data_set.write('Duration of period = ' + str(duration) + 'hr \n \n')
    high_load_date = str(high_load_date['Date'][0]) + '/' + str(high_load_date['Month'][0]) + '/' + str(high_load_date['Year'][0])
    f_data_set.write('Duration of high load date = ' + str(high_load_date) + '\n \n')
    mid_load_date = str(mid_load_date['Date'][0]) + '/' + str(mid_load_date['Month'][0]) + '/' + str(mid_load_date['Year'][0])
    f_data_set.write('Duration of mid load date = ' + str(mid_load_date) + '\n \n')
    low_load_date = str(low_load_date['Date'][0]) + '/' + str(low_load_date['Month'][0]) + '/' + str(low_load_date['Year'][0])
    f_data_set.write('Duration of low load date = ' + str(low_load_date) + '\n \n')

    ##Wrapping up 
    f_data_set.write('End \n')    
    f_data_set.close    
    
    ##Plotting the graph of the load profiles 
    
    ##High load profile
    fig = plt.figure()

    ax = fig.add_subplot(111)           ##Create matplotlib axes
    ax.set_ylabel('Cooling demand (kWh)') 
    ax2 = ax.twinx()                    ##Create another axes thta shares the same x-axis as ax    
    ax2.set_ylabel('Temperature (' + r'$\degree$C'+ ')')     
    
    total_load = pd.DataFrame(columns = ['Load'])
    
    for i in range (0, duration):
        temp_data = [high_load['ss_gv2_demand'][i] + high_load['ss_hsb_demand'][i] + high_load['ss_pfa_demand'][i] + high_load['ss_ser_demand'][i] + high_load['ss_fir_demand'][i]]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Load'])
        total_load = total_load.append(temp_df, ignore_index = True)
        
    bx1 = total_load['Load'].plot(kind='bar', color='lightblue', ax=ax, xticks = total_load.index, rot = 0, label = 'Cooling demand')
    bx2 = high_load_weather['T_DB'].plot(kind='line', color='red', ax=ax2, xticks = high_load_weather.index, rot = 0, label = 'Drybulb Temperature')
    bx2 = high_load_weather['T_WB'].plot(kind='line', color='black', ax=ax2, xticks = high_load_weather.index, rot = 0, label = 'Wetbulb Temperature')     

    objects = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23')    
    bx1.set_xticklabels(objects)
    bx1.set_xlim([-0.5, 23.5])
    bx1.legend(loc = 'upper right')
    bx2.legend(loc = 'upper left')
    
    xlabel_text = 'Date = ' + high_load_date
    bx1.set_xlabel(xlabel_text)
    
    plt.title('High load profile')
    plt.savefig('C:\\Optimization_zlc\\input_data\\3_chiller_1_demand_12ts_3_period_input_data\\high_load\\input_data_plots', dpi=1000)
    plt.close()   
    
    ##Mid load profile 
    fig = plt.figure()

    ax = fig.add_subplot(111)           ##Create matplotlib axes
    ax.set_ylabel('Cooling demand (kWh)') 
    ax2 = ax.twinx()                    ##Create another axes thta shares the same x-axis as ax    
    ax2.set_ylabel('Temperature (' + r'$\degree$C'+ ')')     
    
    total_load = pd.DataFrame(columns = ['Load'])
    
    for i in range (0, duration):
        temp_data = [mid_load['ss_gv2_demand'][i] + mid_load['ss_hsb_demand'][i] + mid_load['ss_pfa_demand'][i] + mid_load['ss_ser_demand'][i] + mid_load['ss_fir_demand'][i]]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Load'])
        total_load = total_load.append(temp_df, ignore_index = True)
        
    bx1 = total_load['Load'].plot(kind='bar', color='lightblue', ax=ax, xticks = total_load.index, rot = 0, label = 'Cooling demand')
    bx2 = mid_load_weather['T_DB'].plot(kind='line', color='red', ax=ax2, xticks = mid_load_weather.index, rot = 0, label = 'Drybulb Temperature')
    bx2 = mid_load_weather['T_WB'].plot(kind='line', color='black', ax=ax2, xticks = mid_load_weather.index, rot = 0, label = 'Wetbulb Temperature')     

    objects = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23')    
    bx1.set_xticklabels(objects)
    bx1.set_xlim([-0.5, 23.5])
    bx1.legend(loc = 'upper right')
    bx2.legend(loc = 'upper left')
    
    xlabel_text = 'Date = ' + mid_load_date
    bx1.set_xlabel(xlabel_text)
    
    plt.title('Mid load profile')
    plt.savefig('C:\\Optimization_zlc\\input_data\\3_chiller_1_demand_12ts_3_period_input_data\\mid_load\\input_data_plots', dpi=1000)
    plt.close()  
    
    ##Low load profile 
    fig = plt.figure()

    ax = fig.add_subplot(111)           ##Create matplotlib axes
    ax.set_ylabel('Cooling demand (kWh)') 
    ax2 = ax.twinx()                    ##Create another axes thta shares the same x-axis as ax    
    ax2.set_ylabel('Temperature (' + r'$\degree$C'+ ')')     
    
    total_load = pd.DataFrame(columns = ['Load'])
    
    for i in range (0, duration):
        temp_data = [low_load['ss_gv2_demand'][i] + low_load['ss_hsb_demand'][i] + low_load['ss_pfa_demand'][i] + low_load['ss_ser_demand'][i] + low_load['ss_fir_demand'][i]]
        temp_df = pd.DataFrame(data = [temp_data], columns = ['Load'])
        total_load = total_load.append(temp_df, ignore_index = True)
        
    bx1 = total_load['Load'].plot(kind='bar', color='lightblue', ax=ax, xticks = total_load.index, rot = 0, label = 'Cooling demand')
    bx2 = low_load_weather['T_DB'].plot(kind='line', color='red', ax=ax2, xticks = low_load_weather.index, rot = 0, label = 'Drybulb Temperature')
    bx2 = low_load_weather['T_WB'].plot(kind='line', color='black', ax=ax2, xticks = low_load_weather.index, rot = 0, label = 'Wetbulb Temperature')     

    objects = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23')    
    bx1.set_xticklabels(objects)
    bx1.set_xlim([-0.5, 23.5])
    bx1.legend(loc = 'upper right')
    bx2.legend(loc = 'upper left')
    
    xlabel_text = 'Date = ' + low_load_date
    bx1.set_xlabel(xlabel_text)
    
    plt.title('Low load profile')
    plt.savefig('C:\\Optimization_zlc\\input_data\\3_chiller_1_demand_12ts_3_period_input_data\\low_load\\input_data_plots', dpi=1000)
    plt.close() 
    return 


#########################################################################################################################################################################
##Additional functions 

##This function converts the hour into a string format 
def hour_in_military_format (hour):
    
    if hour <= 9:
        ret_value = '0' + str(hour) + '00'
    else:
        ret_value = str(hour) + '00'
        
    return ret_value

#########################################################################################################################################################################
##Running the extraction algorithm  
if __name__ == '__main__':
    define_load_periods()