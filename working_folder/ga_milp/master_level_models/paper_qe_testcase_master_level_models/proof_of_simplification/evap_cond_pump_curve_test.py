##This is the a script to determine the maximum flowrates of the condenser and evaporator pumps 

##AF1 information 
af1_x2 = -0.0001266405
af1_x = 0.0112272822
af1_cst = 12.3463827922

af1_e_x3 = -0.0000003355
af1_e_x2 = 0.0001014045
af1_e_x = 0.0053863673
af1_e_cst = 3.8221779914

##AF2 and 3 information
af2_3_x2 = -0.0000136254
af2_3_x = 0.0001647403
af2_3_cst = 21.4327511013

af2_3_e_x3 = 0
af2_3_e_x2 = -0.0000106288
af2_3_e_x = 0.0310754128
af2_3_e_cst = 18.9432666214

##AR1 information 
ar1_x2 = -0.0000552287
ar1_x = 0.0127459461
ar1_cst = 28.8570326545

ar1_x3 = 0
ar1_x2 = -0.0000218828
ar1_x = 0.0599176697
ar1_cst = 22.8337836011

##AR2 and 3 information 
ar2_3_x2 = -0.0000090818
ar2_3_x = 0.0029568794
ar2_3_cst = 45.1880038403 

ar2_e_x3 = 0
ar2_e_x2 = -0.0000228942
ar2_e_x = 0.0721558792
ar2_e_cst = 76.4863706961

##Determining the system curve for the lowest delta p case in each of the chiller evaporators 

##Chiller 1 evaporator network 
ch1_evap_coeff = 0.000246472
ch1_common_coeff = 1.66667E-05



