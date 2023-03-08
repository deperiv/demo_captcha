# Librerías
from selenium                       import webdriver
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support     import expected_conditions as EC
from selenium.webdriver.common.by   import By

import time
import pandas as pd

# Opciones de navegación
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")

DRIVER_PATH = "C:\\Users\\Dperazar\\QA\\Tools\\Selenium\\chromedriver_win32\\chromedriver.exe"

driver = webdriver.Chrome(DRIVER_PATH, chrome_options=options)

# Inicializamos el navegador
driver.get("https://eltiempo.es")

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      "button.didomi-components-button didomi-button didomi-dismiss-button didomi-components-button--color didomi-button-highlight highlight-button".replace(" ", "."))))\
    .click()

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      "input#term")))\
    .send_keys("Madrid")

time.sleep(3)

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'i.icon.icon-search')))\
    .click()

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                      'i.icon_weather_s.icon.icon-sm.icon-city')))\
    .click()

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      "/html/body/div[5]/div[1]/div[4]/div/section[4]/section/div/article/section/ul[1]/li[2]/h2")))\
    .click()

WebDriverWait(driver, 5)\
    .until(EC.element_to_be_clickable((By.XPATH,
                                      '/html/body/div[5]/div[1]/div[4]/div/section[4]/section/div[1]/ul/li[1]/ul')))\

texto_columnas = driver.find_element(By.XPATH, '/html/body/div[5]/div[1]/div[4]/div/section[4]/section/div[1]/ul/li[1]/ul')
texto_columnas = texto_columnas.text

tiempo_manana = texto_columnas.split("\n")

# Crear dataframe que almacena hora, temperatura y velocidad del viento
len_row = 9
info_rows = [tiempo_manana[len_row*i:len_row*i+len_row] for i in list(range(len(tiempo_manana)//len_row))]
imp_rows = [[row[1], row[3], row[6]] for row in info_rows]

df = pd.DataFrame(imp_rows, columns=["Hora", "Temperatura", "Velocidad del viento [Km/h]"])
print(df)

# hora_l = []
# temperatura_l = []
# viento_l = []

# for i in range(0, len(tiempo_manana)-1, 7):
#     hora_l.append(tiempo_manana[i+1])
#     temperatura_l.append(tiempo_manana[i+3])
#     viento_l.append(tiempo_manana[i+6])

# df = pd.DataFrame({"Horas": hora_l, "Temperatura": temperatura_l, "Velocidad del viento [Km/h]": viento_l})
# print(df)

df.to_csv("C:\\Users\\Dperazar\\QA\\Projects\\Webscrapping\\resultado.csv", index=False)

driver.quit()


