"""
(C) 2020 Genentech. All rights reserved.

Created on Jul 1, 2018

@author: Krisztina Boda

Module for performing operations related to chemical scaffolds
"""


import re
import shutil
from typing import Dict

from openeye import oechem


def scaff_mol_to_smirks(scaffold_file: str) -> str:
    '''Convert scaffold in MDL mol file format to SMIRKS representing reaction
       to fragment molecule into scaffold and R groups
       inspired by scaffoldToSmirks in
       https://github.com/chemalot/autocorrelator/blob/master/src/autocorrelator/apps/SdfTransformer.java

       @TODO make more general so it can take table of SMILES

    Parameters
    ----------
    scaffold_file
        path to MDL mol scaffold file
    Returns
    -------
    str
        SMIRKS string representing fragmenting reaction
    '''

    smi_flags = oechem.OEOFlavor_SMI_AtomStereo | \
        oechem.OEOFlavor_SMI_BondStereo | \
        oechem.OEOFlavor_SMI_AtomMaps | \
        oechem.OEOFlavor_SMI_Isotopes
    scaffold = oechem.OEGraphMol()
    reader = oechem.oemolistream()
    reader.open(scaffold_file)
    reader.SetFormat(oechem.OEFormat_MDL)
    oechem.OEReadMolecule(reader, scaffold)
    oechem.OEAssignAromaticFlags(scaffold)

    for atom in scaffold.GetAtoms():
        atom_name = atom.GetName()
        if atom_name != '' and atom_name[0] == 'R':
            atom.SetAtomicNum(oechem.OEElemNo_U)
            atom.SetFormalCharge(int(atom_name[1:]))

    rg_pos_to_atom_map: Dict[int, oechem.OEAtomBase] = {}
    at_map_idx = 1
    for atom in scaffold.GetAtoms():
        charge = atom.GetFormalCharge()
        if charge > 0 and atom.GetAtomicNum() == oechem.OEElemNo_U:
            if charge in rg_pos_to_atom_map:
                raise RuntimeError(f'U+{charge} found multiple times')
            charge += 10
            atom.SetFormalCharge(charge)
            rg_pos_to_atom_map[charge] = atom
        else:
            atom.SetMapIdx(at_map_idx)
            at_map_idx += 1
            atom.SetImplicitHCount(0)

    product_smi = oechem.OECreateSmiString(scaffold, smi_flags)

    for pos, atom in rg_pos_to_atom_map.items():
        atom.SetAtomicNum(0)
        atom.SetFormalCharge(0)
        atom.SetMapIdx(at_map_idx)

        product_smi += f'.[U+{pos - 10}][*:{at_map_idx}]'
        at_map_idx += 1

    smirks = oechem.OECreateSmiString(scaffold, smi_flags) + '>>' + product_smi

    return smirks


def identify_core_in_smirks(smirks: str) -> str:
    """look for molecule with more than one U+ on product side of SMIRKS string
       and tag that molecule as the core by adding 10 to the charges
       representing the attachment points.  If no product has more than one
       attachment point pick the first fragment as core.

    Parameters
    ----------
    smirks
        SMIRKS string representing reaction with attachment points
        represented as U+charge where charge indicates R group
        mapping (as opposed to SMIRKS atom mapping)
    Returns
    -------
    str
        SMIRKS string as above with the U+charge adjusted to indicate which
        fragment is considered the core (scaffold)
    """

    reactant = smirks.split('>>')[0]
    products = smirks.split('>>')[1].split('.')
    core = None
    core_index = -1
    for product_index, product in enumerate(products):
        if len(re.findall(r'U\+\d?', product)) > 1:
            if core is not None:
                raise RuntimeError(f'More than one fragment with two or more '
                                   f'attachment points: {core}, {product}')
            core = product
            core_index = product_index
    if core is None:    # nothing found with > 1 attachment point pick first fragment as core
        core = products[0]
        core_index = 0
    core_molecule = oechem.OEGraphMol()
    if not oechem.OESmilesToMol(core_molecule, core):
        raise RuntimeError('Core molecule ({core_molecule}) is not valid')
    for atom in core_molecule.GetAtoms():
        if atom.GetAtomicNum() == oechem.OEElemNo_U:
            charge = atom.GetFormalCharge()
            if charge < 11:  # if charge >= 11 the core was already marked
                atom.SetFormalCharge(charge + 10)
    core_smirks = oechem.OEMolToSmiles(core_molecule)
    products[core_index] = core_smirks
    return reactant + '>>' + '.'.join(products)


def mark_smirks_cores(smirks_file: str) -> None:
    """rewrite SMIRKS file with following convention
       to mark core in product with charges > 10;
       c.f., identify_core_in_smirks, above

    Parameters
    ----------
    smirks_file
        path of file containing SMIRKS string to convert; should
        have format of SMIRKS name
                       SMIRKS name

    Returns
    -------
    None
        Side effect: smirks_file will be rewritten
    """
    #pylint:  disable=W1514
    with open(smirks_file, "r") as smirks_in_file, \
            open(smirks_file + ".tmp", "w") as smirks_out_file:   #pylint: disable=W1514
        for smirks_line in smirks_in_file:
            if smirks_line.startswith('#'):
                smirks_out_file.write(smirks_line)
            else:
                smirks_split = smirks_line.split()
                if len(smirks_split) == 2:
                    smirks, name = smirks_split
                    smirks = identify_core_in_smirks(smirks)
                    smirks_out_file.write(f'{smirks}\t{name}')
    shutil.move(smirks_file, smirks_file + ".bak")
    shutil.move(smirks_file + ".tmp", smirks_file)
