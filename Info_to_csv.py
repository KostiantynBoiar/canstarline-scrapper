from selenium import webdriver
from selenium.webdriver.firefox.service import Service
import pdfkit
from selenium.webdriver.firefox.options import Options
import os
import pdfkit
from selenium.webdriver.common.by import By
import time
import requests
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import threading
import json

options = Options()
options.add_argument("--headless")
main_urls = []
lock = threading.Lock()

replace_ru_dict = {}
replace_us_dict = {}

with open("replace_words_ru.json", 'r', encoding='utf-8') as f:
    replace_ru_dict = json.load(f)
    print(replace_ru_dict)
f.close()


with open("replace_words_us.json", 'r', encoding='utf-8') as f:
    replace_us_dict = json.load(f)
    print(replace_us_dict)
f.close()

def parse(urls):
    print(urls)

    try:
        driver = webdriver.Firefox(options=options)
        for url in urls:

            buffer_name = ''
            buffer_can_a = ''
            buffer_can_b = ''
            buffer_can_c = ''
            buffer_can_lin_a = ''
            buffer_can_lin_ab = ''
            buffer_can_imoimi = ''
            results = []
            
            #if url in get_url_column_from_csv():
            #    continue

            print(f'{url} not in CSV')
            driver.get(url)
            time.sleep(2.5)
            driver.execute_script("document.cookie = '_language=en';")

        # Refresh the page
            driver.refresh()
            time.sleep(1)

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
                firmware = driver.find_element(By.CSS_SELECTOR, "#root > section > main > section > div > div.ant-row > div > div > div > div > div > div > div > div > span.ant-select-selection-item").text
                j = 0
                for rows in driver.find_elements(By.CSS_SELECTOR, "div > div.functions-tables > div:nth-child(1) > div > div > div > div > div > div > table > tbody > tr"):
                    

                    name = rows.find_element(By.CSS_SELECTOR, "div > div.functions-tables > div:nth-child(1) > div > div > div > div > div > div > table > tbody > tr > td:nth-child(1)").text
                    try:
                        name_gazer_ru = name.replace(name, replace_ru_dict[name])
                    except:
                        name_gazer_ru = ''
                    try:
                        name_gazer_us = name.replace(name, replace_us_dict[name])
                    except:
                        name_gazer_us = ''

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
                        #row = brand, model, year, version, buffer_name, buffer_can_a, buffer_can_b, buffer_can_c, buffer_can_lin_a, buffer_can_lin_ab, buffer_can_imoimi, comment, url
                        row = '', '', '', '', '', '', '', '', '', '', '', '', '',  comment, ''

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

                        if j == 0:
                            row = firmware, brand, model, year, version, name, name_gazer_ru, name_gazer_us, CAN_A, CAN_B, CAN_C, LIN_A, LIN_AB, IMO_IMI, comment, url
                            results.append(row)
                            print(row)
                        else:
                            row = firmware, brand, model, year, version, name, name_gazer_ru, name_gazer_us, CAN_A, CAN_B, CAN_C, LIN_A, LIN_AB, IMO_IMI, comment, url
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
                        row = firmware, brand, model, year, version, f'Button: {item}', '', CAN_A, CAN_B, CAN_C, LIN_A, LIN_AB, IMO_IMI, comment, url

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

def save_to_csv(items, version='us'):
    df = pd.DataFrame(items, columns=['Firmware','Brand', 'Model', 'Year', 'Version', 'Function', 'Function Ru', 'Function Us', 'CAN_A', 'CAN_B', 'CAN_C', 'LIN_A', 'LIN_AB', 'IMO/IMI', 'Comment', 'URL'])
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
    count_of_threads = 1
    chunks = [main_urls[i:i + count_of_threads] for i in range(0, len(main_urls), count_of_threads)]
         
    with ThreadPoolExecutor(max_workers=count_of_threads) as executor:
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