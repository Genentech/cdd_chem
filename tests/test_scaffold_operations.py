"""
(C) 2020 Genentech. All rights reserved.

Test file for cdd_chem module.
"""

import os

import pytest_check as check

from cdd_chem.oechem import scaffold_operations


def test_01_identify_core():
    test_smirks = "[O:4]=[C:3](N[C;H2])c1[n:2][c:1]2[cH:8][cH:9][c:7](N([C&H2,#1:11])[C,S:5]=[O:6])cn2[cH:10]1>>" \
        "[C;H2][U+].[O:4]=[C:3](N[U+])c3[n:2][c:1]4[cH:8][cH:9][c:7](N([U+2])[U+3])cn4[cH:10]3.[O:6]=[C,S:5][U+2].[C&H2,#1:11][U+3]"
    expected_smirks = "[O:4]=[C:3](N[C;H2])c1[n:2][c:1]2[cH:8][cH:9][c:7](N([C&H2,#1:11])[C,S:5]=[O:6])cn2[cH:10]1>>" \
        "[C;H2][U+].[cH:9]1[cH:8][c:1]2[n:2]c([cH:10]n2c[c:7]1N([U+12])[U+13])[C:3](=[O:4])N[U+11].[O:6]=[C,S:5][U+2].[C&H2,#1:11][U+3]"

    result = scaffold_operations.identify_core_in_smirks(test_smirks)
    check.equal(expected_smirks, result)


def test_02_rewrite_smirks_file(shared_datadir):
    # pylint: disable=line-too-long
    smirks_path = os.path.join(shared_datadir, "imidazopyridine.smirks.tab")

    expected_buf = ("""# scaffold.rgExtraction (last updated 12/05/2018)\t \n"""
                    """# R-Groups cf scaffold of interest\t \n"""
                    """# SMIRKS	Name\n"""
                    """[O:4]=[C:3](N[C;H2])c1[n:2][c:1]2[cH:8][cH:9][c:7](N([C&H2,#1:11])[C,S:5]=[O:6])cn2[cH:10]1>>[C;H2][U+].[cH:9]1[cH:8][c:1]2[n:2]c([cH:10]n2c[c:7]1N([U+12])[U+13])[C:3](=[O:4])N[U+11].[O:6]=[C,S:5][U+2].[C&H2,#1:11][U+3]\timidazopyridine""")     # noqa: E501
    scaffold_operations.mark_smirks_cores(smirks_path)
    with open(smirks_path, "r", encoding='UTF-8') as smirks_file:
        buf = smirks_file.read()
    check.equal(expected_buf, buf)
