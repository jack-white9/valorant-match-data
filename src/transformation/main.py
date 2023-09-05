import json
import pandas as pd
from collections import defaultdict


def read(file):
    with open(file, 'r') as f:
        raw_match_data = json.load(f)
    return raw_match_data


def insert_value(table, data):
    for col, value in data.items():
        table[col].append(value)


def curate(raw_match_data):
    map = defaultdict(list)

    for match in raw_match_data:
        for player in match['players']['all_players']:
            column_to_value_map = {
                'match_id': match['metadata']['matchid'],
                'match_timestamp_local': match['metadata']['game_start_patched'],
                'map_name': match['metadata']['map'],
                'rounds_played': match['metadata']['rounds_played'],
                'player_name': player['name'],
                'agent_name': player['character'],
                'session_playtime': player['session_playtime'].get('minutes', ''),
                'score': player['stats']['score'],
                'kills': player['stats']['kills'],
                'deaths': player['stats']['deaths'],
                'assists': player['stats']['assists'],
                'headshots': player['stats']['headshots'],
                'bodyshots': player['stats']['bodyshots'],
                'legshots': player['stats']['legshots'],
                'dmg_made': player['damage_made'],
                'dmg_received': player['damage_received']
            }

            for col, value in column_to_value_map.items():
                insert_value(map, {col: value})
    return map


def main():
    raw_data = read('competitive-match-data-2023-09-03.json') # TODO - replace with s3 object
    curated_data = curate(raw_data)
    df = pd.DataFrame(curated_data)
    print(df)


if __name__ == '__main__':
    main()
