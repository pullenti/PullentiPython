
fetch:
	wget http://www.pullenti.ru/DownloadFile.aspx?file=PullentiPython.zip -O PullentiPython.zip
	rm -r demo pullenti
	unzip PullentiPython.zip
	rm PullentiPython.zip

wheel:
	python setup.py bdist_wheel

upload:
	twine upload dist/*

clean:
	find pullenti -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info
