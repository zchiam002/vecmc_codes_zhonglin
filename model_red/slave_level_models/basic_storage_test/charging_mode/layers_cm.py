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
    
def checktype_layers_cm (unit_type):                  ##Input the unit type here
    unit_type = 'layers'
    return unit_type
    
def layers_cm (layerslist):
    import pandas as pd 
    
    ##Layers definition

    ##Type and name in layer variable 
    
    ##Chiller evaporator side layers
    layer = ['flow', 'chil_flow']                                               ##Chiller outlet flow to storage, customers, common pipe, etc                           
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['temp_chil', 'chil_temp']                                          ##Chiller outlet temp to storage, customers, common pipe, etc                           
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    ##Storage internal layers
    layer = ['flow', 's_cold_2_hot_flow']                                       ##From the cold layer to the hot layer                          
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)      
    
    ##Return layers 
    layer = ['flow', 'ss_2_ret_flow']                                           ##Flow return layer                          
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        
    
    layer = ['flow', 'ss_2_ret_flow']                                           ##Temp return layer                          
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)      
    
    
    
    
    

    
    return layerslist


