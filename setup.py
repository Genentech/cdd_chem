#!/usr/bin/env python
"""
(C) 2021 Genentech. All rights reserved.

The setup script.

"""

import ast
import os
import re

from setuptools import find_packages, setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.md') as history_file:
    history = history_file.read()

# requirements are defined in the conda package level (see conda/meta.yaml.in)

requirements = []
setup_requirements = []

VERSION = None
abspath = os.path.dirname(os.path.abspath(__file__))
version_file_name = os.path.join(abspath, "cdd_chem", "__init__.py")
with open(version_file_name) as version_file:
    version_file_content = version_file.read()
    version_regex = re.compile(r"__version__\s+=\s+(.*)")
    match = version_regex.search(version_file_content)
    assert match, "Cannot find version number (__version__) in {}".format(version_file_name)
    VERSION = str(ast.literal_eval(match.group(1)))

setup(
    author="Alberto Gobbi",
    author_email='gobbi.alberto@gene.com',
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    description="General purpose helper classes around the RDKit and Openeye toolkits for handling molecular input files.",
    entry_points={
        'console_scripts': [
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/x-rst',
    include_package_data=True,
    keywords='cdd_chem',
    name='cdd_chem',
    packages=find_packages(),
    package_data={'cdd_chem': ['cdd_chem/tests/data/*',]},
    setup_requires=setup_requirements,
    tests_require=['pytest', 'scripttest'],
    test_suite='cdd_chem.tests',
    scripts=['cdd_chem/tests/cdd_chem_package_test.py'],
    url='https://code.roche.com/SMDD/python/cdd_chem.git',
    version=VERSION,   # please update version number in "cdd_chem"/__init__.py file
    zip_safe=False,
)
