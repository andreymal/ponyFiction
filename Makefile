all :
	true

pylint :
	pylint --output-format=colorized --rcfile=pylint.ini \
		bleach \
		html5lib \
		ponyFiction \
		registration \
		sanitizer \
		*.py \
		2>&1 | less -SR

pylint-int :
	pylint --output-format=colorized --rcfile=pylint.ini \
		ponyFiction \
		*.py \
		--int-import-graph=file.dot


clean :
	find -name '*.pyc' -exec rm -rf '{}' \;
