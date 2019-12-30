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
    
def checktype_layers (unit_type):                  ##Input the unit type here
    unit_type = 'layers'
    return unit_type
    
def layers (layerslist):
    import pandas as pd 
    
    ##Layers definition

    ##Type and name in layer variable 
    
    ##General chiller layers  
    layer = ['flow', 'chillers_to_substations_storage_q_out']                               ##Chillers to substations/storage cooling load                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
 
    layer = ['flow', 'chiller_heat_rej']                                                    ##Chillers to cooling towers                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)       
  
    ##Chiller specific layer 
    layer = ['flow', 'chiller1_flow_evap_pump']                                             ##Chiller1 flow to evaporator pump                                 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        

    layer = ['flow', 'chiller1_flow_cond_pump']                                             ##Chiller1 flow to condenser pump                                
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)  
    
    layer = ['flow', 'chiller2_flow_evap_pump']                                             ##Chiller2 flow to evaporator pump                                
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        

    layer = ['flow', 'chiller2_flow_cond_pump']                                             ##Chiller2 flow to condenser pump                                 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['flow', 'chiller3_flow_evap_pump']                                             ##Chiller3 flow to evaporator pump                                 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        

    layer = ['flow', 'chiller3_flow_cond_pump']                                             ##Chiller3 flow to condenser pump                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)  
    
    ##Network layers

    layer = ['flow', 'chiller_2_e_nwk_flow']                                                ##Combined flowrate in the evaporator network                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)   
    
    layer = ['flow', 'chiller_2_c_nwk_flow']                                                ##Combined flowrate in the condenser network                       
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)   
    
    layer = ['pressure', 'e_nwk_2_ep1']                                                     ##Pressure flow from evaporator network to evaporator pump1                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)       
    
    layer = ['pressure', 'e_nwk_2_ep2']                                                     ##Pressure flow from evaporator network to evaporator pump2                         
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        
    
    layer = ['pressure', 'e_nwk_2_ep3']                                                     ##Pressure flow from evaporator network to evaporator pump3                           
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        
    
    layer = ['pressure', 'c_nwk_2_cp1']                                                     ##Pressure flow from condenser network to condenser pump1                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)       
    
    layer = ['pressure', 'c_nwk_2_cp2']                                                     ##Pressure flow from condenser network to condenser pump2                         
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        
    
    layer = ['pressure', 'c_nwk_2_cp3']                                                     ##Pressure flow from condenser network to condenser pump3                           
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)      
    
    layer = ['flow', 'combined_ss_to_dist_nwk_flow']                                        ##The flowrate from the combined substation to the distribution pump                      
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)      
    
    layer = ['pressure', 'combined_ss_to_dist_nwk_pressure']                                ##The pressure flow from the combined substation to the distribution pump                      
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)     
    
    return layerslist


