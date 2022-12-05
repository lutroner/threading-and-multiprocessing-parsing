import csv
from time import perf_counter, sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

NUM_OF_PAGES = 2  # Задаем количество страниц для парсинга

options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument("--headless=chrome")
options_chrome.add_argument("log-level=3")


def write_csv(data: list) -> None:
    with open("file.csv", "w") as file:
        print("Создаю CSV файл..")
        writer = csv.writer(file)
        writer.writerows(data)


def get_page_data(url) -> list[list]:
    """Парсит страницу переданного на вход url. Задержка 0.8 сек
    подобрана экспериментально, чтобы при скролинге страницы успевали
    подгрузиться все данные.

    Args:
        url (str): url страницы coinmarketcap со 100 монетами
    """
    res = []
    with webdriver.Chrome(chrome_options=options_chrome) as browser:
        browser.get(url)
        for _ in range(9):  # Скролим страницу вниз для загрузки всех данных
            browser.execute_script("window.scrollBy(0,1000)")
            sleep(0.8)
        trs = browser.find_element(By.TAG_NAME, "tbody").find_elements(
            By.TAG_NAME, "tr"
        )
        for tr in trs:
            tds = tr.find_elements(By.TAG_NAME, "td")[1:]
            res.append([el.text.strip() for el in tds if el])
        return res


def main() -> None:
    """Основная функция. Здесь задается нужное количество страниц.
    Парсинг страниц последовательный.
    """
    res = []
    for i in range(1, NUM_OF_PAGES + 1):
        url = f"https://coinmarketcap.com/?page={i}"
        print(f"Парсинг страницы {url}...")
        lst = get_page_data(url)
        res.extend(lst)
    write_csv(res)


if __name__ == "__main__":
    t1_start = perf_counter()
    main()
    print(f"Исполнение синхронного скрипта: {perf_counter()-t1_start:.2f} сек.")
