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
    
def checktype_layers_4nc (unit_type):                  ##Input the unit type here
    unit_type = 'layers'
    return unit_type
    
def layers_4nc (layerslist):
    import pandas as pd 
    
    ##Layers definition

    ##Type and name in layer variable\    
         
    ##All return layers
    layer = ['balancing_only', 'dist_nwk_outlet']                           ##The consolidation of flow from all substations and the common pipe                          
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True) 
    
    layer = ['balancing_only', 'evapnwk_consol_flow']                           ##The consolidation of flow from all substations and the common pipe                          
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)         
    
    
    return layerslist


