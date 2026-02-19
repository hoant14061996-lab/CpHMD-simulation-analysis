import numpy as np
import matplotlib.pyplot as plt

# pH values (more finely spaced for smooth curves)
pH = np.linspace(0, 10, 500)  # 500 points between 0 and 14 for a smoother curve

# Residue parameters
residues = {
    "Asp6": {"a0": 0.844666, "a1": 4.39712},
    "Glu10": {"a0": 0.810162, "a1": 3.55517},
    "Asp11": {"a0": 0.840295, "a1": 5.19174},
    "Glu15": {"a0": 0.739642, "a1": 3.66922},
    "Asp16": {"a0": 1.00747, "a1": 3.01645},
    "Hsp26": {"a0": 0.849469, "a1": 6.35699},
}

marker_color = 'red'  # Choose a color for the markers

# Plot
plt.figure(figsize=(5, 5))

for residue, params in residues.items():
    a0, a1 = params["a0"], params["a1"]
    S = 1 / (1 + 10**(a0 * (a1 - pH)))  # Calculate S
    line, = plt.plot(pH, S, label=f"{residue}")

# Annotate only pH values between 3 and 7
annotate_pH = np.array([3, 4, 5, 6, 7])  # Specific pH values to annotate
for residue, params in residues.items():
    a0, a1 = params["a0"], params["a1"]
    S_annotate = 1 / (1 + 10**(a0 * (a1 - annotate_pH)))  # Calculate S for annotate_pH
    for pH_value, S_value in zip(annotate_pH, S_annotate):
        #plt.annotate(f"({pH_value}, {S_value:.2f})", xy=(pH_value, S_value), 
        #             textcoords="offset points", xytext=(5, -10), fontsize=8)
        #plt.scatter(annotate_pH, S_annotate, marker="o", color=plt.gca().lines[-1].get_color())  # Use same color as the curve
        plt.scatter(annotate_pH, S_annotate, marker="o", color=marker_color, zorder=5)  # Use different color for markers


# Add horizontal line at S = 0.5
plt.axhline(y=0.5, color='black', linestyle='--', linewidth=1.5, label="S=0.5")

# Customize the plot
plt.xlabel("pH", fontsize=20)
plt.ylabel("S", fontsize=20)
plt.title("Titration curves of residues", fontsize=14)

# Position the legend at the bottom-right corner
plt.legend(title="Residues", fontsize=10, loc='lower right')
plt.grid(True)

 #Set x-ticks and y-ticks color to blue
#plt.tick_params(axis='x', fontsize=14)  # X-axis tick labels in blue
#plt.tick_params(axis='y', fontsize=14)  # Y-axis tick labels in blue

plt.xticks(fontsize=18)
plt.yticks(fontsize=18)

plt.tight_layout()
plt.savefig("titration-curve-rep1.png", dpi=400)

# Show the plot
plt.show()
