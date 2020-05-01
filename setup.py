#!/usr/bin/env python
import os
from setuptools import setup, find_packages

PATH = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(PATH, 'README.md')) as fp:
    DESC = fp.read()


setup(
    name='django-inlineedit',
    version='1.1',
    description='Add inline editble fields to your templates',
    long_description=DESC,
    keywords='django, forms, editing',
    author='Pedro Tavares',
    author_email='web@ptavares.com',
    url='https://github.com/ptav/django-inlineedit',
    license='LICENSE',

    packages=find_packages(),
    include_package_data=True,
    
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],

    install_requires=[
        'django'
    ],
    
    zip_safe=False
)
