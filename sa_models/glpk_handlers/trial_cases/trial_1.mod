## Trial run of an example

set CHILLERS;
set CHILLERS_ALT;
set CONST_TRET;
## Variables 

var util_rate{j1 in CHILLERS}, >=0,<=1;				## Ax <= b, this is x

## Parameters

param elec_max{j1 in CHILLERS};					# Terms in the objective function
param temp_con_lim{i in CONST_TRET};				## Ax <= b, this is b
param temp_con_rows{i in CONST_TRET, j1 in CHILLERS};

minimize elect_cons: sum{j1 in CHILLERS_ALT} util_rate[j1]*elec_max[j1];

s.t. c1{i in CONST_TRET}: sum{k in CHILLERS_ALT} temp_con_rows[i,k]*util_rate[k] = temp_con_lim[i];

data;

set CHILLERS_ALT := ch1 ch3;
set CHILLERS := ch1 ch2 ch3;
set CONST_TRET := const_1;

param elec_max := ch1 447.30 ch2 1567.86 ch3 1567.86;
param temp_con_lim := const_1 2.45;
param temp_con_rows : ch1 ch2 ch3:= const_1 1.1133 4.1809 4.1809;

end;