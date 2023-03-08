# Librerías
from selenium                       import webdriver
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support     import expected_conditions as EC
from selenium.webdriver.common.by   import By
from selenium.common.exceptions import TimeoutException

import time
import pandas as pd

import captcha_bypass
from enum import Enum
from typing import Tuple
from pydub import AudioSegment
import speech_recognition as sr
import tempfile
import requests
import os


# Opciones de navegación
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")

DRIVER_PATH = "D:\\ITSENSE_D\\COFACE\\webscrapping\\tools\\chromedriver.exe"

driver = webdriver.Chrome(DRIVER_PATH, options=options)

# Inicializamos el navegador
driver.get("https://antecedentes.policia.gov.co:7005/WebJudicial/index.xhtml")

time.sleep(3)
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

time.sleep(3)

# Input ID number
WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      "input[role='textbox']")))\
    .send_keys("71984381")

# Find captcha iframe
iframe = driver.find_element(By.TAG_NAME, "iframe") 
if iframe.get_attribute("src").startswith("https://www.google.com/recaptcha/api2/anchor"):
    print("FOUND IFRAME ----------")
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

time.sleep(5)

# Select challenge iframe and switch to it
try:
    challenge_iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title='El reCAPTCHA caduca dentro de dos minutos']") 
    driver.switch_to.frame(challenge_iframe)

    # Click on audio button
    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME,
                                        "rc-button goog-inline-block rc-button-audio".replace(" ", "."))))\
        .click()

    # Click on audio download button
    download_link = WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CLASS_NAME,
                                        "rc-audiochallenge-tdownload-link".replace(" ", "."))))\
    # Retrieve audio and convert to .wav                                    
    ret = None
    tmp_dir = tempfile.gettempdir()
    mp3_file = os.path.join(tmp_dir, "D:\ITSENSE_D\COFACE\webscrapping\\tools\\audio.mp3")
    wav_file = os.path.join(tmp_dir, "D:\ITSENSE_D\COFACE\webscrapping\\tools\\audio.wav")
    tmp_files = [mp3_file, wav_file]

    with open(mp3_file, "wb") as f:
        link = download_link.get_attribute("href")
        print(link)
        r = requests.get(link, allow_redirects=True)
        f.write(r.content)
        f.close()

    AudioSegment.from_mp3(mp3_file).export(wav_file, format="wav")

    # Speech to text functionality
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_file) as source:
        recorded_audio = recognizer.listen(source)
        text = recognizer.recognize_google(recorded_audio)

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
    
    # Go back to default content
    driver.switch_to.default_content()
except Exception as e:
    print(str(e))


time.sleep(2)

# Click on "Search" button
WebDriverWait(driver, 5)\
.until(EC.element_to_be_clickable((By.ID,
                                    "j_idt17")))\
.click()

time.sleep(2)

text = driver.find_element(By.XPATH, "//div[@id='form:j_idt8']").text
print(text)

time.sleep(10)

driver.quit()



