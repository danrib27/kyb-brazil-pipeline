from pathlib import Path

import boto3
import requests
from botocore.exceptions import ClientError, NoCredentialsError


def download_file(
    url: str,
    output_path: Path,
    chunk_size: int,
    timeout: float = 30,
) -> None:
    """Download a file from a URL and save it to a local path.

    Args:
        url: The URL of the file to download.
        output_path: The local path where the file will be saved.
        chunk_size: The number of bytes written to disk at a time.
        timeout: Seconds to wait for the server before giving up.
    """
    response = requests.get(url, stream=True, timeout=timeout)
    response.raise_for_status()

    with output_path.open("wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            f.write(chunk)

def upload_2_s3(file_path: Path, bucket_name: str, object_name: str) -> None:
    """Upload a file to an S3 bucket.

    Args:
        file_path: The local path of the file to upload.
        bucket_name: The name of the S3 bucket.
        object_name: The name of the object in the S3 bucket.
    """
    s3_client = boto3.client(
        service_name='s3',
        region_name='us-east-1',
        aws_access_key_id='your_access_key_id',
        aws_secret_access_key='your_secret_access_key'
    )
    try:
        s3_client.upload_file(str(file_path), bucket_name, object_name)
    except (NoCredentialsError, ClientError) as e:
        print(f"Error uploading file to S3: {e}")
