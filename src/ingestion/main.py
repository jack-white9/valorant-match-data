import os
import json
import boto3
import requests
from dotenv import load_dotenv
from datetime import datetime


class Ingestion:
    def __init__(self, access_key, secret_key):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def get_match_data(self, affinity, puuid):
        MATCH_DATA_ENDPOINT = f"https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/{affinity}/{puuid}?mode=competitive&size=100"
        response = requests.get(MATCH_DATA_ENDPOINT)
        # ignore response headers, return data only
        json_data = json.loads(response.text)["data"]
        # encode as UTF-8 bytes for S3 upload
        data_dump = bytes(json.dumps(json_data).encode("UTF-8"))
        return data_dump

    def upload_to_s3(self, bucket, key, file):
        self.client.put_object(Body=file, Bucket=bucket, Key=key)


def main():
    load_dotenv()
    AWS_ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
    ingestion = Ingestion(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    region = os.getenv("REGION")
    puuid = os.getenv("PUUID")
    data = ingestion.get_match_data(region, puuid)

    date_string = datetime.today().strftime("%Y-%m-%d")
    bucket_name = "valorant-data-raw"
    file_name = f"competitive-match-data-{date_string}.json"
    ingestion.upload_to_s3(bucket_name, file_name, data)


def lambda_handler(event, context):
    main()


if __name__ == "__main__":
    main()
