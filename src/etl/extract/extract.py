import os
import json
import boto3
import requests
from dotenv import load_dotenv


def get_s3_client(access_key, secret_key):
    client = boto3.client(
        "s3",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
    )
    return client


def get_match_data(affinity, puuid):
    MATCH_DATA_ENDPOINT = f"https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/{affinity}/{puuid}?mode=competitive&size=100"
    response = requests.get(MATCH_DATA_ENDPOINT)
    # ignore response headers, return data only
    json_data = json.loads(response.text)["data"]
    # encode as UTF-8 bytes for S3 upload
    data_dump = bytes(json.dumps(json_data).encode("UTF-8"))
    return data_dump


def upload_to_s3(s3_client, bucket, key, file):
    s3_client.put_object(Body=file, Bucket=bucket, Key=key)


def main(event, context):
    load_dotenv()
    AWS_ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
    s3_client = get_s3_client(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    region = os.getenv("REGION")
    puuid = os.getenv("PUUID")
    data = get_match_data(region, puuid)

    bucket_name = "valorant-data-raw"
    file_name = f"competitive-match-data.json"
    upload_to_s3(s3_client, bucket_name, file_name, data)


if __name__ == "__main__":
    main(None, None)
