'''
Created on Mar 2, 2019

@author: albertgo
'''

from cdd_chem.util.constants import _Consts

class _DevConsts(_Consts):
    """ Constants for development mode """
    @property
    def acc_database(self):
        return 'accdev1'


# Create singleton with constants
_CddConstants = _Consts()
