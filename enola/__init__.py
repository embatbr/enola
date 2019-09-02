# -*- coding: utf-8 -*-

import click

from enola.products import composer


@click.group()
def external_command():
    pass


external_command.add_command(composer.external_command, name='composer')
