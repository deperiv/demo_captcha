from selenium                       import webdriver
from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support     import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType

import time

# PROXY="169.55.89.6:8123"

# webdriver.DesiredCapabilities.CHROME['proxy'] = {
#     "httpProxy": PROXY,
#     "ftpProxy": PROXY,
#     "sslProxy": PROXY,
#     "proxyType": "MANUAL",

# }

# webdriver.DesiredCapabilities.CHROME['acceptSslCerts']=True

proxy_ip_port = "20.206.106.192:8123"
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = proxy_ip_port
proxy.ssl_proxy = proxy_ip_port

capabilities = webdriver.DesiredCapabilities.CHROME
proxy.add_to_capabilities(capabilities)

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
# options.add_argument('--proxy-server=%s' % PROXY)

DRIVER_PATH = "D:\\ITSENSE_D\\COFACE\\webscrapping\\tools\\chromedriver.exe"

driver = webdriver.Chrome(DRIVER_PATH, options=options, desired_capabilities=capabilities)

# Start browser
driver.get("https://www.whatismyip.com/")
# driver.get("https://antecedentes.policia.gov.co:7005/WebJudicial/index.xhtml")
# driver.get("https://www.google.com/?hl=es")


time.sleep(20)