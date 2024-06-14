import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_steam_appids(query, pages=5):
    appids = []
    for page in range(1, pages + 1):
        url = f"https://store.steampowered.com/search/?term={query}&page={page}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        search_results = soup.find_all('a', class_='search_result_row')
        for result in search_results:
            appid = result['data-ds-appid']
            appids.append(appid)
    return appids

appids = get_steam_appids('indie horror', pages=10)
appids_df = pd.DataFrame(appids, columns=['appid'])
appids_df.to_csv('../data/indie_horror_appids.csv', index=False)

print(f"Collected {len(appids)} appids.")
