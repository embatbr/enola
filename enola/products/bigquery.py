# -*- coding: utf-8 -*-

import os

import click
from google.cloud import bigquery

from enola.utils import get_default_context, run_cmd


# INTERNALS BEGIN


def _create_dataset(project, name, tables_too=False):
    _TEMPLATE = [
        'bq mk --dataset {project}:{dataset}'
    ]

    template_args = {
        'project': project,
        'dataset': name
    }

    run_cmd(_TEMPLATE, template_args)

    if tables_too:
        cmd_default_context = get_default_context()
        gcp_path = '{}/gcp'.format(cmd_default_context['cwd'])
        schemaspath = '{}/bigquery/schemas/{}'.format(gcp_path, name)

        filenames = os.listdir(schemaspath)
        for filename in filenames:
            tablename = filename[0 : -5]
            _create_table(project, name, tablename, schemaspath)


def _create_table(project, dataset_name, name, schemaspath):
    _TEMPLATE = [
        'bq mk --table',
        '{project}:{dataset}.{table}',
        '{schemaspath}'
    ]

    if schemaspath is None:
        cmd_default_context = get_default_context()
        gcp_path = '{}/gcp'.format(cmd_default_context['cwd'])
        schemaspath = '{}/bigquery/schemas/{}'.format(gcp_path, dataset_name)

    schemaspath = '{}/{}.json'.format(schemaspath, name)

    template_args = {
        'project': project,
        'dataset': dataset_name,
        'table': name,
        'schemaspath': schemaspath
    }

    run_cmd(_TEMPLATE, template_args)


def _create_views(views_project, views_dataset, origin_project, origin_dataset, table):
    _TEMPLATE = [
        "bq --project_id {views_project} mk",
        "--use_legacy_sql=false",
        "--view 'SELECT * FROM `{origin_project}.{origin_dataset}.{table}`'",
        "{views_dataset}.{table}"
    ]

    template_args = {
        'views_project': views_project,
        'views_dataset': views_dataset,
        'origin_project': origin_project,
        'origin_dataset': origin_dataset,
        'table': table
    }

    run_cmd(_TEMPLATE, template_args)


def _share_views(views_project, views_dataset, origin_project, origin_dataset, tables):
    client_views_project = bigquery.Client(views_project)
    client_origin_project = bigquery.Client(origin_project)

    views_dataset_obj = bigquery.Dataset(client_views_project.dataset(views_dataset))
    origin_dataset_obj = bigquery.Dataset(client_origin_project.dataset(origin_dataset))

    access_entries = origin_dataset_obj.access_entries

    for table in tables:
        view = bigquery.Table(views_dataset_obj.table(table))
        access_entries.append(
            bigquery.AccessEntry(None, 'view', view.reference.to_api_repr())
        )

    origin_dataset_obj.access_entries = access_entries
    origin_dataset_obj = client_views_project.update_dataset(origin_dataset_obj, ['access_entries'])


# INTERNALS END

# EXTERNALS BEGIN


@click.group()
def external_command():
    pass


# GROUP create BEGIN


@click.group()
def create():
    pass


@click.command()
@click.option('--project', required=True, type=str)
@click.argument('name')
def dataset(project, name):
    _create_dataset(project, name, tables_too=True)


@click.command()
@click.option('--project', required=True, type=str)
@click.option('--dataset', 'dataset_name', required=True, type=str)
@click.argument('name')
@click.option('--schemaspath', default=None, type=str)
def table(project, dataset_name, name, schemaspath):
    _create_table(project, dataset_name, name, schemaspath)


@click.command()
@click.argument('views_project')
@click.argument('views_dataset')
@click.argument('origin_project')
@click.argument('origin_dataset')
def views(views_project, views_dataset, origin_project, origin_dataset):
    _create_dataset(views_project, views_dataset)

    cmd_default_context = get_default_context()
    gcp_path = '{}/gcp'.format(cmd_default_context['cwd'])
    schemaspath = '{}/bigquery/schemas/{}'.format(gcp_path, origin_dataset)

    filenames = os.listdir(schemaspath)
    tables = [filename[0 : -5] for filename in filenames]
    for table in tables:
        _create_views(views_project, views_dataset, origin_project, origin_dataset, table)

    _share_views(views_project, views_dataset, origin_project, origin_dataset, tables)


create.add_command(dataset)
create.add_command(table)
create.add_command(views)


# GROUP create END


external_command.add_command(create)


# EXTERNALS END
