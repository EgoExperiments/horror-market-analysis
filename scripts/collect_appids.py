import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import time

class TqdmColored(tqdm):
    def __init__(self, *args, **kwargs):
        kwargs['bar_format'] = '\033[96m{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]\033[0m'
        super().__init__(*args, **kwargs)

def get_steam_appids(query, pages=50):
    appids = []
    for page in TqdmColored(range(1, pages + 1), desc="Fetching game IDs", unit="page"):
        url = f"https://store.steampowered.com/search/?term={query}&page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        search_results = soup.find_all('a', class_='search_result_row')
        for result in search_results:
            appid = result.get('data-ds-appid')
            if appid:
                appids.append(appid)
    return appids

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
os.makedirs(data_dir, exist_ok=True)

appids = get_steam_appids('indie horror', pages=50)  # Adjust pages as needed
appids_df = pd.DataFrame(appids, columns=['appid'])
appids_df.to_csv(os.path.join(data_dir, 'indie_horror_appids.csv'), index=False)
time.sleep(1)
print(f"\033[1m\033[92mCollected {len(appids)} gameids.\033[0m")

