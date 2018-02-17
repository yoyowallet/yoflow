#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='yoflow',
    version='1.0.0',
    author='Gary Evans',
    author_email='gary@yoyowallet.com',
    description='Django workflows',
    long_description=open('README.md').read(),
    platforms=['Any'],
    keywords=['workflow', 'django', 'yoflow'],
    url='http://github.com/yoyowallet/yoflow',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'Django>=1.8'
    ],
    packages=[
        'yoflow'
    ],
    include_package_data=True,
    zip_safe=False,
)