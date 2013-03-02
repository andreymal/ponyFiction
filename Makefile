APP = ponyFiction
SETTINGS = settings
PWD = $(shell pwd)
MANAGESCRIPT = django-admin.py
MANAGE = PYTHONPATH=$(PWD):$(PWD)/$(APP) DJANGO_SETTINGS_MODULE=$(APP).$(SETTINGS) $(MANAGESCRIPT)

all :
	true

run:
	$(MANAGE) runserver

install-db:
	$(MANAGE) syncdb --noinput --migrate

syncdb:
	$(MANAGE) syncdb --noinput

pylint:
	pylint --output-format=colorized --rcfile=pylint.ini \
		ponyFiction \
		*.py 2>&1 | less -SR

pylint-int :
	pylint --output-format=colorized --rcfile=pylint.ini \
		ponyFiction \
		*.py \
		--int-import-graph=ponyFiction.dot

clean:
	find -name '*.pyc' -exec rm -rf '{}' \;
	