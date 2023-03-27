"""
(C) 2020 Genentech. All rights reserved.

Created on Jul 1, 2018

@author: albertgo

Abstraction around RDKit molecule to make it independent
"""
# pylint: disable=E1101

import typing
from typing import Any

import numpy as np
from rdkit import Chem
import rdkit.Geometry.rdGeometry

from .atom import Atom
from .. import BaseAtom
from ..mol import BaseMol


class Mol(BaseMol):
    """Implementation of a molecule object that uses the RDKit toolkit as internal representation."""

    def __init__(self, rd_kit_mol):
        BaseMol.__init__(self, rd_kit_mol)

    def make_read_write(self):
        self._mol = Chem.RWMol(self._mol)

    def make_read_only(self):
        self._mol = Chem.Mol(self._mol)


    def addH(self, addCoords=False): # noqa: N802
        """ add explicit hydrogen
            Note: this will replace the underlying _mol
        """
        self._mol = Chem.AddHs(self._mol, addCoords=addCoords)


    def removeH(self): # noqa: N802
        """ remove explicit hydrogen
            Note: this will replace the underlying _mol
        """
        self._mol = Chem.RemoveHs(self._mol)


    @property
    def num_atoms(self) -> int:
        """Returns the number of atoms in the molecule."""
        return self._mol.GetNumAtoms()

    @property
    def num_bonds(self) -> int:
        """Returns the number of bonds in the molecule."""
        return self._mol.GetNumBonds()

    @property
    def coordinates(self) -> np.ndarray:
        """
        Returns the 3D coordinates of the molecule in a numpy array.

        Returns
        -------
        numpy [nAtoms,3]
        """
        return self._mol.GetConformer().GetPositions()

    @coordinates.setter
    def coordinates(self, positions: np.ndarray) -> None:
        """
        Sets the 3D coordinates of the molecule from a numpy array.

        Parameter
        --------
        positions: numpy [natoms,3]
        """
        conf = self._mol.GetConformer()
        for i, pos in enumerate(positions.astype(np.float64)):
            p3d = rdkit.Geometry.rdGeometry.Point3D(pos[0], pos[1], pos[2])
            conf.SetAtomPosition(i, p3d)

    @property
    def atoms(self):
        """Returns a list of atoms."""
        return [Atom(atom) for atom in self._mol.GetAtoms()]

    @property
    def atom_symbols(self) -> typing.List[str]:
        """Returns a list of atomic symbols."""
        atom_sym: typing.List[str] = []
        for atom in self._mol.GetAtoms():
            atom_sym.append(atom.GetSymbol())
        return atom_sym

    @property
    def atom_types(self) -> typing.List[int]:
        """Returns a list of atomic numbers."""
        atom_types: typing.List[int] = []
        # just to mess with pylint line sy=similarity check
        for atom in self._mol.GetAtoms():
            atom_types.append(atom.GetAtomicNum())
        return atom_types

    def delete_atom(self, at: BaseAtom):
        """
        :param at: atom to be deleted
        """
        self._mol.RemoveAtom(at._at.GetIdx()) # pylint: disable=W0212

    @property
    def canonical_smiles(self) -> str:
        """Returns the canonical isomeric smiles representation of the molecule."""
        isomeric = True
        return Chem.MolToSmiles(self._mol, isomeric)

    @property
    def canonical_non_isomeric_smiles(self) -> str:
        """Returns the canonical non-isomeric smiles representation of the molecule."""
        isomeric = True
        return Chem.MolToSmiles(self._mol, not isomeric)

    @property
    def title(self) -> str:
        """Returns the title of the molecule."""
        return self._mol.GetProp('_Name')

    @title.setter
    def title(self, value:str) -> None:
        """Set the title of  the molecule."""
        self._mol.SetProp("_Name", value)

    def __contains__(self, key: str) -> bool:
        return self._mol.HasProp(key)

    def __getitem__(self, key: str) -> Any:
        if super().__contains__(key): return super().__getitem__(key)

        if self._mol.HasProp(key):
            return self._mol.GetProp(key)
        raise KeyError(f"{self.__class__.__name__} has no key {repr(key)}")

    def __setitem__(self, key: str, value: Any):
        super().__setitem__(key,value)
        self._mol.SetProp(key, value)

    def keys(self) -> typing.Iterator[str]:
        """Yields the property names (keys) of the molecule."""
        for prop_name in self._mol.GetPropNames():
            yield prop_name

    def items(self) -> typing.Iterator[typing.Tuple[str, str]]:
        """Yields the property key - data pairs of the molecule."""
        for item in self._mol.GetPropsAsDict().items():
            key = item[0]
            if super().__contains__(key):
                yield key, super().__getitem__(key)
            else:
                yield item

    def __delitem__(self, key: str):
        """Removes a specific property from the molecule."""
        if super().__contains__(key): super().__delitem__(key)
        self._mol.ClearProp(key)

    @property
    def mol_file(self):
        """Returns the MDL representation of the molecule."""

        return Chem.MolToMolBlock(self._mol)


def from_smiles(smi: str) -> Mol:
    """Creates a molecule object from a smiles string """
    return Mol(Chem.MolFromSmiles(smi))
