#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='wild',
    version='0.0.1',
    description='Wildebeest API',
    long_description=
    ('Official API for https://d3.n3ncloud.co.kr, accessible using a command line '
     'tool implemented in Python. Beta release - N3NCloud reserves the right to '
     'modify the API functionality currently offered.'),
    author='N3NCloud',
    author_email='admin@n3ncloud.co.kr',
    url='https://github.com/n3nc/wildebeest-api',
    keywords=['Wildebeest', 'wild', 'API'],
    entry_points={'console_scripts': ['wild = wb.cli:main']},
    test_suite='wb.cli.main',
    install_requires=[
        # Restriction that urllib3's version is less than 1.25 needed to avoid
        # requests dependency problem.
        'urllib3 >= 1.21.1, < 1.25',
        'requests'
    ],
    packages=find_packages(),
    license='Apache 2.0')