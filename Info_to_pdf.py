from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import pdfkit
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import os
import pdfkit
from selenium.webdriver.common.by import By
import time
from PIL import Image, ImageDraw, ImageFont
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import random


options = Options()
options.add_argument("--headless")

driver = webdriver.Firefox(options=options)


def download_car_image(driver, final_filename):
    save_folder = f'C:/Users/Kostiantyn/Documents/PythonScripts/pr1/{final_filename}'
    # Создаем папку для сохранения изображений, если она не существует
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    # Находим все элементы с указанным селектором
    image = driver.find_element(By.CSS_SELECTOR, "#root > section > main > section > div > div.ant-row > div > div > div > div > a")
    # Скачиваем изображения
    image_url = image.get_attribute("href")
    image_name = f"AA_Car_Photo_{final_filename}.jpg"  
    image_path = os.path.join(save_folder, image_name)
    with open(image_path, "wb") as f:
            f.write(requests.get(image_url).content)
            print(f"Изображение {image_name} успешно скачано.")
    f.close()
    
def download_images(driver, final_filename, filename_var):

    save_folder = f'C:/Users/Kostiantyn/Documents/PythonScripts/pr1/{final_filename}'
    # Создаем папку для сохранения изображений, если она не существует
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    # Находим все элементы с указанным селектором
    
    for elem in driver.find_elements(By.CSS_SELECTOR, ".connections .connections-collapse-item"):

        images = elem.find_elements(By.CSS_SELECTOR, ".gallery .gallery-previews_item .gallery-preview-link")
        elem_header = elem.find_element(By.CSS_SELECTOR, "div > div> div.ant-collapse-header > span").text

        for i, image in enumerate(images):
            
            image_url = image.get_attribute("href")
            image_name = f"zImage_{final_filename}_{elem_header}_{i}.jpg"  
            image_path = os.path.join(save_folder, image_name)
            with open(image_path, "wb") as f:
                f.write(requests.get(image_url).content)
                print(f"Изображение {image_name} успешно скачано.")
        f.close()
"""
    # Скачиваем изображения
    for i, image in enumerate(images):
        image_url = image.get_attribute("href")
        image_name = f"zImage_{final_filename}_{filename_var}_{i}.jpg"  
        image_path = os.path.join(save_folder, image_name)
        with open(image_path, "wb") as f:
            f.write(requests.get(image_url).content)
            print(f"Изображение {image_name} успешно скачано.")
    f.close()
"""

def caputure_element_as_screenshot(url_models):

    service = Service("geckodriver.exe")
    service.start()

    for final_url in url_models:
        print(final_url)
        try:
            driver.get(f'{final_url}#connections')
            time.sleep(3)
        except:
            continue

        try:
            brand = driver.find_element(By.CSS_SELECTOR, "#root > section > main > section > div > form > div > div:nth-child(2) > div > div > div.ant-col.ant-form-item-control > div > div > div > div > span.ant-select-selection-item")
            model = driver.find_element(By.CSS_SELECTOR, "#root > section > main > section > div > form > div > div.ant-col.ant-col-xs-24.ant-col-sm-16.ant-col-md-16 > div > div:nth-child(1) > div > div > div.ant-col.ant-form-item-control > div > div > div > div > span.ant-select-selection-item")
            year = driver.find_element(By.CSS_SELECTOR, "#root > section > main > section > div > form > div > div.ant-col.ant-col-xs-24.ant-col-sm-16.ant-col-md-16 > div > div:nth-child(2) > div > div > div.ant-col.ant-form-item-control > div > div > div > div > span.ant-select-selection-item")
            version = driver.find_element(By.CSS_SELECTOR, "#root > section > main > section > div > form > div > div.ant-col.ant-col-xs-24.ant-col-sm-16.ant-col-md-16 > div > div:nth-child(3) > div > div > div.ant-col.ant-form-item-control > div > div > div > div > span.ant-select-selection-item") 
            
            final_filename = f'{brand.text} {model.text} {(year.text).replace(' ', '')} {(version.text).replace('Все комплектации', 'All versions')}'
            print(final_filename)
            #wait = WebDriverWait(driver, 10)
            time.sleep(2)
            for elems in driver.find_elements(By.CSS_SELECTOR, ".ant-collapse>.ant-collapse-item>.ant-collapse-header .ant-collapse-header-text"):
                driver.implicitly_wait(10)
                elems.click()

            css_selectors = [".device-connection", "#root > section > main > section > div > form", ".download-firmware-button", ".filter-item.filter-firmware .ant-form-item-row", "#root > section > main > section > div > div.ant-tabs.ant-tabs-top.ant-tabs-large.single-model_tabs > div.ant-tabs-nav > div.ant-tabs-nav-wrap > div > div:nth-child(3)", "#root > section > main > section > div > div.ant-tabs.ant-tabs-top.ant-tabs-large.single-model_tabs > div.ant-tabs-nav > div.ant-tabs-nav-wrap > div > div:nth-child(4)", "#root > section > main > section > div > div.ant-tabs.ant-tabs-top.ant-tabs-large.single-model_tabs > div.ant-tabs-nav > div.ant-tabs-nav-wrap > div > div:nth-child(5)", ".firmware-version-banner_container"]
            download_car_image(driver, final_filename)



            for selector in css_selectors:
                driver.implicitly_wait(4)
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    try:
                        driver.execute_script("arguments[0].style.display='none'", element)
                    except:
                        continue

            var = 1
            img_id = 0
            bool_var = False
            for elem in driver.find_elements(By.CSS_SELECTOR, ".connections .connections-collapse-item"):

                for var_elem in elem.find_elements(By.CSS_SELECTOR, ".ant-tabs-tab-btn, .ant-tabs-tab-remove"):
                    var += 1
                print(var)

                elem_header = elem.find_element(By.CSS_SELECTOR, "div > div> div.ant-collapse-header > span").text
                elem.screenshot(f"C:/Users/Kostiantyn/Documents/PythonScripts/pr1/{final_filename}/{final_filename}_{elem_header}_Option 1.png")
                img_id += 1

                #download_images(driver, final_filename, elem_header, 'Option 1', elem)    
                var_elements = elem.find_elements(By.CSS_SELECTOR, f".ant-tabs-tab-btn, .ant-tabs-tab-remove")
                for var_element in var_elements:
                    if var_element.get_attribute("aria-selected") == 'true':
                        continue
                    else:
                        try:
                            var_element.click()
                            elem.screenshot(f"C:/Users/Kostiantyn/Documents/PythonScripts/pr1/{final_filename}/{final_filename}_{elem_header}_{var_element.text}.png")
                            img_id += 1
                        except:
                            print("Element does not exsist")


                var = 1

            download_images(driver, final_filename, '')

            img_id = 0

            driver.find_element(By.CSS_SELECTOR, "#root > section > main > section > div > div.ant-tabs.ant-tabs-top.ant-tabs-large.single-model_tabs > div.ant-tabs-nav > div.ant-tabs-nav-wrap > div > div:nth-child(1)").click()
            time.sleep(1)


            css_selectors_reg = ["#root > section > main > section > div > div.ant-row > div:nth-child(3) > div > div > div > div > div > button", ".firmware-version-banner_container"]

            for selector in css_selectors_reg:
                driver.implicitly_wait(4)
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                for element in elements:
                    try:
                        driver.execute_script("arguments[0].style.display='none'", element)
                    except:
                        continue
        

          
            css_selector_reg = '#root > section > main'
            element_reg = driver.find_element(By.CSS_SELECTOR, css_selector_reg)
            element_reg.screenshot(f'C:/Users/Kostiantyn/Documents/PythonScripts/pr1/{final_filename}/zFunctions_{final_filename}_reg.png')

            create_pdf_from_screenshots(final_filename)


        except Exception as e:
            print(e)
            continue


