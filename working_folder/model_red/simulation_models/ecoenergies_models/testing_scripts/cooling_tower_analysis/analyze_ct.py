##This script analyzes builds the cooling tower model

def analyze_ct (raw_data):
    
    import pandas as pd 
    
    dim_raw_data = raw_data.shape
    print(dim_raw_data)
    
    cleansed_data = pd.DataFrame(columns = ['Tin', 'Tout', 'Twb', 'E', 'mw', 'ma'])
    
    for i in range (0, dim_raw_data[0]):
        
        cond1 = raw_data['Tin'][i] - raw_data['Tout'][i]                        ##To check if Tin > Tout
        cond2 = raw_data['Tout'][i] - raw_data['Twb'][i]                        ##To check if Tout > Twb
        
        if (raw_data['mw'][i] <= 0) and (raw_data['ma'][i] > 0):                ##Conditions where fan is turn on but there is no flow
            cond3 = 1
        else:
            cond3 = 0
        
        if (raw_data['ma'][i] <= 0) and (raw_data['E'][i] > 0):                ##Conditions where fan is turn on but there is no air
            cond4 = 1
        else:
            cond4 = 0
            
        eff = (raw_data['Tin'][i] - raw_data['Tout'][i]) / (raw_data['Tin'][i] - raw_data['Twb'][i])
        if eff >= 1:
            cond5 = 1
        else:
            cond5 = 0
            
        if (cond1 >= 0) and (cond2 > 0) and (cond3 == 0) and (cond4 == 0) and (cond5 == 0):
            
            temp_data = [raw_data['Tin'][i], raw_data['Tout'][i], raw_data['Twb'][i], raw_data['E'][i], raw_data['mw'][i], raw_data['ma'][i]]
            temp_df = pd.DataFrame(data = [temp_data], columns = ['Tin', 'Tout', 'Twb', 'E', 'mw', 'ma'])
            cleansed_data = cleansed_data.append(temp_df, ignore_index = True)
            
    dim_cleansed_data = cleansed_data.shape
    print(dim_cleansed_data)
    
    return 



def perform_regression (raw_data):
    
    import numpy as np
    import pandas as pd
    from sklearn import linear_model 
    
    dim_raw_data = raw_data.shape
    
    ##To perform multivariate regression amongst the variables 
    valuesX = np.zeros((dim_raw_data[0], 5))
    valuesY = np.zeros((dim_raw_data[0], 1))
    
    for i in range (0, dim_raw_data[0]):
        
        valuesX[i, 0] = (raw_data['ma'][i] / raw_data['mw'][i]) * (raw_data['Tin'][i] - raw_data['Twb'][i])
        valuesX[i, 1] = (raw_data['Tin'][i] - raw_data['Twb'][i]) * (raw_data['Tin'][i] - raw_data['Twb'][i])       
        valuesX[i, 2] = (pow((raw_data['ma'][i] / raw_data['mw'][i]), 2)) * (raw_data['Tin'][i] - raw_data['Twb'][i])
        valuesX[i, 3] = (pow((raw_data['Tin'][i] - raw_data['Twb'][i]), 2)) * (raw_data['Tin'][i] - raw_data['Twb'][i])
        valuesX[i, 4] = ((raw_data['ma'][i] / raw_data['mw'][i]) * (raw_data['Tin'][i] - raw_data['Twb'][i]) ) * (raw_data['Tin'][i] - raw_data['Twb'][i])
        
        valuesY[i, 0] = (raw_data['Tin'][i] - raw_data['Tout'][i])
    
    clf = linear_model.LinearRegression(fit_intercept = True)
    clf.fit(valuesX, valuesY)
    result_1 = clf.score(valuesX, valuesY, sample_weight=None)
    lin_coeff_1 = clf.coef_
    int_1 = clf.intercept_
    
    print(result_1)
    print(lin_coeff_1)
    print(int_1)
    
    return

###########################################################################################################################################################
##Running the test script   
if __name__ == '__main__':
    import pandas as pd
    raw_data = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\testing_scripts\\cooling_tower_analysis\\raw_data.csv')
    #analyze_ct (raw_data)
    perform_regression (raw_data)