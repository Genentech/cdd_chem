"""

Serialize and deserialize bit vectors (i.e., molecule fingerprints)

Operate on fingerprints represented as numpy.array with one element
for each bit

"""

import base64

import numpy


def to_base64(bits: numpy.array) -> bytes:
    """Convert fingerprint represented as numpy.array (one element per bit)
       to base64 encoded string.

       Parameters
       ----------
       bits
            the fingerprint to convert; represented as one-dimensional
            numpy array with one element per bit

       Returns
       -------
            base64 encoded representation of fingerprint
    """

    int_array = bits.astype(numpy.short)
    packed = numpy.packbits(int_array)
    b64_bits = base64.b64encode(packed)
    return b64_bits


def from_base64(b64_bits: bytes, np_type: type) -> numpy.array:
    """Convert base64 encoded bit fingerprint to array representation
       (one element per bit)

       Parameters
       ----------
       b64_bits
            base64 encoded representation of fingerprint
       np_type
            data type for the numpy array to return

        Returns
        -------
            numpy array representation of fingerprint
    """

    packed = numpy.frombuffer(base64.b64decode(b64_bits.strip()), dtype=numpy.uint8)
    int_array = numpy.unpackbits(packed)
    return int_array.astype(np_type)
