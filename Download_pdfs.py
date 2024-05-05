from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests
import os

options = Options()
options.headless = True  # чтобы браузерный интерфейс не отображался

def download_pdfs(url):
    driver = webdriver.Firefox(options=options)
    driver.get(url)
    links = []

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Извлекаем все теги <option> из элемента с id = "man"
    man_select = soup.find('select', {'id': 'man'})
    if man_select:
        man_options = man_select.find_all('option')
        for option in man_options:
            man = option['value']
            links.append(man)

    driver.quit()
    for link in links[28::]:
        r = requests.get(f"https://install.starline.ru/list.php?man={link}")
        soup1 = BeautifulSoup(r.text, 'html.parser')
        rows = soup1.find_all('tr')

        for row in rows:
            columns = row.find_all('td')
            
            # Проверяем условие: если пятый столбец равен 'S96', извлекаем данные
            if len(columns) >= 5:
                try:
                    brand = columns[0].text.strip()
                    model = columns[1].text.strip()
                    year = columns[2].text.strip()
                    configuration = columns[3].text.strip().replace("Старт-Стоп", "Start-stop").replace("АКПП", "AT").replace("Ключ", "Key").replace("МКПП", "MT")
                    conf = columns[4].text.strip()
                    link = columns[5].find('a')['href']
                    full_link = f"https://install.starline.ru/{link}"
                    
                    # Создаем каталог для сохранения PDF-файлов, если его еще нет
                    directory = f"{brand} {model} {year} {configuration} {conf}"
                    os.makedirs(directory, exist_ok=True)
                    
                    # Скачиваем PDF-файл
                    pdf_file = f"{directory}/{directory}.pdf"
                    with open(pdf_file, 'wb') as f:
                        f.write(requests.get(full_link).content)
                except:
                    continue
                print(f"Скачан PDF-файл: {pdf_file}")

if __name__ == "__main__":
    url = "https://install.starline.ru/"
    download_pdfs(url)
