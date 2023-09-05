import os
import json
import boto3
import pandas as pd
from collections import defaultdict


def get_s3_client(access_key, secret_key):
    return boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )


def get_json_from_s3(client, bucket, key):
    obj = client.get_object(Bucket=bucket, Key=key)
    string_data = obj["Body"].read()
    json_data = json.loads(string_data)
    return json_data


def insert_value(table, data):
    for col, value in data.items():
        table[col].append(value)


def curate(raw_match_data):
    map = defaultdict(list)

    for match in raw_match_data:
        for player in match["players"]["all_players"]:
            column_to_value_map = {
                "match_id": match["metadata"].get("matchid", ""),
                "match_timestamp_local": match["metadata"].get(
                    "game_start_patched", ""
                ),
                "map_name": match["metadata"].get("map", ""),
                "rounds_played": match["metadata"].get("rounds_played", 0),
                "player_name": player.get("name", ""),
                "agent_name": player.get("character", ""),
                "session_playtime_minutes": player["session_playtime"].get(
                    "minutes", 0
                ),
                "score": player["stats"].get("score", 0),
                "kills": player["stats"].get("kills", 0),
                "deaths": player["stats"].get("deaths", 0),
                "assists": player["stats"].get("assists", 0),
                "headshots": player["stats"].get("headshots", 0),
                "bodyshots": player["stats"].get("bodyshots", 0),
                "legshots": player["stats"].get("legshots", 0),
                "dmg_made": player.get("damage_made", 0),
                "dmg_received": player.get("damage_received", 0),
            }

            for col, value in column_to_value_map.items():
                insert_value(map, {col: value})
    return map


def main():
    AWS_ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")

    s3_client = get_s3_client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    raw_data = get_json_from_s3(
        s3_client, "valorant-data-raw", "competitive-match-data-2023-09-03.json"
    )
    curated_data = curate(raw_data)
    df = pd.DataFrame(curated_data)
    print(df)


if __name__ == "__main__":
    main()
