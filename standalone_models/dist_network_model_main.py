##This script is dedicated to running the standalone models for the distribution network 
def run_distribution_network_model_main ():
    
    from dist_network_models import dist_nwk_org
    from dist_network_models import dist_nwk_piecewise_pressure
    from dist_network_models import dist_nwk_piecewise_pressure_reg_pumpnwk
    from dist_network_models import dist_nwk_piecewise_pressure_reg_pumpnwk_bilinear_temp

    ###########################################################################
    ##Testing the distribution network models
    ###########################################################################
    ##There are 4 models in this section 
        ##1. Original evaporator network model, formulated using first principles.  
        ##2. Piecewise linearization of pressure drop.  
        ##3. Regression of pump and network electricity consumption.
        ##4. Linearization of bilinear temperature and flowrate variables.
        
    
    return 

