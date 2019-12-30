##This script extracts the raw data, and prepares them for model validation 

def plotting_error ():
            
    ##Plotting results of evap pump 
    #plot_evap_nwk_pumps ()
    
    ##Plotting results of distribution pump
    plot_dist_nwk_pump ()
    
    ##Plotting results of the cooling towers
    plot_cooling_towers_error ()
    
    ##Plotting the results of the chillers 
    plot_chiller_error ()
     
    return 

###################################################################################################################################################################################
##Auxillary functions 
    
##Plotting chiller error functions 
def plot_chiller_error ():
    import matplotlib.pyplot as plt 
    import pandas as pd 
    import numpy as np
    
    data_processed = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\validation_scripts\\output_csv_files\\chiller1_models_output.csv')
    
    dim_data_processed = data_processed.shape 
    
    mae_df = pd.DataFrame(columns = ['mae'])
    counter = 0
    
    for i in range (0, dim_data_processed[0]):
        mae = 100 * abs(data_processed['E_org'][i] - data_processed['E_m1'][i]) / data_processed['E_org'][i]
        temp_df = pd.DataFrame(data = [mae], columns = ['mae'])
        mae_df = mae_df.append(temp_df, ignore_index = True)
        counter = counter + 1
        
    ##Calculating the average MAE error 
    total_mae = sum(mae_df['mae'][:])
    ave_mae = total_mae / counter 
    print('Average MAE for chillers: ', ave_mae)
    
    
    ##Writing the y = x line     
    fig = plt.figure()
    plt.plot(data_processed['E_org'][:], data_processed['E_m3'][:], '.', label = '')
    plt.ylabel('Abstracted GNU model, ' + r'$\.E$ (kWh)')
    plt.xlabel('Raw data, ' + r'$\.E$ (kWh)')
    plt.axes().get_xaxis().set_ticks([])
    plt.axes().get_yaxis().set_ticks([])
    
    lims = [
        np.min([plt.axes().get_xlim(), plt.axes().get_ylim()]),  # min of both axes
        np.max([plt.axes().get_xlim(), plt.axes().get_ylim()]),  # max of both axes
        ]
    # now plot both limits against eachother
    plt.axes().plot(lims, lims, 'k-', alpha=0.75, zorder=0, label = 'y = x')
    plt.axes().set_xlim(lims)
    plt.axes().set_ylim(lims)
    
    plt.legend(loc = 'best')
    
    plt.savefig('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\error_plots\\chiller_raw_plots.png', dpi = 1000)
    
    return

##A function to deal with the cooling towers 
def plot_cooling_towers_error ():
    
    import os
    import pandas as pd
    import numpy as np
    from raw_data_prep_aux import ct_model_vs_raw_bilin
    from raw_data_prep_aux import ct_model_elect_calc
    from raw_data_prep_aux import calibrate_cooling_tower_model
    from raw_data_prep_aux import process_ct_data_manual_calibrate
    from raw_data_prep_aux import calibrate_cooling_tower_model_based_elect
    from raw_data_prep_aux import calc_elect_uem_only
    import matplotlib.pyplot as plt     
    
    ##Calibrating the regression coefficients based on electricity 
    ct_reg_coeff = calibrate_cooling_tower_model_based_elect ()
    
