# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='mapping_tool',
    version='0.1.0',
    description='Create OSM maps automatically',
    long_description=readme,
    author='Bosse Sottmann',
    author_email='bosse.sottmann@stud.uni-heidelberg.de',
    url='https://github.com/BoSott/mapping_tool/',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
