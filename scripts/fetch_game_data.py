import os
import time
import requests
import pandas as pd
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class TqdmColored(tqdm):
    def __init__(self, *args, **kwargs):
        kwargs['bar_format'] = '\033[96m{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]\033[0m'
        super().__init__(*args, **kwargs)

def get_steamspy_data(appid, retries=3, backoff_factor=0.3):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=(500, 502, 504),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    try:
        response = session.get(f'http://steamspy.com/api.php?request=appdetails&appid={appid}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for appid {appid}: {e}")
        return None

# Load appIDs from the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
appids_df = pd.read_csv(os.path.join(data_dir, 'indie_horror_appids.csv'))
appids = appids_df['appid'].tolist()

data = []
for appid in TqdmColored(appids, desc="Analyzing game data", unit="appid"):
    game_data = get_steamspy_data(appid)
    if game_data:
        data.append(game_data)
    #time.sleep(1)  # Add a delay between requests to avoid overwhelming the server

# Convert to DataFrame
games_df = pd.DataFrame(data)
games_df.to_csv(os.path.join(data_dir, 'indie_horror_games_data.csv'), index=False)
time.sleep(1)
print("\033[1m\033[92mData collection complete.\033[0m")
