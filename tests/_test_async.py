import asyncio
import unittest

import blinker


class TestAsync(unittest.TestCase):
    def test_send_async(self):
        calls = []

        @asyncio.coroutine
        def receiver_a(sender):
            calls.append(receiver_a)
            return 'value a'

        @asyncio.coroutine
        def receiver_b(sender):
            calls.append(receiver_b)
            return 'value b'

        def receiver_c(sender):
            calls.append(receiver_c)
            return 'value c'

        sig = blinker.Signal()
        sig.connect(receiver_a)
        sig.connect(receiver_b)
        sig.connect(receiver_c)

        @asyncio.coroutine
        def collect():
            return sig.send_async()

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(collect())

        expected = {
            receiver_a: 'value a',
            receiver_b: 'value b',
            receiver_c: 'value c',
        }

        assert set(calls) == set(expected.keys())
        collected_results = {v.result() for r, v in results}
        assert collected_results == set(expected.values())

    def test_send_async_with_values(self):
        some_signal = blinker.Signal("some_signal")

        @some_signal.connect
        async def receive(sender, **kwargs):
            assert sender == "sender"
            assert kwargs.get("foo") == "bar"

            return "done"

        async def send():
            return some_signal.send_async("sender", **{"foo": "bar"})

        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(send())

        assert len(results) == 1

        done = [v.result() for r, v in results][0]
        assert done == "done"
