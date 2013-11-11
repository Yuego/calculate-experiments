#!/usr/bin/env python
from setuptools import setup, find_packages
import sys
sys.path.insert(0, '..')

from calculate_next.lib import __version__

setup(
    name='calculate_next',
    version=__version__,
    author='Artem Vlasov',
    author_email='root@proscript.ru',
    url='https://github.com/Yuego/calculate-experiments',
    download_url='https://github.com/Yuego/calculate-experiments/archive/v{0}.tar.gz'.format(__version__),

    description='Calculate Linux experimental Library',
    long_description=open('README.rst').read(),

    license='MIT license',
    install_requires=[
        'pyparsing>=2',
        'six',
    ],
    tests_require=[
        'tox',
    ],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'Development Status :: 1 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
