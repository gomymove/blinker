[![Build Status](https://travis-ci.org/gomymove/blinker.svg?branch=master)](https://travis-ci.org/gomymove/blinker)

🍴 This library is a fork of blinker, with added support for
**async and coroutine receivers**.
It works like the original, and offers a new ``send_async`` method
[as proposed here](https://github.com/jek/blinker/issues/17).


# Blinker

Blinker provides a fast dispatching system that allows any number of
interested parties to subscribe to events, or "signals".

Signal receivers can subscribe to specific senders or receive signals
sent by any sender.

```python
>>> from blinker import signal
>>> started = signal('round-started')
>>> def each(round):
...     print "Round %s!" % round
...
>>> started.connect(each)

>>> def round_two(round):
...     print "This is round two."
...
>>> started.connect(round_two, sender=2)

>>> for round in range(1, 4):
...     started.send(round)
...
Round 1!
Round 2!
This is round two.
Round 3!
```

See the [Blinker documentation](https://pythonhosted.org/blinker/) for more information.

## Async support

Send a signal asynchronously to coroutine receivers.

```python
>>> async def receiver_a(sender):
...     return 'value a'
...
>>> async def receiver_b(sender):
...     return 'value b'
...
>>> ready = signal('ready')
>>> ready.connect(receiver_a)
>>> ready.connect(receiver_b)
...
>>> async def collect():
...     return ready.send_async('sender')
...
>>> loop = asyncio.get_event_loop()
>>> results = loop.run_until_complete(collect())
>>> len(results)
2
>>> [v.result() for r, v in results][0]
value a
```

## Requirements

Blinker requires Python 2.7, Python 3.4 or higher, or Jython 2.7 or higher.
