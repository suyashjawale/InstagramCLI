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
    description="CLI Tool made by reverse engineering Instagram API Calls.",
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
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: '
        'Libraries :: Python Modules',
        'Operating System :: Microsoft :: Windows'
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'bs4'
    ]
)
