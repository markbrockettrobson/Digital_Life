from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import integers

from digital_life.src.sample import Sample


class TestPythonDiceInterpreter(TestCase):
    @given(test_value=integers())
    def test_add_one(self, test_value: int):
        self.assertEqual(Sample.add_one(test_value) - 1, test_value)
