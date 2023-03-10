from selenium                       import webdriver
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support     import expected_conditions as EC
from selenium.webdriver.common.by   import By

import time

from pydub import AudioSegment
import speech_recognition as sr

import numpy as np
import tempfile
import requests
import os

EXT_PATH = "D:\\ITSENSE_D\\COFACE\\webscrapping\\tools\\touchVPN.crx"

# ext_folder = "D:\\ITSENSE_D\\COFACE\\webscrapping\\tools\\touchVPN"

# CEDULA = "1026595200"
# CEDULA = "71984381"
CEDULA = "10773983"

DRIVER_PATH = "D:\\ITSENSE_D\\COFACE\\webscrapping\\tools\\chromedriver.exe"

USER_AGENT_LIST = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                    ]

EXTENSION_LINK = "chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html"
POLNAL_LINK = "https://antecedentes.policia.gov.co:7005/WebJudicial/index.xhtml"
IP_LINK = "https://www.whatismyip.com/"

PATH = "D:\\ITSENSE_D\\COFACE\\webscrapping\\tools\\"

def delay(min=2,max=5):
    time.sleep(np.random.randint(min,max))    

userAgent_id = np.random.randint(0,5)

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_extension(EXT_PATH)
# options.add_extension(f"load-extension={ext_folder}")
options.add_argument(f'user-agent={USER_AGENT_LIST[userAgent_id]}')
options.add_argument(r'--user-data-dir=C:\Users\Usuario\AppData\Local\Google\Chrome\User Data\Default')

driver = webdriver.Chrome(DRIVER_PATH, options=options)

# Start browser
driver.get(EXTENSION_LINK)

delay()
# #obtain parent window handle
# parent = driver.window_handles[0]
# #obtain browser tab window
# chld = driver.window_handles[1]
# #switch to browser tab
# driver.switch_to.window(chld)
# print("Page title for browser tab:")
# print(driver.title)
# #close browser tab window
# driver.close()
# #switch to parent window
# driver.switch_to.window(parent)
# print("Page title for parent window:")
# print(driver.title)

# delay()

# Connect to VPN
WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.ID,
                                        "ConnectionButton")))\
        .click()

delay()

# Go to POLNAL website
driver.get(POLNAL_LINK)

delay()

# Check "Accept terms and conditions" radio button
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    "input[value='true']")))\
    .click()

# Click on "Send" button
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    "button[role='button']")))\
    .click()

delay(5,8)

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                    "input[role='textbox']")))\
    .send_keys(CEDULA)

# Find captcha iframe
iframe = driver.find_element(By.TAG_NAME, "iframe") 
if iframe.get_attribute("src").startswith("https://www.google.com/recaptcha/api2/anchor"):
    captcha = iframe

ret = None
tmp_dir = tempfile.gettempdir()
mp3_file = os.path.join(tmp_dir, "_tmp.mp3")
wav_file = os.path.join(tmp_dir, "_tmp.wav")
tmp_files = [mp3_file, wav_file]

# Switch to captcha iframe
driver.switch_to.frame(iframe)

# Click on "Not a robot" checkbox
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CLASS_NAME,
                                    "recaptcha-checkbox-border")))\
    .click()

# Go back to default content
driver.switch_to.default_content()

delay()

# Select challenge iframe and switch to it
iframes = driver.find_elements(By.TAG_NAME, "iframe") 
print([iframe.get_attribute("src") for iframe in iframes])

challenge_iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title='El reCAPTCHA caduca dentro de dos minutos']") 
driver.switch_to.frame(challenge_iframe)

try:
    # Click on audio button
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME,
                                        "rc-button goog-inline-block rc-button-audio".replace(" ", "."))))\
        .click()
    
    print("----------FOUND IFRAME - IMAGE CHALLENGE----------")

    recognition_res = 1
    while recognition_res:
        try:
            # Click on audio download button
            download_link = WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                "rc-audiochallenge-tdownload-link".replace(" ", "."))))\
            
            # Retrieve audio and convert to .wav                                    
            ret = None
            tmp_dir = tempfile.gettempdir()
            mp3_file = os.path.join(tmp_dir, PATH+"audio.mp3")
            wav_file = os.path.join(tmp_dir, PATH+"audio.wav")
            tmp_files = [mp3_file, wav_file]

            with open(mp3_file, "wb") as f:
                link = download_link.get_attribute("href")
                r = requests.get(link, allow_redirects=True)
                f.write(r.content)
                f.close()

            AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")

            # Speech to text functionality
            recognizer = sr.Recognizer()

            with sr.AudioFile(wav_file) as source:
                recorded_audio = recognizer.listen(source)
                text = recognizer.recognize_google(recorded_audio, language="es-CO")
                
            recognition_res = 0

        except Exception as e:
            print("Error: " + str(e))

            # Click on "load new audio" button
            WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                "rc-button goog-inline-block rc-button-reload".replace(" ", "."))))\
                .click()
            
            delay()
            
    # Input text in field
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.ID,
                                        "audio-response")))\
        .send_keys(text)

    # Click the "Verify" button to complete
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.ID,
                                        "recaptcha-verify-button")))\
        .click()
except:
    pass

# Go back to default content
driver.switch_to.default_content()
delay()

# Click on "Search" button
WebDriverWait(driver, 5)\
.until(EC.element_to_be_clickable((By.ID,
                                    "j_idt17")))\
.click()

delay()

text = driver.find_element(By.XPATH, "//div[@id='form:j_idt8']").text
print(text)

driver.quit()

