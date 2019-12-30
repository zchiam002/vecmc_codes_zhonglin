##This is the cooling tower model 

##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'utility'
    return unit_type
    
def cooling_tower5 (ct5_mdv, utilitylist, streams, cons_eqns, cons_eqns_terms):
    from cooling_tower5_compute import cooling_tower5_compute
    import pandas as pd
    import numpy as np
    
    ##Model description:
    ##Built based on the Universal Engineering Model for Cooling Towers by L.Lu
    ##The regression based model is further linearized into 2 steps illustrating the dependency of the cooling tower inlet temperature and the fan power consumption 
    ##This is all calculated based fixed exit temperatures and ambient conditions
    ##The assumption made in this model is that the temperature of make up water is neglected. 
    ##The water conspution is linear to the delta t, computed using rules of the thumb
    
    ##Legend of input variables 
    ##ct5_tin                   - the predefined inlet temperature for the cooling tower
    ##ct5_totalconfigflow       - the total flowrate through all parallel cooling tower units (this is only 1 of the units)
    ##ct5_twb                   - the current wet_bulb temperature 
    
    ##Processing list of master decision variables as parameters 
    ct5_tin = ct5_mdv['Value'][0]
    ct5_totalconfigflow = ct5_mdv['Value'][1]
    ct5_twb = ct5_mdv['Value'][2]
    
    ##Define dictionary of values
    
    cooling_tower5 = {}
    #Input constants 
    
    ##1
    ct5_ct_total_towers = {}                                                    ##The total number of cooling towers in the given configuration, i.e. parallel to this unit
    ct5_ct_total_towers['value'] = 5
    ct5_ct_total_towers['units'] = '-'
    ct5_ct_total_towers['status'] = 'cst_input'
    cooling_tower5['ct5_ct_total_towers'] = ct5_ct_total_towers 

    ##2
    ct5_tempin = {}
    ct5_tempin['value'] = ct5_tin
    ct5_tempin['units'] = '-'
    ct5_tempin['status'] = 'cst_input'
    cooling_tower5['ct5_tempin'] = ct5_tempin    

    ##3
    ct5_totalcflow = {}
    ct5_totalcflow['value'] = ct5_totalconfigflow
    ct5_totalcflow['units'] = '-'
    ct5_totalcflow['status'] = 'cst_input'
    cooling_tower5['ct5_totalcflow'] = ct5_totalcflow   

    ##4
    ct5_t_wetbulb = {}
    ct5_t_wetbulb['value'] = ct5_twb
    ct5_t_wetbulb['units'] = 'K'
    ct5_t_wetbulb['status'] = 'cst_input'
    cooling_tower5['ct5_t_wetbulb'] = ct5_t_wetbulb   


    ##Defined constants 
    
    ##5
    ct5_c0 = {}                                                                 ##These are regression dervied constants 
    ct5_c0['value'] = -0.00438358798331472
    ct5_c0['units'] = '-'
    ct5_c0['status'] = 'cst_input'
    cooling_tower5['ct5_c0'] = ct5_c0 

    ##6
    ct5_c1 = {}
    ct5_c1['value'] = 1.91940641297341
    ct5_c1['units'] = '-'
    ct5_c1['status'] = 'cst_input'
    cooling_tower5['ct5_c1'] = ct5_c1 

    ##7
    ct5_c2 = {}
    ct5_c2['value'] = 0.00416533100346986
    ct5_c2['units'] = '-'
    ct5_c2['status'] = 'cst_input'
    cooling_tower5['ct5_c2'] = ct5_c2 

    ##8
    ct5_c3 = {}
    ct5_c3['value'] = -0.000998423522765983
    ct5_c3['units'] = '-'
    ct5_c3['status'] = 'cst_input'
    cooling_tower5['ct5_c3'] = ct5_c3 

    ##9
    ct5_c4 = {}
    ct5_c4['value'] = -0.0000392281842431352
    ct5_c4['units'] = '-'
    ct5_c4['status'] = 'cst_input'
    cooling_tower5['ct5_c4'] = ct5_c4 

    ##10
    ct5_c5 = {}
    ct5_c5['value'] = 0.00099995800591648
    ct5_c5['units'] = '-'
    ct5_c5['status'] = 'cst_input'
    cooling_tower5['ct5_c5'] = ct5_c5 

    ##11
    ct5_lin_fan_coeff = {}                                                      ##This is calculated based on the maximum power consumption of 22kWh with linear assumption
    ct5_lin_fan_coeff['value'] = 0.0000596016981065624
    ct5_lin_fan_coeff['units'] = '-'
    ct5_lin_fan_coeff['status'] = 'cst_input'
    cooling_tower5['ct5_lin_fan_coeff'] = ct5_lin_fan_coeff  

    #12
    ct5_max_fan_power = {}
    ct5_max_fan_power['value'] = 22
    ct5_max_fan_power['units'] = 'kWh'
    ct5_max_fan_power['status'] = 'cst_input'
    cooling_tower5['ct5_max_fan_power'] = ct5_max_fan_power

    ##13
    ct5_drift_perc = {}
    ct5_drift_perc['value'] = 0.0027
    ct5_drift_perc['units'] = '-'
    ct5_drift_perc['status'] = 'cst_input'
    cooling_tower5['ct5_drift_perc'] = ct5_drift_perc  

    ##14
    ct5_evap_perc = {}
    ct5_evap_perc['value'] = 0.01 / 5.6
    ct5_evap_perc['units'] = '-'
    ct5_drift_perc['status'] = 'cst_input'
    cooling_tower5['ct5_evap_perc'] = ct5_evap_perc  

    ##15
    ct5_water_adj_coeff = {}
    ct5_water_adj_coeff['value'] = 0.6351                                       ##Regression derived correlation factor 
    ct5_water_adj_coeff['units'] = '-'
    ct5_water_adj_coeff['status'] = 'cst_input'
    cooling_tower5['ct5_water_adj_coeff'] = ct5_water_adj_coeff    

    ##Dependent constants
    ct5_dc = np.zeros((15,1))                                                   ##Initialize the list, note the number of constants 
    
    ct5_dc[0,0] = cooling_tower5['ct5_ct_total_towers']['value']
    ct5_dc[1,0] = cooling_tower5['ct5_tempin']['value']
    ct5_dc[2,0] = cooling_tower5['ct5_totalcflow']['value']
    ct5_dc[3,0] = cooling_tower5['ct5_t_wetbulb']['value']
    ct5_dc[4,0] = cooling_tower5['ct5_c0']['value']
    ct5_dc[5,0] = cooling_tower5['ct5_c1']['value']
    ct5_dc[6,0] = cooling_tower5['ct5_c2']['value']
    ct5_dc[7,0] = cooling_tower5['ct5_c3']['value']
    ct5_dc[8,0] = cooling_tower5['ct5_c4']['value']
    ct5_dc[9,0] = cooling_tower5['ct5_c5']['value']
    ct5_dc[10,0] = cooling_tower5['ct5_lin_fan_coeff']['value'] 
    ct5_dc[11,0] =  cooling_tower5['ct5_max_fan_power']['value']
    ct5_dc[12,0] = cooling_tower5['ct5_drift_perc']['value']
    ct5_dc[13,0] = cooling_tower5['ct5_evap_perc']['value']
    ct5_dc[14,0] = cooling_tower5['ct5_water_adj_coeff']['value']

    ct5_dc_calc = cooling_tower5_compute(ct5_dc)
    
    ##16
    ct5_delt_min = {}
    ct5_delt_min['value'] = ct5_dc_calc[0,0]
    ct5_delt_min['units'] = 'K'
    ct5_delt_min['status'] = 'calc'
    cooling_tower5['ct5_delt_min'] = ct5_delt_min 
    
    ##17
    ct5_delt_max = {}
    ct5_delt_max['value'] = ct5_dc_calc[1,0]
    ct5_delt_max['units'] = 'K'
    ct5_delt_max['status'] = 'calc'
    cooling_tower5['ct5_delt_max'] = ct5_delt_max

    ##18
    ct5_max_power_at_max_delt = {}
    ct5_max_power_at_max_delt['value'] = ct5_dc_calc[2,0]
    ct5_max_power_at_max_delt['units'] = 'K'
    ct5_max_power_at_max_delt['status'] = 'calc'
    cooling_tower5['ct5_max_power_at_max_delt'] = ct5_max_power_at_max_delt

    ##19
    ct5_fmax = {}
    ct5_fmax['value'] = ct5_dc_calc[3,0]
    ct5_fmax['units'] = 'K'
    ct5_fmax['status'] = 'calc'
    cooling_tower5['ct5_fmax'] = ct5_fmax

    ##20
    ct5_min_water_cons = {}
    ct5_min_water_cons['value'] = ct5_dc_calc[4,0]
    ct5_min_water_cons['units'] = 'm3/h'
    ct5_min_water_cons['status'] = 'calc'
    cooling_tower5['ct5_min_water_cons'] = ct5_min_water_cons

    ##21
    ct5_grad_water_cons_coeff = {}
    ct5_grad_water_cons_coeff['value'] = ct5_dc_calc[5,0]
    ct5_grad_water_cons_coeff['units'] = '-'
    ct5_grad_water_cons_coeff['status'] = 'calc'
    cooling_tower5['ct5_grad_water_cons_coeff'] = ct5_grad_water_cons_coeff

    ##Unit definition 
    
    ##Unit 1
    ct5 = {}
    ct5['Name'] = 'ct5'
    ct5['Fmin'] = 0
    ct5['Fmax'] = cooling_tower5['ct5_fmax']['value']                           ##The maximum is determined by the maximum power consumed at maximum achievable delta t 
    ct5['Cost1'] = 0                                                            ##With this embedded in the model, there is no longer a need for an explicit constraint 
    ct5['Cost2'] = 0
    ct5['Cinv1'] = 0
    ct5['Cinv2'] = 0
    ct5['Power1'] = 0
    ct5['Power2'] = cooling_tower5['ct5_max_power_at_max_delt']['value']
    ct5['Impact1'] = 0
    ct5['Impact2'] = 0

    unitinput = [ct5['Name'], ct5['Fmin'], ct5['Fmax'], ct5['Cost1'], ct5['Cost2'], ct5['Cinv1'], ct5['Cinv2'], 
                 ct5['Power1'], ct5['Power2'], ct5['Impact1'], ct5['Impact2']]   
    unitdf = pd.DataFrame(data = [unitinput], columns=['Name', 'Fmin', 
                                   'Fmax', 'Cost1', 'Cost2', 'Cinv1', 'Cinv2', 'Power1', 'Power2', 'Impact1', 'Impact2'])
    utilitylist = utilitylist.append(unitdf, ignore_index=True)
    
    ##Layer and stream definition 
    
    ##Stream 1
    stream1 = {}
    stream1['Unit_Name'] = 'ct5'
    stream1['Type'] = 'balancing_only'
    stream1['Name'] = 'ct5_tout'
    stream1['Layer'] = 'ct2chilcond_ret'
    stream1['Min_Flow'] = cooling_tower5['ct5_tempin']['value'] / cooling_tower5['ct5_ct_total_towers']['value']
    stream1['Grad_Flow'] = -cooling_tower5['ct5_delt_max']['value'] / cooling_tower5['ct5_ct_total_towers']['value']
    stream1['InOut'] = 'out'
    
    streaminput = [stream1['Unit_Name'], stream1['Type'], stream1['Name'], stream1['Layer'], stream1['Min_Flow'], stream1['Grad_Flow'], 
                   stream1['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True) 
    
    ##Stream 2
    stream2 = {}
    stream2['Unit_Name'] = 'ct5'
    stream2['Type'] = 'balancing_only'
    stream2['Name'] = 'ct5_water_in'
    stream2['Layer'] = 'water_exchange'
    stream2['Min_Flow'] = cooling_tower5['ct5_min_water_cons']['value']
    stream2['Grad_Flow'] = cooling_tower5['ct5_grad_water_cons_coeff']['value']
    stream2['InOut'] = 'in'
    
    streaminput = [stream2['Unit_Name'], stream2['Type'], stream2['Name'], stream2['Layer'], stream2['Min_Flow'], stream2['Grad_Flow'], 
                   stream2['InOut']]
    streamdf = pd.DataFrame(data = [streaminput], columns=['Parent', 'Type', 'Name', 'Layer', 'Flow_min', 'Flow_grad', 'InOut'])
    streams = streams.append(streamdf, ignore_index=True)    
    
    return utilitylist, streams, cons_eqns, cons_eqns_terms
    
    
    
    
    
    
    
    
