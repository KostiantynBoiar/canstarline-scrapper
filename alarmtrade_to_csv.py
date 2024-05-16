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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


options = Options()
options.add_argument("--headless")



def parse(driver, brands_count):
    
    items = []

    try:

        for brand_iter in range(1, brands_count):
            
            time.sleep(2)
            element_to_hover_over = driver.find_element(By.CSS_SELECTOR, "#select_brand")
            actions = ActionChains(driver)
            actions.move_to_element(element_to_hover_over).perform()
            element_to_click = driver.find_element(By.CSS_SELECTOR, f"#select_brand > option:nth-child({brand_iter})")
            element_to_click.click()
            time.sleep(0.5)
            brand = driver.find_element(By.CSS_SELECTOR, f"#select_brand > option:nth-child({brand_iter})").text
            
            models_count = get_model(driver)
            

            for model_iter in range(1, models_count):
                
                firmware_count = get_firmware(driver)
                time.sleep(2)
                element_to_hover_over = driver.find_element(By.CSS_SELECTOR, "#select_model")
                actions = ActionChains(driver)
                actions.move_to_element(element_to_hover_over).perform()
                element_to_click = driver.find_element(By.CSS_SELECTOR, f"#select_model > option:nth-child({model_iter})")
                element_to_click.click()
                time.sleep(1.5)
                model = driver.find_element(By.CSS_SELECTOR, f"#select_model > option:nth-child({model_iter})").text
                
                try:
                    for firmware_iter in range(1, firmware_count + 1):
                        
                        time.sleep(2)
                        element_to_hover_over = driver.find_element(By.CSS_SELECTOR, "#select_car")
                        actions = ActionChains(driver)
                        actions.move_to_element(element_to_hover_over).perform()
                        element_to_click = driver.find_element(By.CSS_SELECTOR, f"#select_car > option:nth-child({firmware_iter})")
                        element_to_click.click()
                        time.sleep(1.5)
                        firmware = driver.find_element(By.CSS_SELECTOR, f"#select_car > option:nth-child({firmware_iter})").text

                        tr_count_table_1 = driver.find_elements(By.CSS_SELECTOR, "#car_info > table:nth-child(1) > tbody > tr")
                        tr_count_table_2 = driver.find_elements(By.CSS_SELECTOR, "#car_info > table:nth-child(2) > tbody > tr")
                        tr_count_table_3 = driver.find_elements(By.CSS_SELECTOR, "#car_info > table:nth-child(3) > tbody > tr")
                        tr_table_1_counter = 0
                        tr_table_2_counter = 0
                        tr_table_3_counter = 0
                        tr_table_4_counter = 0

                        
                        tr_count_table_4 = driver.find_elements(By.CSS_SELECTOR, "#car_info > table:nth-child(4) > tbody > tr")
                            
                        for tr_table_4 in tr_count_table_4:
                            tr_table_4_counter += 1




                        for tr_table_2 in tr_count_table_2:
                            tr_table_2_counter += 1
                        
                        for tr_table_1 in tr_count_table_1:
                            tr_table_1_counter += 1

                        for tr_table_3 in tr_count_table_3:
                            tr_table_3_counter += 1


                        for i in range(1, tr_table_1_counter):
                            option = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(1) > tbody > tr:nth-child({i}) > td:nth-child(1)").text
                            info = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(1) > tbody > tr:nth-child({i}) > td:nth-child(2)").text
                            row = brand, model, firmware, option, '', '', '', '', '', '', '', '', info
                            print(row)
                            items.append(row)

                        for i in range(3, tr_table_2_counter):
                            
                            
                            option = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(2) > tbody > tr:nth-child({i}) > td:nth-child(1)").text

                            try:
                                exe_can_1 = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(2) > tbody > tr:nth-child({i}) > td:nth-child(2) > i")
                                exe_can_1 = '+'
                            except:
                                exe_can_1 = '-'

                            try:
                                exe_can_2 = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(2) > tbody > tr:nth-child({i}) > td:nth-child(3) > i")
                                exe_can_2 = '+'
                            except:
                                exe_can_2 = '-'

                            try:
                                exe_can_3 = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(2) > tbody > tr:nth-child({i}) > td:nth-child(4) > i")
                                exe_can_3 = '+'
                            except:
                                exe_can_3 = '-'

                            try:
                                exe_lin = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(2) > tbody > tr:nth-child({i}) > td:nth-child(5) > i")
                                exe_lin = '+'
                            except:
                                exe_lin = '-'


                            try:
                                read_can_1 = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(2) > tbody > tr:nth-child({i}) > td:nth-child(6) > i")
                                read_can_1 = '+'
                            except:
                                read_can_1 = '-'

                            try:
                                read_can_2 = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(2) > tbody > tr:nth-child({i}) > td:nth-child(7) > i")
                                read_can_2 = '+'
                            except:
                                read_can_2 = '-'

                            try:
                                read_can_3 = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(2) > tbody > tr:nth-child({i}) > td:nth-child(8) > i")
                                read_can_3 = '+'
                            except:
                                read_can_3 = '-'

                            try:
                                read_lin = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(2) > tbody > tr:nth-child({i}) > td:nth-child(9) > i")
                                read_lin = '+'
                            except:
                                read_lin = '-'

                            try:
                                explanation = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(2) > tbody > tr:nth-child({i}) > td:nth-child(10)").text
                            except:
                                explanation = '-'
                            
                            row = brand, model, firmware, option, exe_can_1, exe_can_2, exe_can_3, exe_lin, read_can_1, read_can_2, read_can_3, read_lin, explanation
                            items.append(row)
                            print(row)

                        
                        for i in range(4, tr_table_2_counter):
                            
                            try:
                                option = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(3) > tbody > tr:nth-child({i}) > td:nth-child(1)").text
                            except:
                                continue
                            try:
                                exe_can_1 = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(3) > tbody > tr:nth-child({i}) > td:nth-child(2) > i")
                                exe_can_1 = '+'
                            except:
                                exe_can_1 = '-'

                            try:
                                exe_can_2 = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(3) > tbody > tr:nth-child({i}) > td:nth-child(3) > i")
                                exe_can_2 = '+'
                            except:
                                exe_can_2 = '-'

                            try:
                                exe_can_3 = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(3) > tbody > tr:nth-child({i}) > td:nth-child(4) > i")
                                exe_can_3 = '+'
                            except:
                                exe_can_3 = '-'

                            try:
                                exe_lin = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(3) > tbody > tr:nth-child({i}) > td:nth-child(5) > i")
                                exe_lin = '+'
                            except:
                                exe_lin = '-'


                            try:
                                read_can_1 = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(3) > tbody > tr:nth-child({i}) > td:nth-child(6) > i")
                                read_can_1 = '+'
                            except:
                                read_can_1 = '-'

                            try:
                                read_can_2 = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(3) > tbody > tr:nth-child({i}) > td:nth-child(7) > i")
                                read_can_2 = '+'
                            except:
                                read_can_2 = '-'

                            try:
                                read_can_3 = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(3) > tbody > tr:nth-child({i}) > td:nth-child(8) > i")
                                read_can_3 = '+'
                            except:
                                read_can_3 = '-'

                            try:
                                read_lin = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(3) > tbody > tr:nth-child({i}) > td:nth-child(9) > i")
                                read_lin = '+'
                            except:
                                read_lin = '-'

                            try:
                                explanation = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(3) > tbody > tr:nth-child({i}) > td:nth-child(10)").text
                            except:
                                explanation = '-'
                            
                            row = brand, model, firmware, option, exe_can_1, exe_can_2, exe_can_3, exe_lin, read_can_1, read_can_2, read_can_3, read_lin, explanation
                            items.append(row)
                            print(row)

                        try:
                            for i in range(1, tr_table_4_counter + 1):
                                option = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(4) > tbody > tr:nth-child({i}) > td:nth-child(1)").text
                                info = driver.find_element(By.CSS_SELECTOR, f"#car_info > table:nth-child(4) > tbody > tr:nth-child({i}) > td:nth-child(2)").text
                                row = brand, model, firmware, option, '', '', '', '', '', '', '', '', info
                                print(row)
                                items.append(row)
                        except:
                                print("No 4th table on the page")
                                continue
                except:
                    continue
                

    except Exception as e:
        save_to_csv(items)
        print(e)
    
    finally:
        save_to_csv(items)        
        driver.quit()


