from setuptools import setup, find_packages
from os.path import join, dirname

import yandex_word_exporter

setup(
    name='yandex_word_exporter',
    version=yandex_word_exporter.__version__,
    author='ko3luhbka',
    description='Tool for exporting words from Yandex.Translate collections',
    long_description=open(join(dirname(__file__), 'README.md')).read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts':
            ['export_words = yandex_word_exporter.words_getter:main']
    },
    install_requires=[
        'beautifulsoup4==4.8.2',
        'selenium==3.141.0',
    ],
)
