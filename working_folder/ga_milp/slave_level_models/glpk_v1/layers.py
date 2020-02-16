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
    layer = ['balancing_only', 'chil2sp1']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    ##Type and name in layer variable    
    layer = ['balancing_only', 'sp12cp']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    ##Type and name in layer variable    
    layer = ['balancing_only', 'sp12gv2']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    ##Type and name in layer variable       
    layer = ['balancing_only', 'sp12hsb']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
     
    ##Type and name in layer variable      
    layer = ['balancing_only', 'sp12pfa']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    ##Type and name in layer variable       
    layer = ['balancing_only', 'sp12ser']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
     
    ##Type and name in layer variable      
    layer = ['balancing_only', 'sp12fir']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)

    ##Type and name in layer variable      
    layer = ['balancing_only', 'ss2sp2']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)

    ##Type and name in layer variable      
    layer = ['balancing_only', 'sp22ch1']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    ##Type and name in layer variable      
    layer = ['balancing_only', 'sp22ch2']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)  
    
    ##Type and name in layer variable      
    layer = ['balancing_only', 'sp22ch3']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True) 
    
    ##Type and name in layer variable 
    layer = ['balancing_only', 'chilcond2sp3']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)  
    
    ##Type and name in layer variable 
    layer = ['balancing_only', 'ct2chilcond_ret']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True) 
    
    ##Type and name in layer variable
    layer = ['balancing_only', 'water_exchange']
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True) 
    
    return layerslist


