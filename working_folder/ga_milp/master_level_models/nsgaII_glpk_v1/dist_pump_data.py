##This function returns the related distribution pump coefficients for the selected pumps 

def dist_pump_data(dist_pump):
    import numpy as np
    
    ##dist_pump[0] --- pumpaf1_1
    ##dist_pump[1] --- pumpaf1_2
    ##dist_pump[2] --- pumpaf2_1
    ##dist_pump[3] --- pumpaf2_2
    ##dist_pump[4] --- pumpaf3_1
    ##dist_pump[5] --- pumpaf3_2
    ##dist_pump[6] --- pumpaf3_3
    
    ##The data for the pump curve 
    pump_curve = np.zeros((7,3))
    
    pump_curve[0,0] = -0.0001037875
    pump_curve[0,1] = 0.0324647918
    pump_curve[0,2] = 46.1796318122

    pump_curve[1,0] = -0.0000242521
    pump_curve[1,1] = 0.0132106447
    pump_curve[1,2] = 50.3198893609

    pump_curve[2,0] = -0.0000151451
    pump_curve[2,1] = 0.0119236210
    pump_curve[2,2] = 58.2250275059

    pump_curve[3,0] = -0.0000036319
    pump_curve[3,1] = -0.0002190621
    pump_curve[3,2] = 73.1928514998

    pump_curve[4,0] = -0.0001095722
    pump_curve[4,1] = 0.0228923489
    pump_curve[4,2] = 35.2618445622

    pump_curve[5,0] = -0.0000220090
    pump_curve[5,1] = 0.0091939614
    pump_curve[5,2] = 34.0585340963

    pump_curve[6,0] = -0.0000220090
    pump_curve[6,1] = 0.0091939614
    pump_curve[6,2] = 34.0585340963

    ##The data for the pump power consumption curve 
    pump_power = np.zeros((7,3))
    
    pump_power[0,0] = -0.0000456328
    pump_power[0,1] = 0.1072050404
    pump_power[0,2] = 22.7694786782

    pump_power[1,0] = 0.0000095593
    pump_power[1,1] = 0.0548196056
    pump_power[1,2] = 53.1923042054

    pump_power[2,0] = -0.0000055276
    pump_power[2,1] = 0.0771653808
    pump_power[2,2] = 106.7867892025

    pump_power[3,0] = -0.0000123489
    pump_power[3,1] = 0.0845123896
    pump_power[3,2] = 240.8517560062

    pump_power[4,0] = -0.0000372609
    pump_power[4,1] = 0.0745145187
    pump_power[4,2] = 13.8059958033

    pump_power[5,0] = -0.0000077383
    pump_power[5,1] = 0.0506120010
    pump_power[5,2] = 37.8841630174

    pump_power[6,0] = -0.0000077383
    pump_power[6,1] = 0.0506120010
    pump_power[6,2] = 37.8841630174
    
    
    dim_dist_pump = len(dist_pump)
    
    total = 0
    for i in range (0, dim_dist_pump):
        total = total + dist_pump[i]

    curve_data = np.zeros((total,3))
    power_data = np.zeros((total,3))
    
    count = 0
    for i in range (0, dim_dist_pump):
        if dist_pump[i] == 1:
            curve_data[count,0] = pump_curve[i,0]
            curve_data[count,1] = pump_curve[i,1]
            curve_data[count,2] = pump_curve[i,2]

            power_data[count,0] = pump_power[i,0]
            power_data[count,1] = pump_power[i,1]
            power_data[count,2] = pump_power[i,2]

            count = count + 1
    
    return curve_data, power_data