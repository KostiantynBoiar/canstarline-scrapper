from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import pdfkit
from selenium.webdriver.firefox.options import Options
import os
import pdfkit
from selenium.webdriver.common.by import By
import time
from PIL import Image, ImageDraw, ImageFont
import requests
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
from concurrent.futures import ThreadPoolExecutor
import threading


options = Options()
options.add_argument("--headless")
main_urls = []
lock = threading.Lock()


def parse(urls):
    print(urls)

    try:
        driver = webdriver.Firefox(options=options)
        for url in urls:
            buffer_name = ''
            buffer_can_b = ''
            buffer_can_c = ''
            buffer_can_lin_a = ''
            buffer_can_lin_ab = ''
            buffer_can_imoimi = ''
            buffer_can_c = ''

            results = []
            
            #if url in get_url_column_from_csv():
            #    continue

            print(f'{url} not in CSV')
            driver.get(url)
            time.sleep(2.5)
            driver.execute_script("document.cookie = '_language=uk';")

        # Refresh the page
            driver.refresh()
            time.sleep(1)
            """
            element_to_hover_over = driver.find_element(By.CSS_SELECTOR, ".ant-menu-horizontal > .ant-menu-submenu > .ant-menu-submenu-title")
            actions = ActionChains(driver)
            actions.move_to_element(element_to_hover_over).perform()

            # Wait until the element_to_click is clickable
            element_to_click = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div/div/ul/li/span/button/span[text()='English']")))
            element_to_click.click()
"""
            headers_dic = {}
            i = 2
            
            try:
                for headers in driver.find_elements(By.CSS_SELECTOR, "div > div.functions-tables > div:nth-child(1) > div > div > div > div > div > div > table > thead > tr > th > div > div > div:nth-child(2)"):
                    print(headers.text)
                    headers_dic[headers.text] = i
                    i += 1
                if headers_dic == {}:
                    headers_dic = {
                        "CAN-A": 2
                    }
                
                time.sleep(4)
                brand = driver.find_element(By.CSS_SELECTOR, '#root > section > main > section > div > form > div > div:nth-child(2) > div > div > div.ant-col.ant-form-item-control > div > div > div > div > span.ant-select-selection-item').text
                model = driver.find_element(By.CSS_SELECTOR, '#root > section > main > section > div > form > div > div > div > div:nth-child(1) > div > div > div > div > div > div > div > span.ant-select-selection-item').text
                year = driver.find_element(By.CSS_SELECTOR, '#root > section > main > section > div > form > div > div > div > div:nth-child(2) > div > div > div > div > div > div > div > span.ant-select-selection-item').text
                version = driver.find_element(By.CSS_SELECTOR, '#root > section > main > section > div > form > div > div > div > div:nth-child(3) > div > div > div > div > div > div > div > span.ant-select-selection-item').text

                for rows in driver.find_elements(By.CSS_SELECTOR, "div > div.functions-tables > div:nth-child(1) > div > div > div > div > div > div > table > tbody > tr"):
                    

                    name = rows.find_element(By.CSS_SELECTOR, "div > div.functions-tables > div:nth-child(1) > div > div > div > div > div > div > table > tbody > tr > td:nth-child(1)").text
                    try:
                        comment = rows.find_element(By.CSS_SELECTOR, "div > div.functions-tables > div:nth-child(1) > div > div > div > div > div > div > table > tbody > tr > td > div.functions-table_function-commentary").text
                    except:
                        comment = ''


                    
                    try:
                        CAN_A = rows.find_element(By.CSS_SELECTOR, f"div > div.functions-tables > div:nth-child(1) > div > div > div > div > div > div > table > tbody > tr > td:nth-child({headers_dic['CAN-A']}) > div")
                        CAN_A = '+'
                    except:
                        CAN_A = '-'

                    try:
                        CAN_B = rows.find_element(By.CSS_SELECTOR, f"div > div.functions-tables > div:nth-child(1) > div > div > div > div > div > div > table > tbody > tr > td:nth-child({headers_dic['CAN-B']}) > div")
                        CAN_B = '+'
                    except:
                        CAN_B = '-'

                    try:
                        CAN_C = rows.find_element(By.CSS_SELECTOR, f"div > div.functions-tables > div:nth-child(1) > div > div > div > div > div > div > table > tbody > tr > td:nth-child({headers_dic['CAN-C']}) > div")
                        CAN_C = '+'
                    except:
                        CAN_C = '-'

                    try:
                        LIN_A = rows.find_element(By.CSS_SELECTOR, f"div > div.functions-tables > div:nth-child(1) > div > div > div > div > div > div > table > tbody > tr > td:nth-child({headers_dic['LIN-A']}) > div")
                        LIN_A = '+'
                    except:
                        LIN_A = '-'
                    
                    try:
                        LIN_AB = rows.find_element(By.CSS_SELECTOR, f"div > div.functions-tables > div:nth-child(1) > div > div > div > div > div > div > table > tbody > tr > td:nth-child({headers_dic['LIN-AB']}) > div")
                        LIN_AB = '+'
                    except:
                        LIN_AB = '-'

                    try:
                        IMO_IMI = rows.find_element(By.CSS_SELECTOR, f"div > div.functions-tables > div:nth-child(1) > div > div > div > div > div > div > table > tbody > tr > td:nth-child({headers_dic['IMO/IMI']}) > div")
                        IMO_IMI = '+'
                    except:
                        IMO_IMI = '-'
                    
                    # Если name совпадает с comment
                    if name == comment:
                        row = '', '', '', '', '', '', '', '', '', '', '', comment, ''
                        results.append(row)
                        print(row)

                        # Очищаем буферы
                        buffer_name = ''
                        buffer_can_a = ''
                        buffer_can_b = ''
                        buffer_can_c = ''
                        buffer_can_lin_a = ''
                        buffer_can_lin_ab = ''
                        buffer_can_imoimi = ''
                        continue
                    else:
                        # Добавляем данные в буферы
                        buffer_name = name
                        buffer_can_a = CAN_A
                        buffer_can_b = CAN_B
                        buffer_can_c = CAN_C
                        buffer_can_lin_a = LIN_A
                        buffer_can_lin_ab = LIN_AB
                        buffer_can_imoimi = IMO_IMI

                        row = brand, model, year, version, name, CAN_A, CAN_B, CAN_C, LIN_A, LIN_AB, IMO_IMI, comment, url
                        results.append(row)
                        print(row)
                i = 1
                print(headers_dic)

                for con in driver.find_elements(By.CSS_SELECTOR, "div > div.functions-tables > div.ant-table-wrapper.functions-table.table-striped"):
                    
                    item_rows = []
                    comment_rows = []
                    for button in con.find_elements(By.CSS_SELECTOR, ".functions-table .functions-table_row.__expanded td"):
                        item_rows.append(button.text)

                    for comment in con.find_elements(By.CSS_SELECTOR, ".functions-table .ant-table-expanded-row td"):
                        comment_rows.append(comment.text)
                    
                    for item, comment in zip(item_rows, comment_rows):
                        row = brand, model, year, version, f'Button: {item}', CAN_A, CAN_B, CAN_C, LIN_A, LIN_AB, IMO_IMI, comment, url

                        results.append(row)
                        print(row)
    
            except Exception as e:
                print(e)
                continue

            finally:
                with lock:
                    save_to_csv(results)
    
    except Exception as e:
        print(e)

    finally:
        driver.quit()
        print('Driver has been delete')



