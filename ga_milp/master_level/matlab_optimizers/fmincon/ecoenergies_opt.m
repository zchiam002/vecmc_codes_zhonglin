function [ value ] = ecoenergies_opt( x )
%This function takes in values from matlab to run python function 
%x is a row with 408 values
csvwrite('C:\Optimization_zlc\master_level\Matlab_Optimizers\Fmincon\temp_value_storage\test_value_in.csv', x) ;
command = 'python C:\Optimization_zlc\master_level\Matlab_Optimizers\Fmincon\fmincon_run_function_script.py' ;
[a, b] = system(command);
y = csvread('C:\Optimization_zlc\master_level\Matlab_Optimizers\Fmincon\temp_value_storage\test_value_out.csv');
disp(y);
value = y;
end

