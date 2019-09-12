# -*- coding: utf-8 -*-

import click

import enola
from enola.products import composer


@click.group()
def external_command():
    pass


from enola import products
for module_name, module in products.EXTERNALS.items():
    external_command.add_command(module.external_command, name=module_name)
