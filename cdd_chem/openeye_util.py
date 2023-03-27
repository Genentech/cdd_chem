"""
(C) 2020 Genentech. All rights reserved.

Created on Feb 13, 2019

@author: albertgo

Module for Openeye utilities.
"""

from openeye import oechem


def createMol(molfile):  # noqa: N802
    # pylint:  disable=invalid-name
    """
    Returns an OEGraphMol with the given molfile

    @type molfile: str
    @param molfile: The molfile representation of the molecule

    @rtype: OEGraphMol
    @return: The OEGraphMol of the molecule
    """
    mol = oechem.OEGraphMol()
    mol = stringToMol(mol, molfile)
    return mol


def addSDData(mol, sd_data):  # noqa: N802
    # pylint:  disable=invalid-name
    """
    Append the SD data from a dictionary to the mol

    @type mol: OEGraphMol
    @param mol: The molecule to which parameters are added
    @type sd_data: dict
    @param sd_data: key value pairs to assign to the molecule

    @rtype: OEGraphMol
    @return: the molecule with append SD data pairs
    """
    for key, value in sd_data.items():
        oechem.OEAddSDData(mol, key, value)


def writeSDFile(mol_list, output_file):  # noqa: N802
    # pylint:  disable=invalid-name
    """
    Write the list of molecules to the output file

    @type molList: list
    @param molList: List of OEGraphMols to be writen to file
    @type: str
    @param outputFile: The output file name
    """
    ofs = oechem.oemolostream()

    if output_file and not ofs.open(output_file):
        oechem.OEThrow.Fatal('Cannot open: %s', output_file)

    if not oechem.OEIsWriteable(oechem.OEFormat_SDF):
        oechem.OEThrow.Fatal('%s format not writeable', oechem.OEGetFormatString(oechem.OEFormat_SDF))

    for mol in mol_list:
        oechem.OEWriteMolecule(ofs, mol)

    ofs.close()


def stringToMol(mol, mol_str):  # noqa: N802
    # pylint:  disable=invalid-name
    """
    Create a OEGraphMol from a molfile string

    @type mol: OEGraphMol
    @param mol: The molecule
    @type mol_str: str
    @param mol_str: The string representation of the molfile

    @rtype: OEGraphMol
    @return: The mol with the given molecule
    """
    ifs = oechem.oemolistream()
    ifs.openstring(mol_str)
    ifs.SetFormat(oechem.OEFormat_MDL)

    oechem.OEReadMolecule(ifs, mol)
    ifs.close()

    return mol
