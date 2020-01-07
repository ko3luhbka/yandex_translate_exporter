import csv
import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

# Path to Selenium Webdriver
DRIVER_PATH = os.path.abspath('geckodriver')
# Credentials to authenticate to Yandex.Translate service
EMAIL = ''
PASSWORD = ''
# File where parsed page is saved to
HTML_SOURCE = 'page_source.html'
# Resulting CSV file
CSV_FILE = 'word_trans.csv'
# Yandex.Translate options
BASE_URL = 'https://translate.yandex.ru/collections'
COLLECTION_NAME = 'my'  # Words collection which must be proceeded


def init_webdriver():
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    return webdriver.Firefox(executable_path=DRIVER_PATH)


def _fill_in_and_hit_return(
    driver,
    elem_name,
    field_value,
):
    wait = WebDriverWait(driver, 10)
    wait.until(expected_conditions.presence_of_element_located(
        (By.NAME, elem_name)
    ))
    elem = driver.find_element_by_name(elem_name)
    elem.send_keys(field_value)
    elem.send_keys(Keys.RETURN)


def auth_with_google(
    driver,
    email=EMAIL,
    password=PASSWORD
):
    """
    I don't have Yandex account so authenticate with Google
    """
    wait = WebDriverWait(driver, 10)
    driver.get(BASE_URL)
    driver.find_element_by_class_name('button_enter').click()
    wait.until(expected_conditions.element_to_be_clickable(
        (By.CLASS_NAME, 'passp-social-block__list-item-gg')
    ))
    original_window = driver.current_window_handle
    assert len(driver.window_handles) == 1
    driver.find_element_by_class_name('passp-social-block__list-item-gg').click()
    wait.until(expected_conditions.number_of_windows_to_be(2))

    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    _fill_in_and_hit_return(driver, 'identifier', email)
    time.sleep(2)
    _fill_in_and_hit_return(driver, 'password', password)

    wait.until(expected_conditions.number_of_windows_to_be(1))
    driver.switch_to.window(original_window)
    time.sleep(5)


def get_html_source(
    driver,
    collection_name=COLLECTION_NAME
):
    """
    Load page with user defined words collections and get its source code
    """
    auth_with_google(driver=driver)
    users_collections = driver.find_element_by_id('collectionListContent')
    collections = users_collections.find_element_by_tag_name('ul')
    for coll in collections.find_elements_by_tag_name('li'):
        coll = coll.find_element_by_class_name('collection-name')
        coll_name = coll.find_element_by_class_name('collection-title')
        if coll_name.text == collection_name:
            print('Collection "{0}" found!'.format(collection_name))
            coll_name.click()
    time.sleep(2)
    source = driver.page_source
    driver.close()
    return source


def parse_html(html_file):
    """
    Walk through HTML source code building dict {word: translation} and
    adding it to list for further CSV converting
    """
    with open(html_file) as f:
        soup = BeautifulSoup(f, 'html.parser')
    word_trans_list = []
    for item in soup.find_all(class_='record-item'):
        word = item.find(class_='record-item_text')
        translation = item.find(class_='record-item_translation')
        if word:
            word_str = word.find('div', attrs={'dir': 'ltr'}).string
        if translation:
            trans_str = translation.find('div', attrs={'dir': 'ltr'}).string
        word_trans_list.append(
            {
                'word': word_str.strip(),
                'translation': trans_str.strip()
            }
        )
    return word_trans_list


def convert_dict_to_csv(words_dict, csv_file=CSV_FILE):
    """
    Convert {word: translation} dictionary to CSV
    """
    if os.path.exists(csv_file):
        print('CSV file is already exist, exiting')
        return
    with open(csv_file, 'w') as f:
        fieldnames = ['word', 'translation']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in words_dict:
            writer.writerow(item)


def main(html_source=HTML_SOURCE):
    if not all([EMAIL, PASSWORD]):
        raise ValueError('Email and password should not be empty!')
    if os.path.exists(html_source):
        print('HTML file is already exist, skipping page scrapping')
    else:
        driver = init_webdriver()
        page_source = get_html_source(driver)
        with open(html_source, 'w') as f:
            f.write(page_source)

    source_parsed = parse_html(html_source)
    convert_dict_to_csv(source_parsed)


if __name__ == '__main__':
    main()
