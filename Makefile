.PHONY: all install list readme release templates test version


PACKAGE := $(shell grep '^PACKAGE =' setup.py | cut -d "'" -f2)
VERSION := $(shell head -n 1 $(PACKAGE)/VERSION)
MAINTAINER := $(shell head -n 1 MAINTAINER.md)


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

release:
	git checkout master && git pull origin && git fetch -p
	git log --pretty=format:"%C(yellow)%h%Creset %s%Cgreen%d" --reverse -20
	@echo "Releasing v$(VERSION) in 10 seconds. Press <CTRL+C> to abort" && sleep 10
	git commit -a -m 'v$(VERSION)' && git tag -a v$(VERSION) -m 'v$(VERSION)'
	git push --follow-tags

templates:
	sed -i -E "s/@(\w*)/@$(MAINTAINER)/" .github/issue_template.md
	sed -i -E "s/@(\w*)/@$(MAINTAINER)/" .github/pull_request_template.md

test:
	pylama $(PACKAGE)
	tox

version:
	@echo $(VERSION)
