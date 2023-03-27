"""
(C) 2020 Genentech. All rights reserved.

Test file for cdd_chem module.
"""

import os

import pytest_check as check

try:
    from cdd_chem.rdkit.io import MolInputStream
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError("RDKit Toolkit not found, cannot run this test") from exc


def test_read(shared_datadir):
    inf = MolInputStream(os.path.join(shared_datadir / 'test_CCCO_confs.sdf'))
    atomic_sum = 0
    for mol in inf:
        for atom in mol.atoms:
            atomic_sum += atom.atomic_num
    check.equal(170, atomic_sum)


def test_has_next(shared_datadir):
    inf = MolInputStream(os.path.join(shared_datadir / 'test_CCCO_confs.sdf'))
    atomic_sum = 0
    n = 0
    while inf.has_next():
        mol = inf.__next__()
        for atom in mol.atoms:
            atomic_sum += atom.atomic_num
        n += 1
    check.equal(5, n)
    check.equal(170, atomic_sum)



def test_read_c5(shared_datadir):
    inf = MolInputStream(os.path.join(shared_datadir / 'C5.sdf'))
    atomic_sum = 0
    for mol in inf:
        for atom in mol.atoms:
            atomic_sum += atom.atomic_num
    check.equal(11, atomic_sum)
