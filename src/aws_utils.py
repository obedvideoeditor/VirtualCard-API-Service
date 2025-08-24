import boto3
from src.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, S3_BUCKET
from datetime import datetime

s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def log_to_s3(message: str):
    timestamp = datetime.now().isoformat()
    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=f"logs/{timestamp}.txt",
        Body=message.encode()
    )
