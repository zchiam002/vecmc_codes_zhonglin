##Example of how the linear program should be developed 

set UTILITIES;
set PROCESSES;
set LAYERS_balancing_only_chil2sp1_in within UTILITIES;
set LAYERS_balancing_only_chil2sp1_out within UTILITIES;
set LAYERS_balancing_only_sp12cp_in within UTILITIES;
set LAYERS_balancing_only_sp12cp_out within UTILITIES;
set LAYERS_balancing_only_sp12gv2_in within UTILITIES;
set LAYERS_balancing_only_sp12gv2_out within UTILITIES;
set LAYERS_balancing_only_sp12hsb_in within UTILITIES;
set LAYERS_balancing_only_sp12hsb_out within UTILITIES;
set LAYERS_balancing_only_sp12pfa_in within UTILITIES;
set LAYERS_balancing_only_sp12pfa_out within UTILITIES;
set LAYERS_balancing_only_sp12ser_in within UTILITIES;
set LAYERS_balancing_only_sp12ser_out within UTILITIES;
set LAYERS_balancing_only_sp12fir_in within UTILITIES;
set LAYERS_balancing_only_sp12fir_out within UTILITIES;
set LAYERS_balancing_only_ss2sp2_in within UTILITIES;
set LAYERS_balancing_only_ss2sp2_out within UTILITIES;
set LAYERS_balancing_only_ss22ch1_in within UTILITIES;
set LAYERS_balancing_only_ss22ch1_out within PROCESSES;
set LAYERS_balancing_only_ss22ch2_in within UTILITIES;
set LAYERS_balancing_only_ss22ch2_out within PROCESSES;
set LAYERS_balancing_only_ss22ch3_in within UTILITIES;
set LAYERS_balancing_only_ss22ch3_out within PROCESSES;

set CONSTRAINTS_unit_binary_rhs_totaluse_ch1;
set CONSTRAINTS_unit_binary_rhs_totaluse_ch2;
set CONSTRAINTS_unit_binary_rhs_totaluse_ch3;

set CONSTRAINTS_unit_binary_eqterms_totaluse_ch1 within UTILITIES; 
set CONSTRAINTS_unit_binary_eqterms_totaluse_ch2 within UTILITIES; 
set CONSTRAINTS_unit_binary_eqterms_totaluse_ch3 within UTILITIES; 

param unit_binary_rhs_totaluse_ch1{r1 in CONSTRAINTS_unit_binary_rhs_totaluse_ch1};
param unit_binary_rhs_totaluse_ch2{r2 in CONSTRAINTS_unit_binary_rhs_totaluse_ch2};
param unit_binary_rhs_totaluse_ch3{r3 in CONSTRAINTS_unit_binary_rhs_totaluse_ch3};

param unit_binary_eqterms_totaluse_ch1{q1 in CONSTRAINTS_unit_binary_eqterms_totaluse_ch1};
param unit_binary_eqterms_totaluse_ch2{q2 in CONSTRAINTS_unit_binary_eqterms_totaluse_ch2};
param unit_binary_eqterms_totaluse_ch3{q3 in CONSTRAINTS_unit_binary_eqterms_totaluse_ch3};

set CONSTRAINTS_stream_limit_ssgv2_in within UTILITIES;
set CONSTRAINTS_stream_limit_ssgv2_out within UTILITIES;
set CONSTRAINTS_stream_limit_sshsb_in within UTILITIES;
set CONSTRAINTS_stream_limit_sshsb_out within UTILITIES;
set CONSTRAINTS_stream_limit_sspfa_in within UTILITIES;
set CONSTRAINTS_stream_limit_sspfa_out within UTILITIES;
set CONSTRAINTS_stream_limit_ssser_in within UTILITIES;
set CONSTRAINTS_stream_limit_ssser_out within UTILITIES;
set CONSTRAINTS_stream_limit_ss_in within UTILITIES;
set CONSTRAINTS_stream_limit_ssgv2_out within UTILITIES;