#    ##Calibrating the regression coefficients 
#    ct_reg_coeff = calibrate_cooling_tower_model ()
    
    ##Loading the cleansed data of the cooling towers
    ct_raw_data = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_testing\\ct_cleansed_3.csv')
    
    #Model vs raw data 
    if os.path.exists('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_testing\\model_vs_raw_elect.csv'):
        model_vs_raw_elect = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_testing\\model_vs_raw_elect.csv')
    else:
        model_vs_raw_elect = ct_model_elect_calc (ct_raw_data, ct_reg_coeff)
        model_vs_raw_elect.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_testing\\model_vs_raw_elect.csv')    
    
    ##Calculating error 
    dim_model_vs_raw_elect = model_vs_raw_elect.shape
    total_mae = sum(model_vs_raw_elect['mae'][:])
    ave_mae = total_mae / dim_model_vs_raw_elect[0]
    print('Average MAE for cooling towers: ', ave_mae)        
    
    ##Plotting the data 
    plt.figure()    
    plt.plot(model_vs_raw_elect['elect_raw'][:], model_vs_raw_elect['elect_model'][:], '.', label = '')

    plt.ylabel('Abstracted UEM model, ' + r'$\.E$ (kWh)')
    plt.xlabel('Raw data, ' + r'$\.E$ (kWh)')
    plt.axes().get_xaxis().set_ticks([])
    plt.axes().get_yaxis().set_ticks([])

    lims = [
    np.min([plt.axes().get_xlim(), plt.axes().get_ylim()]),  # min of both axes
    np.max([plt.axes().get_xlim(), plt.axes().get_ylim()]),  # max of both axes
    ]
    # now plot both limits against eachother
    plt.axes().plot(lims, lims, 'k-', alpha=0.75, zorder=0, label = 'y = x')
    plt.axes().set_xlim(lims)
    plt.axes().set_ylim(lims)
    
    plt.legend(loc = 'best')

    plt.savefig('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\error_plots\\cooling_towers_raw_plots.png', dpi = 1000)
    
    plt.show()    

    return    

    
##A function to deal with the distribution network pumps 
def plot_dist_nwk_pump ():
    
    import os
    import pandas as pd 
    import matplotlib.pyplot as plt 
    import numpy as np
    from raw_data_prep_aux import determine_pump_with_most_data_dist
    from raw_data_prep_aux import combine_af32_33_calc_elect
    from raw_data_prep_aux import del_error_dist_model_results
    
    #Client load data 
    client_load = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\historical_data\\New folder\\raw_data_csv\\client_load_data.csv')
    
    ##Pump electricity data 
    pump_data = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\historical_data\\New folder\\raw_data_csv\\pump_raw_data.csv')
    
    ##Trying to decide the pump with the most data 
    #determine_pump_with_most_data_dist(pump_data)
    if os.path.exists('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\pump_nwk_testing\\3233_pump_elect_model_vs_raw.csv'):
        model_vs_raw = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\pump_nwk_testing\\3233_pump_elect_model_vs_raw.csv')
    else:
        model_vs_raw = combine_af32_33_calc_elect (pump_data, client_load)
        model_vs_raw.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\pump_nwk_testing\\3233_pump_elect_model_vs_raw.csv')
    ##Deleting errornous data 
    model_vs_raw_cleansed = del_error_dist_model_results (model_vs_raw)

    ##Calculating error 
    dim_model_vs_raw_cleansed = model_vs_raw_cleansed.shape
    total_mae = sum(model_vs_raw_cleansed['mae_error'][:])
    ave_mae = total_mae / dim_model_vs_raw_cleansed[0]
    print('Average MAE for distribution pump: ', ave_mae)
    
    ##Plotting the data 
    plt.plot(model_vs_raw_cleansed['pump_power'][:], model_vs_raw_cleansed['pump_power_model'][:], '.', label = '')
    
    plt.ylabel('Abstracted distribution pump model, ' + r'$\.E$ (kWh)')
    plt.xlabel('Raw data, ' + r'$\.E$ (kWh)')
    plt.axes().get_xaxis().set_ticks([])
    plt.axes().get_yaxis().set_ticks([])    
    
    lims = [
    np.min([plt.axes().get_xlim(), plt.axes().get_ylim()]),  # min of both axes
    np.max([plt.axes().get_xlim(), plt.axes().get_ylim()]),  # max of both axes
    ]
    # now plot both limits against eachother
    plt.axes().plot(lims, lims, 'k-', alpha=0.75, zorder=0, label = 'y = x')
    plt.axes().set_xlim(lims)
    plt.axes().set_ylim(lims)
    
    plt.legend(loc = 'best')
    
    plt.savefig('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\error_plots\\dist_pump_raw_plots.png', dpi = 1000)
    
    plt.show()
    
    return 

