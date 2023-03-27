'''
    Use this to import the constants depending on your environment setting.
    Currently the AESTEL_LEVEL variable is used but finally we should use a
    different one

    from cdd_chem.util.constants import import_constants
    cddConst = import_constants()

    print(cddConst.smdd_dir)

    # Creator: Alberto
'''


import os
import importlib
import sys
from os import path
from typing import Optional

class _Consts:
    """ impementation for prd constants """
    if os.name != 'nt':
        @property
        def smdd_dir(self):
            """ SMDD directory for linux"""
            return '/gne/data/smdd'
    elif os.name == 'nt':
        @property
        def smdd_dir(self):
            """ SMDD directory for Windows"""
            return '//smddfiles.gene.com/smdd'


    @property
    def apps_dir(self):
        """ Directory location with cdd applications """
        ad = os.environ.get('AESTEL_DIR')
        if ad is None:
            raise EnvironmentError("AESTEL_DIR not defined!")

        return os.path.join(ad, "..")


    @property
    def acc_database(self):
        """ SMID dtabase instance name """
        return 'accprd2'


    @property
    def mail_server(self):
        """ mail_server hostname """
        return "smtp.gene.com"


# Create singleton with constants
_CddConstants = _Consts()


def import_constants():
    # pylint: disable=W0212
    """ import contant definition based on PYTHON_LEVEL environment variables """

    level = os.getenv("PYTHON_LEVEL")
    if level is not None and not level.endswith('prd') and level != "":
        return importlib.import_module(f"cdd_chem.util.constants_{level}")._CddConstants

    return importlib.import_module("cdd_chem.util.constants")._CddConstants


def replace_consts(strg: str) -> str:
    """replace all "$" prefixed occurrences of constant names in strg by the
       constant value
    """

    cnst = import_constants()

    property_names = [p for p in dir(cnst) if
                      isinstance(getattr(cnst.__class__, p), property)]

    for key in property_names:
        strg = strg.replace(f"${key}", getattr(cnst, key))

    return strg


def replace_consts_and_env(strg: Optional[str]) -> Optional[str]:
    """replace all "$" prefixed occurrences of constant or environment
       variable names in strg by the constant value.

       Env variable have precedence

     Finally replaces "$installDir" with directory main method

    """
    if strg is None:
        return strg

    for key, value in os.environ.items():
        strg = strg.replace(f"${key}", value)

    idir = get_installation_dir()
    assert idir is not None
    strg = strg.replace("$installDir", idir)

    return replace_consts(strg)


def get_installation_dir() -> Optional[str]:
    # pylint: disable=W0702
    """ Directory from which this python script was started """
    try:
        return os.path.dirname(path.abspath(sys.modules['__main__'].__file__))
    except: # noqa: E722
        try:
            return os.path.dirname(sys.argv[0])
        except: # noqa: E722
            return None   # this might be interactive console
