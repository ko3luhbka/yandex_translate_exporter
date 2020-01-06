import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import config


def init_webdriver():
    options = webdriver.FirefoxOptions()
    options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    # options.add_argument('--headless')
    return webdriver.Firefox(executable_path=config.driver_path)


def _fill_in_and_hit_return(
    driver: webdriver.Firefox,
    elem_name: str,
    field_value: str,
):
    wait = WebDriverWait(driver, 10)
    wait.until(expected_conditions.presence_of_element_located(
        (By.NAME, elem_name)
    ))
    elem = driver.find_element_by_name(elem_name)
    elem.send_keys(field_value)
    elem.send_keys(Keys.RETURN)


def auth_via_google(
    driver: webdriver.Firefox,
    email: str = config.email,
    password: str = config.password
):
    """
    I don't have Yandex account so authenticate using Google account
    """
    wait = WebDriverWait(driver, 10)
    driver.get(config.base_url)
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

    _fill_in_and_hit_return(driver, 'identifier', config.email)
    time.sleep(2)
    _fill_in_and_hit_return(driver, 'password', config.password)

    wait.until(expected_conditions.number_of_windows_to_be(1))
    driver.switch_to.window(original_window)
    time.sleep(5)


def get_words_from_collection(
    driver: webdriver.Firefox,
    collection_name: str = config.collection_name
):
    auth_via_google(driver=driver)
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
