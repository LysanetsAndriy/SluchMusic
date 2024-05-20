# s3_helper.py
import boto3
from flask import current_app


def download_file_from_s3(key, bucket_name):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=current_app.config['S3_KEY'],
        aws_secret_access_key=current_app.config['S3_SECRET']
    )

    try:
        # Create a file path to save the downloaded file
        download_path = f"/tmp/{key}"

        # Download the file from S3
        s3.download_file(bucket_name, key, download_path)

        return download_path
    except Exception as e:
        print(f"Error downloading file: {e}")
        return None
