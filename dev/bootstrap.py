from os.path import join, dirname, abspath


DEV_DIR = dirname(abspath(__file__))
print DEV_DIR

with open(join(dirname(DEV_DIR), 'local_settings.py'), 'w') as f:
    f.write('from ponyFiction.dev_settings import *\n')
    f.write('import sys\n')
    f.write('sys.path.append(%r)\n' % DEV_DIR)