# import required modules
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
from record_audio import AudioRecorder
import os
import tempfile
from dotenv import load_dotenv
import logging
from upload_and_webhook import upload_file_to_bucket, call_webhook
import sys 
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

class JoinGoogleMeet:
    def __init__(self):
        self.mail_address = os.getenv('EMAIL_ID')
        self.password = os.getenv('EMAIL_PASSWORD')
        self.join_name = os.getenv('JOIN_NAME', 'Bot')
        self.meet_code = os.getenv('MEET_CODE', '')
        # create chrome instance with notifications blocked
        opt = Options()
        opt.add_argument('--disable-blink-features=AutomationControlled')
        opt.add_argument('--start-maximized')
        opt.add_argument('--disable-notifications')
        opt.add_argument('--mute-audio')
        opt.add_argument('--enable-automation')
        opt.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 2
        })
        self.driver = webdriver.Chrome(options=opt)
        self.actions = ActionChains(self.driver)

    def Glogin(self):
        logger.info("Starting Gmail login activity")
        # Login Page
        self.driver.get('https://accounts.google.com/')
        
        # input Gmail
        email_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="email"]'))
        )
        email_input.click()
        email_input.send_keys(self.mail_address)
        time.sleep(2)
        
        next_button = self.driver.find_element(By.ID, "identifierNext")
        next_button.click()
        
        # input Password
        time.sleep(3.5)
        # Using direct keyboard input for password
        password_input = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"]'))
        )
        password_input.send_keys(self.password)
        time.sleep(0.8)
        password_input.send_keys(Keys.ENTER)
        
        logger.info("Gmail login activity: Done")
        time.sleep(2.5)

    def joinMeeting(self):
        logger.info("Navigating to Google Meet and waiting for meeting code input")
        # Go to Google Meet
        self.driver.get('https://meet.google.com/')
        
        # Wait for the code input field to be clickable
        code_input = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[type="text"]'))
        )
        try:
            code_input.click()
        except Exception as e:
            # Dispatch a MouseEvent click to avoid scrolling
            self.driver.execute_script("""
                var evt = new MouseEvent('click', {
                    bubbles: true,
                    cancelable: true,
                    view: window
                });
                arguments[0].dispatchEvent(evt);
            """, code_input)
            logger.info("Used JavaScript MouseEvent to click code input without scrolling")
        time.sleep(1)
        code_input.clear()
        time.sleep(1)
        # Send meeting code character by character
        for char in self.meet_code:
            code_input.send_keys(char)
            time.sleep(0.1)
        logger.info(f"Entered meeting code: {self.meet_code}")
        time.sleep(0.8)
        code_input.send_keys(Keys.ENTER)
        
        # Wait for page to load
        time.sleep(8)
        
        # Try to find the join button directly using various selectors
        join_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Ask to join')]/ancestor::button | //span[contains(text(), 'Join now')]/ancestor::button"))
        )
        join_button.click()
        logger.info("Clicked join button, waiting to be let in...")

        # Wait until meeting is joined by waiting for an element like the "Leave call" button
        WebDriverWait(self.driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(@aria-label, 'Leave call')]"))
        )
        logger.info("Joined the meeting")
        time.sleep(3)

    def sendChatMessage(self, message):
        # Open chat with keyboard
        for i in range(2):
            self.actions.send_keys(Keys.TAB).perform()
            time.sleep(0.6)
        self.actions.send_keys(Keys.ENTER).perform()
        time.sleep(1.5)
        
        # Type message
        self.actions.send_keys(message).perform()
        time.sleep(0.5)
        self.actions.send_keys(Keys.ENTER).perform()
        logger.info(f"Sent chat message: {message}")
        
        # Close chat
        self.actions.send_keys(Keys.TAB).perform()
        self.actions.send_keys(Keys.ENTER).perform()
        logger.info("Closed chat box")

    def monitorParticipants(self):
        logger.info("Starting participants monitoring...")
        while True:
            try:
                # Using provided CSS selector for displaying current participant count
                participants_element = self.driver.find_element(By.CSS_SELECTOR, "#yDmH0d > c-wiz > div > div > div.TKU8Od > div.crqnQb > div > div:nth-child(8) > div > div > div.jsNRx > nav > div:nth-child(2) > div > div > div")
                count_text = participants_element.text.strip()
                if count_text and count_text.isdigit():
                    count = int(count_text)
                    logger.info(f"Detected {count} participants")
                    if count <= 1:
                        logger.info("Last person in call detected.")
                        break
                else:
                    logger.info("Participant count text not found or not numeric.")
            except Exception as e:
                logger.error("Error detecting participants: " + str(e))
            time.sleep(5)

def main():
    logger.info("Starting main execution")
    temp_dir = tempfile.mkdtemp()
    
    # Generate name based on current time
    current_time = datetime.now()
    file_name = f"meeting_{current_time.strftime('%Y-%m-%d_%H-%M-%S')}.wav"
    
    audio_path = os.path.join(temp_dir, file_name)
    duration = int(os.getenv('RECORDING_DURATION', 60))
    
    obj = JoinGoogleMeet()
    obj.Glogin()
    obj.joinMeeting()
    # Start recording using AudioRecorder's start/stop methods (assumed to exist)
    recorder = AudioRecorder()
    recorder.start_recording(audio_path, duration)
    logger.info("Recording started")
    # Monitor participants until you're the last person in the call
    obj.monitorParticipants()
    recorder.stop_recording()
    logger.info("Recording stopped because you're the last person in the call")
    
    
    
    # GOOGLE CLOUD STORAGE UPLOAD
        # Fetch required configuration from environment variables
    bucket_name = os.getenv('BUCKET_NAME')
    webhook_url = os.getenv('WEBHOOK_URL')
    
    if not bucket_name or not webhook_url:
        logger.error("Bucket name or webhook URL not set in environment variables.")
        sys.exit(1)
    
    destination_blob_name = os.path.basename(audio_path)
    
    # Upload the file
    upload_file_to_bucket(audio_path, bucket_name, destination_blob_name)
    
    # Call the webhook with basic payload information
    payload = {
        "file": destination_blob_name,
        "bucket": bucket_name
    }
    call_webhook(webhook_url, payload)



# call the main function
if __name__ == "__main__":
    main()
