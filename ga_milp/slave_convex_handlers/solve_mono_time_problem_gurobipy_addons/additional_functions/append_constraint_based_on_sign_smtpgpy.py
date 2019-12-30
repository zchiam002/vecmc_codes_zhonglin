##This function appends the required constraint based on the sign of the equation 
def append_constraint_based_on_sign_smtpgpy (grb_model, lhs_value, rhs_value, sign, current_index):
    
    import gurobipy as grb 
    
    ##grb_model --- the associated gruobi model 
    ##lhs_value --- the left hand side part of the equation 
    ##rhs_value --- the right hand side part of the equation 
    ##sign --- the associated sign 
    ##current_index --- the counter for the constraints 
    
    if sign == 'less_than_equal_to':
        grb_model.addConstr(lhs_value <= rhs_value, 'c' + str(current_index))  
        current_index = current_index + 1
    elif sign == 'greater_than_equal_to':
        grb_model.addConstr(lhs_value >= rhs_value, 'c' + str(current_index))  
        current_index = current_index + 1      
    elif sign == 'equal_to':
        grb_model.addConstr(lhs_value == rhs_value, 'c' + str(current_index))  
        current_index = current_index + 1  
        
    return grb_model, current_index