# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import io
import json

import click

import jsontableschema


DIR = os.path.abspath(os.path.dirname(__file__))
VERSION_FILE = os.path.join(os.path.dirname(__file__), 'VERSION')
VERSION = io.open(VERSION_FILE, encoding='utf-8').read().strip()


@click.group()
def main():
    """The entry point into the CLI."""


@main.command()
def info():
    """Return info on this version of JSON Table Schema"""
    click.echo(json.dumps({'version': VERSION}, ensure_ascii=False, indent=4))


@main.command()
@click.argument('data')
@click.option('--row_limit', default=0, type=int)
@click.option('--encoding', default='utf-8')
@click.option('--to_file')
def infer(data, row_limit, encoding, to_file):

    """Infer a schema from data.

    * data must be a local filepath
    * data must be CSV
    * the file encoding is assumed to be UTF-8 unless an encoding is passed
      with --encoding
    * the first line of data must be headers
    * these constraints are just for the CLI

    """

    if not row_limit:
        row_limit = None

    with io.open(data, mode='r+t', encoding=encoding) as stream:
        try:
            headers = stream.readline().rstrip('\n').split(',')
            values = jsontableschema.compat.csv_reader(stream)
        except UnicodeDecodeError:
            response = "Could not decode the data file as {0}. " \
                "Please specify an encoding to use with the " \
                "--encoding argument.".format(encoding)
        else:
            response = jsontableschema.infer(headers, values,
                                             row_limit=row_limit)

        if to_file:
            with io.open(to_file, mode='w+t', encoding='utf-8') as dest:
                dest.write(json.dumps(response, ensure_ascii=False, indent=2))

    click.echo(response)


@main.command()
@click.argument('schema')
def validate(schema):

    """Validate that a supposed schema is in fact a JSON Table Schema."""

    errors = [e.message for e in jsontableschema.validator.iter_errors(schema)]
    if not errors:
        click.echo(False)
    else:
        click.echo(True)
        click.echo(errors)


if __name__ == '__main__':
    main()
