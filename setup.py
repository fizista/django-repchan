#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import codecs
import platform
from pkg_resources import parse_version

try:
    from setuptools import setup, find_packages, Command
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages, Command

import repchan as distmeta

if os.path.exists("README.md"):
    long_description = codecs.open("README.md", "r", "utf-8").read()
else:
    long_description = ""


VERSION_STATUS = {
    'pl':'Development Status :: 1 - Planning',
    'pa':'Development Status :: 2 - Pre-Alpha',
    'a':'Development Status :: 3 - Alpha',
    'b':'Development Status :: 4 - Beta'}

try:
    version_status = VERSION_STATUS[parse_version(distmeta.__version__)[2][1:]]
except:
    version_status = 'Development Status :: 5 - Production/Stable'

setup(
    name='repchan',
    version=distmeta.__version__,
    packages=find_packages(exclude=['ez_setup', ]),
    scripts=[],

    install_requires=[
        "django>=1.4.0",
    ],

    package_data={
        '': ['*.txt', '*.rst'],
    },

    platforms=["any"],

    author=distmeta.__author__,
    author_email=distmeta.__contact__,
    description=distmeta.__doc__,
    license="BSD",
    keywords="django version control models",
    url=distmeta.__homepage__,

    zip_safe=False, # test it

    classifiers=[
        version_status,
        "Framework :: Django",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        #"Programming Language :: Python :: 2.5",
        #"Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: POSIX",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={},
    long_description=long_description,
)
