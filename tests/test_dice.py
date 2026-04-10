import unittest

from classes.Dice import DICE_CLASS, Dice


class TestDice(unittest.TestCase):
    def test_calculate_oposite_side_d6(self):
        expected = {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}
        for value, opposite in expected.items():
            with self.subTest(value=value):
                self.assertEqual(Dice.calculate_oposite_side(DICE_CLASS.D6, value), opposite)

    def test_calculate_oposite_side_d10(self):
        expected = {0: 9, 1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1, 9: 0}
        for value, opposite in expected.items():
            with self.subTest(value=value):
                self.assertEqual(Dice.calculate_oposite_side(DICE_CLASS.D10, value), opposite)

    def test_calculate_oposite_side_d12(self):
        self.assertEqual(Dice.calculate_oposite_side(DICE_CLASS.D12, 1), 12)
        self.assertEqual(Dice.calculate_oposite_side(DICE_CLASS.D12, 12), 1)

    def test_calculate_oposite_side_d20(self):
        self.assertEqual(Dice.calculate_oposite_side(DICE_CLASS.D20, 1), 20)
        self.assertEqual(Dice.calculate_oposite_side(DICE_CLASS.D20, 20), 1)

    def test_calculate_oposite_side_d100(self):
        self.assertEqual(Dice.calculate_oposite_side(DICE_CLASS.D100, 0), 90)
        self.assertEqual(Dice.calculate_oposite_side(DICE_CLASS.D100, 90), 0)

    def test_calculate_oposite_side_not_supported(self):
        self.assertIsNone(Dice.calculate_oposite_side(DICE_CLASS.D4, 1))
        self.assertIsNone(Dice.calculate_oposite_side(DICE_CLASS.D8, 1))

    def test_validate_dice_value_common_dice(self):
        valid_cases = [
            (DICE_CLASS.D4, 1),
            (DICE_CLASS.D4, 4),
            (DICE_CLASS.D6, 3),
            (DICE_CLASS.D8, 8),
            (DICE_CLASS.D10, 0),
            (DICE_CLASS.D10, 9),
            (DICE_CLASS.D12, 6),
            (DICE_CLASS.D20, 20),
        ]

        for dice_type, value in valid_cases:
            with self.subTest(dice_type=dice_type, value=value):
                self.assertTrue(Dice.validate_dice_value(dice_type, value))

    def test_validate_dice_value_invalid_bounds(self):
        invalid_cases = [
            (DICE_CLASS.D4, 0),
            (DICE_CLASS.D6, 7),
            (DICE_CLASS.D8, 9),
            (DICE_CLASS.D10, -1),
            (DICE_CLASS.D12, 13),
            (DICE_CLASS.D20, 21),
            (DICE_CLASS.D100, 100),
        ]

        for dice_type, value in invalid_cases:
            with self.subTest(dice_type=dice_type, value=value):
                self.assertFalse(Dice.validate_dice_value(dice_type, value))

    def test_validate_dice_value_d100_multiples_of_ten_only(self):
        self.assertTrue(Dice.validate_dice_value(DICE_CLASS.D100, 0))
        self.assertTrue(Dice.validate_dice_value(DICE_CLASS.D100, 10))
        self.assertTrue(Dice.validate_dice_value(DICE_CLASS.D100, 90))

        self.assertFalse(Dice.validate_dice_value(DICE_CLASS.D100, 1))
        self.assertFalse(Dice.validate_dice_value(DICE_CLASS.D100, 11))
        self.assertFalse(Dice.validate_dice_value(DICE_CLASS.D100, 95))


if __name__ == "__main__":
    unittest.main()
