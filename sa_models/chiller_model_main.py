##This script is dedicated to running the standalone models for the chiller
def run_chiller_model_main ():
    
    from chiller_models import chiller_gnu
    from chiller_models import chiller_gnu_stepwise_cop
    from chiller_models import chiller_gnu_stepwise_cop_lprelax
    
    ###########################################################################
    ##Testing the chiller models
    ###########################################################################
    ##There are 3 models in this section 
        ##1. the original gordon-ng universal chiller model. 
        ##2. where the COP is step-wise linearized. 
        ##3. where bilinear temperature and flowrate variables are also linearized. 

    ##Setting up the parameters for the chiller models (based on the small chiller in ecoenergies la-marina)
    reg_cst = []
    reg_cst.append(0.123020043325872)       ##Regression based constants, please google Gordon-Ng Universal Chiller Model on how to get these values. 
    reg_cst.append(1044.79734873891)
    reg_cst.append(0.0204660495029597)
    qc_coeff = 1.09866273284186             ##Relationship between the condenser and evaporator thermal exchange. This is an average coefficient.
    steps = 4                               ##Number of linear pieces for the chiller's COP
    bilin_pieces = 20                       ##Number of bilinear pieces for linearizing the bilinear variables 
    
    ##Additional variables needed for linearizing certain variables
    mevap_max = 633.6169025                 ##Maximum evaporator flowrate (m3/h)
    mcond_max = 1050                        ##Maximum condenser flowrate (m3/h)
    twb = 30                                ##Thermodynamic wetbulb temperature (deg C)
    
    ##Variables for the chiller model
    Tin_evap = 6.92196897                   ##Inlet temperature to the chiller's evaporator (deg C)
    Tout_evap = 5                           ##Outlet temperature of the chiller's evaporator (deg C)
    Tin_cond = 28.44221012                  ##Inlet temperature to the chiller's condenser (deg C)
    mevap = 217.3903135                     ##Water flowrate at the chiller's evaporator (m3/h)
    mcond = 1050                            ##Water flowrate at the chiller's condenser (m3/h)
    Qe_max = 2000                           ##Maximum cooling capacity of the chiller (kWh)
    
    ##Running model 1
    result_1, result_1_df = chiller_gnu(reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap, mcond, Qe_max)
    ##Running model 2
    result_2, result_2_df = chiller_gnu_stepwise_cop(reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap, mcond, Qe_max, steps)
    ##Running model 3
    result_3, result_3_df = chiller_gnu_stepwise_cop_lprelax (reg_cst, qc_coeff, Tin_evap, Tout_evap, Tin_cond, mevap, mcond, 
                                                              Qe_max, steps, bilin_pieces, mevap_max, mcond_max, twb)
    
    ##Printing the results 
    print('Chiller model 1')
    print(result_1_df)
    print('Chiller model 2')
    print(result_2_df)   
    print('Chiller model 3')
    print(result_3_df)    
    
    return 