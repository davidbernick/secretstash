#!/usr/bin/env python

from setuptools import setup

setup(
    name='SecretStash',
    version='0.1',
    description='SecretStash',
    author='David Bernick',
    author_email='dbernick@gmail.com',
    install_requires=[
                      'django',
                      'django-guardian',
                      'boto',
                      'django-social-auth',
                      'django-bootstrap3',
                      'djangorestframework',
                      'drf-compound-fields',
                      'markdown',
                      'django-filter',
                      'south',
                      'django-debug-toolbar',
                      ],
)