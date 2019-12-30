import matplotlib.pyplot as plt 
import pandas as pd 
import numpy as np

data_processed = pd.read_csv('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\validation_scripts\\output_csv_files\\chiller1_models_output.csv')

##Calculating absloute error 
dim_data_processed = data_processed.shape

mae_error = 0
for i in range (0, dim_data_processed[0]):
    mae_error = mae_error + abs(data_processed['E_m1'][i] - data_processed['E_m3'][i])

mae_error_final = mae_error / dim_data_processed[0]

print(mae_error_final)

##Writing the y = x line 

fig = plt.figure()
plt.plot(data_processed['E_m1'][:], data_processed['E_m3'][:], '.', label = '')
plt.ylabel('Abstracted GNU model, n=4, m=8, ' + r'$\.E$ (kWh)')
plt.xlabel('GNU model, ' + r'$\.E$ (kWh)')
plt.axes().get_xaxis().set_ticks([])
plt.axes().get_yaxis().set_ticks([])

lims = [
    np.min([plt.axes().get_xlim(), plt.axes().get_ylim()]),  # min of both axes
    np.max([plt.axes().get_xlim(), plt.axes().get_ylim()]),  # max of both axes
    ]
# now plot both limits against eachother
plt.axes().plot(lims, lims, 'k-', alpha=0.75, zorder=0, label = 'y = x')
plt.axes().set_xlim(lims)
plt.axes().set_ylim(lims)

plt.legend(loc = 'best')

plt.savefig('C:\\Optimization_zlc\\simulation_models\\ecoenergies_models\\validation_scripts\\output_csv_files\\gnu_compare.png', dpi = 1000)