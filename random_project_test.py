import unittest
from random_project import force_money


class ForceIntTest(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(force_money("4"), 4)
        self.assertEqual(force_money("4.00"), 4)
        self.assertEqual(force_money("$3.95"), 3.95)
        self.assertEqual(force_money("$3 888.01"), 3888.01)
        self.assertEqual(force_money("$3 888,01"), 3888.01)
        self.assertEqual(force_money("$3,95"), 3.95)


if __name__ == "__main__":
    unittest.main()
