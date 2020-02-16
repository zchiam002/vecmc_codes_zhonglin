##This function takes in a value, checks the intended sign before and returns the string with the proper sign 

def single_sign_string(value, sign_before):
    
    return_value = ''
    
    if sign_before == '-':
        ##- X - case
        if value < 0:
            return_value = ' + ' + str(-1 * value)
        ##special case of 0
        elif value == 0:
            return_value = ' - ' + str(0.0)
        ##- X + case
        else:
            return_value = ' - ' + str(value)
            
    else:
        ##+ X - case
        if value < 0:
            return_value = ' - ' + str(-1 * value)
        ##special case of 0
        elif value == 0:
            return_value = ' + ' + str(0.0)
        ##+ X + case
        else:
            return_value = ' + ' + str(value)
            
    return return_value