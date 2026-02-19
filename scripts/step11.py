#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import glob

# Match all the relevant files
data_files = sorted(glob.glob("ph*-rep1-row-12.dat"))

# Start the figure before the loop
plt.figure(figsize=(6, 5))

for file_path in data_files:
    # Load data
    data = np.loadtxt(file_path, skiprows=1)

    # Extract columns
    time_steps = data[:, 0]  # Time
    values = data[:, 3]      # Unprot

    # Generate label from file name
    name_parts = file_path.replace(".dat", "").split("-")
    pH = "pH" + name_parts[0][2:]  # Extract pH info (e.g., "ph3" → "pH3")

    # Plot
    plt.plot(time_steps, values, marker=".", linestyle='-', label=f"{pH}")

# Final plot settings
plt.ylim(0, 1.5)
plt.xlabel("Time (ns)", fontsize=20)
plt.ylabel("Deprotonated fraction (S)", fontsize=20)
plt.xticks(fontsize=22)
plt.yticks(fontsize=22)
plt.title("Asp16", fontsize=20)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("Asp6_rep1_pHs.png", dpi=450)
plt.close()
