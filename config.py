import os


# Path to Selenium Webdriver
driver_path = os.path.abspath('geckodriver')

# Credentials to authenticate using Google. May be also specified
# as positional arguments when running words_getter.py
email = ''
password = ''

# Yandex.Translate options
base_url = 'https://translate.yandex.ru/collections'
collection_name = 'my'  # Words collection which must be proceeded
