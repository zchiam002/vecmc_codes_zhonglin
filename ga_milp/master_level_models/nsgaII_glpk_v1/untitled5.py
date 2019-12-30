##This is a test script

from master_to_slave import master_to_slave 
import pandas as pd

sub_station_tinlim = 278.15
sub_station_toutlim = 287.15

twb = 295.6243491
iv = [1800, 30, 50, 0, 0]
demand = pd.DataFrame(data = [iv], columns = ['ss_gv2_demand', 'ss_hsb_demand', 'ss_pfa_demand', 'ss_ser_demand', 'ss_fir_demand'])


allm_var = [259.6844386989431, 
 157.25551631602471, 
 504.39480377758736, 
 1010.4323071712936, 
 448.07100763628119, 
 884.89494697028749, 
 0.17462496392949203, 
 0.10176837941856497, 
 0.11368382476319461, 
 0.18932359748017155, 
 0.20428232363946291, 
 0.21631691076911394, 
 302.93324480622806, 
 9.2385669162692157, 
 287.50782869457453, 
 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0]
 
master_to_slave(allm_var, sub_station_tinlim, sub_station_toutlim, demand, twb)