param stream_limit_ssgv2_in{s1 in CONSTRAINTS_stream_limit_ssgv2_in};
param stream_limit_sshsb_in{s2 in CONSTRAINTS_stream_limit_sshsb_in};
param stream_limit_sspfa_in{s3 in CONSTRAINTS_stream_limit_sspfa_in};
param stream_limit_ssser_in{s4 in CONSTRAINTS_stream_limit_ssser_in};
param stream_limit_ssfir_in{s5 in CONSTRAINTS_stream_limit_ssfir_in};

param stream_limit_ssgv2_out{g1 in CONSTRAINTS_stream_limit_ssgv2_out};
param stream_limit_sshsb_out{g2 in CONSTRAINTS_stream_limit_sshsb_out};
param stream_limit_sspfa_out{g3 in CONSTRAINTS_stream_limit_sspfa_out};
param stream_limit_ssser_out{g4 in CONSTRAINTS_stream_limit_ssser_out};
param stream_limit_ssfir_out{g5 in CONSTRAINTS_stream_limit_ssfir_out};



## Parameters

param fmin_util{j in UTILITIES};
param fmax_util{j in UTILITIES};
param power1_util{j in UTILITIES};
param power2_util{j in UTILITIES};

param fmin_proc{l in PROCESSES};
param fmax_proc{l in PROCESSES};
param power1_proc{l in PROCESSES};
param power2_proc{l in PROCESSES};

param chil2sp1_in_fmin{i1 in LAYERS_balancing_only_chil2sp1_in};
param chil2sp1_in_fgrad{i1 in LAYERS_balancing_only_chil2sp1_in};
param chil2sp1_out_fmin{k1 in LAYERS_balancing_only_chil2sp1_out};
param chil2sp1_out_fgrad{k1 in LAYERS_balancing_only_chil2sp1_out};

param sp12cp_in_fmin{i2 in LAYERS_balancing_only_sp12cp_in};
param sp12cp_in_fgrad{i2 in LAYERS_balancing_only_sp12cp_in};
param sp12cp_out_fmin{k2 in LAYERS_balancing_only_sp12cp_out};
param sp12cp_out_fgrad{k2 in LAYERS_balancing_only_sp12cp_out};

param sp12gv2_in_fmin{i3 in LAYERS_balancing_only_sp12gv2_in};
param sp12gv2_in_fgrad{i3 in LAYERS_balancing_only_sp12gv2_in};
param sp12gv2_out_fmin{k3 in LAYERS_balancing_only_sp12gv2_out};
param sp12gv2_out_fgrad{k3 in LAYERS_balancing_only_sp12gv2_out};

param sp12hsb_in_fmin{i4 in LAYERS_balancing_only_sp12hsb_in};
param sp12hsb_in_fgrad{i4 in LAYERS_balancing_only_sp12hsb_in};
param sp12hsb_out_fmin{k4 in LAYERS_balancing_only_sp12hsb_out};
param sp12hsb_out_fgrad{k4 in LAYERS_balancing_only_sp12hsb_out};

param sp12pfa_in_fmin{i5 in LAYERS_balancing_only_sp12pfa_in};
param sp12pfa_in_fgrad{i5 in LAYERS_balancing_only_sp12pfa_in};
param sp12pfa_out_fmin{k5 in LAYERS_balancing_only_sp12pfa_out};
param sp12pfa_out_fgrad{k5 in LAYERS_balancing_only_sp12pfa_out};

param sp12ser_in_fmin{i6 in LAYERS_balancing_only_sp12ser_in};
param sp12ser_in_fgrad{i6 in LAYERS_balancing_only_sp12ser_in};
param sp12ser_out_fmin{k6 in LAYERS_balancing_only_sp12ser_out};
param sp12ser_out_fgrad{k6 in LAYERS_balancing_only_sp12ser_out};

param sp12fir_in_fmin{i7 in LAYERS_balancing_only_sp12fir_in};
param sp12fir_in_fgrad{i7 in LAYERS_balancing_only_sp12fir_in};
param sp12fir_out_fmin{k7 in LAYERS_balancing_only_sp12fir_out};
param sp12fir_out_fgrad{k7 in LAYERS_balancing_only_sp12fir_out};

