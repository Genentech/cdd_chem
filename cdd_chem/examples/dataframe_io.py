#!/usr/bin/env python3
"""
(C) 2020 Genentech. All rights reserved.

cdd_chem example script
'"""
import argparse
import sys

import numpy
import pandas

from cdd_chem.io import dataframe_from_sd_file, dataframe_to_sd_file


def main() -> int:
    """Console script"""
    args = parse_options()

    # read Pandas dataframe from CSV file then write it to SD file
    data = pandas.read_csv(args.input_dataframe)
    dataframe_to_sd_file(data,
                         "CISMILES",
                         "G-Number",
                         args.output_sd,
                         "RD_FP_128",
                         "MFP")

    # read data from SD file into a Pandas dataframe and write to CSV file
    sd_data = dataframe_from_sd_file(args.input_sd,
                                     "CISMILES",
                                     1,
                                     fingerprint_sd_field_name="RD_FP_128",
                                     fingerprint_bit_data_type=numpy.float32,
                                     fingerprint_column_prefix="MFP")
    sd_data.to_csv(args.output_dataframe)

    return 0


def parse_options() -> argparse.Namespace:
    """Parse main options."""
    parser = argparse.ArgumentParser(description="Command line arguments:")
    parser.add_argument('--input-dataframe', type=str, metavar='csvfile', required=True, help='input dataframe')
    parser.add_argument('--output-sd', type=str, metavar='molfile', required=True, help='output molecule file')
    parser.add_argument('--input-sd', type=str, metavar='csvfile', required=True, help='input dataframe')
    parser.add_argument('--output-dataframe', type=str, metavar='molfile', required=True, help='output molecule file')
    return parser.parse_args()


if __name__ == "__main__":
    sys.exit(main())
