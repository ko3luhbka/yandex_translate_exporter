import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


DRIVER_PATH = os.path.abspath('geckodriver')
BASE_URL = 'https://translate.yandex.ru/collections'

EMAIL = 'ko3luhbka@gmail.com'
PASSWORD = 'Eeepc1215b'

options = webdriver.FirefoxOptions()
options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# options.add_argument('--headless')

driver = webdriver.Firefox(executable_path=DRIVER_PATH)
wait = WebDriverWait(driver, 10)


def get_words_from_collection(name):
    users_collections = driver.find_element_by_id('collectionListContent')
    collections = users_collections.find_element_by_tag_name('ul')
    for coll in collections.find_elements_by_tag_name('li'):
        coll = coll.find_element_by_class_name('collection-name')
        coll_name = coll.find_element_by_class_name('collection-title')
        if coll_name.text == name:
            print('collection found!')
            coll_name.click()
    time.sleep(2)
    return driver.page_source


def _fill_in_and_hit_return(elem_name, field_value):
    wait.until(expected_conditions.presence_of_element_located((By.NAME, elem_name)))
    elem = driver.find_element_by_name(elem_name)
    elem.send_keys(field_value)
    elem.send_keys(Keys.RETURN)


def auth_via_google(email=EMAIL, password=PASSWORD):
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

    _fill_in_and_hit_return('identifier', EMAIL)
    time.sleep(2)
    _fill_in_and_hit_return('password', PASSWORD)

    wait.until(expected_conditions.number_of_windows_to_be(1))
    driver.switch_to.window(original_window)
    time.sleep(5)


auth_via_google()
time.sleep(3)
page_source = get_words_from_collection('my')
driver.close()
