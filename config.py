import argparse
import os


# Path to Selenium Webdriver
driver_path = os.path.abspath('geckodriver')

# Creds to authenticate using Google
email = ''
password = ''

# Yandex.Translate options
base_url = 'https://translate.yandex.ru/collections'
collection_name = 'my'  # Words collection which must be proceeded
