import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from flask import current_app


def upload_file_to_s3(file_path, file_name, file_content_type, bucket_name):
    s3 = boto3.client(
        service_name="s3",
        aws_access_key_id=current_app.config['S3_KEY'],
        aws_secret_access_key=current_app.config['S3_SECRET']
    )

    try:
        s3.upload_file(
            file_path,
            bucket_name,
            file_name,
            ExtraArgs={
                "ContentType": file_content_type
            }
        )
    except (NoCredentialsError, PartialCredentialsError) as e:
        return {"error": str(e)}

    return f"{current_app.config['S3_LOCATION']}{file_name}"
