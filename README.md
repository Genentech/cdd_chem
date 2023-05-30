# CDD Chem Library

General purpose helper classes around the [RDKit](https://www.rdkit.org/) and
[Openeye](https://www.eyesopen.com/) toolkits for handling molecular input files.
This packages tries to abstract the toolkits away and thus provides a toolkit
independent interface to dealing with molecular files and, to some extend, with
molecule objects.

The underlying toolkit can be set with `cdd_chem.toolkit.set_toolkit`.  If it's not
set then the underlying toolkit is taken from the `CDDLIB_TOOLKIT` environment
variable. If this environment variable is not set then the default toolkit will be
`oechem` provided that `oechem` can be imported.  Otherwise the toolkit will be set
to `rdkit`.

The package is still under development but here is an example on how to get started:

```
#!/usr/bin/env python3

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
```

## Features

Toolkit-agnostic features for:

- Reading and writing molecules to SD files
- Converting between molecules and SMILES
- Setting and retrieving properties of molecules
- Reading and writing pandas dataframes containing representations of molecules with properties

## Credits

This Python package was created with

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
