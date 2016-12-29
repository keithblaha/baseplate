from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import collections
import unittest

from baseplate import random

from .. import mock


class WeightedChoiceTests(unittest.TestCase):
    def test_empty_list(self):
        with self.assertRaises(ValueError):
            random.weighted_choice([], lambda i: i)

    def test_negative_weight(self):
        with self.assertRaises(ValueError):
            random.weighted_choice(["a"], lambda i: -1)

    @mock.patch("random.random")
    def test_iterator(self, random_random):
        iterator = (n for n in range(10))

        random_random.return_value = 0.0
        choice = random.weighted_choice(iterator, lambda i: i)
        self.assertEqual(choice, 1)

    @mock.patch("random.random")
    def test_choice(self, random_random):
        weight_fn = lambda i: 3 if i == "c" else 1
        items = [
            "a", # 1
            "b", # 1
            "c", # 3
            "d", # 1
        ]

        random_random.return_value = 0.5
        choice = random.weighted_choice(items, weight_fn)
        self.assertEqual(choice, "c")

    def test_distribution(self):
        weight_fn = lambda i: ord(i)-96
        items = [
            "a", # 1
            "b", # 2
            "c", # 3
            "d", # 4
        ]

        choices = collections.Counter()
        for _ in range(10000):
            choice = random.weighted_choice(items, weight_fn)
            choices[choice] += 1

        # we give a bit of fuzz factor here since we're
        # allowing true randomness in this test and don't
        # want spurious failures.
        self.assertLess(abs(1000 - choices["a"]), 150)
        self.assertLess(abs(2000 - choices["b"]), 150)
        self.assertLess(abs(3000 - choices["c"]), 150)
        self.assertLess(abs(4000 - choices["d"]), 150)
