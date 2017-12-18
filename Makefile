.PHONY: all install list profiles test version


PACKAGE := $(shell grep '^PACKAGE =' setup.py | cut -d "'" -f2)
VERSION := $(shell head -n 1 $(PACKAGE)/VERSION)


all: list

install:
	pip install --upgrade -e .[develop]

list:
	@grep '^\.PHONY' Makefile | cut -d' ' -f2- | tr ' ' '\n'

profiles:
	wget -O tableschema/profiles/table-schema.json https://specs.frictionlessdata.io/schemas/table-schema.json

test:
	pylama $(PACKAGE)
	tox

version:
	@echo $(VERSION)
