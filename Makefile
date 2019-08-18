.DEFAULT_GOAL := build

.PHONY: default
default: build ;

build:
	python3 bin/generate.py --source src --destination exams

install:
	pip3 install --user -r requirements.txt
