import numpy as np
import matplotlib.pyplot as plt

# Define file path
file_path = "ph3-asp6-charge.dat"

# Load data
data = np.loadtxt(file_path)

# Extract columns
time_steps = data[:, 0]  # Column 1
values = data[:, 1]      # Column 3

# Scale time to 40 ns
time_ns = (time_steps / max(time_steps))*40

# Plot the data as points
plt.figure(figsize=(5, 4))
plt.scatter(time_ns, values, marker=".", color="b")
plt.xlabel("Time (ns)")

plt.ylabel("λ-Values")
#plt.ylabel("χ-Values", fontsize=14)

plt.title("Asp6 (pH3)")
plt.legend()
plt.grid(True)
plt.savefig("ph3-asp6-charge.png", dpi=450)
plt.show()
