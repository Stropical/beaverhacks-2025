import os
import logging
from google.cloud import storage
from google.oauth2 import service_account
from dotenv import load_dotenv
from google.cloud import speech_v1 as speech
import requests
import json

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Specify the path to the service account key file
key_path = "./google_key.json"

# Create credentials object
credentials = service_account.Credentials.from_service_account_file(key_path)

def upload_file_to_bucket(source_file_path, bucket_name, destination_blob_name):
    """Uploads a file to the given Google Cloud Storage bucket."""
    storage_client = storage.Client(credentials=credentials, project="lunar-reef-455922-n4")
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_path)
    logger.info(f"File {source_file_path} uploaded to {bucket_name}/{destination_blob_name}.")
    
    # Return the GCS URI for the uploaded file
    gcs_uri = f"gs://{bucket_name}/{destination_blob_name}"
    return gcs_uri

def transcribe_audio(gcs_uri, language_code="en-US"):
    """Transcribes an audio file stored in Google Cloud Storage using Speech-to-Text API."""
    
    # Create Speech-to-Text client
    speech_client = speech.SpeechClient(credentials=credentials)
    
    # Configure the request with multi-channel support
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Specify your audio encoding
        sample_rate_hertz=44100,  # Set to your audio’s sample rate
        language_code=language_code,
        enable_automatic_punctuation=True,
        audio_channel_count=2,
        enable_separate_recognition_per_channel=True,
        use_enhanced=True,  # Use enhanced models for better accuracy
        model="video",  # Choose a model appropriate for your content
        speech_contexts=[speech.SpeechContext(phrases=["Jira", "domain-specific", "terms"])]
    )
    
    # Perform the transcription
    logger.info(f"Starting transcription for {gcs_uri}")
    operation = speech_client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=300)
    
    # Process the response (combine transcripts from all channels)
    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    
    logger.info("Transcription completed successfully")
    
    # Send transcript to webhook
    try:
        webhook_url = "https://velazquc.app.n8n.cloud/webhook-test/e09f1d0a-af70-4493-b8b5-92f3dc22ee5b"
        if webhook_url:
            # Prepare payload
            payload = {
                "transcript": transcript,
                "audio_uri": gcs_uri,
                "language_code": language_code
            }
            
            print(webhook_url)
            
            # Send POST request to webhook
            response = requests.post(webhook_url, json=payload)
            
            # Check if request was successful
            if response.status_code >= 200 and response.status_code < 300:
                logger.info(f"Transcript successfully sent to webhook. Status code: {response.status_code}")
                logger.info(f"Response content: {response.content}")
            else:
                logger.error(f"Failed to send transcript to webhook. Status code: {response.status_code}")
                logger.info(f"Response content: {response.content}")
        else:
            logger.warning("WEBHOOK_URL not configured. Skipping webhook notification.")
    except Exception as e:
        logger.error(f"Error sending transcript to webhook: {str(e)}")
    
    return transcript


if __name__ == "__main__":
    # Define the GCS URI
    gcs_uri = "gs://n8n_meeting_recordings/meeting_2025-04-05_16-36-49.wav"
    
    # Transcribe the audio file
    transcription = transcribe_audio(gcs_uri)
    print("Transcription:", transcription)

