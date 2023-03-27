#!/usr/bin/env python3
"""
(C) 2020 Genentech. All rights reserved.

cdd_chem example script
'"""
import cdd_chem

print("utilizing toolkit:", cdd_chem.get_toolkit())
mol = cdd_chem.from_smiles("c1ccccc1")
print("molecule type", type(mol))
print("number of atoms", mol.num_atoms)
