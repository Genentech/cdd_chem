"""
(C) 2020 Genentech. All rights reserved.

Created on Feb 13, 2019

@author: albertgo

Implement an iterator to provide conformers of molecules.
"""

import logging
import typing

from openeye import oechem
from openeye import oeomega
from openeye import oeff
from cdd_chem.oechem.mol import Mol

log = logging.getLogger(__name__)


class ConformerOption():
    """Encapsulates options for conformer generation."""
    # pylint: disable=too-few-public-methods

    def __init__(self):
        self.omega_opts = oeomega.OEOmegaOptions()


CONFOPT_SINGLE = ConformerOption()
CONFOPT_SINGLE.omega_opts.SetMaxConfs(1)

CONFOPT_DEFAULT = ConformerOption()

CONFOPT_POLAR_H = ConformerOption()
CONFOPT_POLAR_H.omega_opts.SetSampleHydrogens(True)

CONFOPT_STRAIN = ConformerOption()
# Openeye seems to be using openeye.oeff.OEMMFFSheffieldFFType_MMFF94Smod_NOESTAT in
# openeye.oeomega.OEOmegaOptions(oeomega.OEOmegaSampling_Dense)
CONFOPT_STRAIN.omega_opts.SetBuildForceField(oeff.OEMMFFSheffieldFFType_MMFF94S_SHEFF)
CONFOPT_STRAIN.omega_opts.SetEnergyWindow(50)
CONFOPT_STRAIN.omega_opts.SetMaxConfs(500)


class ConformerGenerator():
    """Class that generates conformation using Omega TK."""

    def __init__(self,
                 mol_in_iter: typing.Iterator,
                 conf_options: ConformerOption = CONFOPT_DEFAULT,
                 max_conf: int = None):
        """
        Parameters
        ----------
        mol_in_iter
            an MolInputStream over molecules to be enumerated
        conf_options
            A conformer_option object describing the parameters used
        max_conf
            overwrite conformer number in conf_options
        """
        self.mol_in = mol_in_iter

        omega_opts = conf_options.omega_opts
        if max_conf is not None:
            omega_opts = oeomega.OEOmegaOptions(omega_opts)
            omega_opts.SetMaxConfs(max_conf)

        self.omega = oeomega.OEOmega(omega_opts)
        self.mc_mol = None
        self.conf_iter = None
        self.mol_num_confs = 0

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def __next__(self):
        # pylint: disable=protected-access
        if self.conf_iter is None:
            while True:
                graph_mol = self.mol_in.__next__()
                # need to keep handle on mcMol or confIter will be invalidated
                self.mc_mol = oechem.OEMol(graph_mol._mol)
                if self.omega(self.mc_mol):
                    self.conf_iter = self.mc_mol.GetConfs()
                    self.mol_num_confs = self.mc_mol.NumConfs()
                    break
                log.warning("Omega did not generate conformers")

        ret = self.conf_iter.next()
        self.mol_num_confs -= 1
        if self.mol_num_confs == 0:
            self.conf_iter = None

        return Mol(ret)

    def __exit__(self, *args):
        self.close()

    def close(self):
        """Terminate the iterator and release resources."""
        self.conf_iter = None
        self.mc_mol = None
        self.omega = None
