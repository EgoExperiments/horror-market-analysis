import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_steam_appids(query, pages=20):
    appids = []
    for page in range(1, pages + 1):
        url = f"https://store.steampowered.com/search/?term={query}&page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        search_results = soup.find_all('a', class_='search_result_row')
        for result in search_results:
            appid = result.get('data-ds-appid')
            if appid:
                appids.append(appid)
    return appids

# Ensure the data directory exists relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
os.makedirs(data_dir, exist_ok=True)

# Get appids for indie horror games
appids = get_steam_appids('indie horror', pages=10)  # Adjust pages as needed
appids_df = pd.DataFrame(appids, columns=['appid'])
appids_df.to_csv(os.path.join(data_dir, 'indie_horror_appids.csv'), index=False)

print(f"Collected {len(appids)} appids.")