param ss2sp2_in_fmin{i8 in LAYERS_balancing_only_ss2sp2_in};
param ss2sp2_in_fgrad{i8 in LAYERS_balancing_only_ss2sp2_in};
param ss2sp2_out_fmin{k8 in LAYERS_balancing_only_ss2sp2_out};
param ss2sp2_out_fgrad{k8 in LAYERS_balancing_only_ss2sp2_out};

param ss22ch1_in_fmin{i9 in LAYERS_balancing_only_ss22ch1_in};
param ss22ch1_in_fgrad{i9 in LAYERS_balancing_only_ss22ch1_in};
param ss22ch1_out_fmin{k9 in LAYERS_balancing_only_ss22ch1_out};
param ss22ch1_out_fgrad{k9 in LAYERS_balancing_only_ss22ch1_out};

param ss22ch2_in_fmin{i10 in LAYERS_balancing_only_ss22ch2_in};
param ss22ch2_in_fgrad{i10 in LAYERS_balancing_only_ss22ch2_in};
param ss22ch2_out_fmin{k10 in LAYERS_balancing_only_ss22ch2_out};
param ss22ch2_out_fgrad{k10 in LAYERS_balancing_only_ss22ch2_out};

param ss22ch3_in_fmin{i11 in LAYERS_balancing_only_ss22ch3_in};
param ss22ch3_in_fgrad{i11 in LAYERS_balancing_only_ss22ch3_in};
param ss22ch3_out_fmin{k11 in LAYERS_balancing_only_ss22ch3_out};
param ss22ch3_out_fgrad{k11 in LAYERS_balancing_only_ss22ch3_out};


## Variables 

var util_rate{j in UTILITIES}, >= 0, <= 100;
var util_onoff{j in UTILITIES}, integer, >=0, <=1;

var proc_rate{l in PROCESSES}, >= fmin_proc[l], <= fmax_proc[l];
var proc_onoff{l in PROCESSES}, = 1;

## Objective function 

minimize power: sum{j in UTILITIES} (util_rate[j]*power2_util[j] + util_onoff[j]*power1_util[j]) +
		sum{l in PROCESSES} (proc_rate[l]*power2_proc[l] + proc_onoff[l]*power1_proc[l]);

## Constraints 

s.t. obj_var1{j in UTILITIES}: (fmin_util[j]*util_onoff[j] - util_rate[j]) <= 0;
s.t. obj_var2{j in UTILITIES}: (util_rate[j] - fmax_util[j]*util_onoff[j]) <= 0;

s.t. lay_cons1: sum{i1 in LAYERS_balancing_only_chil2sp1_in} (chil2sp1_in_fmin[i1]*util_onoff[i1] + chil2sp1_in_fgrad[i1]*util_rate[i1]) - 
	   sum{k1 in LAYERS_balancing_only_chil2sp1_out} (chil2sp1_out_fmin[k1]*util_onoff[k1] + chil2sp1_out_fgrad[k1]*util_rate[k1])
	   = 0;
s.t. lay_cons2: (sum{i2 in LAYERS_balancing_only_sp12cp_in} (sp12cp_in_fmin[i2]*util_onoff[i2] + sp12cp_in_fgrad[i2]*util_rate[i2])) - 
	   (sum{k2 in LAYERS_balancing_only_sp12cp_out} (sp12cp_out_fmin[k2]*util_onoff[k2] + sp12cp_out_fgrad[k2]*util_rate[k2])) 
	   = 0;
s.t. lay_cons3: (sum{i3 in LAYERS_balancing_only_sp12gv2_in} (sp12gv2_in_fmin[i3]*util_onoff[i3] + sp12gv2_in_fgrad[i3]*util_rate[i3])) - 
	   (sum{k3 in LAYERS_balancing_only_sp12gv2_out} (sp12gv2_out_fmin[k3]*util_onoff[k3] + sp12gv2_out_fgrad[k3]*util_rate[k3])) 
	   = 0;
