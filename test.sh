#!/bin/bash
PYTHONPATH=. py.test --cov jsontableschema --cov-config .coveragerc $@
