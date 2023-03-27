'''
Created on Apr 22, 2019

@author: albertgo
'''
import os

import logging.config as logconfig

import pkg_resources

def initialize_loggger(module_name: str, log_file: str = None):
    """
    Arguments:
    ----------
    module_name: name of module in which to look for the log ini file first
                 if the logfile does not exist the location of this file is used via __name__
    log_file: name of log ini file if overwriting 'log.ini'
    """

    if log_file is not None:
        if not log_file.upper().endswith(".INI") or not os.path.exists(log_file):
            log_ini = pkg_resources.resource_filename(module_name, f"log.{log_file}.ini")
            if not os.path.exists(log_ini):
                log_ini = pkg_resources.resource_filename(__name__, f"log.{log_file}.ini")
                if not os.path.exists(log_ini):
                    log_ini = pkg_resources.resource_filename(module_name, log_file)
                    if not os.path.exists(log_ini):
                        log_ini = pkg_resources.resource_filename(__name__, log_file)
                    if not os.path.exists(log_ini):
                        raise ValueError(f'{log_file} not found in {module_name} and {__name__}')
    else:
        log_file = 'log.ini'
        log_ini = pkg_resources.resource_filename(module_name, log_file)
        if not os.path.exists(log_ini):
            log_ini = pkg_resources.resource_filename(__name__, log_file)
        if not os.path.exists(log_ini):
            raise ValueError(f'{log_file} not found in {module_name} and {__name__}')

    logconfig.fileConfig(log_ini, defaults={'log_filename': "log.log"}, disable_existing_loggers=False)
