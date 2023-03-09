from fastapi      import FastAPI
from pydantic     import BaseModel

from selenium                       import webdriver
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support     import expected_conditions as EC
from selenium.webdriver.common.by   import By
from selenium.common.exceptions     import TimeoutException

import time

from pydub import AudioSegment
import speech_recognition as sr
import tempfile
import requests
import os

app = FastAPI(title="Police - Web crawler",
              description="API that retrieves data from Police website",
              version="0.1.0")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")

DRIVER_PATH = "D:\\ITSENSE_D\\COFACE\\webscrapping\\tools\\chromedriver.exe"

@app.get("/", tags=["home"])
def home():
    message = {
        "status": 200,
        "message": [
            "Police - Web crawler - Home"
        ]
    }
    return message

def is_elem_present(driver: webdriver, locator_type: str, locator: str, timeout: int):
    try:
        return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((locator_type, locator)))
    except TimeoutException:
        return False


@app.post('/search',)
def search(query:dict):
    id = str(query["id"])

    driver = webdriver.Chrome(DRIVER_PATH, options=options)

    # Start browser
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

    WebDriverWait(driver, 5)\
        .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        "input[role='textbox']")))\
        .send_keys(id)

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

    time.sleep(1)

    # Select challenge iframe and switch to it
    iframes = driver.find_elements(By.TAG_NAME, "iframe") 
    print([iframe.get_attribute("src") for iframe in iframes])

    challenge_iframe = driver.find_element(By.CSS_SELECTOR, "iframe[title='El reCAPTCHA caduca dentro de dos minutos']") 
    driver.switch_to.frame(challenge_iframe)

    # Check whether the captcha has a challenge or not
    audio_button = is_elem_present(
            driver, By.CLASS_NAME, "rc-button goog-inline-block rc-button-audio".replace(" ", "."), 5)

    if audio_button:
        # Click on audio button
        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.CLASS_NAME,
                                            "rc-button goog-inline-block rc-button-audio".replace(" ", "."))))\
            .click()
        
        print("----------FOUND IFRAME - IMAGE CHALLENGE----------")

        recognition_res = 1
        count = 0
        while recognition_res:
            try:
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
            
            # The audio is probably pure noise
            except Exception as e:
                count += 1
                if count > 5:
                    text = False
                    recognition_res = 0
                                    
                print("Error: " + str(e))

                # Click on "load new audio" button
                WebDriverWait(driver, 5)\
                    .until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                    "rc-button goog-inline-block rc-button-reload".replace(" ", "."))))\
                    .click()
                time.sleep(1)
        
        # No transcription was achieved
        if not text:
            message = {
                "status": 500,
                "ID": id,
                "message": "Audio recognition error"
            }
            return message  
        
        else:
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
    time.sleep(1)

    # Click on "Search" button
    WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.ID,
                                        "j_idt17")))\
    .click()

    time.sleep(2)

    text = driver.find_element(By.XPATH, "//div[@id='form:j_idt8']").text
    print(text)

    driver.quit()

    message = {
        "status": 200,
        "ID": id,
        "message": text
    }
    return message  
