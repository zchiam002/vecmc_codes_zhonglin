##This function is used to check the number of objective functions. If it is a mono objective problem, it will return an error. 

def nsga_ii_para_imple_objective_description_function(input_v):
    
    ##input_v['population']                     ---     population
    ##input_v['generations']                    ---     generations
    ##input_v['num_obj_func']                   ---     num_obj_func    
    ##input_v['selection_choice_data']          ---     selection_choice_data
    ##input_v['crossover_perc']                 ---     crossover_perc
    ##input_v['mutation_distribution_index']    ---     mutation_distribution_index
    ##input_v['mutation_perc']                  ---     mutation_perc
    ##input_v['crossover_distribution_index']   ---     crossover_distribution_index    
    ##input_v['variable_list']                  ---     variable_list
    ##input_v['initial_variable_values']        ---     initial_variable_values
    ##input_v['parallel_process']               ---     parallel_process
    ##input_v['obj_func_plot']                  ---     obj_func_plot
    ##input_v['cores_used']                     ---     cores_used     
    ##input_v['objAll']                         ---     []
    ##input_v['xAll']                           ---     []
   
    number_of_objectives = input_v['num_obj_func']

    if number_of_objectives < 2:
        print ('This is a multi-objective optimization function hence the minimum number of objectives is two')
        return
    
    else:
        dim_variable_list = input_v['variable_list'].shape
        
        number_of_decision_variables = dim_variable_list[0]
            
        return number_of_objectives, number_of_decision_variables
        
##Copyright (c) 2009, Aravind Seshadri
##All rights reserved.

##Redistribution and use in source and binary forms, with or without  modification, are permitted provided that the following 
##conditions are met:

##   * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer 
##     in the documentation and/or other materials provided with the distribution
##     
##THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT 
##NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL 
##THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES 
##(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
##HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
##ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    
  