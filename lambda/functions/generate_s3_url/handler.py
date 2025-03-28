import json
import boto3
import uuid
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3_client = boto3.client('s3')
BUCKET_NAME = "mahjong-develop"

def lambda_handler(event, context):
    logger.info("Lambda function invoked with event: %s", event)
    # Create a unique object key
    object_key = f"uploads/{uuid.uuid4()}.jpg"
    
    # Generate a pre-signed URL valid for 300 seconds (5 minutes)
    try:
        presigned_url = s3_client.generate_presigned_url(
            'put_object',
            Params={
                'Bucket': BUCKET_NAME,
                'Key': object_key,
                'ContentType': 'image/jpeg'
            },
            ExpiresIn=300
        )
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
    
    # Return the URL and the object key in JSON format
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"  # Enable CORS if needed
        },
        "body": json.dumps({"url": presigned_url, "file_key": object_key})
    }

