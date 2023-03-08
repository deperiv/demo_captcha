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

text = driver.find_element(By.XPATH, "//div[@id='j_idt8']").text
print(text)

time.sleep(10)

driver.quit()



