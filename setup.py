#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['wagtailfontawesome']

setup_requirements = []

test_requirements = []

setup(
    author="Marco Westerhof",
    author_email='m.westerhof@lukkien.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Easily manage 404s from the wagtail admin",
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='wagtail_managed404',
    name='wagtail_managed404',
    packages=find_packages(include=['wagtail_managed404']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mwesterhof/wagtail_managed404',
    version='0.1.1',
    zip_safe=False,
)
