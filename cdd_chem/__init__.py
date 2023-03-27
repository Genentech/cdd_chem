"""
(C) 2020 Genentech. All rights reserved.

Top-level package for CDD Chem.

"""
__author__ = """Alberto Gobbi"""
__email__ = "gobbi.alberto@gene.com"

# This is the only please that the package version number is hard coded.
# Please do not edit the version number manually.
# Use 'invoke package.bump-dev' or package.bump-minor instead

__version__ = "0.4.27"

from cdd_chem.atom import BaseAtom
from cdd_chem.mol import BaseMol
from cdd_chem.mol import from_smiles

from cdd_chem.util.string import strip_spaces_as_in_first_line
from cdd_chem.util.unix import exec_tcsh

from cdd_chem.toolkit import get_toolkit
