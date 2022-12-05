import csv
import threading
from time import perf_counter, sleep

from selenium import webdriver
from selenium.webdriver.common.by import By

NUM_OF_PAGES = 2  # Задаем количество страниц для парсинга

# Multithread approach
options_chrome = webdriver.ChromeOptions()
options_chrome.add_argument("--headless=chrome")
options_chrome.add_argument("log-level=3")


def write_csv(data: list[list]) -> None:
    """Зпись данных в CSV файл.

    Args:
        data (list[list]): список списков с одной страницы
    """
    with open("file.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerows(data)


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
        write_csv(res)


def main() -> None:
    """Основная функция. Здесь задается нужное количество страниц.
    Каждая страница парсится в отдельном потоке, который также создает
    отдельный экземпляр вебрдайвера.
    """
    threads = []
    urls = [f"https://coinmarketcap.com/?page={i}" for _ in range(1, NUM_OF_PAGES + 1)]
    for i, url in enumerate(urls, 1):
        t = threading.Thread(target=get_data, args=(url,))
        print(f"Парсинг страницы {url} в потоке Thread {i}...")
        t.start()
        threads.append(t)
    for t in threads:
        t.join()


if __name__ == "__main__":
    t1_start = perf_counter()
    main()
    print(f"Исполнение многопоточного скрипта: {(perf_counter()-t1_start):.2f} сек.")
