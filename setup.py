# -*- coding: utf-8 -*-
import os
from setuptools import setup


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except:
        return ''


setup(
    name='celery-api',
    version='0.1',
    py_modules=['celery_api'],
    url='https://github.com/imankulov/celery-api',
    license='BSD',
    author='Roman Imankulov',
    author_email='roman.imankulov@gmail.com',
    description='Celery API discovery module',
    long_description=read('README.rst'),
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ),
    install_requires=[
        'celery>=3.0',
    ],
)
