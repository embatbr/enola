# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


setup(
    name='enola',
    version=open('version').read().strip(),
    url='https://github.com/dotz-open-datalab/enola',
    description='Command line tool to execute smarter deployments in cloud environments.' ,
    long_description=open('README.md').read(),
    author='Eduardo Tenório',
    author_email={
        'dotz': 'eduardo.tenorio@dotz.com',
        'personal': 'embatbr@gmail.com'
    },
    license='WTFPL',
    packages=[
        'enola',
        'enola.products'
    ],
    install_requires=[
        'Click==7.0'
    ],
    entry_points='''
        [console_scripts]
        enola=enola:external_command
    '''
)
