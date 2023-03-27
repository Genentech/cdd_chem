"""
Created on Mar 2, 2019

@author: albertgo
"""

import time
from cdd_chem.util.io import warn  # noqa: F401; # pylint: disable=W0611


class MyTimer:
    """
    Example:
            with time_it.MyTimer(dev):
                test(dev, tin)
    """

    def __init__(self, prefix):
        self.start = time.time()
        self.prefix = prefix

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        runtime = end - self.start
        msg = f'{self.prefix} The function took {runtime:10.3f} seconds to complete'
        warn(msg)
