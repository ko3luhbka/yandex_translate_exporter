import os

from bs4 import BeautifulSoup

from source_getter import get_words_from_collection, init_webdriver


SOURCE_FILE = 'page_source.html'
if not os.path.exists(SOURCE_FILE):
    driver = init_webdriver()
    page_source = get_words_from_collection(driver)
    with open(SOURCE_FILE, 'w') as f:
        f.write(page_source)

with open(SOURCE_FILE) as f:
    soup = BeautifulSoup(f, 'html.parser')

res = soup.find_all(class_='record-item')
print(res)
