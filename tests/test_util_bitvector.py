import numpy

from cdd_chem.util import bit_vector

test_array = numpy.asarray([0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
                            1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0,
                            0.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0,
                            1.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1.0, 0.0,])


def test_encode():
    result = bit_vector.to_base64(test_array)
    assert result == b"UY5lpg=="

def test_decode():
    result = bit_vector.from_base64(b"UY5lpg==", numpy.float32)
    assert numpy.array_equal(result, test_array)
