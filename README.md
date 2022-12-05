# Применение threading и multiprocessing для ускорения парсинга с Selenium Webdriver в Python

## Описание
Пример парсинга сайта [coinmarketcap](https://coinmarketcap.com) с использованием ```Selenium Webdriver``` с применением 3 различных подходов:
1. Стандартного синхронного парсина
2. Парсинга с применением потоков и библиотеки ```threading```
3. Парсинга с использованием и библиотеки ```multiprocessing```

## Установка
Установите зависимости командой 
```
pip install -r requirement.txt
```
Также для работы потребуется установленный и сконфигурированный ```Chrome Webdriver```

## Запуск и результаты
В каждом из скриптов есть переменная ```NUM_OF_PAGES``` - желаемое количество страниц для парсинга. Для скрипта ```3_3_coinmarket_multiproc.py``` также задается ```NUM_OF_CORES``` - желаемое количество ядер процессора (здесь имеет смысл указывать количество именно физических ядер). В результате выполнения каждый из скриптов должен вывести время выполнения и отчет в виде CSV файла. CSV файлы многопоточного и многоядерных скриптов выдают неупорядоченные таблицы, что связанно с особенностями работы таких подходов(какие-то потоки/процессы могут спарсить свою выборку со страницы в 100 монет быстрее других и дописать это в итоговый файл).
В итогам были сделаны следующие выводы:
1. Использование потоков и ядер процессора и запуск параллельного/конкурентного исполнения вебдрайвера позволило в рамках моей достаточно древней конфигурации ноута(Intel i5 с 2мя физическими ядрами, 16Gb, SSD)) ускорить время выполнения скрипта от 1.5 до 2.5 раз в зависимости от заданного количества страниц.
2. Использование ```multiprocessing``` наиболее оправдано если на каждом физическом ядре процессора запускается свой ```webdriver```.
3. На моем железе подход с ```multiprocessing``` не дал значительного преимущества в сравнении с ```threading``` (за исключением ситуации когда запускаем количество webdriver = количество физических ядер), а на большом количестве (десятки страниц) скорей всего даже проиграет за счет необходимости постоянного переключения и перезапуска новых процессов на одних и тех же двух ядрах.

P.S Данное сравнение и описание не является исчерпывающим и может содержать неточности в формулировках и результатах. Нахожусь в стадии изучения данных технолигий и буду рад любым советам/корректировкам.