"""Extensions to the standard library `random` module."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import random


def weighted_choice(items, weight_key):
    """Choose a random element from a sequence with weighted distribution.

    :param items: A sequence of items to choose from.
    :param weight_key: A function that takes an
        item in ``items`` and returns a non-negative integer
        weight for that item.

    :return: The chosen item.

    :raises: :py:exc:`ValueError` if any weights are negative or there are no
        items.

    .. testsetup::

        import random
        from baseplate.random import weighted_choice
        random.seed(12345)

    An example of usage:

    .. doctest::

        >>> words = ["apple", "banana", "cantelope"]
        >>> weighted_choice(words, weight_key=lambda word: len(word))
        'banana'

    """
    tickets = 0
    items_with_weights = []
    for item in items:
        weight = weight_key(item)
        if weight < 0:
            raise ValueError("weight for %r must be non-negative" % item)
        tickets += weight
        items_with_weights.append((item, weight))

    if tickets == 0:
        raise ValueError("at least one item must have weight")

    winning_ticket = random.random() * tickets
    current_ticket = 0
    for item, weight in items_with_weights:
        current_ticket += weight
        if current_ticket > winning_ticket:
            return item
    else:  # pragma: nocover
        raise RuntimeError("weighted_choice failed unexpectedly")
