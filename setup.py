#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

VERSION = '0.3.3'

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = ['chattool>=2.6.1', "python-dotenv>=0.17.0"]

test_requirements = ['pytest>=3']

setup(
    author="Rex Wang",
    author_email='1073853456@qq.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="Interact with ChatGPT in terminal via chattool",
    install_requires=requirements,
    license="MIT license",
    # long_description=readme + '\n\n' + history ,
    include_package_data=True,
    keywords='askchat',
    name='askchat',
    packages=find_packages(include=['askchat', 'askchat.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/rexwzh/askchat',
    version=VERSION,
    zip_safe=False,
)
