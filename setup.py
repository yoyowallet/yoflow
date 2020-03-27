#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(
    name='yoflow',
    version='1.0.0',
    author='Gary Evans',
    author_email='dev@yoyowallet.com',
    description='Django workflows',
    long_description=long_description,
    long_description_content_type="text/markdown",
    platforms=['Any'],
    keywords=['django', 'yoflow', 'workflow'],
    url='http://github.com/yoyowallet/yoflow',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3',
        'Framework :: Django :: 3.2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'Django>=2.2'
    ],
    packages=[
        'yoflow'
    ],
    setup_requires=[
        'setuptools>=38.6.0'
    ],
    include_package_data=True,
    zip_safe=False,
)
