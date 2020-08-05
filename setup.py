#!/usr/bin/python

from setuptools import setup, find_packages

setup(
    name='wild',
    version='1.0.1',
    description='Wildebeest CLI for Data Catalog at https://www.n3ncloud.co.kr',
    long_description=
    ('Official CLI for Wildebeest for N3NCLOUD, accessible using a command line tool implemented in Python 3.\n\n'
      'Wildbeest is a CKAN-based solution for building data portals that share public data by DCAT standards.'
      'Wildbeest provides the most efficient disclosure of registered datasets and standard protocols for sharing data with other data catalog systems. Wildbeest uses the most compatible standard format and is the best solution for global data sharing. You can get more information on the Wildebeest Documents(http://d3.n3ncloud.co.kr/wildebeest/1.0) and N3NCLOUD(https://www.n3ncloud.co.kr/).'),
    author='N3NCLOUD',
    author_email='mgkim@n3ncloud.co.kr',
    url='https://github.com/n3nc/wild-cli',
    download_url = 'https://github.com/n3nc/wild-cli/archive/v_10.tar.gz',
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
    'License :: OSI Approved :: Apache Software License',  
    'Environment :: Console',
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ])