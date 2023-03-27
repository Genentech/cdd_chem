"""
(C) 2020 Genentech. All rights reserved.

Test file for cdd_chem module.
"""

from importlib import import_module

from cdd_chem.mol import BaseMol


def new_molecule_for_testing(toolkit: str, *args, **kwargs) -> BaseMol:
    """Creates a new molecule for the given toolkit."""

    if toolkit.lower() == "openeye":
        mol_module = import_module("cdd_chem.oechem.mol")
    elif toolkit.lower() == "rdkit":
        mol_module = import_module("cdd_chem.rdkit.mol")
    else:
        raise ValueError("TEST_TOOLKIT not recognized."
                         " Expected values are openeye or rdkit")

    instance = mol_module.Mol(*args, **kwargs)
    return instance
