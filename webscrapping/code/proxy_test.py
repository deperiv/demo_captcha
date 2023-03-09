from selenium                       import webdriver
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support     import expected_conditions as EC
from selenium.webdriver.common.by   import By

import time

import speech_recognition as sr
import os

import numpy as np

PROXY = "190.61.88.147:8080"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
options.add_argument('--proxy-server=%s' % PROXY)

DRIVER_PATH = "D:\\ITSENSE_D\\COFACE\\webscrapping\\tools\\chromedriver.exe"

driver = webdriver.Chrome(DRIVER_PATH, options=options)

# Start browser
driver.get("https://www.whatismyip.com/")

time.sleep(10)