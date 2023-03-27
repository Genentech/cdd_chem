"""
(C) 2020 Genentech. All rights reserved.

Test file for cdd_chem module.
"""
import pytest_check as check

from cdd_chem.mol import from_smiles


def test_mol():
    molecule = from_smiles('C1[C+]CCC1')
    check.equal('C1CC[C+]C1', molecule.canonical_smiles)

    molecule['ID'] = "testValue"
    check.equal(molecule['ID'], "testValue")

    check.equal(1,molecule.formal_charge)

def test_mol_title():
    molecule = from_smiles('C1[C+]CCC1')
    molecule.title = "Test Molecule"
    check.equal(molecule.title, "Test Molecule")
