import subprocess

# Settings
max_frame = 2000 #number of total frames
step = 50
frame_to_ns = lambda x: f"{x * 0.002:.1f}ns_rep2"  # e.g., 1000 frames = 2ns, assuming 1 frame = 2 ps

ph_values = [3, 4, 5, 6, 7]
base_filename = "ph{}-rep1.lamb-0-{}.sx"
script = "cptpKa-png-colour.pl"

# Loop over frame ranges
for end_frame in range(step, max_frame + 1, step):
    # Label like "2ns", "4ns", etc.
    label = frame_to_ns(end_frame)
    
    # Build the list of files for all pH values
    files = [base_filename.format(ph, end_frame) for ph in ph_values]
    
    # Final command
    cmd = ["perl", script, label] + files
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd)