s.t. lay_cons4: (sum{i4 in LAYERS_balancing_only_sp12hsb_in} (sp12hsb_in_fmin[i4]*util_onoff[i4] + sp12hsb_in_fgrad[i4]*util_rate[i4])) - 
	   (sum{k4 in LAYERS_balancing_only_sp12hsb_out} (sp12hsb_out_fmin[k4]*util_onoff[k4] + sp12hsb_out_fgrad[k4]*util_rate[k4])) 
	   = 0;
s.t. lay_cons5: (sum{i5 in LAYERS_balancing_only_sp12pfa_in} (sp12pfa_in_fmin[i5]*util_onoff[i5] + sp12pfa_in_fgrad[i5]*util_rate[i5])) - 
	   (sum{k5 in LAYERS_balancing_only_sp12pfa_out} (sp12pfa_out_fmin[k5]*util_onoff[k5] + sp12pfa_out_fgrad[k5]*util_rate[k5])) 
	   = 0;
s.t. lay_cons6: (sum{i6 in LAYERS_balancing_only_sp12ser_in} (sp12ser_in_fmin[i6]*util_onoff[i6] + sp12ser_in_fgrad[i6]*util_rate[i6])) - 
	   (sum{k6 in LAYERS_balancing_only_sp12ser_out} (sp12ser_out_fmin[k6]*util_onoff[k6] + sp12ser_out_fgrad[k6]*util_rate[k6])) 
	   = 0;
s.t. lay_cons7: (sum{i7 in LAYERS_balancing_only_sp12fir_in} (sp12fir_in_fmin[i7]*util_onoff[i7] + sp12fir_in_fgrad[i7]*util_rate[i7])) - 
	   (sum{k7 in LAYERS_balancing_only_sp12fir_out} (sp12fir_out_fmin[k7]*util_onoff[k7] + sp12fir_out_fgrad[k7]*util_rate[k7])) 
	   = 0;
s.t. lay_cons8: (sum{i8 in LAYERS_balancing_only_ss2sp2_in} (ss2sp2_in_fmin[i8]*util_onoff[i8] + ss2sp2_in_fgrad[i8]*util_rate[i8])) - 
	   (sum{k8 in LAYERS_balancing_only_ss2sp2_out} (ss2sp2_out_fmin[k8]*util_onoff[k8] + ss2sp2_out_fgrad[k8]*util_rate[k8])) 
	   = 0;
s.t. lay_cons9: (sum{i9 in LAYERS_balancing_only_ss22ch1_in} (ss22ch1_in_fmin[i9]*util_onoff[i9] + ss22ch1_in_fgrad[i9]*util_rate[i9])) - 
	   (sum{k9 in LAYERS_balancing_only_ss22ch1_out} (ss22ch1_out_fmin[k9]*proc_onoff[k9] + ss22ch1_out_fgrad[k9]*proc_rate[k9])) 
	   = 0;
s.t. lay_cons10: (sum{i10 in LAYERS_balancing_only_ss22ch2_in} (ss22ch2_in_fmin[i10]*util_onoff[i10] + ss22ch2_in_fgrad[i10]*util_rate[i10])) - 
	   (sum{k10 in LAYERS_balancing_only_ss22ch2_out} (ss22ch2_out_fmin[k10]*proc_onoff[k10] + ss22ch2_out_fgrad[k10]*proc_rate[k10])) 
	   = 0;
s.t. lay_cons11: (sum{i11 in LAYERS_balancing_only_ss22ch3_in} (ss22ch3_in_fmin[i11]*util_onoff[i11] + ss22ch3_in_fgrad[i11]*util_rate[i11])) - 
	   (sum{k11 in LAYERS_balancing_only_ss22ch3_out} (ss22ch3_out_fmin[k11]*proc_onoff[k11] + ss22ch3_out_fgrad[k11]*proc_rate[k11])) 
	   = 0;
