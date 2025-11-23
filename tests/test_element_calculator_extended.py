import unittest
from calc.element_calculator import calculate_elements, get_quality, get_element

class TestElementCalculatorExtended(unittest.TestCase):
    def test_get_quality(self):
        self.assertEqual(get_quality("Aries"), "Cardinal")
        self.assertEqual(get_quality("Taurus"), "Fixed")
        self.assertEqual(get_quality("Gemini"), "Mutable")
        self.assertEqual(get_quality("Cancer"), "Cardinal")
        self.assertIsNone(get_quality("Unknown"))

    def test_calculate_elements_and_qualities(self):
        # Mock planets input
        planets = {
            "Sun": "Aries",      # Fire, Cardinal (4)
            "Moon": "Taurus",    # Earth, Fixed (4)
            "Asc": "Gemini",     # Air, Mutable (4)
            "Mercury": "Cancer", # Water, Cardinal (3)
            "Venus": "Leo",      # Fire, Fixed (3)
            "Mars": "Virgo",     # Earth, Mutable (3)
            "Jupiter": "Libra",  # Air, Cardinal (2)
            "Saturn": "Scorpio"  # Water, Fixed (2)
        }
        
        # Ruler of Asc (Gemini) is Mercury. Mercury is in Cancer (Water, Cardinal).
        # So +2 to Water, +2 to Cardinal.

        # Expected Element Points:
        # Fire: Sun(4) + Venus(3) = 7
        # Earth: Moon(4) + Mars(3) = 7
        # Air: Asc(4) + Jupiter(2) = 6
        # Water: Mercury(3) + Saturn(2) + Ruler(2) = 7
        # Total: 27

        # Expected Quality Points:
        # Cardinal: Sun(4) + Mercury(3) + Jupiter(2) + Ruler(2) = 11
        # Fixed: Moon(4) + Venus(3) + Saturn(2) = 9
        # Mutable: Asc(4) + Mars(3) = 7
        # Total: 27

        scores, percentages, q_scores, q_percentages = calculate_elements(planets)

        self.assertEqual(scores["Fire"], 7)
        self.assertEqual(scores["Earth"], 7)
        self.assertEqual(scores["Air"], 6)
        self.assertEqual(scores["Water"], 7)

        self.assertEqual(q_scores["Cardinal"], 11)
        self.assertEqual(q_scores["Fixed"], 9)
        self.assertEqual(q_scores["Mutable"], 7)

        # Check percentages sum to approx 100
        self.assertAlmostEqual(sum(percentages.values()), 100, delta=0.1)
        self.assertAlmostEqual(sum(q_percentages.values()), 100, delta=0.1)

if __name__ == "__main__":
    unittest.main()
