import os
import boto3
import requests
from dotenv import load_dotenv


class Ingestion:
    def __init__(self, access_key, secret_key):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def get_match_data(self, affinity, puuid):
        res = requests.get(
            f"https://api.henrikdev.xyz/valorant/v3/by-puuid/matches/{affinity}/{puuid}"
        )
        print(res.status_code)
        return res.text

    def upload_to_s3(self, bucket, key, file):
        self.client.put_object(Body=file, Bucket=bucket, Key=key)


def main():
    load_dotenv()
    AWS_ACCESS_KEY_ID = os.getenv("ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
    ingestion = Ingestion(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)

    region = "ap"
    puuid = "2ecce5c6-6d31-579c-bf56-bf6743e19270"
    data = ingestion.get_match_data(region, puuid)

    bucket_name = "valorant-data-raw"
    file_name = "valorant_data.json"
    ingestion.upload_to_s3(bucket_name, file_name, data)


def lambda_handler(event, context):
    main()


if __name__ == "__main__":
    main()
