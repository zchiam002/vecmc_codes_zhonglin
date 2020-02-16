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
    
def checktype_layers_nwk_choice_4 (unit_type):                  ##Input the unit type here
    unit_type = 'layers'
    return unit_type
    
def layers_nwk_choice_4 (layerslist):
    import pandas as pd 
    
    ##Layers definition
    
    ##Type and name in layer variable 
    layer = ['balancing_only', 'chil2gv2_temp']                                 ##Layer to handle all chiller evaporator outlet temperatures
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'chil2gv2_flow']                                 ##Layer to handle all chiller evaporator outlet temperatures
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
        
    layer = ['balancing_only', 'chil_flow_check']                               ##Layer to handle all chiller evaporator outlet temperatures
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['balancing_only', 'gv2_ss2ch1_ret']                                ##Layer to handle all chiller evaporator outlet temperatures
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    

    return layerslist


