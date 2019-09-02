# -*- coding: utf-8 -*-

import os


def get_default_context():
    return {
        'cwd': os.getcwd()
    }
