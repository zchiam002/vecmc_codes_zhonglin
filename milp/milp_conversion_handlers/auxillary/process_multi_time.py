##This function handles multi-time data for the linear program 

def process_multi_time (modelname):
    
    import pandas as pd
    multi_time_data = pd.read_csv('C:\\Optimization_zlc\\models\\la_marina_demand.csv')
    
    rows=len(multi_time_data.index)
    
    model_multi_time_data = pd.DataFrame(columns = ['Name', 'Value', 'Unit'])
    
    for i in range (0,rows):
        if modelname in multi_time_data['Name'][i]:
            value = [multi_time_data['Name'][i], multi_time_data['Value'][i], multi_time_data['Unit'][i]]
            temp = pd.DataFrame(data = [value], columns = ['Name', 'Value', 'Unit'])
            model_multi_time_data = model_multi_time_data.append(temp, ignore_index=True)
            
    return model_multi_time_data