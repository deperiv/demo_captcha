# Librerías
from selenium                       import webdriver
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support     import expected_conditions as EC
from selenium.webdriver.common.by   import By

import time
import pandas as pd

from selenium import webdriver
from selenium_recaptcha import Recaptcha_Solver

# Opciones de navegación
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")

DRIVER_PATH = "C:\\Users\\Dperazar\\QA\\Tools\\Selenium\\chromedriver_win32\\chromedriver.exe"

driver = webdriver.Chrome(DRIVER_PATH, options=options)

driver.get('https://www.google.com/recaptcha/api2/demo')

time.sleep(3)

solver = Recaptcha_Solver(
driver=driver, # Your Web Driver
debug=False
)
solver.solve_recaptcha()