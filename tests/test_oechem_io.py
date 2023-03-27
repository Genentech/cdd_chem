"""
(C) 2020 Genentech. All rights reserved.

Test file for cdd_chem module.
"""
import os

import pytest_check as check

try:
    from cdd_chem.oechem.io import MolInputStream
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError("Openeye Toolkit not found, cannot run this test") from exc


def test_read(shared_datadir):
    atomic_sum = 0
    with MolInputStream(os.path.join(shared_datadir / 'test_CCCO_confs.sdf')) as inf:
        for mol in inf:
            for atom in mol.atoms:
                atomic_sum += atom.atomic_num
    check.equal(170, atomic_sum)


def test_has_next(shared_datadir):
    atomic_sum = 0
    with MolInputStream(os.path.join(shared_datadir / 'test_CCCO_confs.sdf')) as inf:
        while inf.has_next():
            mol = inf.__next__()
            for atom in mol.atoms:
                atomic_sum += atom.atomic_num
    check.equal(170, atomic_sum)


def test_coords(shared_datadir):
    coord_sum = 0.0
    with MolInputStream(os.path.join(shared_datadir / 'test_CCCO_confs.sdf')) as inf:
        for mol in inf:
            coord_sum += mol.coordinates.sum()

    check.almost_equal(115.7458003279753, coord_sum, rel=0.1)

    coord_sum = 0.0
    with MolInputStream(os.path.join(shared_datadir / 'test_CCCO_confs.sdf')) as inf:
        for mol in inf:
            coords = mol.coordinates
            coords = coords * 2.0
            mol.coordinates = coords
            coord_sum += mol.coordinates.sum()

    check.almost_equal(115.7458003279753 * 2.0, coord_sum, rel=0.1)


def test_read_c5(shared_datadir):
    inf = MolInputStream(os.path.join(shared_datadir / 'C5.sdf'))
    atomic_sum = 0
    for mol in inf:
        for atom in mol.atoms:
            atomic_sum += atom.atomic_num
    check.equal(11, atomic_sum)
