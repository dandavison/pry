import os

from setuptools import setup, find_packages

setup(
    name='pry',
    packages=find_packages(),
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'pry = pry:main',
        ],
    },
)
