from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import pdfkit
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import os
import pdfkit
from selenium.webdriver.common.by import By
import time
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains



options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)




def get_links(urls):

    driver.get(urls[0])
    time.sleep(2)
    element_to_hover_over = driver.find_element(By.CSS_SELECTOR, ".ant-menu-horizontal > .ant-menu-submenu > .ant-menu-submenu-title")
    actions = ActionChains(driver)
    actions.move_to_element(element_to_hover_over).perform()
    time.sleep(1)
    #element_to_click = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/ul/li/span/button/span[text()='English']")
    element_to_click = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/ul/li/span/button/span[text()='Український']")
    element_to_click.click()

    urls_brands = []
    for link in urls:
        driver.get(link)
        driver.implicitly_wait(3)
        url_brand = driver.find_elements(By.CSS_SELECTOR, "#root > section > main > section > div > div.brands-all > div > div > div > div > div > ul > li > a")
        for url in url_brand:
            urls_brands.append(url.get_attribute('href'))
    
    url_models = []
    i = 0
    for url_brand in urls_brands:
#        if i == 3:
#            break
        i += 1
        print(url_brand)
        driver.get(url_brand)
        url_model = driver.find_elements(By.CSS_SELECTOR, "#root > section > main > section > div > div.ant-list.ant-list-grid.models-list > div > div > div > div > div > div > div > div > div.ant-list.equipments-list > div > div > ul > li > a")
        for url in url_model:
            url_models.append(url.get_attribute('href'))

    url_firmware = []
    return url_models


def main():
    urls = ["https://can.starline.ru/40"]
    links = get_links(urls)

if __name__ == '__main__':
    main()