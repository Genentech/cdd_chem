"""
(C) 2020 Genentech. All rights reserved.

Created on Jul 1, 2018

@author: albertgo

Concrete implementation of the abstract Atom class using Openeye toolkit.
"""

from openeye import oechem

from ..atom import BaseAtom


class Atom(BaseAtom):
    """Implementation of an atom object that uses the Openeye toolkit as internal representation."""

    def __init__(self, openeye_atom: oechem.OEAtomBase):
        BaseAtom.__init__(self, openeye_atom)

    @property
    def atomic_num(self) -> int:
        """Returns the atomic number."""
        return self._at.GetAtomicNum()

    @atomic_num.setter
    def atomic_num(self, num:int):
        """ set the atomic number of this atom """
        self._at.SetAtomicNum(num)

    @property
    def symbol(self) -> str:
        """Returns the atomic symbol."""
        return oechem.OEGetAtomicSymbol(self._at.GetAtomicNum())

    @property
    def index(self) -> int:
        """Returns index of atom in molecule."""
        return self._at.GetIdx()

    @property
    def total_hydrogen_count(self) -> int:
        """Returns the total hydrogen count (implicit + explicit)."""
        return self._at.GetTotalHCount()

    @property
    def formal_charge(self) -> int:
        """Returns the formal charge of this atom."""
        return self._at.GetFormalCharge()
