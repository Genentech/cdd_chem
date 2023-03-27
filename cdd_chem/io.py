"""
(C) 2020 Genentech. All rights reserved.

Created on Feb 13, 2019

@author: albertgo

Module to provide input/output operations for the generic (toolkit agnostic)
chemistry API.
'"""

import typing

from abc import ABCMeta
from abc import abstractmethod
from collections import deque
from importlib import import_module
from typing import Optional, Dict

import numpy
import pandas
from pandas import DataFrame

from cdd_chem.mol import BaseMol, from_smiles
from cdd_chem.toolkit import get_toolkit
from cdd_chem.util.IterableAlgorithm import IterableAlgorithm
from cdd_chem.util import bit_vector


class BaseMolInputStream(IterableAlgorithm[BaseMol], metaclass=ABCMeta):
    """Base Class for reading molecule objects."""

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @abstractmethod
    def has_next(self) -> bool:
        """Checks whether iterator still has molecules."""

    @abstractmethod
    def __next__(self):
        """Moves iterator forward"""

    def close(self):
        """Terminates the iterator and free the list of molecules."""


class MemMolStream(BaseMolInputStream):
    """Molecule stream that holds a list of molecules in memory."""

    def __init__(self, mol_list: typing.List[BaseMol] = None) -> None:
        '''
        Initializes this in memory MolStream

        Arguments
        ---------
        init_list
            list of molecules to be in the stream, you may also use add_mol
            later.

        '''
        super().__init__()

        self._mols: typing.Deque[BaseMol] = deque()
        if mol_list is not None:
            for mol in mol_list:
                self._mols.append(mol)

    def add_mol(self, mol: BaseMol) -> None:
        """Adda molecule to the internal list.

        Parameters
        ----------
        mol
            Molecule to append.

        Returns
        -------
        None
        """
        self._mols.append(mol)

    def __enter__(self):
        return self

    def has_next(self) -> bool:
        """Checks whether iterator still has molecules.

        Parameters
        ----------
        None

        Returns
        -------
        bool
            True is molecules still in list; False otherwise
        """
        if len(self._mols) > 0:
            return True
        return False

    def __iter__(self):
        return self

    def __next__(self) -> BaseMol:
        try:
            return self._mols.popleft()
        except IndexError:
            raise StopIteration() # pylint: disable=W0707

    def __exit__(self, *args):
        self.close()

    def close(self) -> None:
        """Terminates the iterator and free the list of molecules.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._mols.clear()


class BaseMolOutputStream(metaclass=ABCMeta):
    """Molecule output stream for writing molecules to file using the OpenEye toolkit."""

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    @abstractmethod
    def write_mol(self, mol:BaseMol):
        """Writes molecule to stream."""
        pass # pylint: disable=W0107

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    @abstractmethod
    def close(self):
        """Closes output stream."""


def get_mol_input_stream(*args, **kwargs) -> BaseMolInputStream:
    """Create an input stream for molecules.
        Depending on the TOOLKIT variable this will be either RDKit or Openeye.
    """

    io_module = _import_iomodule(get_toolkit())
    instance = io_module.MolInputStream(*args, **kwargs)
    return instance


def get_mol_output_stream(*args, **kwargs) -> BaseMolOutputStream:
    """Create an output stream for molecules.
       Depending on the TOOLKIT variable this will be either RDKit or Openeye.
    """

    io_module = _import_iomodule(get_toolkit())
    instance = io_module.MolOutputStream(*args, **kwargs)
    return instance


def _import_iomodule(toolkit: str):
    if toolkit == "openeye":
        io_module = import_module("cdd_chem.oechem.io")
    elif toolkit == "rdkit":
        io_module = import_module("cdd_chem.rdkit.io")
    else:
        raise ValueError(f"TOOLKIT ({toolkit}) not recognized."
                         " Expected values are openeye or rdkit."
                         " You can specify the 'CDDLIB_TOOLKIT' environment variable")
    return io_module


# pylint: disable=R0913
def dataframe_to_sd_file(dataframe: DataFrame,
                         smiles_column: str,
                         id_column: str,
                         file_path: str,
                         fingerprint_sd_field_name: Optional[str] = None,
                         fingerprint_column_prefix: Optional[str] = None) -> None:
    """Write compounds and associated descriptor data from pandas
       DataFrame to SD file, if a fingerprint is included
       (implied by providing fingerprint_column_prefix)
       write a base64 encoded representation of the fingerprint

       Parameters
       ----------
       dataframe
           data to write
       smiles_column
           name of column containing SMILES for compound
       id_column
           name of column containing identifier for compound
       file_path
           path to output sd file
       fingerprint_sd_field_name
           tag for writing fingerprint to sd file
       fingerprint_column_prefix
           prefix of columns containing fingerprint bits

       Returns
       -------
           None
    """
    print(f"HERE: TOOLKIT={get_toolkit()}")
    field_index = {kee: i for i, kee in enumerate(list(dataframe))}
    with get_mol_output_stream(file_path) as writer:
        fingerprint_fields = []
        if fingerprint_column_prefix is not None:
            fingerprint_fields = [kee for kee in field_index if fingerprint_column_prefix in kee]
        for row in dataframe.itertuples(index=False):
            the_mol = from_smiles(row[field_index[smiles_column]])
            the_mol.title = row[field_index[id_column]]
            if fingerprint_fields != []:
                fingerprint_bits = row[field_index[fingerprint_fields[0]]:
                                       field_index[fingerprint_fields[-1]] + 1]
                fingerprint = bit_vector.to_base64(numpy.asarray(fingerprint_bits))
            for kee in field_index:
                if kee == smiles_column:
                    continue
                if fingerprint_fields != [] and kee == fingerprint_fields[0]:
                    the_mol[typing.cast(str, fingerprint_sd_field_name)] = fingerprint.decode()
                if kee in fingerprint_fields:
                    continue
                if pandas.isna(row[field_index[kee]]):
                    the_mol[kee] = ""
                else:
                    the_mol[kee] = str(row[field_index[kee]])
            writer.write_mol(the_mol)


# pylint: disable=R0912,R0913,R0914
def dataframe_from_sd_file(file_path: str,
                           smiles_column: str,
                           smiles_index: int,
                           id_column: Optional[str] = None,
                           id_field_name: Optional[str] = None,
                           id_index: Optional[int] = None,
                           fingerprint_sd_field_name: Optional[str] = None,
                           fingerprint_bit_data_type: Optional[type] = None,
                           fingerprint_column_prefix: Optional[str] = None,
                           column_dtypes: Optional[Dict[str, str]] = None) -> DataFrame:
    """Read compounds and associated descriptor data from an SD file into
       a pandas DataFrame.

       Parameters
       ----------
       file_path
           path to input sd file
       smiles_column
           name of column in which to store SMILES representation of molecule
       smiles_index
           index at which to insert SMILES in column list
       id_column
           name of column in which to store unique identifier for molecule
       id_field_name
           tag for reading unique identifier for molecule; if None take
           identifier from molecule title
       id_index
           index at which to inset unique identifier in column list; note
           this is inserted after inserting the SMILES string so account
           for the smiles_index in specifying id_index
       fingerprint_sd_field_name
           tag for reading fingerprint from sd file
       fingerprint_bit_data_type
           data type to use for representing fingerprint bits
       fingerprint_column_prefix
           prefix for generating column names for fingerprint bits
        column_dtypes
           mapping of column names to explicit types, this is currently
           implemented only for numeric types

       Returns
       -------
           Molecules and descriptor data
    """

    data_dict_list = []
    first = True

    with get_mol_input_stream(file_path) as reader:
        for mol in reader:
            if fingerprint_sd_field_name is not None:
                fingerprint_bits = bit_vector.from_base64(mol[fingerprint_sd_field_name].encode(),
                                                          typing.cast(type, fingerprint_bit_data_type))
            if first:
                fields = list(mol.keys())
                fields[smiles_index:smiles_index] = [smiles_column]
                if id_column is not None:
                    fields[id_index:id_index] = [id_column]
                if fingerprint_sd_field_name is not None:
                    fingerprint_index = fields.index(fingerprint_sd_field_name)
                    fingerprint_columns = [f"{fingerprint_column_prefix}{bit:04d}"
                                           for bit in range(fingerprint_bits.size)]
                    fields[fingerprint_index:fingerprint_index+1] = fingerprint_columns
                first = False
            data_dict = {}
            for kee in fields:
                value = mol.get(kee, "")
                try:
                    value = float(value)
                except ValueError:
                    pass
                data_dict[kee] = value
            data_dict[smiles_column] = mol.canonical_smiles
            if id_column is not None:
                if id_field_name is None:
                    data_dict[id_column] = mol.title
                else:
                    data_dict[id_column] = mol.get(id_field_name)
            if fingerprint_sd_field_name is not None:
                for bit in range(fingerprint_bits.size):
                    data_dict[f"{fingerprint_column_prefix}{bit:04d}"] = fingerprint_bits[bit]
            data_dict_list.append(data_dict)
    data = DataFrame(data_dict_list).convert_dtypes()
    if column_dtypes is not None:
        for column, dtype in column_dtypes.items():
            if column in data:
                data[column] = pandas.to_numeric(data[column], errors="coerce").astype(dtype)
    if mixed_dtypes := {c: dtype for c in data.columns if (dtype := pandas.api.types.infer_dtype(data[c])).startswith("mixed")}:
        for column in mixed_dtypes:
            data[column] = data[column].astype(str)

    return data