s.t. ub_cons1: (sum{r1 in CONSTRAINTS_unit_binary_eqterms_totaluse_ch1} unit_binary_eqterms_totaluse_ch1[r1]*util_onoff[r1]) - 
	       (sum{q1 in CONSTRAINTS_unit_binary_rhs_totaluse_ch1} unit_binary_rhs_totaluse_ch1[q1]) <= 0;

s.t. ub_cons2: (sum{r2 in CONSTRAINTS_unit_binary_eqterms_totaluse_ch2} (unit_binary_eqterms_totaluse_ch2[r2]*util_onoff[r2])) - 
	       (sum{q2 in CONSTRAINTS_unit_binary_rhs_totaluse_ch2} (unit_binary_rhs_totaluse_ch2[q2])) <= 0;

s.t. ub_cons3: (sum{r3 in CONSTRAINTS_unit_binary_eqterms_totaluse_ch3} (unit_binary_eqterms_totaluse_ch3[r3]*util_onoff[r3])) - 
	       (sum{q3 in CONSTRAINTS_unit_binary_rhs_totaluse_ch3} (unit_binary_rhs_totaluse_ch3[q3])) <= 0;

s.t. sl_cons1{s1 in CONSTRAINTS_stream_limit_ssgv2_in} 

 
data;

set CONSTRAINTS_unit_binary_rhs_totaluse_ch1 := totaluse_ch1;
set CONSTRAINTS_unit_binary_rhs_totaluse_ch2 := totaluse_ch2;
set CONSTRAINTS_unit_binary_rhs_totaluse_ch3 := totaluse_ch3;

set CONSTRAINTS_unit_binary_eqterms_totaluse_ch1 := ch1_1 ch1_2 ch1_3 ch1_4; 
set CONSTRAINTS_unit_binary_eqterms_totaluse_ch2 := ch2_1 ch2_2 ch2_3 ch2_4; 
set CONSTRAINTS_unit_binary_eqterms_totaluse_ch3 := ch3_1 ch3_2 ch3_3 ch3_4;

param unit_binary_rhs_totaluse_ch1 := totaluse_ch1 1;
param unit_binary_rhs_totaluse_ch2 := totaluse_ch2 1;
param unit_binary_rhs_totaluse_ch3 := totaluse_ch3 1;

param unit_binary_eqterms_totaluse_ch1 := ch1_1 1 ch1_2 1 ch1_3 1 ch1_4 1;
param unit_binary_eqterms_totaluse_ch2 := ch2_1 1 ch2_2 1 ch2_3 1 ch2_4 1;
param unit_binary_eqterms_totaluse_ch3 := ch3_1 1 ch3_2 1 ch3_3 1 ch3_4 1;

set CONSTRAINTS_stream_limit_ssgv2_in := ssgv2;
set CONSTRAINTS_stream_limit_ssgv2_out := ssgv2;
set CONSTRAINTS_stream_limit_sshsb_in := ssgv2;
set CONSTRAINTS_stream_limit_sshsb_out := ssgv2;
set CONSTRAINTS_stream_limit_sspfa_in := ssgv2;
set CONSTRAINTS_stream_limit_sspfa_out := ssgv2;
set CONSTRAINTS_stream_limit_ssser_in := ssgv2;
set CONSTRAINTS_stream_limit_ssser_out := ssgv2;
set CONSTRAINTS_stream_limit_ss_in := ssgv2;
set CONSTRAINTS_stream_limit_ssgv2_out := ssgv2;

param stream_limit_ssgv2_in := ssgv2 278.15;
param stream_limit_sshsb_in := sshsb 278.15;
param stream_limit_sspfa_in := sspfa 278.15;
param stream_limit_ssser_in := ssser 278.15;
param stream_limit_ssfir_in := ssfir 278.15;

param stream_limit_ssgv2_out := ssgv2 287.15;
param stream_limit_sshsb_out := sshsb 287.15;
param stream_limit_sspfa_out := sspfa 287.15;
param stream_limit_ssser_out := ssser 287.15;
param stream_limit_ssfir_out := ssfir 287.15;

