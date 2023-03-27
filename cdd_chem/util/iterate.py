'''
Created on Mar 2, 2019

@author: albertgo
'''

from typing import TypeVar, Iterator

T = TypeVar('T') # pylint: disable=C0103

class PushbackIterator(Iterator[T]):
    """ Wraps an iterator adding the pushback() method
    """

    def __init__(self, iterator):
        """
        Parameter
        --------
        iterator: iterator to be wrapped
        """

        self.__dict__['_iterator'] = iterator
        self.__dict__['_pushed'] = []

    def pushback(self, item: T):
        """ return item to the top of the iterator """

        self._pushed.append(item)

    def __next__(self) -> T:
        if len(self._pushed) > 0:
            return self._pushed.pop()

        return next(self._iterator)


    def has_next(self) -> bool:
        """ Return True if there are more items to fetch """
        if len(self._pushed) > 0:
            return True

        try:
            self.pushback(next(self._iterator))
        except StopIteration:
            return False
        return True

    def __iter__(self):
        return self

    def __getattr__(self, attr):
        return getattr(self._iterator, attr)

    def __setattr__(self, attr, value):
        return setattr(self._iterator, attr, value)
