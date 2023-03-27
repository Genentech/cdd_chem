"""
Module containing input/output operations using the OpenEye Toolkit.

Created on Jul 1, 2018

@author: albertgo
"""

import io
import gzip
import sys
import re
import os
from typing import Any

import rdkit

from cdd_chem.rdkit.mol import Mol
from cdd_chem.io import BaseMolInputStream, BaseMolOutputStream


class MolInputStream(BaseMolInputStream):
    """Provide an iterator for reading molecules using RDKit

       @TODO specify format?
    """
    sdf_re = re.compile(".sdf(.gz)?$", re.I)
    smi_re = re.compile(".smi(.gz)?$", re.I)

    def __init__(self, file_path, **kwargs):
        super().__init__()

        self.file_path = file_path
        self.next_mol = None

        if MolInputStream.sdf_re.match(file_path) is not None or \
           MolInputStream.smi_re.match(file_path) is not None:
            self._in1 = None
            in_s = sys.stdin.buffer
        else:
            in_s = io.open(self.file_path, "rb") # pylint: disable=R1732
            self._in1 = in_s

        if self.file_path.endswith("gz"):
            in_s = gzip.open(in_s, mode="rb")
            self._in2 = in_s
        else:
            self._in2 = None

        if MolInputStream.sdf_re.search(self.file_path) is not None:
            if kwargs is None:
                kwargs = {}
            if "removeHs" not in kwargs:
                kwargs['removeHs'] = False
            if "sanitize" not in kwargs:
                kwargs['sanitize'] = False   # this is more oelike

            self._in3 = rdkit.Chem.ForwardSDMolSupplier(in_s, **kwargs)

        # elif MolInputStream.smiRE.search(self.file_path) is not None:
        #   self._in3 = Chem.SmilesMolSupplier(self._in2)
        else:
            raise Exception("Unknown file format: " + self.file_path)

    def has_next(self):
        if self.next_mol is not None:
            return True

        try:
            self.next_mol = Mol(next(self._in3))
            return True
        except StopIteration:
            return False

    def __next__(self):
        if self.next_mol is not None:
            res = self.next_mol
            self.next_mol = None
            return res

        return Mol(next(self._in3))

    def close(self):
        # self._in3.close()
        if self._in2 is not None:
            self._in2.close()
        if self._in1 is not None:
            self._in1.close()


class MolOutputStream(BaseMolOutputStream):
    """Molecule output stream for writing molecules to file using the RDKit toolkit."""

    def __init__(self, file_path: str):
        super().__init__(file_path)

        out: Any

        if self.file_path.endswith("gz"):
            if self.file_path.startswith(".sdf") or self.file_path.startswith(".smi"):
                out = os.fdopen(sys.stdout.fileno(), "wb", closefd=False)
                self._out1 = None
            else:
                out = io.open(self.file_path, "wb") # pylint: disable=R1732
                self._out1 = out

            out = gzip.open(out, encoding='UTF-8', mode='wt')
            self._out2 = out
        else:
            if self.file_path.startswith(".sdf") or self.file_path.startswith(".smi"):
                out = sys.stdout
                self._out1 = None
            else:
                out = io.open(self.file_path, 'wt', encoding='UTF-8') # pylint: disable=R1732
                self._out1 = out

            self._out2 = None

        if MolInputStream.sdf_re.search(self.file_path) is not None:
            self._out3 = rdkit.Chem.SDWriter(out)
        elif MolInputStream.smi_re.search(self.file_path) is not None:
            self._out3 = rdkit.Chem.SmilesWriter(out)
        else:
            raise Exception("Unknown file format: " + self.file_path)

    def write_mol(self, mol):
        """Writes molecule to stream."""
        # pylint: disable=protected-access
        self._out3.write(mol._mol)

    def close(self):
        """Closes output stream."""
        self._out3.close()
        if self._out2 is not None:
            self._out2.close()
        if self._out1 is not None:
            self._out1.close()
