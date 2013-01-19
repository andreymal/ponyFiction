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

clean :
	find -name '*.pyc' -exec rm -rf '{}' \;