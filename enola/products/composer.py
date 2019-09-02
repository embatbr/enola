# -*- coding: utf-8 -*-

import json

import click

from enola.utils import get_default_context


@click.group()
def external_command():
    pass


def get_context():
    cmd_context = get_default_context()
    cmd_context.update({
        'gcp_path': '{}/gcp'.format(cmd_context['cwd'])
    })

    return cmd_context


@click.command()
@click.argument('env')
def build(env):
    context = get_context()
    with open('{}/composer/{}.json'.format(context['gcp_path'], env)) as f:
        config = json.load(f)

    print(config)

    click.echo('Google Composer <build> [{}]'.format(env))


external_command.add_command(build)
