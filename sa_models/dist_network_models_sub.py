##This sub model helps the main script deal with the pump selection and network choice 

def dist_nwk_pump_select (choice):
    
    ##choice            --- the choice of the pump and network configuration
    
    ##Pump parameters for pressure drop and electricity 
    ##The pressure drop curves will be in the quadratic form while the electricity curve will be in the cubic form 
    ##The coefficients are arranged in the form of x3, x2, x and the constant 
    ice_1 = [-0.0001037875, 0.0324647918, 46.1796318122]
    ice_2 = [-0.0000242521, 0.0132106447, 50.3198893609]
    tro_1 = [-0.0000151451, 0.0119236210, 58.2250275059]
    tro_2 = [-0.0000036319, 0.0002190621, 73.1928514998]
    fir_1 = [-0.0001095722, 0.0228923489, 35.2618445622]
    fir_2 = [-0.0000220090, 0.0091939614, 34.0585340963]
    fir_3 = [-0.0000220090, 0.0091939614, 34.0585340963]
    
    ##Linear form, should have better extrapolating properties 
    ice_1_e = [0, 0, 0.0808859098, 25.2120639936]
    ice_2_e = [0, 0, 0.0657066672, 51.3224088316]
    tro_1_e = [0, 0, 0.0681194850, 109.1652441249]
    tro_2_e = [0, 0, 0.0478802545, 258.2809387668]
    fir_1_e = [0, 0, 0.0576830445, 14.9708262065]
    fir_2_e = [0, 0, 0.0426887573, 39.0983410015]
    fir_3_e = [0, 0, 0.0426887573, 39.0983410015]   

    return_values = {}

    if choice == 0:
        return_values['nwk_choice'] = 0
        return_values['ice_branch_pump_delp'] = ice_1
        return_values['ice_branch_pump_elect'] = ice_1_e
        return_values['tro_branch_pump_delp'] = tro_1
        return_values['tro_branch_pump_elect'] = tro_1_e
        return_values['fir_branch_pump_delp'] = fir_1
        return_values['fir_branch_pump_elect'] = fir_1_e
    elif choice == 1:
        return_values['nwk_choice'] = 0
        return_values['ice_branch_pump_delp'] = ice_1
        return_values['ice_branch_pump_elect'] = ice_1_e
        return_values['tro_branch_pump_delp'] = tro_1
        return_values['tro_branch_pump_elect'] = tro_1_e
        return_values['fir_branch_pump_delp'] = fir_2
        return_values['fir_branch_pump_elect'] = fir_2_e        
    elif choice == 2:
        return_values['nwk_choice'] = 0
        return_values['ice_branch_pump_delp'] = ice_1
        return_values['ice_branch_pump_elect'] = ice_1_e
        return_values['tro_branch_pump_delp'] = tro_1
        return_values['tro_branch_pump_elect'] = tro_1_e
        return_values['fir_branch_pump_delp'] = fir_3
        return_values['fir_branch_pump_elect'] = fir_3_e 
    elif choice == 3:
        return_values['nwk_choice'] = 0
        return_values['ice_branch_pump_delp'] = ice_1
        return_values['ice_branch_pump_elect'] = ice_1_e
        return_values['tro_branch_pump_delp'] = tro_2
        return_values['tro_branch_pump_elect'] = tro_2_e
        return_values['fir_branch_pump_delp'] = fir_1
        return_values['fir_branch_pump_elect'] = fir_1_e   
    elif choice == 4:
        return_values['nwk_choice'] = 0
        return_values['ice_branch_pump_delp'] = ice_1
        return_values['ice_branch_pump_elect'] = ice_1_e
        return_values['tro_branch_pump_delp'] = tro_2
        return_values['tro_branch_pump_elect'] = tro_2_e
        return_values['fir_branch_pump_delp'] = fir_2
        return_values['fir_branch_pump_elect'] = fir_2_e 
    elif choice == 5:
        return_values['nwk_choice'] = 0
        return_values['ice_branch_pump_delp'] = ice_1
        return_values['ice_branch_pump_elect'] = ice_1_e
        return_values['tro_branch_pump_delp'] = tro_2
        return_values['tro_branch_pump_elect'] = tro_2_e
        return_values['fir_branch_pump_delp'] = fir_3
        return_values['fir_branch_pump_elect'] = fir_3_e
    elif choice == 6:
        return_values['nwk_choice'] = 0
        return_values['ice_branch_pump_delp'] = ice_2
        return_values['ice_branch_pump_elect'] = ice_2_e
        return_values['tro_branch_pump_delp'] = tro_1
        return_values['tro_branch_pump_elect'] = tro_1_e
        return_values['fir_branch_pump_delp'] = fir_1
        return_values['fir_branch_pump_elect'] = fir_1_e
    elif choice == 7:
        return_values['nwk_choice'] = 0
        return_values['ice_branch_pump_delp'] = ice_2
        return_values['ice_branch_pump_elect'] = ice_2_e
        return_values['tro_branch_pump_delp'] = tro_1
        return_values['tro_branch_pump_elect'] = tro_1_e
        return_values['fir_branch_pump_delp'] = fir_2
        return_values['fir_branch_pump_elect'] = fir_2_e
    elif choice == 8:
        return_values['nwk_choice'] = 0
        return_values['ice_branch_pump_delp'] = ice_2
        return_values['ice_branch_pump_elect'] = ice_2_e
        return_values['tro_branch_pump_delp'] = tro_1
        return_values['tro_branch_pump_elect'] = tro_1_e
        return_values['fir_branch_pump_delp'] = fir_3
        return_values['fir_branch_pump_elect'] = fir_3_e
    elif choice == 9:
        return_values['nwk_choice'] = 0
        return_values['ice_branch_pump_delp'] = ice_2
        return_values['ice_branch_pump_elect'] = ice_2_e
        return_values['tro_branch_pump_delp'] = tro_2
        return_values['tro_branch_pump_elect'] = tro_2_e
        return_values['fir_branch_pump_delp'] = fir_1
        return_values['fir_branch_pump_elect'] = fir_1_e
    elif choice == 10:
        return_values['nwk_choice'] = 0
        return_values['ice_branch_pump_delp'] = ice_2
        return_values['ice_branch_pump_elect'] = ice_2_e
        return_values['tro_branch_pump_delp'] = tro_2
        return_values['tro_branch_pump_elect'] = tro_2_e
        return_values['fir_branch_pump_delp'] = fir_2
        return_values['fir_branch_pump_elect'] = fir_2_e
    elif choice == 11:
        return_values['nwk_choice'] = 0
        return_values['ice_branch_pump_delp'] = ice_2
        return_values['ice_branch_pump_elect'] = ice_2_e
        return_values['tro_branch_pump_delp'] = tro_2
        return_values['tro_branch_pump_elect'] = tro_2_e
        return_values['fir_branch_pump_delp'] = fir_3
        return_values['fir_branch_pump_elect'] = fir_3_e 



    elif choice == 12:
        return_values['nwk_choice'] = 1
        return_values['ice_tro_branch_pump_delp'] = ice_1
        return_values['ice_tro_branch_pump_elect'] = ice_1_e
        return_values['fir_branch_pump_delp'] = fir_1
        return_values['fir_branch_pump_elect'] = fir_1_e         
    elif choice == 13:
        return_values['nwk_choice'] = 1
        return_values['ice_tro_branch_pump_delp'] = ice_1
        return_values['ice_tro_branch_pump_elect'] = ice_1_e
        return_values['fir_branch_pump_delp'] = fir_2
        return_values['fir_branch_pump_elect'] = fir_2_e
    elif choice == 14:
        return_values['nwk_choice'] = 1
        return_values['ice_tro_branch_pump_delp'] = ice_1
        return_values['ice_tro_branch_pump_elect'] = ice_1_e
        return_values['fir_branch_pump_delp'] = fir_3
        return_values['fir_branch_pump_elect'] = fir_3_e
    elif choice == 15:
        return_values['nwk_choice'] = 1
        return_values['ice_tro_branch_pump_delp'] = ice_2
        return_values['ice_tro_branch_pump_elect'] = ice_2_e
        return_values['fir_branch_pump_delp'] = fir_1
        return_values['fir_branch_pump_elect'] = fir_1_e  
    elif choice == 16:
        return_values['nwk_choice'] = 1
        return_values['ice_tro_branch_pump_delp'] = ice_2
        return_values['ice_tro_branch_pump_elect'] = ice_2_e
        return_values['fir_branch_pump_delp'] = fir_2
        return_values['fir_branch_pump_elect'] = fir_2_e
    elif choice == 17:
        return_values['nwk_choice'] = 1
        return_values['ice_tro_branch_pump_delp'] = ice_2
        return_values['ice_tro_branch_pump_elect'] = ice_2_e
        return_values['fir_branch_pump_delp'] = fir_3
        return_values['fir_branch_pump_elect'] = fir_3_e
    elif choice == 18:
        return_values['nwk_choice'] = 1
        return_values['ice_tro_branch_pump_delp'] = tro_1
        return_values['ice_tro_branch_pump_elect'] = tro_1_e
        return_values['fir_branch_pump_delp'] = fir_1
        return_values['fir_branch_pump_elect'] = fir_1_e
    elif choice == 19:
        return_values['nwk_choice'] = 1
        return_values['ice_tro_branch_pump_delp'] = tro_1
        return_values['ice_tro_branch_pump_elect'] = tro_1_e
        return_values['fir_branch_pump_delp'] = fir_2
        return_values['fir_branch_pump_elect'] = fir_2_e
    elif choice == 20:
        return_values['nwk_choice'] = 1
        return_values['ice_tro_branch_pump_delp'] = tro_1
        return_values['ice_tro_branch_pump_elect'] = tro_1_e
        return_values['fir_branch_pump_delp'] = fir_3
        return_values['fir_branch_pump_elect'] = fir_3_e
    elif choice == 21:
        return_values['nwk_choice'] = 1
        return_values['ice_tro_branch_pump_delp'] = tro_2
        return_values['ice_tro_branch_pump_elect'] = tro_2_e
        return_values['fir_branch_pump_delp'] = fir_1
        return_values['fir_branch_pump_elect'] = fir_1_e
    elif choice == 22:
        return_values['nwk_choice'] = 1
        return_values['ice_tro_branch_pump_delp'] = tro_2
        return_values['ice_tro_branch_pump_elect'] = tro_2_e
        return_values['fir_branch_pump_delp'] = fir_2
        return_values['fir_branch_pump_elect'] = fir_2_e
    elif choice == 23:
        return_values['nwk_choice'] = 1
        return_values['ice_tro_branch_pump_delp'] = tro_2
        return_values['ice_tro_branch_pump_elect'] = tro_2_e
        return_values['fir_branch_pump_delp'] = fir_3
        return_values['fir_branch_pump_elect'] = fir_3_e



    elif choice == 24:
        return_values['nwk_choice'] = 2
        return_values['ice_branch_pump_delp'] = ice_1
        return_values['ice_branch_pump_elect'] = ice_1_e
        return_values['tro_fir_branch_pump_delp'] = tro_1
        return_values['tro_fir_branch_pump_elect'] = tro_1_e                                        
    elif choice == 25:
        return_values['nwk_choice'] = 2
        return_values['ice_branch_pump_delp'] = ice_2
        return_values['ice_branch_pump_elect'] = ice_2_e
        return_values['tro_fir_branch_pump_delp'] = tro_1
        return_values['tro_fir_branch_pump_elect'] = tro_1_e 
    elif choice == 26:
        return_values['nwk_choice'] = 2
        return_values['ice_branch_pump_delp'] = ice_1
        return_values['ice_branch_pump_elect'] = ice_1_e
        return_values['tro_fir_branch_pump_delp'] = tro_2
        return_values['tro_fir_branch_pump_elect'] = tro_2_e
    elif choice == 27:
        return_values['nwk_choice'] = 2
        return_values['ice_branch_pump_delp'] = ice_2
        return_values['ice_branch_pump_elect'] = ice_2_e
        return_values['tro_fir_branch_pump_delp'] = tro_2
        return_values['tro_fir_branch_pump_elect'] = tro_2_e
    elif choice == 28:
        return_values['nwk_choice'] = 2
        return_values['ice_branch_pump_delp'] = ice_1
        return_values['ice_branch_pump_elect'] = ice_1_e
        return_values['tro_fir_branch_pump_delp'] = fir_1
        return_values['tro_fir_branch_pump_elect'] = fir_1_e
    elif choice == 29:
        return_values['nwk_choice'] = 2
        return_values['ice_branch_pump_delp'] = ice_2
        return_values['ice_branch_pump_elect'] = ice_2_e
        return_values['tro_fir_branch_pump_delp'] = fir_1
        return_values['tro_fir_branch_pump_elect'] = fir_1_e
    elif choice == 30:
        return_values['nwk_choice'] = 2
        return_values['ice_branch_pump_delp'] = ice_1
        return_values['ice_branch_pump_elect'] = ice_1_e
        return_values['tro_fir_branch_pump_delp'] = fir_2
        return_values['tro_fir_branch_pump_elect'] = fir_2_e
    elif choice == 31:
        return_values['nwk_choice'] = 2
        return_values['ice_branch_pump_delp'] = ice_2
        return_values['ice_branch_pump_elect'] = ice_2_e
        return_values['tro_fir_branch_pump_delp'] = fir_2
        return_values['tro_fir_branch_pump_elect'] = fir_2_e
    elif choice == 32:
        return_values['nwk_choice'] = 2
        return_values['ice_branch_pump_delp'] = ice_1
        return_values['ice_branch_pump_elect'] = ice_1_e
        return_values['tro_fir_branch_pump_delp'] = fir_3
        return_values['tro_fir_branch_pump_elect'] = fir_3_e
    elif choice == 33:
        return_values['nwk_choice'] = 2
        return_values['ice_branch_pump_delp'] = ice_2
        return_values['ice_branch_pump_elect'] = ice_2_e
        return_values['tro_fir_branch_pump_delp'] = fir_3
        return_values['tro_fir_branch_pump_elect'] = fir_3_e     


 
    elif choice == 34:
        return_values['nwk_choice'] = 3
        return_values['ice_tro_fir_branch_pump_delp'] = ice_1
        return_values['ice_tro_fir_branch_pump_elect'] = ice_1_e
    elif choice == 35:
        return_values['nwk_choice'] = 3
        return_values['ice_tro_fir_branch_pump_delp'] = ice_2
        return_values['ice_tro_fir_branch_pump_elect'] = ice_2_e
    elif choice == 36:
        return_values['nwk_choice'] = 3
        return_values['ice_tro_fir_branch_pump_delp'] = tro_1
        return_values['ice_tro_fir_branch_pump_elect'] = tro_1_e
    elif choice == 37:
        return_values['nwk_choice'] = 3
        return_values['ice_tro_fir_branch_pump_delp'] = tro_2
        return_values['ice_tro_fir_branch_pump_elect'] = tro_2_e
    elif choice == 38:
        return_values['nwk_choice'] = 3
        return_values['ice_tro_fir_branch_pump_delp'] = fir_1
        return_values['ice_tro_fir_branch_pump_elect'] = fir_1_e
    elif choice == 39:
        return_values['nwk_choice'] = 3
        return_values['ice_tro_fir_branch_pump_delp'] = fir_2
        return_values['ice_tro_fir_branch_pump_elect'] = fir_2_e
    elif choice == 40:
        return_values['nwk_choice'] = 3
        return_values['ice_tro_fir_branch_pump_delp'] = fir_3
        return_values['ice_tro_fir_branch_pump_elect'] = fir_3_e
                          
    return return_values