#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='csv2qif',
    version='0.0.1',
    description='Convert CSV exported from your bank account to QIF file',
    long_description=read("README.md"),
    author='Paweł Walczak',
    author_email='fighter.poul@gmail.com',
    packages=find_packages(exclude=["tests"]),
    entry_points={
        'console_scripts': [
            'csv2qif = csv2qif:main',
            'csv2qif-plugins = csv2qif:plugins',
        ],
    },
    python_requires='>3.5',
    license=read("LICENSE")
)


