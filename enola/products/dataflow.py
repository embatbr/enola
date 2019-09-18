# -*- coding: utf-8 -*-

import click

from enola.utils import read_product_config, run_cmd


# INTERNALS BEGIN


def _mavenize(path, template_project):
    _TEMPLATES = [
        'rm {path}/pom-{template_project}.xml',
        'rm -Rf code-{template_project}',
        'cp {path}/projects/{template_project}/pom.xml {path}/pom-{template_project}.xml',
        'rm -Rf {path}/code-{template_project}',
        'mkdir {path}/code-{template_project}',
        'mkdir {path}/code-{template_project}/base',
        'mkdir {path}/code-{template_project}/base/encoders',
        'mkdir {path}/code-{template_project}/executors',
        'mkdir {path}/code-{template_project}/options',
        'mkdir {path}/code-{template_project}/steps',
        '{path}/projects/{template_project}/src-maker.sh'
    ]

    for template in _TEMPLATES:
        run_cmd([template], {
            'path': path,
            'template_project': template_project,
        })


# INTERNALS END

# EXTERNALS BEGIN


@click.group()
def external_command():
    pass


@click.command()
@click.argument('env')
@click.option('--path', default='.', show_default=True)
def build(env, path):
    config = read_product_config('dataflow', env)

    _mavenize(path, config['template_project'])

    # run_cmd(['ls {path}'], {'path': path})


external_command.add_command(build)
