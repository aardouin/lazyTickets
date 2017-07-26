#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

import lazytickets

setup(
    name='lazytickets',

    version=lazytickets.__version__,

    packages=find_packages(),

    author='Alexis Ardouin',

    description='A lazy tool to generate scrum tickets',

    include_package_data=True,

    install_requires=['Pillow'],

    url='https://github.com/aardouin/lazyTickets',

    classifiers=[
        'Programming Language :: Python',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6.2'
    ],

    entry_points={
        'console_scripts': [
            'lazytickets = lazytickets.main:main',
        ],
    }
)