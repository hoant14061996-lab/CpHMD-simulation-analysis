import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Data from the table
residues = ["D6", "E10", "D11", "E15", "D16", "H26"]
model_pka = [4.0, 4.4, 4.0, 4.4, 4.0, 7.0]

# Calculate the average pKa from the three replicates
#sim_pka = [4.51295,  3.59425, 5.30160, 3.52840, 2.93605, 6.27400] #rep1 
#sim_pka = [4.488133, 3.529300, 5.337833, 3.707567, 2.424033, 6.412800] #rep2
sim_pka = [4.488133, 3.695875, 5.070000, 3.710800, 3.182650, 6.351550] #rep3

# Calculate ΔpKa
delta_pka = sim_pka - np.array(model_pka)

# Linear regression for pKa (Simulation) vs pKa (Model)
slope_sim, intercept_sim, r_value_sim, _, _ = linregress(model_pka, sim_pka)

# Plotting
fig, axs = plt.subplots(1, 2, figsize=(10, 3))

# Subplot A: pKa (Simulation) vs pKa (Model)
axs[0].scatter(model_pka, sim_pka, color='blue')
#axs[0].plot(model_pka, intercept_sim + slope_sim * np.array(model_pka), 'r',
            #label=f'Fit: y={slope_sim:.2f}x+{intercept_sim:.2f}, $R^2$={r_value_sim**2:.2f}')
axs[0].set_xlabel("Model pKa")
axs[0].set_ylabel("Simulation pKa")
axs[0].legend()
axs[0].grid(True)
axs[0].set_title("pKa (Simulation) vs Model")

# Subplot B: ΔpKa vs Model pKa
#axs[1].scatter(model_pka, delta_pka, color='red')
#axs[1].axhline(0, color='gray', linestyle='--')
#axs[1].set_xlabel("Model pKa")
#axs[1].set_ylabel("ΔpKa (Simulation - Model)")
#axs[1].grid(True)
#axs[1].set_title("B. ΔpKa vs Model")

#plt.tight_layout()
# Save the plot as EPS
#plt.savefig("pka_analysis.eps", format='eps')

#plt.show()

# Subplot C: Bar plot of ΔpKa per residue
axs[1].bar(residues, delta_pka, color='green')
axs[1].axhline(0, color='gray', linestyle='--')
axs[1].set_xlabel("Titratable Residues")
axs[1].set_ylabel("ΔpKa (Simulation - Model)")
axs[1].set_title(" ΔpKa per Residue")
axs[1].tick_params(axis='x', rotation=0)
axs[1].grid(True)

plt.tight_layout()
plt.savefig("pka-shift-rep1.png", dpi=400)
plt.show()

plt.print(delta_pka)

