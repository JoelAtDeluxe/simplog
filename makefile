clean:
	rm -rf dist/*

re-version:
	echo "tbd"

pypi-build: clean
	python setup.py sdist	

upload:
	twine check dist/* 
	twine upload dist/* 