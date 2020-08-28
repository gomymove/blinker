import pickle
import unittest

from blinker._utilities import symbol


class TestUtilities(unittest.TestCase):
    def test_symbols(self):
        foo = symbol('foo')
        assert foo.name == 'foo'
        assert foo is symbol('foo')

        bar = symbol('bar')
        assert foo is not bar
        assert foo != bar
        assert not foo == bar

        assert repr(foo) == 'foo'


    def test_pickled_symbols(self):
        foo = symbol('foo')

        for protocol in 0, 1, 2:
            roundtrip = pickle.loads(pickle.dumps(foo))
            assert roundtrip is foo
