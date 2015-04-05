# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys
import io
import json
import csv
import click
import jtskit


@click.group()
def main():
    """The entry point into the CLI."""


@main.command()
@click.argument('data')
@click.option('--row_limit', default=0, type=int)
@click.option('--to_file')
def infer(data, row_limit, to_file):

    """Infer a schema from data.

    * data must be a local filepath
    * data must be CSV
    * data must be UTF-8 encoded
    * the first line of data must be headers
    * these constraints are just for the CLI

    """

    if not row_limit:
        row_limit = None

    with io.open(data, mode='r+t', encoding='utf-8') as stream:
        headers = stream.readline().rstrip('\n').split(',')
        values = csv.reader(stream)
        response = jtskit.infer(headers, values, row_limit=row_limit)

    if to_file:
        with io.open(to_file, mode='w+t', encoding='utf-8') as dest:
            dest.write(json.dumps(response, ensure_ascii=False, indent=2))

    click.echo(response)


@main.command()
@click.argument('schema')
def ensure(schema):

    """Ensure a supposed schema is a JSON Table Schema."""

    valid, errors = jtskit.ensure(schema)

    click.echo(valid)
    click.echo(errors)


if __name__ == '__main__':
    main()