def save_to_csv(items, version='us'):
    df = pd.DataFrame(items, columns=['brand', 'model', 'firmware', 'option', 'exe_can_1', 'exe_can_2', 'exe_can_3', 'exe_lin', 'read_can_1', 'read_can_2', 'read_can_3', 'read_lin', 'explanation'])
    df = df.drop_duplicates()  # Удаление дубликатов
    df.to_csv(f'data_alarmtrade_{version}.csv', mode='a', index=False)


def get_brands(driver, url):
    
    driver.get(url)

    count = 0

    brands = driver.find_elements(By.CSS_SELECTOR, "#select_brand > option")
    for brand in brands:
        count += 1
    
    print(f'Count of brands: {count}')
    return count


def get_model(driver):

    count = 0

    brands = driver.find_elements(By.CSS_SELECTOR, "#select_model > option")
    for brand in brands:
        count += 1
    
    print(f'Count of models: {count}')
    return count

def get_firmware(driver):
    count = 0

    brands = driver.find_elements(By.CSS_SELECTOR, "#select_car > option")
    for brand in brands:
        count += 1
    
    print(f'Count of firmwares: {count}')
    return count

def main(url = "https://loader.alarmtrade.ru/"):
    
    driver = webdriver.Firefox(options=options)
    brands_count = get_brands(driver, url)
    parse(driver, brands_count)

if __name__ == '__main__':
    main()