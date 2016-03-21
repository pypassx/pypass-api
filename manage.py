#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    manager
    ~~~~~~~

    This module is a project interface to run, and interact with the db and
    etc.

    :copyright: (c) 2016 by Mehdy Khoshnoody.
    :license: GPLv2, see LICENSE for more details.
"""
import click


def print_version(ctx, param, value):
    """
        prints the App name and it's current version
    :param ctx: app context
    :param param: function parameters
    :param value:
    """
    if not value or ctx.resilient_parsing:
        return
    ctx.exit()


@click.group()
@click.option('--version', '-v', callback=print_version, expose_value=False,
              is_flag=True, is_eager=True)
def main():
    """
        PyPass API
    """
    pass


@main.group()
def web():
    """
        Web interface of project
    """
    pass


@web.command()
def run():
    pass

if __name__ == '__main__':
    main()
