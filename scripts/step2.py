import os
import glob
from collections import defaultdict

# Dictionary to hold data: key = row number (No.), value = list of tuples (time, No., resid, unprot)
row_data = defaultdict(list)

# Process each .sx file in order of time (extracted from filename)
for filename in sorted(glob.glob("ph7-rep1.lamb-0-*.sx"), key=lambda x: int(x.split("-")[-1].split(".")[0])):
    # Extract lambda value and convert to time in ns
    lamb_value = int(filename.split("-")[-1].split(".")[0])
    time_ns = lamb_value * 0.002  # because 50 → 0.1 ns ⇒ 1 unit = 0.002 ns

    with open(filename, "r") as f:
        for line in f:
            if line.strip().startswith("#") or not line.strip():
                continue
            parts = line.split()
            no = int(parts[0])         # Row number
            resid = parts[1]           # Residue ID (ires)
            unprot = parts[3]          # Unprot value
            row_data[no].append((time_ns, no, resid, unprot))

# Write each row's time series into its own file
for no, entries in row_data.items():
    with open(f"ph7-rep1-row-{no}.dat", "w") as out:
        out.write("Time\tNo.\tresid\tunprot\n")
        for time_ns, no, resid, unprot in entries:
            out.write(f"{time_ns:.3f}\t{no}\t{resid}\t{unprot}\n")

print("✅ Done: Each row saved to 'row_X.dat' (X = row number)")
