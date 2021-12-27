import subprocess
from setuptools import setup
import os

push_version = (
    subprocess.run(["git", "describe", "--tags"], stdout=subprocess.PIPE)
    .stdout.decode("utf-8")
    .strip()
)

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='InstagramCLI',
    version=push_version,
    description="InstagramCLI is the most advanced scraping library made by reverse-engineering the Instagram API calls which has low latency.",
    author= 'Suyash Jawale',
    url = 'https://github.com/suyashjawale/InstagramCLI',
    author_email='suyashjawale245@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["InstagramCLI"],
    keywords=['instagram', 'instagramapi', 'instagramcli','api','instagram scraper','bot'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: '
        'Libraries :: Python Modules',
        'Operating System :: Microsoft :: Windows'
    ],
    python_requires='>=3.6',
    install_requires=[
'async-generator',
'attrs',
'blinker',
'Brotli',
'certifi',
'cffi',
'charset-normalizer',
'chromedriver-autoinstaller',
'cryptography',
'h11',
'h2',
'hpack',
'hyperframe',
'idna',
'kaitaistruct',
'outcome',
'pyasn1',
'pycparser',
'pydivert',
'pyOpenSSL',
'pyparsing',
'PySocks',
'requests',
'selenium',
'selenium-wire',
'six',
'sniffio',
'sortedcontainers',
'trio',
'trio-websocket',
'urllib3',
'wsproto',
'zstandard'
    ]
)