import subprocess
import time

def run_command(command):
    process = subprocess.Popen(command, shell=True)
    process.communicate()
    if process.returncode != 0:
        print(f"Error running command: {command}")
        
print("""
      \033[94m
  ______ _____  ____    ________   _______  ______ _____  _____ __  __ ______ _   _ _______ _____  
 |  ____/ ____|/ __ \  |  ____\ \ / /  __ \|  ____|  __ \|_   _|  \/  |  ____| \ | |__   __/ ____| 
 | |__ | |  __| |  | | | |__   \ V /| |__) | |__  | |__) | | | | \  / | |__  |  \| |  | | | (___   
 |  __|| | |_ | |  | | |  __|   > < |  ___/|  __| |  _  /  | | | |\/| |  __| | . ` |  | |  \___ \  
 | |___| |__| | |__| | | |____ / . \| |    | |____| | \ \ _| |_| |  | | |____| |\  |  | |  ____) | 
 |______\_____|\____/  |______/_/ \_\_|    |______|_|  \_\_____|_|  |_|______|_| \_|  |_| |_____/  
 \033[0m
""")
time.sleep(1)

# Step 1: Collect AppIDs
print("")
print("\033[1m\033[94mRunning Scripts...\033[0m")
print("")
time.sleep(1)
run_command("python scripts/collect_appids.py")

# Step 2: Fetch Game Data
print("")
run_command("python scripts/fetch_game_data.py")

# Step 3: Run Analysis Notebook
print("")
print("Starting Jupyter Notebook...")
run_command("jupyter notebook")

