"""
(C) 2020 Genentech. All rights reserved.

Test file for cdd_chem module.
"""

import importlib
import os

import pytest
import pytest_check as check

from cdd_chem import mol
from cdd_chem.rdkit.mol import from_smiles
from .utils_test import new_molecule_for_testing

try:
    from rdkit import Chem
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError("RDKit Toolkit not found, some tests will fail") from exc


TEST_TOOLKIT: str = "rdkit"


class TestChemRDKit:
    """Test class for testing cdd_chem with RDKit."""

    @classmethod
    def setup_class(cls):
        """Setup method for test class."""

    def setup_method(self):
        """Setup method for each test."""
        # pylint: disable=attribute-defined-outside-init
        # pylint: disable=E1101
        rd_mol = Chem.MolFromSmiles("C1CCN[C@@H]1(O)")
        self.rd_molecule = new_molecule_for_testing(TEST_TOOLKIT, rd_mol)

    def test_mol_with_rdkit(self):
        # pylint: disable=protected-access
        # pylint: disable=I1101
        check.is_true(isinstance(self.rd_molecule, mol.BaseMol))
        check.is_true(isinstance(self.rd_molecule._mol, Chem.rdchem.Mol))

    def test_mol_num_atoms_with_rdkit(self):
        check.equal(6, self.rd_molecule.num_atoms)

    def test_mol_num_bonds_with_rdkit(self):
        check.equal(6, self.rd_molecule.num_bonds)

    def test_mol_formal_charge_with_rdkit(self):
        check.equal(0, self.rd_molecule.formal_charge)

    def test_canonical_smiles_with_rdkit(self):
        check.equal("O[C@@H]1CCCN1", self.rd_molecule.canonical_smiles)

    def test_canonical_non_isometic_smiles_with_rdkit(self):
        check.equal("OC1CCCN1", self.rd_molecule.canonical_non_isomeric_smiles)

    def test_mol_atoms_with_rdkit(self):
        check.equal("C", self.rd_molecule.atoms[0].symbol)
        for index, hcount in enumerate([2, 2, 2, 1, 1, 1]):
            message = f"at index {index} expected {hcount}"
            check.equal(hcount, self.rd_molecule.atoms[index].total_hydrogen_count, message)

    def test_mol_set_get_item_with_rdkit(self):
        self.rd_molecule["TestProp"] = "TEST"
        check.equal("TEST", self.rd_molecule["TestProp"])

    def test_mol_raises_key_error_with_rdkit(self):
        message = r"Mol has no key \'Test Prop\'"
        with pytest.raises(KeyError, match=message):
            value = self.rd_molecule["Test Prop"]  # noqa: F841
            print(value)  # this should not be reached

    def test_molfile(self):
        mol_string = self.rd_molecule.mol_file
        check.equal(18, len(mol_string.split("\n")))

    def test_sdf_record(self):
        sdf_string = self.rd_molecule.sdf_record
        check.equal(19, len(sdf_string.split("\n")))

        # check that SD data is not lost
        self.rd_molecule['test'] = 'foo\nbar\n'
        sdf_string = self.rd_molecule.sdf_record
        check.equal(23, len(sdf_string.split("\n")))
        check.is_true('> <test>' in sdf_string)
        check.is_true('foo\n' in sdf_string)
        check.is_true('bar\n' in sdf_string)


    def test_index(self):
        idxs = [at.index for at in self.rd_molecule.atoms]
        assert idxs == [0, 1, 2, 3, 4, 5]


    def test_atomic_num(self):
        ats = list( self.rd_molecule.atoms )
        atNum = [at.atomic_num for at in ats]
        atsStr = str.join(",", [at.symbol for at in ats])
        assert atsStr == "C,C,C,N,C,O"

        for at in ats: at.atomic_num = 2
        atsStr = str.join(",", [at.symbol for at in ats])
        assert atsStr == "He,He,He,He,He,He"

        for at, num in zip(ats, atNum): at.atomic_num = num

        check.equal("OC1CCCN1", self.rd_molecule.canonical_non_isomeric_smiles)


def test_from_smiles():
    # pylint: disable=protected-access
    # pylint: disable= I1101
    mol_module = importlib.import_module("cdd_chem.rdkit.mol")
    check.is_true(hasattr(mol_module, 'from_smiles'))
    rd_mol = mol_module.from_smiles("CCCC")
    check.is_true(isinstance(rd_mol, mol.BaseMol))
    check.is_true(isinstance(rd_mol._mol, Chem.rdchem.Mol))

    rd_mol['ID'] = "testValue"
    check.equal(rd_mol['ID'], "testValue")


def test_mol_sd_properties_with_rdkit(shared_datadir):
    # pylint: disable=E1101
    sdf_mol_supplier = Chem.SDMolSupplier(os.path.join(shared_datadir / "test_CCCO_confs.sdf"))

    rd_mol = new_molecule_for_testing(TEST_TOOLKIT, sdf_mol_supplier[0])
    check.is_true(isinstance(rd_mol, mol.BaseMol))

    check.equal(rd_mol["Total_energy"].strip(), "-6.4528")
    check.equal(rd_mol["MMFF Bond"].strip(), "0.1421")
    check.is_true(tuple(rd_mol.keys()) == ("MMFF VdW", "MMFF Bond", "MMFF Bend", "MMFF StretchBend",
                                           "MMFF Torsion", "Sheffield Solvation",
                                           "Ligand MMFF Intramol. Energy",
                                           "Total_energy"))

    assert(list(rd_mol.items()) == [('MMFF VdW', '   1.7969'),
                                    ('MMFF Bond', '   0.1421'),
                                    ('MMFF Bend', '   0.2773'),
                                    ('MMFF StretchBend', '   0.0063'),
                                    ('MMFF Torsion', '  -3.9742'),
                                    ('Sheffield Solvation', '  -4.7012'),
                                    ('Ligand MMFF Intramol. Energy', '  -1.7516'),
                                    ('Total_energy', '  -6.4528')])

    check.is_true("Total_energy" in rd_mol.keys())
    del rd_mol["Total_energy"]
    check.is_false("Total_energy" in rd_mol.keys())


def test_delete_atom():
    # pylint: disable=protected-access
    rd_mol = from_smiles("COCC")
    rd_mol.make_read_write()
    atList = list(rd_mol.atoms)
    rd_mol.delete_atom(atList[0])
    rd_mol.delete_atom(atList[1])

    ### note this is a difference to oechem where the result is a radical
    assert "CC" == rd_mol.canonical_smiles

    rd_mol.make_read_only()
    assert "CC" == rd_mol.canonical_smiles


def test_removeH(): # noqa: N802
    mmol = from_smiles("[H]O[H]")
    ats = list( mmol.atoms )
    atsStr = str.join(",", [at.symbol for at in ats])
    assert atsStr == "O"

    mmol.addH()
    ats = list( mmol.atoms )
    atsStr = str.join(",", [at.symbol for at in ats])
    assert atsStr == "O,H,H"

    mmol.removeH()
    ats = list( mmol.atoms )
    atsStr = str.join(",", [at.symbol for at in ats])
    assert atsStr == "O"
