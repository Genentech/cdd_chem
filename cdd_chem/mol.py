"""
(C) 2020 Genentech. All rights reserved.

Created on Feb 13, 2019

@author: albertgo

Abstract base class for objects representing a molecule.
"""

import typing
from typing import Any

from abc import ABCMeta
from abc import abstractmethod
from importlib import import_module
import numpy as np
from cdd_chem.atom import BaseAtom
from cdd_chem.toolkit import get_toolkit


class BaseMol(metaclass=ABCMeta):
    """Abstract base class for toolkit agnostic molecule representation."""

    def __init__(self, native_mol_object):
        """Constructor for a molecule.

        Parameters
        ----------
        native_mol_object
            Toolkit molecule object wrapped by BaseMol; either an
            oechem.GraphMol or rdkit.Chem.rdchem.Mol
        """
        assert native_mol_object is not None, "Invalid None molecule"
        self._mol = native_mol_object
        self.objects = {}


    def make_read_write(self):
        """
        if the underlying toolkit requires a molecule to be switched to RW do so
        """

    def make_read_only(self):
        """
        if the underlying toolkit suports RO and RW molecule swithc this to RO
        """

    @abstractmethod
    def addH(self, addCoords=False): # noqa: N802
        """ add explicit hydrogen
        """

    @abstractmethod
    def removeH(self): # noqa: N802
        """ remove explicit hydrogen """


    @property
    @abstractmethod
    def num_atoms(self) -> int:
        """Returns the number of atoms in the molecule."""

    @property
    @abstractmethod
    def num_bonds(self) -> int:
        """Returns the number of bonds in the molecule."""

    @property
    def coordinates(self) -> np.ndarray:
        """
        Returns the 3D coordinates of the molecule in a numpy array.

        Returns
        -------
        numpy [nAtoms,3]
        """

    @coordinates.setter
    def coordinates(self, positions: np.ndarray) -> None:
        """
        Sets the 3D coordinates of the molecule from a numpy array.

        Parameter
        --------
        positions: numpy [natoms,3]
        """

    @property
    @abstractmethod
    def atoms(self) -> typing.List[BaseAtom]:
        """Returns a list of atoms."""


    @property
    @abstractmethod
    def atom_symbols(self) -> typing.List[str]:
        """Returns a list of atomic symbols."""


    @property
    @abstractmethod
    def atom_types(self) -> typing.List[int]:
        """Returns a list of atomic numbers."""


    @abstractmethod
    def delete_atom(self, at: BaseAtom):
        """
        :param at: atom to be deleted
        """

    @property
    def formal_charge(self) -> int:
        """ Returns sum of all formal charges in the molecule """
        return sum([at.formal_charge for at in self.atoms])

    @property
    @abstractmethod
    def canonical_smiles(self) -> str:
        """Returns the canonical isomeric smiles representation of the molecule."""

    @property
    @abstractmethod
    def canonical_non_isomeric_smiles(self) -> str:
        """Returns the canonical non-isomeric smiles representation of the molecule."""

    @property
    @abstractmethod
    def title(self) -> str:
        """Returns the title of the molecule."""


    @title.setter
    @abstractmethod
    def title(self, val) -> None:
        """Set the title of the molecule."""

    ############################### Mol is a dict of values

    @abstractmethod
    def __contains__(self, key) -> bool:
        return key in self.objects

    def get(self, name: str, default: str) -> str:
        """Returns the property associated with the given name."""
        if name in self:
            return self.__getitem__(name)
        return default

    @abstractmethod
    def __getitem__(self, key: str) -> Any:
        return self.objects[key]

    @abstractmethod
    def __setitem__(self, key: str, value: Any):
        self.objects[key] = value

    @abstractmethod
    def keys(self) -> typing.Iterator[str]:
        """Yields the SD tag names (keys) of the molecule."""
        return self.objects.keys()

    @abstractmethod
    def items(self) -> typing.Iterator[typing.Tuple[str, str]]:
        """Yields the SD tag - SD value pairs of the molecule."""
        return self.objects.items()

    @abstractmethod
    def __delitem__(self, key: str):
        del self.objects[key]



    @property
    @abstractmethod
    def mol_file(self) -> str:
        """Returns the MDL string representation of the molecule."""

    @property
    def sdf_record(self) -> str:
        """Returns the SDF string representation of the molecule including all internal (SD) properties """
        res = self.mol_file
        for tag, value in self.items():
            res += f"> <{tag}>\n{str(value).rstrip()}\n\n"

        return res + "$$$$\n"


def from_smiles(smi: str) -> BaseMol:
    """Creates a molecule object from a smiles string."""
    mol_module = None

    toolkit = get_toolkit()
    if toolkit.lower() == "openeye":
        mol_module = import_module("cdd_chem.oechem.mol")
    elif toolkit.lower() == "rdkit":
        mol_module = import_module("cdd_chem.rdkit.mol")

    if mol_module is None or not hasattr(mol_module, 'from_smiles'):
        raise ValueError(f"TOOLKIT {toolkit} not recognized."
                         " Expected values are 'openeye' or 'rdkit'")

    from_smiles_func = getattr(mol_module, 'from_smiles')
    return from_smiles_func(smi)
