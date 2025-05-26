import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from scipy.stats import linregress

# Load input data
input_file = 'input_data.txt'  # Replace with your input file
with open(input_file, 'r') as file:
    DG_diff_OH_0 = float(file.readline().strip())
    DG_diff_O_0 = float(file.readline().strip())

# Equations for DG_diff^OH and DG_diff^O
def DG_diff_OH(URHE, pH):
    return DG_diff_OH_0 + (-0.04) * (-1.42) * (URHE - 0.059 * pH - 1.5) + (-0.08/2) * ((-1.42) * (URHE - 0.059 * pH - 1.5))**2 - 1 * URHE

def DG_diff_O(URHE, pH):
    return DG_diff_O_0 + (-0.17) * (-1.42) * (URHE - 0.059 * pH - 1.5) + (-0.05/2) * ((-1.42) * (URHE - 0.059 * pH - 1.5))**2 - 2 * URHE

# Function to find URHE where both equations are equal
def find_URHE(pH):
    func = lambda URHE: DG_diff_OH(URHE, pH) - DG_diff_O(URHE, pH)
    URHE_solution = fsolve(func, 1.23)  # Initial guess around 1.23 V
    return URHE_solution[0]

# Range of pH values from 0 to 14
pH_values = np.arange(0, 15, 1)

# Find URHE for each pH
URHE_values = np.array([find_URHE(pH) for pH in pH_values])

# Convert URHE to USHE using the formula: USHE = URHE - 0.059 * pH
USHE_values = URHE_values - 0.059 * pH_values

# Save URHE and USHE vs pH data to text files
with open('URHE_vs_pH.txt', 'w') as urhe_file:
    urhe_file.write('pH\tURHE (V)\n')
    for pH, URHE in zip(pH_values, URHE_values):
        urhe_file.write(f'{pH}\t{URHE:.6f}\n')

with open('USHE_vs_pH.txt', 'w') as ushe_file:
    ushe_file.write('pH\tUSHE (V)\n')
    for pH, USHE in zip(pH_values, USHE_values):
        ushe_file.write(f'{pH}\t{USHE:.6f}\n')

# Perform linear regression for URHE and USHE vs pH
slope_urhe, intercept_urhe, _, _, _ = linregress(pH_values, URHE_values)
slope_ushe, intercept_ushe, _, _, _ = linregress(pH_values, USHE_values)

# Plot URHE vs pH
plt.figure(figsize=(8, 6))
plt.plot(pH_values, URHE_values, label='Potential kink vs pH', color='b', marker='o', linestyle='-', markersize=8)

# Add linear regression line and equation for URHE
plt.plot(pH_values, slope_urhe * pH_values + intercept_urhe, 'r--', label=f'Linear fit: y = {slope_urhe:.4f}x + {intercept_urhe:.4f}')
plt.title('with field', fontname='Times New Roman', fontsize=20)
plt.xlabel('pH', fontname='Times New Roman', fontsize=18)
plt.ylabel(r'Potential kink vs. RHE / V', fontname='Times New Roman', fontsize=18)  # Change eV to V
plt.xticks(np.arange(0, 15, 1), fontsize=14)  # Set x-axis ticks from 0 to 14, separated by 1 unit
plt.yticks(fontsize=14)
plt.grid(False)
plt.gca().set_facecolor('white')
plt.legend(fontsize=14)
plt.savefig('URHE_vs_pH.png', dpi=300, bbox_inches='tight')
plt.show()

# Plot USHE vs pH
plt.figure(figsize=(8, 6))
plt.plot(pH_values, USHE_values, label='Potential kink vs pH', color='g', marker='s', linestyle='-', markersize=8)

# Add linear regression line and equation for USHE
plt.plot(pH_values, slope_ushe * pH_values + intercept_ushe, 'r--', label=f'Linear fit: y = {slope_ushe:.4f}x + {intercept_ushe:.4f}')
plt.title('with field', fontname='Times New Roman', fontsize=20)
plt.xlabel('pH', fontname='Times New Roman', fontsize=18)
plt.ylabel(r'Potential kink vs. SHE / V', fontname='Times New Roman', fontsize=18)  # Change eV to V
plt.xticks(np.arange(0, 15, 1), fontsize=14)  # Set x-axis ticks from 0 to 14, separated by 1 unit
plt.yticks(fontsize=14)
plt.grid(False)
plt.gca().set_facecolor('white')
plt.legend(fontsize=14)
plt.savefig('USHE_vs_pH.png', dpi=300, bbox_inches='tight')
plt.show()

