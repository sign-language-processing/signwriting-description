import unittest

from signwriting_description.naive_description import describe_sign_symbols


class TestNaiveDescription(unittest.TestCase):
    def test_describe_sign_returns_string(self):
        fsw = "M530x538S37602508x462S15a11493x494S20e00488x510S22f03469x517"
        description = describe_sign_symbols(fsw)
        self.assertIsInstance(description, str)  # Check if the score is a float


if __name__ == '__main__':
    unittest.main()
