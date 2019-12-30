##This function returns the related evaporator pump coefficients 

def cond_pump_data():
    import numpy as np 
    
    ##The data for the pump curve 
    pump_curve = np.zeros((3,3))
    
    pump_curve[0,0] = -0.0000552287
    pump_curve[0,1] = 0.0127459461
    pump_curve[0,2] = 28.8570326545

    pump_curve[1,0] = -0.0000090818
    pump_curve[1,1] = 0.0029568794
    pump_curve[1,2] = 45.1880038403

    pump_curve[2,0] = -0.0000090818
    pump_curve[2,1] = 0.0029568794
    pump_curve[2,2] = 45.1880038403    
    
    ##The data for the pump power consumption 
    pump_power = np.zeros((3,4))
    
    pump_power[0,0] = -0.0000218828
    pump_power[0,1] = 0.0599176697
    pump_power[0,2] = 22.8337836011

    pump_power[1,0] = -0.0000228942
    pump_power[1,1] = 0.0721558792
    pump_power[1,2] = 76.4863706961

    pump_power[2,0] = -0.0000228942
    pump_power[2,1] = 0.0721558792
    pump_power[2,2] = 76.4863706961   

    ##There is no selection of the pumps
    curve_data = pump_curve 
    power_data = pump_power
    
    return curve_data, power_data 