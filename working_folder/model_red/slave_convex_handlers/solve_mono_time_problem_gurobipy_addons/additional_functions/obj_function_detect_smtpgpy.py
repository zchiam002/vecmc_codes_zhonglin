##This function returns the key to access the correct dataframe columns 
def obj_function_detect_smtpgpy (obj_func):
    ##obj_func --- a string of values
    
    if obj_func == 'investment_cost':
        key = 'Cinv'
    elif obj_func == 'operation_cost':
        key = 'Cost'
    elif obj_func == 'power':
        key = 'Power'
    elif obj_func == 'impact':
        key = 'Impact'
        
    return key
