# -*- coding: utf-8 -*-

import click

from enola.utils import get_default_context, run_cmd


# EXTERNALS BEGIN


@click.group()
def external_command():
    pass


@click.command()
@click.option('--project', required=True, type=str)
@click.option('--dataset', required=True, type=str)
@click.option('--table', default=None, type=str)
def create(project, dataset, table):
    template_args = {
        'project': project,
        'dataset': dataset
    }

    if table is None:
        _TEMPLATE = [
            'bq mk --dataset {project}:{dataset}'
        ]
    else:
        cmd_default_context = get_default_context()
        gcp_path = '{}/gcp'.format(cmd_default_context['cwd'])
        schema_path = '{}/bigquery/schemas/{}/{}.json'.format(gcp_path, dataset, table)

        _TEMPLATE = [
            'bq mk --table',
            '{project}:{dataset}.{table}',
            '{schema_path}'
        ]

        template_args.update({
            'table': table,
            'schema_path': schema_path
        })

    run_cmd(_TEMPLATE, template_args)


external_command.add_command(create)


# EXTERNALS END
