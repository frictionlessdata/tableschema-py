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

readme:
	pip install md-toc
	md_toc -p README.md github --header-levels 3
	sed -i '/(#$(PACKAGE)-py)/,+2d' README.md

test:
	pylama $(PACKAGE)
	tox

version:
	@echo $(VERSION)
