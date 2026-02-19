import pandas as pd
import numpy as np

# Assuming df is your DataFrame
df = pd.read_csv("ph3-asp6.dat")

# Resetting index to start from 0
df.reset_index(drop=True, inplace=True)

# Renumbering index
new_index = np.arange(1, len(df) + 1)
df.index = new_index

# Saving the DataFrame to a new CSV file without commas and index label
df.to_csv("ph3-asp6-new.dat", sep="\t")

print("DataFrame saved successfully without commas.")
