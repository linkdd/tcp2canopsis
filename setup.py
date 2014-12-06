#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='tcp2canopsis',
    version='0.1',
    license='MIT',

    author='David Delassus',
    author_email='david.jose.delassus@gmail.com',
    description='Canopsis Connector which listen for JSON events on TCP port',
    url='https://github.com/linkdd/tcp2canopsis',
    download_url='https://github.com/linkdd/tcp2canopsis/tarball/0.1',
    keywords=['canopsis'],
    classifiers=[],

    scripts=['scripts/tcp2canopsis'],
    packages=find_packages(),
    install_requires=[
        'kombu',
        'Twisted'
    ]
)