#!/usr/bin/python
# -*- coding:Utf-8 -*-

from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()


setup(name='pyfmt',
      version='0.1',
      description='automatic code formatter for python following pep8 using baron FST, like gofmt',
      author='Laurent Peuch',
      long_description=read_md("README.md") + "\n\n" + open("CHANGELOG", "r").read(),
      author_email='cortex@worlddomination.be',
      url='https://github.com/Psycojoker/pyfmt',
      install_requires=['baron<0.4,<=0.3'],
      license='gplv3+',
      keywords='pep8 formatting baron fst code fmt gofmt',
      py_modules=['pyfmt'],
      entry_points={
      'console_scripts': [
          'pyfmt = pyfmt:main',
      ]
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Utilities',
      ]
      )
