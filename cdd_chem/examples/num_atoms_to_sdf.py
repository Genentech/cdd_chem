#!/usr/bin/env python3
"""
(C) 2020 Genentech. All rights reserved.

cdd_chem example script
'"""
import argparse
import sys

from cdd_chem.io import get_mol_input_stream, get_mol_output_stream


def main() -> int:
    """Console script"""
    args = parse_options()

    with get_mol_input_stream(args.input) as in_file, get_mol_output_stream(args.output) as out_file:
        for mol in in_file:
            # set SD tag data (that has to be a string)
            mol['num_atoms'] = str(mol.num_atoms)
            out_file.write_mol(mol)
    return 0


def parse_options() -> argparse.Namespace:
    """Parse main options."""
    parser = argparse.ArgumentParser(description="Command line arguments:")
    parser.add_argument('--input', type=str, metavar='molfile', required=True, help='input molecule file')
    parser.add_argument('--output', type=str, metavar='molfile', required=True, help='output molecule file')
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
