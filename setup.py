#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from setuptools import setup, find_packages
import os
try:  # for pip >= 10
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError:  # for pip <= 9.0.3
    from pip.req import parse_requirements
    from pip.download import PipSession


requirements = parse_requirements(os.path.join(os.path.dirname(__file__), 'requirements.txt'), session=PipSession())


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='csv2qif',
    version='0.0.1',
    description='Convert CSV from your bank account to QIF file',
    long_description=read("README.md"),
    author='Paweł Walczak',
    author_email='fighter.poul@gmail.com',
    packages=find_packages(exclude=["tests"]),
    entry_points={
        'console_scripts': [
            'csv2qif = csv2qif:main',
        ],
    },
    python_requires='>3.5',
    install_requires=[str(requirement.req) for requirement in requirements],
    license=read("LICENSE")
)


