import os
import logging
import requests
from google.cloud import storage
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def upload_file_to_bucket(source_file_path, bucket_name, destination_blob_name):
    """Uploads a file to the given Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    logger.info(f"File {source_file_path} uploaded to {bucket_name}/{destination_blob_name}.")

def call_webhook(webhook_url, payload):
    """Calls a webhook with the provided payload."""
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        logger.info(f"Webhook called successfully: {response.status_code}")
    except Exception as e:
        logger.error(f"Error calling webhook: {str(e)}")
