from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import os
import time
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("no-sandbox")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--headless")
driver = os.path.join("/usr/local/bin","chromedriver")
prefs = {'disk-cache-size': 4096}
chrome_options.add_experimental_option("prefs", prefs)


import urllib.request

PROXY = "185.34.22.225:44050" # IP:PORT or HOST:PORT

# chrome_options.add_argument('--proxy-server=%s' % PROXY)

print(urllib.request.urlopen('http://httpbin.org/ip').read())

browser = webdriver.Chrome(options=chrome_options)

browser.get('https://www.google.nl/')
time.sleep(10)
html = browser.page_source
print(html)