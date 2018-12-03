import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

#allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))
# Utility function to read the README file.
# string in below ...
setup(
    name="django-nathmankindscrumy",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    license="BSD License", #example license
    description='A simple Django App',
    long_description=README,
    url='https://www.nathmankindscrumy.com',
    author="Makinde Nathaniel",
    author_email="nathmankind@gmail.com",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.6',
        'Intended Audience :: Developers',
        "License :: OSI Independent :: BSD License",
        'Operating System :: OS Independent',
        'Programming Language :: Pyhton :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)