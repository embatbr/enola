# -*- coding: utf-8 -*-

import json
import os


def get_default_context():
    return {
        'cwd': os.getcwd()
    }


def read_product_config(product, env):
    cmd_default_context = get_default_context()
    gcp_path = '{}/gcp'.format(cmd_default_context['cwd'])
    product_path = '{}/{}/{}.json'.format(gcp_path, product, env)

    with open(product_path) as f:
        return json.load(f)


def run_cmd(template, template_args):
    cmd_string = template.format(**template_args)
    os.system(cmd_string)
