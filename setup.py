#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='wild',
    packages = ['wild'],
    version='0.1.0',
    description='Wildebeest CLI',
    long_description=
    ('Official CLI for Wildebeest, accessible using a command line '
     'tool implemented in Python.'),
    author='N3NCLOUD',
    author_email='mgkim@n3ncloud.co.kr',
    url='https://github.com/n3nc/wild-cli',
    download_url = 'https://github.com/n3nc/wild-cli',
    keywords=['Wildebeest', 'wild', 'API', 'CLI', 'N3NCLOUD'],
    entry_points={'console_scripts': ['wild = wb.cli:main']},
    install_requires=[
        # Restriction that urllib3's version is less than 1.25 needed to avoid
        # requests dependency problem.
        'urllib3 >= 1.21.1, < 1.25',
        'requests'
    ],
    packages=find_packages(),
    license='Apache 2.0',
    classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'License :: OSI Approved :: Apache 2.0 License',  
    'Environment :: Console',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ])