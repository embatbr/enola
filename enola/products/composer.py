# -*- coding: utf-8 -*-

import click

from enola.utils import read_product_config, run_cmd


CMD_STRING_TEMPLATE = """gcloud beta composer environments create {name} \
    --project {project} \
    --node-count {node-count} \
    --location {location} \
    --zone {zone} \
    --machine-type {machine-type} \
    --disk-size {disk-size} \
    --tags {tags} \
    --image-version {image-version} \
    --python-version {python-version} \
    --network {network} \
    --subnetwork {subnetwork} \
    --airflow-configs {airflow-configs} \
    --labels {labels} \
    --async
"""


def _airflow_configs(configs):
    concat = list()

    for (section, obj) in configs.items():
        for (prop, value) in obj.items():
            concat.append('{}-{}={}'.format(section, prop, value))

    return ','.join(concat)


def _airflow_labels(labels):
    concat = list()

    for (key, value) in labels.items():
        concat.append('{}={}'.format(key, value))

    return ','.join(concat)



@click.group()
def external_command():
    pass


@click.command()
@click.argument('env')
def build(env):
    config = read_product_config('composer', env)
    template_args = {
        'project': config['project'],
        'name': config['name'],
        'node-count': config['node-config']['count'],
        'location': config['node-config']['location'],
        'zone': config['node-config']['zone'],
        'machine-type': config['node-config']['machine-type'],
        'disk-size': config['node-config']['disk-size'],
        'tags': ','.join(config['node-config']['tags']),
        'image-version': config['node-config']['image'],
        'python-version': config['node-config']['python-version'],
        'network': config['network-config']['network'],
        'subnetwork': config['network-config']['subnetwork'],
        'airflow-configs': _airflow_configs(config['airflow-config-overrides']),
        'labels': _airflow_labels(config['labels'])
    }

    run_cmd(CMD_STRING_TEMPLATE, template_args)


external_command.add_command(build)
