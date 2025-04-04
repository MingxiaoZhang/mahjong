import json
import boto3
import numpy as np
from PIL import Image
import io

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    print(f"New image uploaded: {object_key} in bucket: {bucket_name}")
    
    try:
        # Retrieve the image file from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        image_data = response['Body'].read()

        # Convert the image data to a NumPy array
        image = Image.open(io.BytesIO(image_data))
        image_array = np.array(image)

        # Print the NumPy array
        print(image_array)

        return {
            'statusCode': 200,
            'body': 'Image processed successfully.'
        }

    except Exception as e:
        print(f"Error processing image from S3: {e}")
        return {
            'statusCode': 500,
            'body': f"Error processing image: {str(e)}"
        }