def create_pdf_from_screenshots(pdf_path):
    images = []
    folder = f'C:/Users/Kostiantyn/Documents/PythonScripts/pr1/{pdf_path}/'
    screenshot_folder = f'C:/Users/Kostiantyn/Documents/PythonScripts/pr1/{pdf_path}'
    save_folder = f'C:/Users/Kostiantyn/Documents/PythonScripts/pr1//pdf/{pdf_path}'
    for filename in os.listdir(screenshot_folder):
        if filename.endswith(".png") or filename.endswith(".jpeg") or filename.endswith(".jpg"):
            image = Image.open(os.path.join(screenshot_folder, filename)).convert('RGB')
            images.append(image)

    if images:
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)
        images[0].save(f'{save_folder}/{pdf_path}.pdf', save_all=True, append_images=images[1:], mode='RGB')
        print(f'PDF файл создан по пути: {pdf_path}')
    else:
        print("В папке screenshots нет ни одного скриншота.")
    return 

def get_links(urls):

    driver.get(urls[0])
    time.sleep(2)
    element_to_hover_over = driver.find_element(By.CSS_SELECTOR, ".ant-menu-horizontal > .ant-menu-submenu > .ant-menu-submenu-title")
    actions = ActionChains(driver)
    actions.move_to_element(element_to_hover_over).perform()
    time.sleep(1)
    element_to_click = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/ul/li/span/button/span[text()='English']")

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

"""
    for models in url_models:
        driver.get(models)
        time.sleep(2)
        elem = driver.find_element(By.CSS_SELECTOR, "#root > section > main > section > div > div.ant-row > div.ant-col.firmwares-control.ant-col-xs-24.ant-col-sm-4.ant-col-md-4 > div > div > div > div > div > div > div > span.ant-select-selection-item").click()
        try:
            html_code = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]/div")
        except:
            html_code = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div/div[1]")

        soup = BeautifulSoup(html_code.get_attribute('outerHTML'), 'html.parser')

        div_elements = soup.find('div')
        for div_element in div_elements:
            text = div_element.text
            text2 = div_element.find_next('div')
            print(text2)
            print(f'{models}#connection?firmware={text}')
            
           # url_firmware.append(f'{models}#connection?firmware={text}')
   """ 
    

def main():
    urls = ["https://can.starline.ru/20"]#, "https://can.starline.ru/40"]
    links = get_links(urls)
    #links = ['https://can.starline.ru/20/1/6581', 'https://can.starline.ru/40/3/6588']
    caputure_element_as_screenshot(links)
    

if __name__ == "__main__":
    main()