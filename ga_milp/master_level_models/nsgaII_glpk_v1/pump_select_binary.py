##This is the binary pump selection function 

def pump_select_binary (nwk_select, j_value):
    
    return_value = []
    count = 0
    if nwk_select == 1:                                     ##all network need to be served by their own pumps                                        
        for i in range (0,2):                               ##maximum value of count = 12
            for j in range (0,2):
                for k in range (0,3):
                    if count == j_value:
                        if i == 0:
                            return_value.append(1)
                            return_value.append(0)
                        else:
                            return_value.append(0)
                            return_value.append(1)
                            
                        if j == 0:
                            return_value.append(1)
                            return_value.append(0)
                        else:
                            return_value.append(0)
                            return_value.append(1)
                            
                        if k == 0:
                            return_value.append(1)
                            return_value.append(0)
                            return_value.append(0)
                        elif k == 1:
                            return_value.append(0)
                            return_value.append(1)
                            return_value.append(0)
                        else:
                            return_value.append(0)
                            return_value.append(0)
                            return_value.append(1)
                    
                    count = count + 1
                    
                    if count == j_value + 1:
                        break
                if count == j_value + 1:
                    break
            if count == j_value + 1:
                break
                

                    
    elif nwk_select == 2:                                   ##ice and tro share pumps, fir is served by its own                       
        count = 0                                           ##maximum value of count = 12
        for i in range (0,4):
            for j in range (0,3):
                if count == j_value:
                    if i == 0:
                        return_value.append(1)
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(0)
                    elif i == 1:
                        return_value.append(0)
                        return_value.append(1)
                        return_value.append(0)
                        return_value.append(0)
                    elif i == 2:
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(1)
                        return_value.append(0)                        
                    else:
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(1)
                    
                    if j == 0:
                        return_value.append(1)
                        return_value.append(0)
                        return_value.append(0)
                    elif j == 1:
                        return_value.append(0)
                        return_value.append(1)
                        return_value.append(0) 
                    else:
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(1)                         
                                                  
                count = count + 1
                if count == j_value + 1:
                    break
            if count == j_value + 1:
                break
            
    elif nwk_select == 3:                                   ##ice is served by its own pumps, tro and fir share pumps
        count = 0                                           ##maximum value of count = 10
        for i in range (0,2):
            for j in range (0,5):
                if count == j_value:
                    if i == 0:
                        return_value.append(1)
                        return_value.append(0)
                    else:
                        return_value.append(0)
                        return_value.append(1) 
                
                    if j == 0:
                        return_value.append(1)
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(0)
                    elif j == 1:
                        return_value.append(0)
                        return_value.append(1)
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(0)
                    elif j == 2:
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(1)
                        return_value.append(0)
                        return_value.append(0)
                    elif j == 3:
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(1)
                        return_value.append(0)
                    else:
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(0)
                        return_value.append(1)
                
                count = count + 1
                if count == j_value + 1:
                    break
            if count == j_value + 1:
                break
                       
    else:
        count = 0
        for i in range (0,7):
            if count == j_value:
                if i == 0:
                    return_value.append(1)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                elif i == 1:
                    return_value.append(0)
                    return_value.append(1)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                elif i == 2:
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(1)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                elif i == 3:
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(1)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                elif i == 4:
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(1)
                    return_value.append(0)
                    return_value.append(0)
                elif i == 5:
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(1)
                    return_value.append(0)
                else:
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(0)
                    return_value.append(1)
                    
            count = count + 1
            if count == j_value + 1:
                break
                
    return return_value
