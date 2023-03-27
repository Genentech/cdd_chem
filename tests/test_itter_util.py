'''
Created on Mar 2, 2019

@author: albertgo
'''
from cdd_chem.util.iterate import PushbackIterator



def test_pushback_iter():
    it = "string".__iter__()
    pb_it = PushbackIterator(it)

    assert pb_it.__next__() == 's'
    pb_it.pushback('S')

    assert "".join(pb_it) == 'String'

    assert pb_it.has_next() is False

    pb_it.pushback('z')
    assert pb_it.has_next()
    assert pb_it.__next__() == 'z'
