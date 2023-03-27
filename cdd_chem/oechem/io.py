"""
(C) 2020 Genentech. All rights reserved.

Created on Jul 1, 2018

@author: albertgo

Module containing input/output operations using the OpenEye Toolkit.
"""
from typing import Optional, Dict, Collection

import numpy as np
from openeye import oechem

from cdd_chem import BaseMol
from cdd_chem.oechem.mol import Mol

from cdd_chem.io import BaseMolInputStream, BaseMolOutputStream
from cdd_chem.util.IterableAlgorithm import SimpleIterableAlgorithm, IterableAlgorithm


class MolInputStream(BaseMolInputStream):
    """Provide an iterator for reading molecules using the OpenEye toolkit."""

    def __init__(self, file_path: str) -> None:
        super().__init__()

        self.file_path = file_path
        self.ifs = oechem.oemolistream()
        if not self.ifs.open(file_path):
            raise IOError(f"Could not open {file_path}")
        self.next_mol: Optional[Mol] = None

    def has_next(self) -> bool:
        if self.next_mol is not None:
            return True

        mol = oechem.OEGraphMol()
        if oechem.OEReadMolecule(self.ifs, mol):
            self.next_mol = Mol(mol)
            return True
        return False

    def __next__(self):
        if not self.has_next():
            raise StopIteration()

        res = self.next_mol
        self.next_mol = None
        return res

    def close(self):
        if self.ifs is not None:
            self.ifs.close()
        self.ifs = None


class MolOutputStream(BaseMolOutputStream):
    """Molecule output stream for writing molecules to file using the OpenEye toolkit."""

    def __init__(self, file_path: str) -> None:
        super().__init__(file_path)
        self.ofs = oechem.oemolostream(file_path)

    def write_mol(self, mol):
        """Writes molecule to stream."""
        # pylint: disable=protected-access
        oechem.OEWriteMolecule(self.ofs, mol._mol)

    def close(self):
        """Closes output stream."""
        self.ofs.close()


class MolNumpyFormatter(SimpleIterableAlgorithm[BaseMol,BaseMol]):
    """ Format all fields ina molecule object that are np.ndarrays """

    # pylint: disable=E1136   # pylint Interference with typing
    def __init__(self, molIn:IterableAlgorithm[BaseMol],
                 defaultPrecision, fieldPrecision:Dict[str, int]=None) -> None:
        """
        :param molIn: input algorithm
        :param defaultPrecision: number of digits to use by default
        :param fieldPrecision: Dict specifying field_name, precission for fields that deviate from defaultPrecision
        """
        super().__init__(molIn)
        self.defaultPrecision = defaultPrecision
        self.fieldPrecision   = fieldPrecision if fieldPrecision is not None else {}

    def compute(self, mol:BaseMol) -> BaseMol: # pylint: disable=W0221
        for (n,v) in mol.items():
            if isinstance(v, np.ndarray):
                prec = self.fieldPrecision.get(n, self.defaultPrecision)
                vstr = np.array2string(v,precision=prec,suppress_small=True, max_line_width=999999, separator=',', threshold=9999)
                mol[n] = vstr[1:-1].replace(" ",'')
        return mol


class ConvertToNumPy(SimpleIterableAlgorithm[BaseMol,BaseMol]):
    """ Convert fields with float cvs to be numpy objects """

    # pylint: disable=E1136   # pylint Interference with typing
    def __init__(self, molIn:IterableAlgorithm[BaseMol], flds:Collection[str]) -> None:
        """
        :param molIn: input algorithm
        :param flds: Set with field names to check and convert
        """
        super().__init__(molIn)
        self.flds   = flds

    def compute(self, mol:BaseMol) -> BaseMol: # pylint: disable=W0221
        for n in self.flds:
            if n not in mol:
                continue
            val = mol[n]
            if isinstance(val, np.ndarray): continue
            mol[n] = np.fromstring(val, dtype=float, sep=',')
        return mol
