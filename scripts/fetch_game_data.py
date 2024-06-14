import requests
import pandas as pd

def get_steamspy_data(appid):
    response = requests.get(f'http://steamspy.com/api.php?request=appdetails&appid={appid}')
    return response.json()

appids_df = pd.read_csv('../data/indie_horror_appids.csv')
appids = appids_df['appid'].tolist()

data = []
for appid in appids:
    game_data = get_steamspy_data(appid)
    data.append(game_data)

games_df = pd.DataFrame(data)
games_df.to_csv('../data/indie_horror_games_data.csv', index=False)

print("Data collection complete.")
