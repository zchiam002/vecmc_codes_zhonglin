##This is the layers definition file
##The purpose of layers is to define the stream exchange restriction between units 
##They will translate into strict eqaulity constraints in the linear programming model 
##There will be a few types of layers,
    ##balancing_only (available)
    ##heat_cascade... (tbc)
    
##This function is to check the unit type, make sure that all units defined in this file are of the same type  
##There are only 4 types of units 
    ##layers
    ##process
    ##utility
    ##utility_mt
    
def checktype (unit_type):                  ##Input the unit type here
    unit_type = 'layers'
    return unit_type
    
def layers (layerslist):
    import pandas as pd 
    
    ##Layers definition
    
    ##Type and name in layer variable 
    layer = ['balancing_only', 'chil2sp1_temp']                                 ##Layer to handle all chiller evaporator outlet temperatures
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'chil2distnwk_flow']                             ##To handle all the chiller evaporator flowrates 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'chil2distnwk_flow_check']                       ##Additional layer to make sure that all all the flowrate from evaporator
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])            ##tally with that of the master decision input
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    layer = ['balancing_only', 'ch1_2_evap_flow']                               ##A flowrate layer to calculate the evaporator side pressure drop for Chiller 1
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    layer = ['balancing_only', 'ch2_2_evap_flow']                               ##A flowrate layer to calculate the evaporator side pressure drop for Chiller 2
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        
    
    layer = ['balancing_only', 'ch3_2_evap_flow']                               ##A flowrate layer to calculate the evaporator side pressure drop for Chiller 3
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)     
    
    layer = ['balancing_only', 'ch1_2_cond_flow']                               ##A flowrate layer to calculate the condenser side pressure drop for Chiller 1
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    layer = ['balancing_only', 'ch2_2_cond_flow']                               ##A flowrate layer to calculate the condenser side pressure drop for Chiller 2
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        
    
    layer = ['balancing_only', 'ch3_2_cond_flow']                               ##A flowrate layer to calculate the condenser side pressure drop for Chiller 3
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)  
    
    layer = ['balancing_only', 'ch1_evap_2_pump_flow']                          ##A flowrate layer to connect Chiller 1 evaporator to the correspoding pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        
    
    layer = ['balancing_only', 'ch1_evap_2_pump_delp']                          ##A pressure layer to connect Chiller 1 evaporator to the correspoding pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)   

    layer = ['balancing_only', 'ch2_evap_2_pump_flow']                          ##A flowrate layer to connect Chiller 2 evaporator to the correspoding pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        
    
    layer = ['balancing_only', 'ch2_evap_2_pump_delp']                          ##A pressure layer to connect Chiller 2 evaporator to the correspoding pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)      
    
    layer = ['balancing_only', 'ch3_evap_2_pump_flow']                          ##A flowrate layer to connect Chiller 3 evaporator to the correspoding pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        
    
    layer = ['balancing_only', 'ch3_evap_2_pump_delp']                          ##A pressure layer to connect Chiller 3 evaporator to the correspoding pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)       
    
    layer = ['balancing_only', 'ch1_cond_2_pump_flow']                          ##A flowrate layer to connect Chiller 1 condenser to the correspoding pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        
    
    layer = ['balancing_only', 'ch1_cond_2_pump_delp']                          ##A pressure layer to connect Chiller 1 condenser to the correspoding pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)   

    layer = ['balancing_only', 'ch2_cond_2_pump_flow']                          ##A flowrate layer to connect Chiller 2 condenser to the correspoding pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        
    
    layer = ['balancing_only', 'ch2_cond_2_pump_delp']                          ##A pressure layer to connect Chiller 2 condenser to the correspoding pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)      
    
    layer = ['balancing_only', 'ch3_cond_2_pump_flow']                          ##A flowrate layer to connect Chiller 3 condenser to the correspoding pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        
    
    layer = ['balancing_only', 'ch3_cond_2_pump_delp']                          ##A pressure layer to connect Chiller 3 condenser to the correspoding pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True) 
    
    layer = ['balancing_only', 'chil2condret_temp']                             ##To handle all the chiller condenser outlet temperatures
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'chil2condret_flow']                             ##To handle all the chiller condenser outlet flowrates
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    

    layer = ['balancing_only', 'sp1_temp2cp']                                   ##Temperature outlet from sp1_temp to the common pipe
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)      

    layer = ['balancing_only', 'sp1_temp2gv2']                                  ##Temperature outlet from sp1_temp to gv2
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    layer = ['balancing_only', 'sp1_temp2hsb']                                  ##Temperature outlet from sp1_temp to hsb
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'sp1_temp2pfa']                                  ##Temperature outlet from sp1_temp to pfa
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'sp1_temp2ser']                                  ##Temperature outlet from sp1_temp to ser
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)

    layer = ['balancing_only', 'sp1_temp2fir']                                  ##Temperature outlet from sp1_temp to fir
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)

    layer = ['balancing_only', 'ssret_temp2sp2']                                ##Outlet temperatures from all substations to splitter 2
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'ice_nwk2gv2_nwk']                               ##The flowrate from ice to gv2
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'ice_nwk2hsb_nwk']                               ##The flowrate from ice to hsb 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'ice_nwkandgv2_nwk_delp']                        ##A layer to accumulate all the pressure drop components associated with GV2
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'ice_nwkandhsb_nwk_delp']                        ##A layer to accumulate all the pressure drop components associated with HSB
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'tro_nwk2pfa_nwk']                               ##The flowrate from tro to pfa
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'tro_nwk2ser_nwk']                               ##The flowrate from tro to ser 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'tro_nwkandpfa_nwk_delp']                        ##A layer to accumulate all the pressure drop components associated with PFA
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'tro_nwkandser_nwk_delp']                        ##A layer to accumulate all the pressure drop components associated with SER
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'fir_nwk_delp']                                  ##A layer to accumulate all the pressure drop components associated with FIR
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'gv2_nwk2gv2_ss']                                ##The flowrate from gv2 network to gv2 substation
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)      
    
    layer = ['balancing_only', 'hsb_nwk2hsb_ss']                                ##The flowrate from hsb network to hsb substation
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)      
    
    layer = ['balancing_only', 'pfa_nwk2pfa_ss']                                ##The flowrate from pfa network to pfa substation
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)      
    
    layer = ['balancing_only', 'ser_nwk2ser_ss']                                ##The flowrate from ser network to ser substation
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)  

    layer = ['balancing_only', 'fir_nwk2fir_ss']                                ##The flowrate from fir network to fir substation
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)

    layer = ['balancing_only', 'ss2sp2_temp']                                   ##To capture all outlet temperature streams from the substations
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    layer = ['balancing_only', 'sp2_2_ch1ret_temp']                             ##To capture the return temperature to chiller 1 evaporator 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True) 

    layer = ['balancing_only', 'sp2_2_ch2ret_temp']                             ##To capture the return temperature to chiller 2 evaporator 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True) 

    layer = ['balancing_only', 'sp2_2_ch3ret_temp']                             ##To capture the return temperature to chiller 3 evaporator 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)     
    
    layer = ['balancing_only', 'ss_2_dist_pump_flow']                           ##To capture the entire flowrate through the distribution network at any given time 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)     
    
    layer = ['balancing_only', 'ch1_2_af1_flow']                                ##To capture the flowrate of water that af1 has to pump
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)         
    
    layer = ['balancing_only', 'sp3_2_ct1_temp']                                ##To temperature stream to cooling tower 1
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True) 
    
    layer = ['balancing_only', 'sp3_2_ct2_temp']                                ##To temperature stream to cooling tower 2
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)

    layer = ['balancing_only', 'sp3_2_ct3_temp']                                ##To temperature stream to cooling tower 3
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)

    layer = ['balancing_only', 'sp3_2_ct4_temp']                                ##To temperature stream to cooling tower 4
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)

    layer = ['balancing_only', 'sp3_2_ct5_temp']                                ##To temperature stream to cooling tower 5
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    layer = ['balancing_only', 'ct_cond_ret_temp']                              ##To consolidate the exit temperature of the cooling tower water 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)  
    
    layer = ['network_parallel', 'dist_nwk2_selected_pump']                     ##To handle all the pressure_drops from all the branches in the distribution network
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
 
    
    
    return layerslist