def get_brand_links(url, driver):

    urls = []
    driver.get(url[0])
    driver.execute_script("document.cookie = '_language=_en';")

# Refresh the page
    driver.refresh()
    time.sleep(1)

    for i in driver.find_elements(By.CSS_SELECTOR, "#root > section > main > section > div > div.brands-all > div > div > div > div > div > ul > li > a"):
       item = urls.append(i.get_attribute("href"))         
    print(urls)

    return urls


def get_links(urls, driver):

    urls_list = []
    j = 0
    driver.execute_script("document.cookie = '_language=en';")

# Refresh the page
    driver.refresh()
    time.sleep(1)
    for url in urls:

        if j == -1:
            return urls_list
        
        driver.get(url)
        driver.implicitly_wait(2)

        for i in driver.find_elements(By.CSS_SELECTOR, "#root > section > main > section > div > div.ant-list.ant-list-grid.models-list > div > div > div > div > div > div > div > div > div.ant-list.equipments-list > div > div > ul > li > a"):
            
            href = i.get_attribute("href")
            print(href)
            main_urls.append(href)

        j += 1

    driver.quit()
    return urls_list

def save_to_csv(items, version='ua'):
    df = pd.DataFrame(items, columns=['Brand', 'Model', 'Year', 'Version', 'Function', 'CAN_A', 'CAN_B', 'CAN_C', 'LIN_A', 'LIN_AB', 'IMO/IMI', 'Comment', 'URL'])
    df = df.drop_duplicates()  # Удаление дубликатов
    df.to_csv(f'data_{version}.csv', mode='a', index=False)


def main():
    driver = webdriver.Firefox(options=options)
    urls = ["https://can.starline.ru/40"]
    brand_links = get_brand_links(urls, driver)
    get_links(brand_links, driver)


def get_url_column_from_csv():
    file_path = "data_us.csv"
    df = pd.read_csv(file_path)
    return df['url'].to_list()


def parse_chunk(chunk):
    for url in chunk:
        parse(url)


if __name__ == "__main__":
    main()
    #parse(main_urls)
    
    chunks = [main_urls[i:i + 20] for i in range(0, len(main_urls), 20)]
         
    with ThreadPoolExecutor(max_workers=20) as executor:
        executor.map(parse, chunks)

"""
    existing_urls = get_url_column_from_csv()    

    while set(existing_urls) - set(main_urls):  # Пока есть URL, которых нет в data_us.csv
         chunks = [main_urls[i:i + 20] for i in range(0, len(main_urls), 20)]
         
         with ThreadPoolExecutor(max_workers=20) as executor:
             executor.map(parse, chunks)
         
         # Обновляем список существующих URL
         existing_urls = get_url_column_from_csv()

"""   