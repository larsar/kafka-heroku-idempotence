#!/usr/bin/env make
export HOSTNAME := $(shell hostname)

install:
	pip install -r requirements.txt

freeze:
	pip freeze > requirements.txt

venv:
	virtualenv -p python3 venv

