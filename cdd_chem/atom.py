"""
(C) 2020 Genentech. All rights reserved.

Created on Feb 13, 2019

@author: albertgo

Abstract base class for objects representing an atom.
"""

from abc import ABCMeta
from abc import abstractmethod


class BaseAtom(metaclass=ABCMeta):
    """Abstract class hiding the internal representation of an atom object."""

    def __init__(self, native_atom_object):
        self._at = native_atom_object

    @property # type: ignore
    @abstractmethod
    def atomic_num(self) -> int:
        """Returns the atomic number."""

    @atomic_num.setter # type: ignore
    @abstractmethod
    def atomic_num(self, num:int):
        """ set the atomic number of this atom """


    @property
    @abstractmethod
    def symbol(self) -> str:
        """Returns the atomic symbol."""

    @property
    @abstractmethod
    def index(self) -> int:
        """Returns index of atom in molecule."""

    @property
    @abstractmethod
    def total_hydrogen_count(self) -> int:
        """Returns the total hydrogen count (implicit + explicit) of the atom."""

    @property
    @abstractmethod
    def formal_charge(self) -> int:
        """Returns the formal charge of this atom."""
