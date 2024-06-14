import requests
import pandas as pd
import os

def get_steamspy_data(appid):
    response = requests.get(f'http://steamspy.com/api.php?request=appdetails&appid={appid}')
    return response.json()

# Load appIDs from the CSV file
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'data')
appids_df = pd.read_csv(os.path.join(data_dir, 'indie_horror_appids.csv'))
appids = appids_df['appid'].tolist()

data = []
for appid in appids:
    game_data = get_steamspy_data(appid)
    data.append(game_data)

# Convert to DataFrame
games_df = pd.DataFrame(data)
games_df.to_csv(os.path.join(data_dir, 'indie_horror_games_data.csv'), index=False)

print("Data collection complete.")
