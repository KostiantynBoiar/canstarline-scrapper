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


def download_pdf(pdf_url, output_path):
    response = requests.get(pdf_url)
    with open(output_path, 'wb') as file:
        file.write(response.content)



def parce(links):
    
    service = Service("geckodriver.exe")
    service.start()
    
    try:
        for link in links:
            try:
                driver.get(f'{link}#schemes')
                time.sleep(3)
                print(link)
            except:
                continue
            brand = driver.find_element(By.CSS_SELECTOR, "#root > section > main > section > div > form > div > div:nth-child(2) > div > div > div.ant-col.ant-form-item-control > div > div > div > div > span.ant-select-selection-item").text
            model = driver.find_element(By.CSS_SELECTOR, "#root > section > main > section > div > form > div > div.ant-col.ant-col-xs-24.ant-col-sm-16.ant-col-md-16 > div > div:nth-child(1) > div > div > div.ant-col.ant-form-item-control > div > div > div > div > span.ant-select-selection-item").text
            year = driver.find_element(By.CSS_SELECTOR, "#root > section > main > section > div > form > div > div.ant-col.ant-col-xs-24.ant-col-sm-16.ant-col-md-16 > div > div:nth-child(2) > div > div > div.ant-col.ant-form-item-control > div > div > div > div > span.ant-select-selection-item").text
            version = driver.find_element(By.CSS_SELECTOR, "#root > section > main > section > div > form > div > div.ant-col.ant-col-xs-24.ant-col-sm-16.ant-col-md-16 > div > div:nth-child(3) > div > div > div.ant-col.ant-form-item-control > div > div > div > div > span.ant-select-selection-item").text
            
            pdf_elements = driver.find_elements(By.CSS_SELECTOR, 'div > div > div > ul > li > div > div > h4 > a')
            id = 0
            for pdf_element in pdf_elements:

                pdf_url = pdf_element.get_attribute('href')
                
                if pdf_url.startswith('/'):
                    base_url = driver.current_url.split('#')[0]
                    pdf_url = base_url + pdf_url
                
                # Формируем финальное имя файла и путь к папке
                folder_name = f'{brand}_{model}_{year}_{version}'
                folder_name = folder_name.replace('/', '_').replace('\\', '_')
                output_folder = os.path.join('schemes', folder_name)
                os.makedirs(output_folder, exist_ok=True)
                
                final_filename = f'{brand}_{model}_{year}_{version}_{pdf_element.text}_{id}.pdf'
                final_filename = final_filename.replace('/', '_').replace('\\', '_')  # Убираем недопустимые символы
                output_path = os.path.join(output_folder, final_filename)
                id += 1
                print(f'Скачивание PDF из {pdf_url} в файл {output_path}')
                download_pdf(pdf_url, output_path)

    
    finally:
        driver.quit()

def get_links(urls):

    driver.get(urls[0])
    time.sleep(2)
    element_to_hover_over = driver.find_element(By.CSS_SELECTOR, ".ant-menu-horizontal > .ant-menu-submenu > .ant-menu-submenu-title")
    actions = ActionChains(driver)
    actions.move_to_element(element_to_hover_over).perform()
    time.sleep(1)
    element_to_click = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/ul/li/span/button/span[text()='English']")
    #element_to_click = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/ul/li/span/button/span[text()='Український']")
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
    #links = ["https://can.starline.ru/20/23/9726"]

    parce(links)

if __name__ == '__main__':
    main()