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
    
def checktype_layers (unit_type):                  ##Input the unit type here

    ##unit_type     --- a variable to store the type of unit

    unit_type = 'layers'
    
    return unit_type

##Function to record the list of layers 
def layers (layerslist):
    
    ##layerlist         --- the list of layers
    
    import pandas as pd 
    
    ##Layers definition

    ##Type and name in layer variable 
    
    ##Chiller evaporator side layers
    layer = ['flow', 'ch1_2_ch1evapnwk_flow']                                   ##Chiller 1 evap to evap network flow                                 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['flow', 'ch2_2_ch2evapnwk_flow']                                   ##Chiller 2 evap to evap network flow               
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['temp_chil', 'chil2sp1_temp']                                      ##Chillers evap outlet temperatures to splitter1_temp temp                   
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    
    ##Evaporator network to evaporator pumps 
    layer = ['flow', 'ch1evapnwk_2_ch1pump_flow']                               ##Chiller 1 evap nwk to chiller 1 evap pump flow                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    layer = ['flow', 'ch2evapnwk_2_ch2pump_flow']                               ##Chiller 2 evap nwk to chiller 2 evap pump flow                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)                
    
    layer = ['pressure', 'ch1evapnwk_2_ch1pump_delp']                           ##Chiller 1 evap nwk to chiller 1 evap pump delp                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    layer = ['pressure', 'ch2evapnwk_2_ch2pump_delp']                           ##Chiller 2 evap nwk to chiller 2 evap pump delp                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)        

       
    ##Evaporator pumps to distribution network and common pipe
    layer = ['flow', 'evap_nwk_flow']                                           ##Evaporator pumps to distribution network and common pipe flow                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    

    ##Splitter1_temp to substations 
    layer = ['temp_chil', 'sp12cp_temp']                                        ##Splitter1_temp to common pipe temp                                 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)              
    
    layer = ['temp_chil', 'sp12gv2_temp']                                       ##Splitter1_temp to gv2 substation temp                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)       
    
    layer = ['temp_chil', 'sp12hsb_temp']                                       ##Splitter1_temp to hsb substation temp                                 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)         

    
    ##Ice_network, gv2_network and hsb_network 
    layer = ['flow', 'ice_outlet_flow']                                         ##Ice_network to gv2_network and hsb_network flow                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)
    
    layer = ['flow', 'gv2nwk2ss_flow']                                          ##Gv2_network to gv2_substation flow                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    layer = ['pressure', 'gv2_consol_delp']                                     ##Ice_network and gv2_network delp                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)      
    
    layer = ['flow', 'hsbnwk2ss_flow']                                          ##Hsb_network to hsb_substation flow                                  
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    layer = ['pressure', 'hsb_consol_delp']                                     ##Ice_network and hsb_network delp                                 
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)    
    
    
    ##Distribution pump related layers 
    layer = ['flow', 'distnwk_consol_flow']                                     ##All substations to dist_nwk_pump flow                            
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)         

    layer = ['pressure', 'paranwk2distpump_delp']                               ##All parallel network to dist_nwk_pump delp                             
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)  
    
    
    ##Substation to splitter2_temp return temperature 
    layer = ['temp_chil', 'ss2sp2_temp']                                        ##The consolidation of return temperatures from all substations into splitter2_temp                          
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)     
    
    
    ##All return layers
    layer = ['balancing_only', 'evapnwk_consol_flow']                           ##The consolidation of flow from all substations and the common pipe                          
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)     
    
    layer = ['balancing_only', 'sp22chilret_temp']                              ##The consolidation of return temperatures from all splitter2_temp to return temperature unit                         
    layerdf = pd.DataFrame(data = [layer], columns=['Type', 'Name'])
    layerslist = layerslist.append(layerdf, ignore_index=True)     
    
    return layerslist


