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
    layer = ['temp_chil', 'chil2sp1_temp']                                ##Layer to handle all chiller evaporator outlet temperatures
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)

    layer = ['temp_chil', 'sp1_temp2cp']                               
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)   
    
    layer = ['temp_chil', 'sp1_temp2cb']                                
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'distnwk_flow_consol']                                
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
        
    layer = ['flow', 'chil2distnwk_flow']                              
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['temp_chil', 'ss2sp2_temp']                              
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)

    layer = ['balancing_only', 'sp2_2_chret_temp']                              
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)

    return layerslist


