#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os


root = os.path.dirname(__file__)
sphinx_root = open(os.path.join(root, 'sphinxroot.txt'), 'rb').read().strip().decode('utf-8')

ENV = os.getenv('DJANGO_ENV') or open(os.path.join(root, 'environment.txt'), 'rb').read().decode('utf-8').strip()


if ENV in ('test', 'development', 'staging', 'production'):
    path = os.path.join(root, 'ponyFiction', 'environments', ENV + '_sphinx.conf')
    if os.path.isfile(path):
        print(open(path, 'rb').read().decode('utf-8').replace('%SPHINXROOT%', sphinx_root))


local_path = os.path.join(root, 'ponyFiction', 'environments', 'local_sphinx.conf')

if os.path.isfile(local_path):
    print(open(local_path, 'rb').read().decode('utf-8').replace('%SPHINXROOT%', sphinx_root))

print(open(os.path.join(root, 'sphinx.conf'), 'rb').read().decode('utf-8').replace('%SPHINXROOT%', sphinx_root))
