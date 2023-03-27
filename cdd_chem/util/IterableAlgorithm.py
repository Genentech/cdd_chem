"""
  An algorithm that supports iterating over the results.
  The idea is that all methods for processing BaseMolecules are implemented as IterableAlgorithms.
  Then we can easily use them as API stringing together multiple algorithms but we can also use a standard framework
  to automatically implement command line and web service implementations for each algorithm.

   Author: Alberto Gobbi
"""

from abc import ABCMeta, abstractmethod
from contextlib import AbstractContextManager
from typing import TypeVar, Iterator, Optional, Callable, Generic, List

TI = TypeVar('TI')
TO = TypeVar('TO')


class IterableAlgorithm(Iterator[TO], AbstractContextManager, metaclass=ABCMeta):
    """ An algorithm that supports iterating over the resulting TO objects.
        The interface is an iterator with HasNExt method that also is a context handler """


    @abstractmethod
    def has_next(self) -> bool:
        """ has_next """

    def close(self):
        """ Overwrite to close resources """

    def __exit__(self, *args):
        """ close """
        self.close()


class SimpleIterableAlgorithm(IterableAlgorithm[TO],Generic[TI,TO]):
    """ Abstract class to simplify the implementation of an Algorithm that
        reads TI objects from an input algorithm and produces TO obects.

        All that needs to be done is to implement the compute method
    """

    def __init__(self, inItter:IterableAlgorithm[TI]):
        self.inItter = inItter
        self.nextItem: Optional[TO] = None

    # noinspection PyTypeChecker
    @abstractmethod
    def compute(self, item:TI) -> Optional[TO]:   # type: ignore
        """  Overwrite this method changing nextItem to include results of algorithm
             If None is returned the input record will not be passed tot he output
        """


    def __next__(self) -> TO:
        if not self.has_next():
            raise StopIteration

        assert self.nextItem is not None

        ret = self.nextItem
        self.nextItem = None

        return ret

    def has_next(self) -> bool:
        """ has_next """
        if self.nextItem is not None:
            return True

        for nxt in self.inItter:
            ret = self.compute(nxt)
            if ret is not None:
                self.nextItem = ret
                return True

        return False

    def __enter__(self):
        return self

    def __iter__(self):
        return self

    def __exit__(self, *args):
        self.inItter.__exit__(*args)
        super().__exit__(*args)


class LambdaAlgorithm(SimpleIterableAlgorithm[TI, TO]):
    """ Create a SimpleIterableAlgorithm using a lambda function that computes TO from TI """

    def __init__(self, inItter:IterableAlgorithm, lmbda:Callable[[TI], TO]):
        super().__init__(inItter)
        self.compute = lmbda # type: ignore

    def compute(self, item:TI) -> TO: # type: ignore   # mypy does not like this but it is OK
        return item # type: ignore   # this implementation will be overwritten in __init__


class PushbackIterableAlgorithm(IterableAlgorithm[TO],Generic[TI,TO]):
    """ Wraps an IterableAlgorithm adding the pushback() method
    """

    def __init__(self, inItter:IterableAlgorithm[TI]):
        """
        Parameter
        --------
        iterator: iterator to be wrapped
        """
        self.__dict__['inItter'] = inItter
        self.__dict__['_pushed']:List[TO] = []

    def pushback(self, item: TO):
        """ return item to the top of the iterator """

        self._pushed.append(item)


    def __next__(self) -> TO:
        if len(self._pushed) > 0:
            return self._pushed.pop()

        return next(self.inItter)


    def has_next(self) -> bool:
        """ Return True if there are more items to fetch """
        if len(self._pushed) > 0:
            return True

        try:
            self.pushback(next(self.inItter))
        except StopIteration:
            return False
        return True

    def __iter__(self):
        return self

    def __getattr__(self, attr):
        return getattr(self.inItter, attr)

    def __setattr__(self, attr, value):
        return setattr(self.inItter, attr, value)