set UTILITIES := ch1_1 ch1_2 ch1_3 ch1_4 ch2_1 ch2_2 ch2_3 ch2_4 ch3_1 ch3_2 ch3_3 ch3_4 sp1 sscp ssgv2 sshsb
		 sspfa ssser ssfir sp2;

set PROCESSES := ch1_ret ch2_ret ch3_ret;

set LAYERS_balancing_only_chil2sp1_in := ch1_1 ch1_2 ch1_3 ch1_4 ch2_1 ch2_2 ch2_3 ch2_4 ch3_1 ch3_2 ch3_3 ch3_4;
set LAYERS_balancing_only_chil2sp1_out := sp1;
set LAYERS_balancing_only_sp12cp_in := sp1;
set LAYERS_balancing_only_sp12cp_out := sscp;
set LAYERS_balancing_only_sp12gv2_in := sp1;
set LAYERS_balancing_only_sp12gv2_out := ssgv2;
set LAYERS_balancing_only_sp12hsb_in := sp1;
set LAYERS_balancing_only_sp12hsb_out := sshsb;
set LAYERS_balancing_only_sp12pfa_in := sp1;
set LAYERS_balancing_only_sp12pfa_out := sspfa;
set LAYERS_balancing_only_sp12ser_in := sp1;
set LAYERS_balancing_only_sp12ser_out := ssser;
set LAYERS_balancing_only_sp12fir_in := sp1;
set LAYERS_balancing_only_sp12fir_out := ssfir;
set LAYERS_balancing_only_ss2sp2_in := sscp ssgv2 sshsb sspfa ssser ssfir;
set LAYERS_balancing_only_ss2sp2_out := sp2;
set LAYERS_balancing_only_ss22ch1_in := sp2;
set LAYERS_balancing_only_ss22ch1_out := ch1_ret;
set LAYERS_balancing_only_ss22ch2_in := sp2;
set LAYERS_balancing_only_ss22ch2_out := ch2_ret;
set LAYERS_balancing_only_ss22ch3_in := sp2;
set LAYERS_balancing_only_ss22ch3_out := ch3_ret;

param fmin_util := ch1_1 0 ch1_2 0.25 ch1_3 0.5 ch1_4 0.75 ch2_1 0 ch2_2 0.25 ch2_3 0.5 ch2_4 0.75 ch3_1 0 ch3_2 0.25 ch3_3 0.5 ch3_4 0.75 
		   sp1 0 sscp 0 ssgv2 0 sshsb 0 sspfa 0 ssser 0 ssfir 0 sp2 0;
param fmax_util := ch1_1 0.25 ch1_2 0.5 ch1_3 0.75 ch1_4 1 ch2_1 0.25 ch2_2 0.5 ch2_3 0.75 ch2_4 1 ch3_1 0.25 ch3_2 0.5 ch3_3 0.75 ch3_4 1 
		   sp1 1 sscp 1 ssgv2 1 sshsb 1 sspfa 1 ssser 1 ssfir 1 sp2 1;
param power1_util := ch1_1 0.000000 ch1_2 23.933993 ch1_3 -68.947931 ch1_4 -225.794971 ch2_1 0.000000 ch2_2 279.491578 
 	       	     ch2_3 34.470608 ch2_4 -367.074916 ch3_1 0.000000 ch3_2 279.491578 ch3_3 34.470608 
		     ch3_4 -367.074916 sp1 0.000000 sscp 0.000000 ssgv2 0.000000 sshsb 0.000000 sspfa 0.000000 
		     ssser 0.000000 ssfir 0.000000 sp2 0.000000;
param power2_util := ch1_1 403.944904 ch1_2 308.208933 ch1_3 493.972780 ch1_4 703.102167 ch2_1 2027.470328 
		     ch2_2 909.504015 ch2_3 1399.545956 ch2_4 1934.939988 ch3_1 2027.470328 ch3_2 909.504015 
		     ch3_3 1399.545956 ch3_4 1934.939988 sp1 0.000000 sscp 0.000000 ssgv2 0.000000 sshsb 0.000000 
		     sspfa 0.000000 ssser 0.000000 ssfir 0.000000 sp2 0.000000;

