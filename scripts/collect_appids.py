import os
import time
import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

class TqdmColored(tqdm):
    def __init__(self, *args, **kwargs):
        kwargs['bar_format'] = '\033[96m{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]\033[0m'
        super().__init__(*args, **kwargs)

def get_steam_appids_by_tags(tag_ids, pages=1000):
    appids = []
    for page in TqdmColored(range(1, pages + 1), desc="Fetching game IDs", unit="page"):
        url = f"https://store.steampowered.com/search/?term=&tags={','.join(map(str, tag_ids))}&page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        search_results = soup.find_all('a', class_='search_result_row')
        for result in search_results:
            appid = result.get('data-ds-appid')
            if appid:
                appids.append(appid)
    return appids

def get_game_tags(appid):
    url = f"https://store.steampowered.com/app/{appid}/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tags = soup.find_all('a', class_='app_tag')
    tag_names = [tag.get_text(strip=True).lower() for tag in tags]
    return tag_names

# Known tag IDs for 'indie', 'horror', and 'psychological horror'
required_tag_ids = [492, 21, 21978]
required_tags = ['indie', 'horror', 'psychological horror']

script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
os.makedirs(data_dir, exist_ok=True)

appids = get_steam_appids_by_tags(required_tag_ids, pages=1000)

valid_appids = []
for appid in TqdmColored(appids, desc="Validating game tags", unit="appid"):
    tag_names = get_game_tags(appid)
    if all(tag in tag_names for tag in required_tags):
        valid_appids.append(appid)

appids_df = pd.DataFrame(valid_appids, columns=['appid'])
appids_df.to_csv(os.path.join(data_dir, 'indie_horror_appids.csv'), index=False)
#time.sleep(1)
print(f"\033[1m\033[92mCollected {len(valid_appids)} game IDs.\033[0m")
