"""
(C) 2020 Genentech. All rights reserved.

Created on Jul 1, 2018

@author: albertgo

Abstraction around OpenEye Toolkit Mol to make it independent
"""

import typing
from typing import Any

import numpy as np

from openeye import oechem
from .atom import Atom
from ..mol import BaseMol
from ..atom import BaseAtom



class Mol(BaseMol):
    """Implementation of a molecule object that uses the Openeye toolkit as internal representation."""

    def __init__(self, oe_chem_mol):
        BaseMol.__init__(self, oe_chem_mol)


    def addH(self, addCoords=False): # noqa: N802
        """ add explicit hydrogen
        """
        oechem.OEAddExplicitHydrogens(self._mol, False, addCoords)


    def removeH(self): # noqa: N802
        """ remove explicit hydrogen """
        oechem.OESuppressHydrogens(self._mol)

    @property
    def num_atoms(self) -> int:
        """Returns the number of atoms in the molecule."""
        return self._mol.NumAtoms()

    @property
    def num_bonds(self) -> int:
        """Returns the number of bonds in the molecule."""
        return self._mol.NumBonds()

    @property
    def coordinates(self) -> np.ndarray:
        """
        Returns the 3D coordinates of the molecule in a numpy array.

        Returns
        -------
        numpy [nAtoms,3]
        """
        ret = np.empty([self._mol.NumAtoms(), 3])
        coords_dict = self._mol.GetCoords()
        for i, atom in enumerate(self._mol.GetAtoms()):
            ret[i] = coords_dict[atom.GetIdx()]
        return ret

    @coordinates.setter
    def coordinates(self, positions: np.ndarray) -> None:
        """
        Sets the 3D coordinates of the molecule from a numpy array.

        Parameter
        --------
        positions: numpy [natoms,3]
        """
        oe_coords = np.empty((self._mol.GetMaxAtomIdx(), 3))
        for i, atom in enumerate(self._mol.GetAtoms()):
            oe_coords[atom.GetIdx()] = positions[i]
        self._mol.SetCoords(oe_coords.reshape(-1))

    @property
    def atoms(self):
        return [Atom(at) for at in self._mol.GetAtoms()]

    @property
    def atom_symbols(self) -> typing.List[str]:
        """Returns a list of atomic symbols."""
        atom_sym: typing.List[str] = []
        for atom in self._mol.GetAtoms():
            atom_sym.append(oechem.OEGetAtomicSymbol(atom.GetAtomicNum()))
        return atom_sym

    @property
    def atom_types(self) -> typing.List[int]:
        """Returns a list of atomic numbers."""
        atom_types: typing.List[int] = []
        for atom in self._mol.GetAtoms():
            atom_types.append(atom.GetAtomicNum())
        return atom_types

    def delete_atom(self, at:BaseAtom):
        """
        :param at: atom to be deleted
        """
        self._mol.DeleteAtom(at._at) # pylint: disable=W0212

    @property
    def canonical_smiles(self) -> str:
        """Returns the canonical smiles representation of the molecule."""
        return oechem.OEMolToSmiles(self._mol)

    @property
    def canonical_non_isomeric_smiles(self) -> str:
        """Returns the canonical non-isomeric smiles representation of the molecule."""
        return oechem.OECreateCanSmiString(self._mol)

    @property
    def title(self) -> str:
        """Returns the title of the molecule."""
        return self._mol.GetTitle()

    @title.setter
    def title(self, value:str):
        """Sets the title of the molecule."""
        self._mol.SetTitle(value)

    def __contains__(self, key: str) -> bool:
        return oechem.OEHasSDData(self._mol, key)

    def __getitem__(self, key: str) -> Any:
        if super().__contains__(key): return super().__getitem__(key)

        if oechem.OEHasSDData(self._mol, key):
            return oechem.OEGetSDData(self._mol, key)
        # pylint: disable=C0209
        raise KeyError("{} has no key {!r}".format(self.__class__.__name__, key))

    def __setitem__(self, key: str, value: Any):
        super().__setitem__(key,value)
        oechem.OESetSDData(self._mol, key, str(value))

    def keys(self) -> typing.Iterator[str]:
        """Yields the property names (SD tag) of the molecule."""
        # This is likely not thread-safe - what happens if a data pair
        # is added/deleted between iterations?
        for data_pair in oechem.OEGetSDDataPairs(self._mol):
            yield data_pair.GetTag()

    def items(self) -> typing.Iterator[typing.Tuple[str, Any]]:
        """Yields the property key - data pairs(SD data) of the molecule."""
        # This is likely not thread-safe - what happens if a data pair
        # is added/deleted between iterations?
        for data_pair in oechem.OEGetSDDataPairs(self._mol):
            key = data_pair.GetTag()
            if super().__contains__(key) :
                yield (key, super().__getitem__(key))
            else:
                yield (data_pair.GetTag(), data_pair.GetValue())

    def __delitem__(self, key):
        """Removes a specific property (SD data) from the molecule."""
        if super().__contains__(key): super().__delitem__(key)
        oechem.OEDeleteSDData(self._mol, key)

    @property
    def mol_file(self):
        """Returns the MDL representation of the molecule."""
        ofs = oechem.oemolostream()
        ofs.openstring()
        ofs.SetFormat(oechem.OEFormat_MDL)
        my_mol = oechem.OEGraphMol(self._mol)
        # OEWriteMolecule will modify molecule
        oechem.OEWriteMolecule(ofs, my_mol)
        mol_str = ofs.GetString()
        ofs.close()

        return mol_str.decode('utf8')


def from_smiles(smi: str) -> Mol:
    """Creates a molecule object from a smiles string """
    mol = oechem.OEGraphMol()
    oechem.OESmilesToMol(mol, smi)
    return Mol(mol)
