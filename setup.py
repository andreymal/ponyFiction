#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pathlib import Path
from setuptools import setup, find_packages
from ponyFiction import VERSION


with open('README.rst') as readme_file:
    readme = readme_file.read()
with open('HISTORY.rst') as history_file:
    history = history_file.read()
with open('config/requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

package_data = {
    'ponyFiction': [
        filepath for inner_list in [
            [Path(*p.parts[1:]).as_posix() for p in Path('ponyFiction/' + path).glob(pattern) if p.is_file()]
            for path, pattern in [
                ('templates', '**/*'),
                ('static', '**/*'),
                ('frontend', '**/*'),
                ('filters', '**/*.xslt'),
                # Temporary workaround
                ('apis/captcha', '**/*'),
            ]
        ]
        for filepath in inner_list
    ]
}

setup(
    name="ponyFiction",
    version=VERSION,
    description="Fanfiction library for everypony.ru",
    long_description=readme + '\n\n' + history,
    author="Andriy Kushnir (Orhideous)",
    author_email="me@orhideous.name",
    url="https://github.com/RuFimFiction/ponyFiction",
    packages=find_packages(),
    package_data=package_data,
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
