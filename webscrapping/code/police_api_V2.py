from selenium                       import webdriver
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support     import expected_conditions as EC
from selenium.webdriver.common.by   import By
from selenium.common.exceptions     import TimeoutException
from fastapi                        import FastAPI
from pydub                          import AudioSegment
import speech_recognition      as sr
import undetected_chromedriver as uc
import numpy                   as np
import tempfile
import requests
import os
import time


USER_AGENT_LIST = ['Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0',
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
                    ]

PATH = "D:\\ITSENSE_D\\COFACE\\webscrapping\\tools\\"
DRIVER_PATH = PATH + "chromedriver.exe"
EXT_PATH = PATH + "touchVPN.crx"

EXTENSION_LINK = "chrome-extension://bihmplhobchoageeokmgbdihknkjbknd/panel/index.html"
POLNAL_LINK = "https://antecedentes.policia.gov.co:7005/WebJudicial/index.xhtml"
IP_LINK = "https://www.whatismyip.com/"

app = FastAPI(title="Police - Web crawler",
              description="API that retrieves data from Police website",
              version="0.1.0")

def delay(min=2,max=5):
    time.sleep(np.random.randint(min,max))   

def is_elem_present(driver: webdriver, locator_type: str, locator: str, timeout: int):
    try:
        return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((locator_type, locator)))
    except TimeoutException:
        return False
    
@app.get("/", tags=["home"])
def home():
    message = {
        "status": 200,
        "message": [
            "Police - Web crawler - Home"
        ]
    }
    return message

@app.post('/search',)
def search(query:dict):
    id = str(query["id"])

    # userAgent_id = np.random.randint(0,5)

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_extension(EXT_PATH)
    # options.add_argument(f'user-agent={USER_AGENT_LIST[userAgent_id]}')
    # options.add_argument(r'--user-data-dir=C:\Users\Usuario\AppData\Local\Google\Chrome\User Data\Default')

    driver = webdriver.Chrome(DRIVER_PATH, options=options)

    try: 
        # Start browser 
        driver.get(EXTENSION_LINK)
        delay()
        #obtain parent window handle
        parent = driver.window_handles[0]
        #obtain browser tab window
        chld = driver.window_handles[1]
        #switch to browser tab
        driver.switch_to.window(chld)
        #close browser tab window
        driver.close()
        #switch to parent window
        driver.switch_to.window(parent)

        delay()

        # Change IP through VPN
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
        
        delay()

        # Click on "Send" button
        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "button[role='button']")))\
            .click()

        delay()

        WebDriverWait(driver, 5)\
            .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "input[role='textbox']")))\
            .send_keys(id)
        
        delay()
    except:
        message = {
            "status": 500,
            "ID": id,
            "message": "Connection error"
        }
        return message 

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

    # Select challenge iframe and switch to it
    iframes = driver.find_elements(By.TAG_NAME, "iframe") 

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

        delay()

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
            
            # The audio is probably pure noise
            except Exception as e:
                count += 1
                if count > 5:
                    text = False
                    recognition_res = 0
                                    
                print("Error: " + str(e))

                try:
                    # Click on "load new audio" button
                    WebDriverWait(driver, 5)\
                        .until(EC.element_to_be_clickable((By.CLASS_NAME,
                                                        "rc-button goog-inline-block rc-button-reload".replace(" ", "."))))\
                        .click()
                    
                    delay()

                except:
                    message = {
                        "status": 500,
                        "ID": id,
                        "message": "IP has been blacklisted"
                    }
                    return message  
        
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
            
            delay()

            # Click the "Verify" button to complete
            WebDriverWait(driver, 5)\
                .until(EC.element_to_be_clickable((By.ID,
                                                "recaptcha-verify-button")))\
                .click()
        
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

    driver.quit()

    message = {
        "status": 200,
        "ID": id,
        "message": text
    }
    return message  
