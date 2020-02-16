##This function returns the related evaporator pump coefficients 

def evap_pump_data():
    import numpy as np 
    
    ##The data for the pump curve 
    pump_curve = np.zeros((3,3))
    
    pump_curve[0,0] = -0.0001266405
    pump_curve[0,1] = 0.0112272822
    pump_curve[0,2] = 12.3463827922

    pump_curve[1,0] = -0.0000136254
    pump_curve[1,1] = 0.0001647403
    pump_curve[1,2] = 21.4327511013

    pump_curve[2,0] = -0.0000136254
    pump_curve[2,1] = 0.0001647403
    pump_curve[2,2] = 21.4327511013    
    
    ##The data for the pump power consumption 
    pump_power = np.zeros((3,4))
    
    pump_power[0,0] = -0.0000003355
    pump_power[0,1] = 0.0001014045
    pump_power[0,2] = 0.0053863673
    pump_power[0,3] = 3.8221779914

    pump_power[1,0] = 0
    pump_power[1,1] = -0.0000106288
    pump_power[1,2] = 0.0310754128
    pump_power[1,3] = 18.9432666214

    pump_power[2,0] = 0
    pump_power[2,1] = -0.0000106288
    pump_power[2,2] = 0.0310754128   
    pump_power[2,3] = 18.9432666214

    ##There is no selection of the pumps
    curve_data = pump_curve 
    power_data = pump_power
    
    return curve_data, power_data 