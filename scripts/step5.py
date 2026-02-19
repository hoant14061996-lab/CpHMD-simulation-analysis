import pandas as pd
import matplotlib.pyplot as plt

# Load your data
df = pd.read_csv("pka_summary_rep1.dat", sep="\t")

# Get time values
time = df["#Time"]

# Compute mean pKa per residue
mean_pka = df.drop(columns=["#Time"]).mean()

# Calculate delta pKa (deviation from mean)
delta_pka = df.drop(columns=["#Time"]) - mean_pka

# Plot
plt.figure(figsize=(10, 5))

for col in df.columns[1:]:
    pka = df[col]
    delta = delta_pka[col]
    plt.plot(time, pka, label=f"{col} pKa", linewidth=3)
    plt.plot(time, pka - delta, linestyle="--", label=f"{col} Mean", linewidth=2)  # This equals mean_pka[col]

plt.ylim(0, 10)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.xlabel("Time (ns)", fontsize=14)
plt.ylabel("pKa", fontsize=14)
plt.title("pKa (Simulation) and Mean", fontsize=14)
plt.legend(ncol=2, fontsize='small')
plt.grid(True)
print(mean_pka)
plt.tight_layout()
plt.savefig("pka_vs_mean_rep1.png", dpi=400)
plt.show()
