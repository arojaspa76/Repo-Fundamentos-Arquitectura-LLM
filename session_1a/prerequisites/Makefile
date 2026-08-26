setup:
	# Makefile for setting up the environment and running tests running in codespace or linux
	python -m venv ~/ai-course-env
	echo 'if [ -d "$$HOME/ai-course-env" ]; then source "$$HOME/ai-course-env/bin/activate"; fi' >> ~/.bashrc
	
	#. ~/ai-course-env/bin/activate

setup-windows:
	# Makefile for setting up the environment and running tests in Windows
	python -m venv ai-course-env

config-env: setup
	. ~/ai-course-env/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

#config-windows-env: setup-windows
#    powershell -Command ".\ai-course-env\Scripts\Activate.ps1; pip install --upgrade pip; pip install -r requirements.txt"

install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vvv --cov=hello --cov=greeting \
		--cov=smath --cov=web tests
	python -m pytest --nbval notebook.ipynb	#tests our jupyter notebook
	#python -m pytest -v tests/test_web.py #if you just want to test web

debug:
	python -m pytest -vv --pdb	#Debugger is invoked

one-test:
	python -m pytest -vv tests/test_greeting.py::test_my_name4

debugthree:
	#not working the way I expect
	python -m pytest -vv --pdb --maxfail=4  # drop to PDB for first three failures

format:
	black *.py

lint:
	pylint --disable=R,C *.py

all: install lint test format

