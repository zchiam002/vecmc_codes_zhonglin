##This function maps the code number for each pump and network choice 

def convert_dist_nwk_pump_choice():
    import os
    current_directory = os.path.dirname(__file__)[:-76] + '//'     
    import sys 
    sys.path.append(current_directory + 'master_level_models\\chiller_optimization_dist_nwk_ga_nb_master_level_models\\add_ons\\')
    from choose import ncr
    import pandas as pd 
    
    
    ##The number of network choices
    ##This the possible valve combinations which restrict the number of pumps serving each network 
    nwk_choices = 4
    
    ##Choice 1: each parallel network is served by their own pumps 
    ##Choice 2: ice and tro share pumps, fir is served by own pump
    ##Choice 3: tro and fir share pumps, ice is served by own pump
    ##Choice 4: all networks share pumps  
    
    ##Pump choices for each corresponding parallel network 
    ice_pumps = 2
    tro_pumps = 2
    fir_pumps = 3
    
    ##Possible combinations for choice 1
    choice1_pumps = ncr(ice_pumps,1) * ncr(tro_pumps,1) * ncr(fir_pumps,1)
    choice2_pumps = ncr(ice_pumps + tro_pumps, 1) * ncr(fir_pumps, 1)
    choice3_pumps = ncr(tro_pumps + fir_pumps, 1) * ncr(ice_pumps, 1)
    choice4_pumps = ncr(ice_pumps + tro_pumps + fir_pumps, 1)
    
    ##Total number of possible choices
    total_choices = choice1_pumps + choice2_pumps + choice3_pumps + choice4_pumps
    
    ##The idea is that for each of the choices, this function will return 2 outputs
    ##The first is that of the code to activate the associated slave formulation 
    ##The second is that of the code to the parameters of the related pump
    
    ##Assigining combinations 
    choices_lookup_table = pd.DataFrame(columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3'])
    row = 0
    for i in range (0, nwk_choices):
        
        if i == 0:
            ##Enumerating pump combinations for choice 1
            for j in range (0, ice_pumps):
                for k in range (0, tro_pumps):
                    for l in range (0, fir_pumps):
                        nwkc = i
                        
                        if j == 0:
                            ice_1 = 1
                            ice_2 = 0
                        else:
                            ice_1 = 0
                            ice_2 = 1
                            
                        if k == 0:
                            tro_1 = 1
                            tro_2 = 0
                        else:
                            tro_1 = 0
                            tro_2 = 1
                            
                        if l == 0:
                            fir_1 = 1
                            fir_2 = 0 
                            fir_3 = 0
                        elif l == 1:
                            fir_1 = 0 
                            fir_2 = 1
                            fir_3 = 0
                        else:
                            fir_1 = 0
                            fir_2 = 0 
                            fir_3 = 1
                            
                        input_values = [nwkc, ice_1, ice_2, tro_1, tro_2, fir_1, fir_2, fir_3]
                        temp = pd.DataFrame(data = [input_values], columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3'])
                        choices_lookup_table = choices_lookup_table.append(temp, ignore_index=True)
        
        elif i == 1:
            ##Enumerating pump combinations for choice 2
            for j in range (0, ice_pumps + tro_pumps):
                for k in range (0, fir_pumps):
                    nwkc = i
                    
                    if j == 0:
                        ice_1 = 1
                        ice_2 = 0
                        tro_1 = 0
                        tro_2 = 0
                    elif j == 1:
                        ice_1 = 0
                        ice_2 = 1
                        tro_1 = 0
                        tro_2 = 0
                    elif j == 2:
                        ice_1 = 0
                        ice_2 = 0
                        tro_1 = 1
                        tro_2 = 0
                    else:
                        ice_1 = 0
                        ice_2 = 0
                        tro_1 = 0
                        tro_2 = 1
                        
                    if k == 0:
                        fir_1 = 1
                        fir_2 = 0 
                        fir_3 = 0
                    elif k == 1:
                        fir_1 = 0
                        fir_2 = 1
                        fir_3 = 0
                    else:
                        fir_1 = 0
                        fir_2 = 0
                        fir_3 = 1
                        
                    input_values = [nwkc, ice_1, ice_2, tro_1, tro_2, fir_1, fir_2, fir_3]
                    temp = pd.DataFrame(data = [input_values], columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3'])
                    choices_lookup_table = choices_lookup_table.append(temp, ignore_index=True)  
                    
        elif i == 2:
            ##Enumerating pump combinations for choice 3
            for j in range (0, tro_pumps + fir_pumps):
                for k in range (0, ice_pumps):
                    nwkc = i
                    
                    if j == 0:
                        tro_1 = 1
                        tro_2 = 0
                        fir_1 = 0
                        fir_2 = 0
                        fir_3 = 0
                    elif j == 1:
                        tro_1 = 0
                        tro_2 = 1
                        fir_1 = 0
                        fir_2 = 0
                        fir_3 = 0
                    elif j == 2:
                        tro_1 = 0
                        tro_2 = 0
                        fir_1 = 1
                        fir_2 = 0
                        fir_3 = 0
                    elif j == 3:
                        tro_1 = 0
                        tro_2 = 0
                        fir_1 = 0
                        fir_2 = 1
                        fir_3 = 0
                    else:
                        tro_1 = 0
                        tro_2 = 0
                        fir_1 = 0
                        fir_2 = 0
                        fir_3 = 1
    
                    if k == 0:
                        ice_1 = 1
                        ice_2 = 0
                    else:
                        ice_1 = 0
                        ice_2 = 1
    
                    input_values = [nwkc, ice_1, ice_2, tro_1, tro_2, fir_1, fir_2, fir_3]
                    temp = pd.DataFrame(data = [input_values], columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3'])
                    choices_lookup_table = choices_lookup_table.append(temp, ignore_index=True)   
    
        else:
            ##Enumerating pump combinations for choice 4
            for j in range (0, ice_pumps + tro_pumps + fir_pumps):
                nwkc = i
                
                if j == 1:
                    ice_1 = 1
                    ice_2 = 0
                    tro_1 = 0
                    tro_2 = 0
                    fir_1 = 0
                    fir_2 = 0
                    fir_3 = 0
                elif j == 2:
                    ice_1 = 0
                    ice_2 = 1
                    tro_1 = 0
                    tro_2 = 0
                    fir_1 = 0
                    fir_2 = 0
                    fir_3 = 0
                elif j == 3:
                    ice_1 = 0
                    ice_2 = 0
                    tro_1 = 1
                    tro_2 = 0
                    fir_1 = 0
                    fir_2 = 0
                    fir_3 = 0
                elif j == 4:
                    ice_1 = 0
                    ice_2 = 0
                    tro_1 = 0
                    tro_2 = 1
                    fir_1 = 0
                    fir_2 = 0
                    fir_3 = 0
                elif j == 5:
                    ice_1 = 0
                    ice_2 = 0
                    tro_1 = 0
                    tro_2 = 0
                    fir_1 = 1
                    fir_2 = 0
                    fir_3 = 0
                elif j == 6:
                    ice_1 = 0
                    ice_2 = 0
                    tro_1 = 0
                    tro_2 = 0
                    fir_1 = 0
                    fir_2 = 1
                    fir_3 = 0
                else:
                    ice_1 = 0
                    ice_2 = 0
                    tro_1 = 0
                    tro_2 = 0
                    fir_1 = 0
                    fir_2 = 0
                    fir_3 = 1     
                    
                input_values = [nwkc, ice_1, ice_2, tro_1, tro_2, fir_1, fir_2, fir_3]
                temp = pd.DataFrame(data = [input_values], columns = ['nwk_choice', 'ice_1', 'ice_2', 'tro_1', 'tro_2', 'fir_1', 'fir_2', 'fir_3'])
                choices_lookup_table = choices_lookup_table.append(temp, ignore_index=True) 
                
    #choices_lookup_table.to_csv(current_directory + 'master_level_models\\chiller_optimization_dist_nwk_ga_nb_master_level_models\\look_up_tables\\dist_nwk_pump_lookup.csv')
                      
    return choices_lookup_table

