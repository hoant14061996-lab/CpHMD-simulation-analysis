import os
import numpy as np

# File and residue setup
#time_points = range(1, 40, 0.1)  # 2ns to 20ns
time_points = np.arange(0.1, 40.01, 0.1)
residues = [6, 10, 11, 15, 16, 26]
output_file = "pka_summary_rep1.dat"

# Collect data
data = []

for t in time_points:
    filename = f"{t:.1f}ns_rep2.pka"
    pka_values = {resid: None for resid in residues}
    
    if not os.path.exists(filename):
        print(f"Warning: {filename} not found.")
        continue
    
    with open(filename) as f:
        for line in f:
            if line.strip():
                parts = line.split()
                resid = int(parts[0])
                pka = float(parts[1])
                if resid in pka_values:
                    pka_values[resid] = pka
                    
    row = [t] + [pka_values[resid] for resid in residues]
    data.append(row)

# Write summary table
with open(output_file, "w") as f:
    header = ["Time"] + [f"res{r}" for r in residues]
    f.write("\t".join(header) + "\n")
    for row in data:
        f.write(f"{row[0]:.1f}\t" + "\t".join(f"{val:.2f}" if isinstance(val, float) else str(val) for val in row[1:]) + "\n")

print(f"Summary saved to {output_file}")
