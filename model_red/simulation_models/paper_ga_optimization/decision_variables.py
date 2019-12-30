##This are the variables which are handled by the genetic algorithm 

def process_decision_variables ():
    
    import pandas as pd 
    
    ##Chiller decision variables 
    chiller_dv = pd.DataFrame(columns = ['Name', 'Value'])
    temp_data = []
    temp_data.append(['chiller_1_delt', ])
    
    return