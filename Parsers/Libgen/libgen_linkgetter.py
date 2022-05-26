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

with open('libgen_links.txt', 'w') as download_links:
    for page in range(1, 100):
        driver.get('http://libgen.is/search.php?&res=100&req=chinese&phrase=1&view=simple&column=language&sort=def&sortmode=ASC&page=' + str(page))
        driver.implicitly_wait(20)
        driver.maximize_window()

        for row in range(2, 101):
            extension = driver.find_element_by_xpath('./html/body/table[3]/tbody/tr[' + str(row) + ']/td[9]').get_attribute('innerHTML')
            if (extension == 'epub'):
                link = driver.find_element_by_xpath('./html/body/table[3]/tbody/tr[' + str(row) + ']/td[10]/a')
                download_links.write(link.get_attribute('href'))
                download_links.write('\n')