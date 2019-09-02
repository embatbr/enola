# -*- coding: utf-8 -*-

import click


@click.group()
def external_command():
    pass


@click.command()
@click.argument('env')
def build(env):
    click.echo('Google Composer <build> [{}]'.format(env))


external_command.add_command(build)
