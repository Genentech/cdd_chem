"""
(C) 2020 Genentech. All rights reserved.

Test file for cdd_chem module.
"""

import os

import numpy as np
import pytest_check as check

from cdd_chem import BaseMol
from cdd_chem.io import get_mol_input_stream,
from cdd_chem.oechem.io import MolNumpyFormatter
from cdd_chem.toolkit import cdd_toolkit
from cdd_chem.util.IterableAlgorithm import LambdaAlgorithm


def test_read(shared_datadir):
    atomic_sum = 0
    with get_mol_input_stream(os.path.join(shared_datadir / 'test_CCCO_confs.sdf')) as inf:
        for mol in inf:
            for atom in mol.atoms:
                atomic_sum += atom.atomic_num
    check.equal(170, atomic_sum)


def test_numpy_formatter(shared_datadir):

    def lmbda(mol:BaseMol) -> BaseMol:
        """ add test data as np arrays """
        mol['test'] = np.array([1.1111,2.2222])
        mol['test2']= np.array([2.1111, 3.2222])
        return mol

    with get_mol_input_stream(os.path.join(shared_datadir / 'test_CCCO_confs.sdf')) as infl:
        with LambdaAlgorithm(infl, lmbda) as lm:
            with MolNumpyFormatter(lm, 3, {'test2': 2 }) as npf:
                for mol in npf:
                    assert mol['test'] == '1.111,2.222'
                    assert mol['test2']== '2.11,3.22'

