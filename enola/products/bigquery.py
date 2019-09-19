# -*- coding: utf-8 -*-

import os

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
    def _create_table(dataset_schemas_path, template_args, tablename):
        schema_path = '{}/{}.json'.format(dataset_schemas_path, tablename)

        _TEMPLATE = [
            'bq mk --table',
            '{project}:{dataset}.{table}',
            '{schema_path}'
        ]

        template_args.update({
            'table': tablename,
            'schema_path': schema_path
        })

        run_cmd(_TEMPLATE, template_args)

    template_args = {
        'project': project,
        'dataset': dataset
    }

    cmd_default_context = get_default_context()
    gcp_path = '{}/gcp'.format(cmd_default_context['cwd'])
    dataset_schemas_path = '{}/bigquery/schemas/{}'.format(gcp_path, dataset)

    if table is None:
        _TEMPLATE = [
            'bq mk --dataset {project}:{dataset}'
        ]

        run_cmd(_TEMPLATE, template_args)

        filenames = os.listdir(dataset_schemas_path)
        for filename in filenames:
            tablename = filename[0 : -5]
            _create_table(dataset_schemas_path, template_args, tablename)

    else:
        _create_table(dataset_schemas_path, template_args, table)


external_command.add_command(create)


# EXTERNALS END
