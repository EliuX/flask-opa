"""
Flask-OPA
-------------

Flask extension that lets you use Open Policy Agent (OPA) in your project
as a client
"""
from setuptools import setup

setup(
    name='Flask-OPA',
    version='0.1',
    url='https://github.com/EliuX/Flask-OPA',
    license='MIT',
    author='Eliecer Hernandez',
    author_email='eliecerhdz@gmail.com',
    description='Flask extension to use OPA as a client',
    long_description=__doc__,
    py_modules=['flask-opa'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
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
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
