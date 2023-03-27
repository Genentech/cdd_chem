"""
(C) 2021 Genentech. All rights reserved.

Utilities for memory monitoring.
"""
from cdd_chem.util.unix import is_unix
from cdd_chem.util.io import warn  # noqa: F401; # pylint: disable=W0611

# helper function to get rss size, see stat(5) under statm. This is in pages (4k on my linux)


def print_memory_usage():
    # pylint: disable=W0612
    """ memory usage """
    if is_unix():
        with open('/proc/self/statm',encoding='UTF-8') as f:
            (vm_size, vm_rss, shrd, txt, lib_unused, data, dirty_unused) = \
                f.read().split()
        warn(f"MEM vmSize={vm_size:>7s} vmRSS={vm_rss:>7s} shared={shrd:>7s} data={data:>7s}")


def get_rss_gb():
    # pylint: disable=W0612
    """ memory usage """
    if is_unix():
        with open('/proc/self/statm',encoding='UTF-8') as f:
            (vm_size, vm_rss, shrd, txt, lib_unused, data, dirty_unused) = \
                f.read().split()
        return float(vm_rss) * 4. / 1024. / 1024.

    return 0
