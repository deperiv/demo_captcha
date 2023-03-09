from selenium                       import webdriver
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support     import expected_conditions as EC
from selenium.webdriver.common.by   import By

import time

from pydub import AudioSegment
import speech_recognition as sr
import tempfile
import requests
import os

ext_file = "D:\\ITSENSE_D\\COFACE\\webscrapping\\tools\\hola_VPN.crx"
# ext_file = "D:\\ITSENSE_D\\COFACE\\webscrapping\\tools\\uVPN.crx"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_extension(ext_file)

# CEDULA = "1026595200"
# CEDULA = "71984381"
CEDULA = "10773983"

DRIVER_PATH = "D:\\ITSENSE_D\\COFACE\\webscrapping\\tools\\chromedriver.exe"

driver = webdriver.Chrome(DRIVER_PATH, options=options)

# Start browser
driver.get("https://antecedentes.policia.gov.co:7005/WebJudicial/index.xhtml")

time.sleep(240)

driver.quit()
