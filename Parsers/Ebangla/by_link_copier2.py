import os
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setting up all the things
os.environ['PATH'] += r"C:/src/SeleniumChrome"
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "D:\\Downloads\\LibgenBooks"}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome('C:\\src\\SeleniumChrome\\chromedriver.exe', chrome_options=options)

links_file = "bangla_batch8.txt"
write_to = "D:\\BBooks\\batch8\\"

link_cnt = 0
text_cnt = 0
with open(links_file, 'r', encoding='utf-8') as download_links:
    links = download_links.readlines()
    for i in range(link_cnt, len(links)):

        print(link_cnt, '/', len(links), '::::', links[i])
        link_cnt += 1
        driver.get(links[i])
        driver.maximize_window()
        driver.implicitly_wait(2)
        book = driver.find_element(by=By.CLASS_NAME, value='content-sidebar-wrap')
        paragraphs = book.find_elements(by=By.TAG_NAME, value='p')

        with open(write_to + "book_batch8_" + str(link_cnt) + ".txt", 'w', encoding='utf-8') as book_text:
            for paragraph in paragraphs:
                book_text.write(paragraph.text)
                book_text.write('\n')
