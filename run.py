import subprocess

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.communicate()
    if process.returncode != 0:
        print(f"Error running command: {command}")

# Step 1: Collect AppIDs
print("")
print("Running Scripts...")
print("")
run_command("python scripts/collect_appids.py")

# Step 2: Fetch Game Data
print("")
run_command("python scripts/fetch_game_data.py")

# Step 3: Run Analysis Notebook
print("")
print("Starting Jupyter Notebook...")
run_command("jupyter notebook")

