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
            # Attempt JavaScript click if normal click fails
            self.driver.execute_script("arguments[0].click();", code_input)
            logger.info("Used JavaScript to click code input")
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
        logger.info("Sending chat message")
        self.sendChatMessage("Hello, good day everyone!")
        
        # Turn on captions
        time.sleep(2)
        for i in range(6): 
            self.actions.send_keys(Keys.TAB).perform()
            time.sleep(0.6)
        self.actions.send_keys(Keys.ENTER).perform()
        logger.info("Turned on captions")

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

def main():
    logger.info("Starting main execution")
    temp_dir = tempfile.mkdtemp()
    audio_path = os.path.join(temp_dir, "output.wav")
    # Get configuration from environment variables
    duration = int(os.getenv('RECORDING_DURATION', 60))
    
    obj = JoinGoogleMeet()
    obj.Glogin()
    obj.joinMeeting()
    # Record audio after joining
    AudioRecorder().get_audio(audio_path, duration)
    logger.info("Recording completed")

# call the main function
if __name__ == "__main__":
    main()
