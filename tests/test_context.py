from __future__ import with_statement

import unittest

from blinker import Signal


class TestContext(unittest.TestCase):

    def test_temp_connection(self):
        sig = Signal()

        canary = []
        receiver = lambda sender: canary.append(sender)

        sig.send(1)
        with sig.connected_to(receiver):
            sig.send(2)
        sig.send(3)

        assert canary == [2]
        assert not sig.receivers

    def test_temp_connection_for_sender(self):
        sig = Signal()

        canary = []
        receiver = lambda sender: canary.append(sender)

        with sig.connected_to(receiver, sender=2):
            sig.send(1)
            sig.send(2)

        assert canary == [2]
        assert not sig.receivers

    def test_temp_connection_failure(self):
        sig = Signal()

        canary = []
        receiver = lambda sender: canary.append(sender)

        class Failure(Exception):
            pass

        try:
            sig.send(1)
            with sig.connected_to(receiver):
                sig.send(2)
                raise Failure
            sig.send(3)
        except Failure:
            pass
        else:
            raise AssertionError("Context manager did not propagate.")

        assert canary == [2]
        assert not sig.receivers
