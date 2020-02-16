##This function is used to completely describe the objective functions and the range for the decision variable space etc. 

def objective_description_function(input_v):
    
    number_of_objectives = input_v['number_of_objectives']

    if number_of_objectives < 2:
        print ('This is a multi-objective optimization function hence the minimum number of objectives is two')
        return
    
    else:
        number_of_decision_variables = input_v['number_of_decision_variables']
        min_range_of_decision_variable = []
        max_range_of_decision_variable = []
        for i in range (0, number_of_decision_variables):
            min_value = input_v['range_of_decision_variables']['Lower_bound'][i]
            max_value = input_v['range_of_decision_variables']['Upper_bound'][i]
            min_range_of_decision_variable.append(min_value)
            max_range_of_decision_variable.append(max_value)
            
        return number_of_objectives, number_of_decision_variables, min_range_of_decision_variable, max_range_of_decision_variable
        
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
    
  