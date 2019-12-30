##This function processes the variables and maps them into usable variables for the model to work
##Doing this will limit the search space and reduce the chance for infeasible conditions 

def mapping_variables (allm_var):
    from pump_select_binary import pump_select_binary 
    
    x = []
    for i in range (0,6):                                   ##Chiller evaporator and condenser flowrate information
        x.append(allm_var[i])
    sum_perc_flow = 0
    for i in range (6,12):                                  ##The split ratios of the various networks
        sum_perc_flow = sum_perc_flow + allm_var[i]
    
    if sum_perc_flow != 0:
        for i in range (6,12):
            x.append(allm_var[i]/sum_perc_flow)
    else:
        for i in range (6,12):
            x.append(0)
        
    for i in range (12,15):                                 ##The cooling tower temperatures and the return chiller temperature 
        x.append(allm_var[i])
    
    
    if allm_var[15] <= 0.25:
        ##Formulating the network choice data 
        x.append(1)
        x.append(0)
        x.append(0)
        x.append(0)
        number_of_choices = 12                      ##The number of different pump combinations 
        
        for j in range (0,number_of_choices):
            if allm_var[16] <= ((1+j)/number_of_choices):
                y = pump_select_binary(1,j)
                for k in range (0,len(y)):
                    x.append(y[k])
                break
        
    elif allm_var[15] <= 0.5:
        ##Formulating the network choice data 
        x.append(0)
        x.append(1)
        x.append(0)
        x.append(0)
        number_of_choices = 12                      ##The number of different pump combinations 
        
        for j in range (0,number_of_choices):
            if allm_var[16] <= ((1+j)/number_of_choices):
                y = pump_select_binary(2,j)
                for k in range (0,len(y)):
                    x.append(y[k])
                break        
        
    elif allm_var[15] <= 0.75:
        ##Formulating the network choice data 
        x.append(0)
        x.append(0)
        x.append(1)
        x.append(0)
        number_of_choices = 10                      ##The number of different pump combinations 
        
        for j in range (0,number_of_choices):
            if allm_var[16] <= ((1+j)/number_of_choices):
                y = pump_select_binary(3,j)
                for k in range (0,len(y)):
                    x.append(y[k])
                break 
            
    else:        
        ##Formulating the network choice data 
        x.append(0)
        x.append(0)
        x.append(0)
        x.append(1)
        number_of_choices = 7                       ##The number of different pump combinations 
        
        for j in range (0,number_of_choices):
            if allm_var[16] <= ((1+j)/number_of_choices):
                y = pump_select_binary(4,j)
                for k in range (0,len(y)):
                    x.append(y[k])
                break     
    
    return x