##A function to deal with the evaporator pumps and networks
def plot_evap_nwk_pumps ():
    
    import matplotlib.pyplot as plt   
    import sys 
    import os 
    import pandas as pd 
    
    ##eSight data 
    pump_data = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\historical_data\\raw_pump_data.csv')

    ##Cleaning the pump raw data 
    if os.path.exists('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\pump_cleansed.csv'):
        cleansed_pump_data = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\pump_cleansed.csv')
    else:
        cleansed_pump_data = cleanse_pump_data (pump_data)    
    
    dim_cleansed_pump_data = cleansed_pump_data.shape
    x = range(0, dim_cleansed_pump_data[0])
    ##Plotting the flowrates 
    plt.figure()
    plt.plot(x, cleansed_pump_data['af1_flow'][:],'.')
    plt.figure()
    plt.plot(x, cleansed_pump_data['af2_flow'][:],'.')
    plt.figure()
    plt.plot(x, cleansed_pump_data['af3_flow'][:],'.')    

    plt.figure()
    plt.plot(cleansed_pump_data['af1_flow'][:],cleansed_pump_data['af1_energy'][:], '.')
    plt.figure()
    plt.plot(cleansed_pump_data['af2_flow'][:], cleansed_pump_data['af2_energy'][:], '.')
    plt.figure()
    plt.plot(cleansed_pump_data['af3_flow'][:], cleansed_pump_data['af3_energy'][:], '.')
    
    plt.figure()
    plt.hist(cleansed_pump_data['af1_flow'][:])
    plt.figure()
    plt.hist(cleansed_pump_data['af2_flow'][:])
    plt.figure()
    plt.hist(cleansed_pump_data['af3_flow'][:])  
    
    ##Importing the evap pump models 
    sys.path.append('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\')
    from evap_network_models import evap_nwk_piecewise_pressure_reg_pumpnwk 
    
    ##Hyper parameters 
        ##Unnecessary ones 
    tout_chiller = 273.15 + 5
    
    cp_split = 0
    cp_dist_nwk_split = [cp_split, 100 - cp_split]
        ##Important ones 
    steps = 10
    
    ##Initiating a new dataframe for holding return data 
    holding_dataframe = pd.DataFrame(columns = ['en1_flow', 'en2_flow', 'en3_flow', 'ep1_rd', 'ep2_rd', 'ep3_rd', 'ep1_model', 'ep2_model', 'ep3_model'])
       
    for i in range (0, dim_pump_data[0]):
        
        ##Preparing data 
        chiller_input = pd.DataFrame({'Name':['chiller_1_flow', 'chiller_1_supply_temperature', 
                                             'chiller_2_flow', 'chiller_2_supply_temperature', 
                                             'chiller_3_flow', 'chiller_3_supply_temperature'], 
                                     'Value':[cleansed_pump_data['af1_flow'][i], tout_chiller, 
                                              cleansed_pump_data['af2_flow'][i], tout_chiller, 
                                              cleansed_pump_data['af3_flow'][i], tout_chiller]})
                
        return_values, return_values_df = evap_nwk_piecewise_pressure_reg_pumpnwk(chiller_input, cp_dist_nwk_split, steps)
        
        ##Organizing the return values
        temp_data = [cleansed_pump_data['af1_flow'][i], cleansed_pump_data['af2_flow'][i], cleansed_pump_data['af1_flow'][i],
                     cleansed_pump_data['af1_energy'][i], cleansed_pump_data['af2_energy'][i], cleansed_pump_data['af1_energy'][i],
                     return_values_df['Value'][2], return_values_df['Value'][5], return_values_df['Value'][8]] 
        temp_df = pd.DataFrame(data = [temp_data], columns = ['en1_flow', 'en2_flow', 'en3_flow', 'ep1_rd', 'ep2_rd', 'ep3_rd', 'ep1_model', 'ep2_model', 'ep3_model'])
        holding_dataframe = holding_dataframe.append(temp_df, ignore_index = True)
        
        print('Status', i, 'of', dim_pump_data[0])
    
    ##Plotting the graphs 
    plt.figure()    
    plt.plot(holding_dataframe['ep1_rd'][:], holding_dataframe['ep1_model'][:], '.')
    plt.show()
    plt.figure()
    plt.plot(holding_dataframe['ep2_rd'][:], holding_dataframe['ep2_model'][:], '.')
    plt.show()
    plt.figure()
    plt.plot(holding_dataframe['ep3_rd'][:], holding_dataframe['ep3_model'][:], '.')
    plt.show()     
    return 



##A function to cleanse the pump raw data 
def cleanse_pump_data (pump_data):
    
    import pandas as pd 
    
    ##Ridding of all negative flowrates 
    dim_pump_data = pump_data.shape 
    
        ##Initiating a new dataframe to hold the return values
    return_data = pd.DataFrame(columns = list(pump_data))
    
    for i in range (0, dim_pump_data[0]):
        if (pump_data['ar1_energy'][i] <= 0) or (pump_data['ar1_flow'][i] <= 0):
            ar1_energy = 0
            ar1_flow = 0
        else:
            ar1_energy = pump_data['ar1_energy'][i]
            ar1_flow = pump_data['ar1_flow'][i]            
        if (pump_data['ar2_energy'][i] <= 0) or (pump_data['ar2_flow'][i] <= 0):
            ar2_energy = 0
            ar2_flow = 0     
        else:
            ar2_energy = pump_data['ar2_energy'][i]
            ar2_flow = pump_data['ar2_flow'][i]                 
        if (pump_data['ar3_energy'][i] <= 0) or (pump_data['ar3_flow'][i] <= 0):
            ar3_energy = 0
            ar3_flow = 0
        else:
            ar3_energy = pump_data['ar3_energy'][i]
            ar3_flow = pump_data['ar3_flow'][i]                 
        if (pump_data['af1_energy'][i] <= 0) or (pump_data['af1_flow'][i] <= 0):
            af1_energy = 0
            af1_flow = 0
        else:
            af1_energy = pump_data['af1_energy'][i]
            af1_flow = pump_data['af1_flow'][i]     
        if (pump_data['af2_energy'][i] <= 0) or (pump_data['af2_flow'][i] <= 0):
            af2_energy = 0
            af2_flow = 0  
        else:
            af2_energy = pump_data['af2_energy'][i]
            af2_flow = pump_data['af2_flow'][i]     
        if (pump_data['af3_energy'][i] <= 0) or (pump_data['af3_flow'][i] <= 0):
            af3_energy = 0
            af3_flow = 0
        else:
            af3_energy = pump_data['af3_energy'][i]
            af3_flow = pump_data['af3_flow'][i]                 
        if (pump_data['af31_energy'][i] <= 0) and (pump_data['af32_energy'][i] <= 0) and (pump_data['af33_energy'][i] <= 0) and (pump_data['dist_nwk_flow'][i]<= 0):
            af31_energy = 0
            af32_energy = 0
            af33_energy = 0
            dist_nwk_flow = 0
        elif (pump_data['af31_energy'][i] <= 0) and (pump_data['af32_energy'][i] <= 0) and (pump_data['af33_energy'][i] <= 0) and (pump_data['dist_nwk_flow'][i] > 0):
            af31_energy = 0
            af32_energy = 0
            af33_energy = 0
            dist_nwk_flow = pump_data['dist_nwk_flow'][i]   
        elif (pump_data['af31_energy'][i] > 0) and (pump_data['af32_energy'][i] > 0) and (pump_data['af33_energy'][i] > 0) and (pump_data['dist_nwk_flow'][i] <= 0):
            af31_energy = 0
            af32_energy = 0
            af33_energy = 0
            dist_nwk_flow = 0               
        else:
            af31_energy = pump_data['af31_energy'][i]
            af32_energy = pump_data['af32_energy'][i]
            af33_energy = pump_data['af33_energy'][i] 
            dist_nwk_flow = pump_data['dist_nwk_flow'][i] 

        ##Eliminating partial data       
        
        
    
        ##Appending the temporary data
        dow = pump_data['Day of week'][i]
        date = pump_data['Date'][i]
        month = pump_data['Month'][i]
        year = pump_data['Year '][i]
        hour = pump_data['Hour'][i]
        temp_data = [dow, date, month, year, hour, ar1_energy, ar1_flow, ar2_energy, ar2_flow, ar3_energy, ar3_flow, af1_energy, af1_flow, af2_energy, af2_flow, af3_energy,
                     af3_flow, af31_energy, af32_energy, af33_energy, dist_nwk_flow]
        temp_df = pd.DataFrame(data = [temp_data], columns = list(pump_data))
        return_data = return_data.append(temp_df, ignore_index = True)
        
        return_data.to_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\pump_cleansed.csv')
    
    return return_data

###################################################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    plotting_error ()



