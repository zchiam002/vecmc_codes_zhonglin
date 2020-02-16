##This function checks if a value exists in the list 
def check_if_item_in_list_smtpgpy (check_list, item):
    ##check_list --- the list where the item is to be checked against 
    ##item --- the item to be checked 
    
    dim_check_list = len(check_list)
    
    ret_value = 0
    for i in range (0, dim_check_list):
        if check_list[i] == item:
            ret_value = 1
            break
            
    return ret_value