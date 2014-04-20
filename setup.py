#!/usr/bin/python
# -*- coding:Utf-8 -*-

from setuptools import setup


setup(name='pyfmt',
      version='0.1',
      description='automatic code formatter for python following pep8 using baron FST, like gofmt',
      author='Laurent Peuch',
      #long_description='',
      author_email='cortex@worlddomination.be',
      url='https://github.com/Psycojoker/pyfmt',
      install_requires=['baron'],
      license= 'gplv3+',
      keywords='pep8 formatting baron fst code',
      py_modules=['pyfmt'],
      entry_points={
        'console_scripts': [
            'pyfmt = pyfmt:main',
        ]
      }
     )
