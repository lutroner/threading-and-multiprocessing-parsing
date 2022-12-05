import csv
from multiprocessing.pool import Pool
from time import perf_counter, sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

NUM_OF_PAGES = 2  # Задаем количество страниц для парсинга
NUM_OF_CORES = 2  # Задаем количество ядер процессора

# Multiprocessing approach
options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument("--headless=chrome")
options_chrome.add_argument("log-level=3")


def get_data(url: str) -> None:
    """Парсит страницу переданного на вход url. Задержка 0.8 сек
    подобрана экспериментально, чтобы при скролинге страницы успевали
    подгрузиться все данные.

    Args:
        url (str): url страницы coinmarketcap со 100 монетами
    """
    res = []
    with webdriver.Chrome(options=options_chrome) as browser:
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
        with open("file.csv", "a+") as file:
            writer = csv.writer(file)
            writer.writerows(res)


def main() -> None:
    """Основная функция. Здесь задается нужное количество страниц.
    Каждая страница парсится на отдельном ядре, который также создает
    отдельный экземпляр вебрдайвера. Имеет смысл использовать только
    физические ядра.
    """
    urls = [f"https://coinmarketcap.com/?page={i}" for i in range(1, NUM_OF_PAGES + 1)]
    pool = Pool(NUM_OF_CORES)  # задаем количество ядер
    pool.map(get_data, urls)
    pool.close()
    pool.join()


if __name__ == "__main__":
    t1_start = perf_counter()
    main()
    print(f"Время исполнения multiprocessing скрипта: {(perf_counter()-t1_start):.2f}")
