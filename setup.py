#!/usr/bin/env python
"""
Flask-OPA
-------------

Flask extension that lets you use Open Policy Agent (OPA) in your project
as a client
"""
from setuptools import setup, find_packages

__version__ = "1.0.0"


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='Flask-OPA',
    version=__version__,
    url='https://github.com/EliuX/Flask-OPA',
    license='MIT',
    author='Eliecer Hernandez Garbey',
    author_email='eliecerhdz@gmail.com',
    description='Flask extension to use OPA as a client',
    long_description=readme(),
    long_description_content_type="text/markdown",
    py_modules=['flask_opa'],
    zip_safe=False,
    install_requires=[
        'Flask',
        'requests'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration :: Authentication/Directory',
    ],
    project_urls={
        "Bug Tracker": "https://github.com/EliuX/Flask-OPA/issues",
        "Source Code": "https://github.com/EliuX/Flask-OPA",
    }
)
