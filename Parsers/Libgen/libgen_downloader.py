import os
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

os.environ['PATH'] += r"C:/SeleniumDrivers"
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "D:\\Downloads\\LibgenBooks"}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome('C:\\SeleniumDrivers\\chromedriver.exe', chrome_options=options)

with open('libgen_links.txt', 'r') as download_links:
    links = download_links.readlines()
    i = 1
    for link in links:
        my_link = link[:-1]
        print(i, ':', my_link)
        driver.get(my_link)
        driver.maximize_window()
        time.sleep(2)
        driver.implicitly_wait(5)
        try:
            get_button = driver.find_element_by_xpath('//*[@id="download"]/h2/a')
            get_button.click()
        except NoSuchElementException:
            print("Not found", i)
            time.sleep(30)
            pass
        time.sleep(0.5)
        i += 1
