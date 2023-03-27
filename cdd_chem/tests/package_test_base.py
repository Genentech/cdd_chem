"""
(C) 2020 Genentech. All rights reserved.

Tests for cdd_chem package
"""

import os

import cdd_chem.examples
import cdd_chem.tests

from . import run_script


class PackageTestBase:
    """Base test class."""

    @classmethod
    def setup_class(cls):
        """Sets up test class."""

        cls._examples_dir = os.path.dirname(cdd_chem.examples.__file__)
        cls._data_dir = f"{os.path.dirname(cdd_chem.tests.__file__)}/data"

    def test_mol_from_smiles(self):
        """Tests mol_from_smiles.py doc example."""
        # pylint: disable=R0201
        toolkit = os.environ.get("CDDLIB_TOOLKIT", "")
        assert (toolkit in ['openeye', 'rdkit'])

        pyscript = os.path.join(self._examples_dir, "mol_from_smiles.py")
        script = run_script(pyscript)
        assert script.returncode == 0

    def test_num_atoms_to_sdf(self):
        """Tests num_atoms_to_sdf.py doc example."""
        toolkit = os.environ.get("CDDLIB_TOOLKIT", "")
        assert (toolkit in ['openeye', 'rdkit'])

        pyscript = os.path.join(self._examples_dir, "num_atoms_to_sdf.py")

        in_file_name = os.path.join(self._data_dir, "benzene.sdf")
        out_file_name = "benzene-data.sdf"

        script = run_script(pyscript, "--input", in_file_name, "--output", out_file_name)
        assert script.returncode == 0
        assert out_file_name in script.files_created

    def test_dataframe_io(self):
        """Tests dataframe_io.py doc example."""
        toolkit = os.environ.get("CDDLIB_TOOLKIT", "")
        assert (toolkit in ['openeye', 'rdkit'])

        pyscript = os.path.join(self._examples_dir, "dataframe_io.py")

        in_csv = os.path.join(self._data_dir, "training_data_desc_10.csv")
        out_sdf = "df.sdf"
        in_sdf = os.path.join(self._data_dir, "test.sdf")
        out_csv = "df.csv"

        script = run_script(pyscript,
                            "--input-dataframe", in_csv,
                            "--output-sd", out_sdf,
                            "--input-sd", in_sdf,
                            "--output-dataframe", out_csv)

        assert script.returncode == 0
        assert out_sdf in script.files_created
        assert out_csv in script.files_created
