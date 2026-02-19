import subprocess

# Configuration
total_frames = 2000 # N is total number of frames
step_size = 50  # Now we go 0–1000, 0–2000, 0–3000, etc.
input_file = "ph7-rep1.lamb"  # Adjust to match your file name
script = "CptSX.pl"
pH_value = 7  

# Loop over clean frame endpoints
for end in range(step_size, total_frames + 1, step_size):
    start = 0
    cmd = ["perl", script, input_file, str(start), str(end), str(pH_value)]
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)