param fmin_proc := ch1_ret 1 ch2_ret 1 ch3_ret 1;
param fmax_proc := ch1_ret 1 ch2_ret 1 ch3_ret 1;

param power1_proc := ch1_ret 0 ch2_ret 0 ch3_ret 0;
param power2_proc := ch1_ret 0 ch2_ret 0 ch3_ret 0;

param chil2sp1_in_fmin := ch1_1 27.872861 ch1_2 27.872861 ch1_3 27.872861 ch1_4 27.872861  ch2_1 128.563570
 			  ch2_2 128.563570 ch2_3 128.563570 ch2_4 128.563570 ch3_1 128.563570 ch3_2 128.563570
 			  ch3_3 128.563570 ch3_4 128.563570;
param chil2sp1_in_fgrad := ch1_1 -0.819310391 ch1_2 -0.819310391 ch1_3 -0.819310391 ch1_4 -0.819310391 ch2_1 -4.894437653
 			   ch2_2 -4.894437653 ch2_3 -4.894437653 ch2_4 -4.894437653 ch3_1 -4.894437653 ch3_2 -4.894437653 
			   ch3_3 -4.894437653 ch3_4 -4.894437653;
param chil2sp1_out_fmin := sp1 0;
param chil2sp1_out_fgrad := sp1 1000;


param sp12cp_in_fmin := sp1 0;
param sp12cp_in_fgrad := sp1 1000;
param sp12cp_out_fmin := sscp 0;
param sp12cp_out_fgrad := sscp 1000;

param sp12gv2_in_fmin := sp1 0;
param sp12gv2_in_fgrad := sp1 1000;
param sp12gv2_out_fmin := ssgv2 0;
param sp12gv2_out_fgrad := ssgv2 1000;

param sp12hsb_in_fmin := sp1 0;
param sp12hsb_in_fgrad := sp1 1000;
param sp12hsb_out_fmin := sshsb 0;
param sp12hsb_out_fgrad := sshsb 1000;

param sp12pfa_in_fmin := sp1 0;
param sp12pfa_in_fgrad := sp1 1000;
param sp12pfa_out_fmin := sspfa 0;
param sp12pfa_out_fgrad := sspfa 1000;

param sp12ser_in_fmin := sp1 0;
param sp12ser_in_fgrad := sp1 1000;
param sp12ser_out_fmin := ssser 0;
param sp12ser_out_fgrad := ssser 1000;

param sp12fir_in_fmin := sp1 0;
param sp12fir_in_fgrad := sp1 1000;
param sp12fir_out_fmin := ssfir 0;
param sp12fir_out_fgrad := ssfir 1000;

param ss2sp2_in_fmin := sscp 0 ssgv2 0.632784448 sshsb 0.632784448 sspfa 0.632784448 ssser 0.632784448 ssfir 0;
param ss2sp2_in_fgrad := sscp 100 ssgv2 299.810165 sshsb 199.873443 sspfa 199.873443 ssser 199.873443 ssfir 0;
param ss2sp2_out_fmin := sp2 0;
param ss2sp2_out_fgrad := sp2 1000;

param ss22ch1_in_fmin := sp2 0;
param ss22ch1_in_fgrad := sp2 1000;
param ss22ch1_out_fmin := ch1_ret 0;
param ss22ch1_out_fgrad := ch1_ret 285;

param ss22ch2_in_fmin := sp2 0;
param ss22ch2_in_fgrad := sp2 1000;
param ss22ch2_out_fmin := ch2_ret 0;
param ss22ch2_out_fgrad := ch2_ret 285;

param ss22ch3_in_fmin := sp2 0;
param ss22ch3_in_fgrad := sp2 1000;
param ss22ch3_out_fmin := ch3_ret 0;
param ss22ch3_out_fgrad := ch3_ret 285;
end;