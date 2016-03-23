#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from os.path import dirname, join
from setuptools import setup, find_packages
from ponyFiction import VERSION


def read(*args):
    return open(join(dirname(__file__), *args), encoding="utf-8").read()

readme = read("README.md")
requirements = read("config", "requirements.txt").splitlines(),

setup(
    name="ponyFiction",
    version=VERSION,
    description="Fanfiction library for everypony.ru",
    long_description=readme,
    author="Andriy Kushnir (Orhideous)",
    author_email="me@orhideous.name",
    url="https://github.com/RuFimFiction/ponyFiction",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license="GPLv3",
    zip_safe=False,
    keywords=["stories", "library", "fanfiction"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: No Input/Output (Daemon)",
        "Framework :: Django",
        "Framework :: Django :: 1.8",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Russian",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Utilities",
    ]
)
