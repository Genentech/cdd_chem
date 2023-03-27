"""
(C) 2020 Genentech. All rights reserved.

Test file for cdd_chem module.
"""
import importlib
import os
import pytest

import pytest_check as check

from cdd_chem import mol
from cdd_chem.oechem.mol import from_smiles

from .utils_test import new_molecule_for_testing

try:
    from openeye import oechem
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError("Openeye Toolkit not found, some tests will fail") from exc

TEST_TOOLKIT: str = "openeye"


class TestChemOpeneye:
    """Test class for testing cdd_chem with OpenEye."""

    @classmethod
    def setup_class(cls):
        """Setup method for test class."""

    def setup_method(self):
        """Setup method for each test."""
        # pylint: disable=attribute-defined-outside-init
        oe_mol = oechem.OEGraphMol()
        check.is_true(oechem.OESmilesToMol(oe_mol, "C1CCN[C@@H]1(O)"))
        self.oe_molecule = new_molecule_for_testing(TEST_TOOLKIT, oe_mol)

    def test_mol_with_openeye(self):
        # pylint: disable=protected-access
        check.is_true(isinstance(self.oe_molecule, mol.BaseMol))
        check.is_true(isinstance(self.oe_molecule._mol, oechem.OEMolBase))

    def test_mol_num_atoms_with_openeye(self):
        check.equal(7, self.oe_molecule.num_atoms)

    def test_mol_num_bonds_with_openeye(self):
        check.equal(7, self.oe_molecule.num_bonds)

    def test_mol_formal_charge_with_openeye(self):
        check.equal(0, self.oe_molecule.formal_charge)

    def test_canonical_smiles_with_openeye(self):
        check.equal("C1C[C@H](NC1)O", self.oe_molecule.canonical_smiles)

    def test_canonical_non_isometic_smiles_with_openeye(self):
        check.equal("C1CC(NC1)O", self.oe_molecule.canonical_non_isomeric_smiles)

    def test_mol_atoms_with_openeye(self):
        check.equal("C", self.oe_molecule.atoms[0].symbol)
        for index, hcount in enumerate([2, 2, 2, 1, 1, 0, 1]):
            message = f"at index {index} expected {hcount}"
            check.equal(hcount, self.oe_molecule.atoms[index].total_hydrogen_count, message)

    def test_mol_raises_key_error_with_openeye(self):
        message = r"Mol has no key \'Test Prop\'"
        with pytest.raises(KeyError, match=message):
            value = self.oe_molecule["Test Prop"]  # noqa: F841
            print(value)  # this should not be reached

    def test_mol_set_get_item_with_openeye(self):
        self.oe_molecule["TestProp"] = "TEST"
        check.equal("TEST", self.oe_molecule["TestProp"])

    def test_molfile(self):
        mol_string = self.oe_molecule.mol_file
        check.equal(20, len(mol_string.split("\n")))

    def test_sdf_record(self):
        sdf_string = self.oe_molecule.sdf_record
        check.equal(21, len(sdf_string.split("\n")))

        # check that SD data is not lost
        self.oe_molecule['test'] = 'foo\nbar\n'
        sdf_string = self.oe_molecule.sdf_record
        check.equal(25, len(sdf_string.split("\n")))
        check.is_true('> <test>' in sdf_string)
        check.is_true('foo\n' in sdf_string)
        check.is_true('bar\n' in sdf_string)

    def test_index(self):
        idxs = [at.index for at in self.oe_molecule.atoms]
        assert idxs == [0, 1, 2, 3, 4, 5, 6]


    def test_atomic_num(self):
        ats = list( self.oe_molecule.atoms )
        atNum = [ at.atomic_num for at in ats ]
        atsStr = str.join(",",[ at.symbol for at in ats ])
        assert atsStr == "C,C,C,N,C,H,O"

        for at in ats: at.atomic_num = 2
        atsStr = str.join(",",[ at.symbol for at in ats ])
        assert atsStr == "He,He,He,He,He,He,He"

        for at, num in zip(ats, atNum): at.atomic_num = num

        check.equal("C1CC(NC1)O", self.oe_molecule.canonical_non_isomeric_smiles)


def test_from_smiles():
    # pylint: disable=protected-access
    mol_module = importlib.import_module("cdd_chem.oechem.mol")
    check.is_true(hasattr(mol_module, 'from_smiles'))
    oe_mol = mol_module.from_smiles("CCCC")
    check.is_true(isinstance(oe_mol, mol.BaseMol))
    check.is_true(isinstance(oe_mol._mol, oechem.OEGraphMol))

    oe_mol['ID'] = "testValue"
    check.equal(oe_mol['ID'], "testValue")


def test_mol_sd_properties_with_openeye(shared_datadir):
    ifs = oechem.oemolistream(os.path.join(shared_datadir / "test_CCCO_confs.sdf"))
    new_mol = oechem.OEGraphMol()
    check.is_true(oechem.OEReadMolecule(ifs, new_mol))

    oe_mol = new_molecule_for_testing(TEST_TOOLKIT, new_mol)
    check.is_true(isinstance(oe_mol, mol.BaseMol))

    check.equal("-6.4528", oe_mol["Total_energy"].strip())
    check.equal("0.1421", oe_mol["MMFF Bond"].strip())
    assert(tuple(oe_mol.keys()) == ("MMFF VdW", "MMFF Bond", "MMFF Bend", "MMFF StretchBend",
                                    "MMFF Torsion", "Sheffield Solvation",
                                    "Ligand MMFF Intramol. Energy",
                                    "Total_energy"))

    assert(list(oe_mol.items()) == [('MMFF VdW', '   1.7969'),
                                    ('MMFF Bond', '   0.1421'),
                                    ('MMFF Bend', '   0.2773'),
                                    ('MMFF StretchBend', '   0.0063'),
                                    ('MMFF Torsion', '  -3.9742'),
                                    ('Sheffield Solvation', '  -4.7012'),
                                    ('Ligand MMFF Intramol. Energy', '  -1.7516'),
                                    ('Total_energy', '  -6.4528')])

    check.is_true("Total_energy" in oe_mol.keys())
    del oe_mol["Total_energy"]
    check.is_false("Total_energy" in oe_mol.keys())

def test_delete_atom():
    oe_mol = from_smiles("COCC")
    oe_mol.make_read_write()
    atList = list(oe_mol.atoms)
    oe_mol.delete_atom(atList[0])
    oe_mol.delete_atom(atList[1])
    oe_mol.make_read_only()
    assert "C[CH2]" == oe_mol.canonical_smiles


def test_removeH(): # noqa: N802
    mmol = from_smiles("O")
    ats = list(mmol.atoms)
    atsStr = str.join(",", [at.symbol for at in ats])
    assert atsStr == "O"

    mmol.addH()
    ats = list(mmol.atoms)
    atsStr = str.join(",", [at.symbol for at in ats])
    assert atsStr == "O,H,H"

    mmol.removeH()
    ats = list(mmol.atoms)
    atsStr = str.join(",", [at.symbol for at in ats])
    assert atsStr == "O"
