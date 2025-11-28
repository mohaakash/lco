"""
Test cases for element_calculator.py

This file contains various test cases to verify the functionality of:
- Planet position parsing
- Element calculation
- Quality (modality) calculation
- Both weighted and count-based methods
"""

from element_calculator import (
    get_element,
    get_quality,
    get_ruler_of_asc,
    calculate_elements,
    calculate_qualities,
    parse_planet_positions_robust
)


def test_get_element():
    """Test element assignment for zodiac signs"""
    print("\n" + "="*60)
    print("TEST 1: get_element() - Element Assignment")
    print("="*60)
    
    test_cases = [
        ("Aries", "Fire"),
        ("Taurus", "Earth"),
        ("Gemini", "Air"),
        ("Cancer", "Water"),
        ("Leo", "Fire"),
        ("Virgo", "Earth"),
        ("Libra", "Air"),
        ("Scorpio", "Water"),
        ("Sagittarius", "Fire"),
        ("Capricorn", "Earth"),
        ("Aquarius", "Air"),
        ("Pisces", "Water"),
    ]
    
    passed = 0
    failed = 0
    
    for sign, expected in test_cases:
        result = get_element(sign)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"{status}: {sign:12} -> {result:6} (expected: {expected})")
        if result == expected:
            passed += 1
        else:
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")


def test_get_quality():
    """Test quality (modality) assignment for zodiac signs"""
    print("\n" + "="*60)
    print("TEST 2: get_quality() - Quality Assignment")
    print("="*60)
    
    test_cases = [
        ("Aries", "Cardinal"),
        ("Taurus", "Fixed"),
        ("Gemini", "Mutable"),
        ("Cancer", "Cardinal"),
        ("Leo", "Fixed"),
        ("Virgo", "Mutable"),
        ("Libra", "Cardinal"),
        ("Scorpio", "Fixed"),
        ("Sagittarius", "Mutable"),
        ("Capricorn", "Cardinal"),
        ("Aquarius", "Fixed"),
        ("Pisces", "Mutable"),
    ]
    
    passed = 0
    failed = 0
    
    for sign, expected in test_cases:
        result = get_quality(sign)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"{status}: {sign:12} -> {result:8} (expected: {expected})")
        if result == expected:
            passed += 1
        else:
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")


def test_get_ruler_of_asc():
    """Test ascendant ruler assignment"""
    print("\n" + "="*60)
    print("TEST 3: get_ruler_of_asc() - Ascendant Rulers")
    print("="*60)
    
    test_cases = [
        ("Aries", "Mars"),
        ("Taurus", "Venus"),
        ("Gemini", "Mercury"),
        ("Cancer", "Moon"),
        ("Leo", "Sun"),
        ("Virgo", "Mercury"),
        ("Libra", "Venus"),
        ("Scorpio", "Mars"),
        ("Sagittarius", "Jupiter"),
        ("Capricorn", "Saturn"),
        ("Aquarius", "Saturn"),
        ("Pisces", "Jupiter"),
    ]
    
    passed = 0
    failed = 0
    
    for sign, expected in test_cases:
        result = get_ruler_of_asc(sign)
        status = "✓ PASS" if result == expected else "✗ FAIL"
        print(f"{status}: {sign:12} ruled by {result:8} (expected: {expected})")
        if result == expected:
            passed += 1
        else:
            failed += 1
    
    print(f"\nResults: {passed} passed, {failed} failed")


def test_calculate_qualities():
    """Test the count-based quality calculation (7 planets only)"""
    print("\n" + "="*60)
    print("TEST 4: calculate_qualities() - Count-Based Method")
    print("="*60)
    
    # Test Case 1: Balanced distribution
    print("\nTest Case 1: Balanced Distribution")
    planets_1 = {
        "Sun": "Aries",      # Cardinal
        "Moon": "Cancer",    # Cardinal
        "Mercury": "Taurus", # Fixed
        "Venus": "Leo",      # Fixed
        "Mars": "Gemini",    # Mutable
        "Jupiter": "Virgo",  # Mutable
        "Saturn": "Pisces",  # Mutable
        "Asc": "Libra"       # Should be ignored
    }
    
    qualities, percentages = calculate_qualities(planets_1)
    print(f"Qualities (counts): {qualities}")
    print(f"Percentages: {percentages}")
    print(f"Expected: Cardinal=2, Fixed=2, Mutable=3")
    print(f"Note: Asc (Libra/Cardinal) should be IGNORED")
    
    # Test Case 2: All Cardinal
    print("\nTest Case 2: All Cardinal")
    planets_2 = {
        "Sun": "Aries",
        "Moon": "Cancer",
        "Mercury": "Libra",
        "Venus": "Capricorn",
        "Mars": "Aries",
        "Jupiter": "Cancer",
        "Saturn": "Libra",
        "Asc": "Taurus"  # Should be ignored
    }
    
    qualities, percentages = calculate_qualities(planets_2)
    print(f"Qualities (counts): {qualities}")
    print(f"Percentages: {percentages}")
    print(f"Expected: Cardinal=100%, Fixed=0%, Mutable=0%")
    
    # Test Case 3: Missing planets
    print("\nTest Case 3: Missing Planets")
    planets_3 = {
        "Sun": "Leo",
        "Moon": "Scorpio",
        "Mercury": None,
        "Venus": "Aquarius",
        "Mars": None,
        "Jupiter": "Taurus",
        "Saturn": None,
    }
    
    qualities, percentages = calculate_qualities(planets_3)
    print(f"Qualities (counts): {qualities}")
    print(f"Percentages: {percentages}")
    print(f"Total planets counted: {sum(qualities.values())} (should be 4)")


def test_calculate_elements():
    """Test the weighted point-based element and quality calculation"""
    print("\n" + "="*60)
    print("TEST 5: calculate_elements() - Weighted Point Method")
    print("="*60)
    
    # Test Case: Sample chart
    print("\nSample Chart:")
    planets = {
        "Sun": "Leo",        # Fire, 4 points
        "Moon": "Cancer",    # Water, 4 points
        "Asc": "Libra",      # Air, 4 points
        "Mercury": "Virgo",  # Earth, 3 points
        "Venus": "Leo",      # Fire, 3 points
        "Mars": "Gemini",    # Air, 3 points
        "Jupiter": "Pisces", # Water, 2 points
        "Saturn": "Capricorn" # Earth, 2 points
    }
    
    # Ruler of Asc (Libra) is Venus (in Leo/Fire) -> +2 points to Fire
    
    elem_scores, elem_pct, qual_scores, qual_pct = calculate_elements(planets)
    
    print("\nElement Scores (points):")
    for elem, score in elem_scores.items():
        print(f"  {elem:6}: {score} points")
    
    print("\nElement Percentages:")
    for elem, pct in elem_pct.items():
        print(f"  {elem:6}: {pct}%")
    
    print("\nQuality Scores (points):")
    for qual, score in qual_scores.items():
        print(f"  {qual:8}: {score} points")
    
    print("\nQuality Percentages:")
    for qual, pct in qual_pct.items():
        print(f"  {qual:8}: {pct}%")
    
    print("\nExpected Fire: 4(Sun) + 3(Venus) + 2(Ruler bonus) = 9 points")
    print("Expected Water: 4(Moon) + 2(Jupiter) = 6 points")
    print("Expected Earth: 3(Mercury) + 2(Saturn) = 5 points")
    print("Expected Air: 4(Asc) + 3(Mars) = 7 points")


def test_parse_planet_positions():
    """Test planet position parsing from sample text"""
    print("\n" + "="*60)
    print("TEST 6: parse_planet_positions_robust() - Text Parsing")
    print("="*60)
    
    # Sample text that might come from a PDF
    sample_text = """
    Planetary Positions
    
    Sun         15° 23' Leo
    Moon        8° 45' Cancer
    Mercury     22° 10' Virgo
    Venus       3° 56' Leo
    Mars        18° 32' Gemini
    Jupiter     12° 08' Pisces
    Saturn      25° 41' Capricorn
    Asc.        7° 15' Libra
    """
    
    planets = parse_planet_positions_robust(sample_text)
    
    print("\nParsed Planets:")
    for planet, sign in planets.items():
        print(f"  {planet:10}: {sign}")
    
    print("\nExpected:")
    print("  Sun       : Leo")
    print("  Moon      : Cancer")
    print("  Mercury   : Virgo")
    print("  Venus     : Leo")
    print("  Mars      : Gemini")
    print("  Jupiter   : Pisces")
    print("  Saturn    : Capricorn")
    print("  Asc       : Libra")


def test_comparison():
    """Compare weighted vs count-based quality calculations"""
    print("\n" + "="*60)
    print("TEST 7: Comparison - Weighted vs Count-Based")
    print("="*60)
    
    planets = {
        "Sun": "Aries",      # Cardinal, 4 points
        "Moon": "Taurus",    # Fixed, 4 points
        "Asc": "Gemini",     # Mutable, 4 points (only in weighted)
        "Mercury": "Cancer", # Cardinal, 3 points
        "Venus": "Leo",      # Fixed, 3 points
        "Mars": "Virgo",     # Mutable, 3 points
        "Jupiter": "Libra",  # Cardinal, 2 points
        "Saturn": "Scorpio", # Fixed, 2 points
    }
    
    # Ruler of Asc (Gemini) is Mercury (in Cancer/Cardinal) -> +2 to Cardinal
    
    # Weighted method
    _, _, qual_scores, qual_pct_weighted = calculate_elements(planets)
    
    # Count method
    qual_counts, qual_pct_count = calculate_qualities(planets)
    
    print("\nWeighted Method (includes Asc + Ruler bonus):")
    print(f"  Scores: {qual_scores}")
    print(f"  Percentages: {qual_pct_weighted}")
    
    print("\nCount Method (7 planets only, no Asc):")
    print(f"  Counts: {qual_counts}")
    print(f"  Percentages: {qual_pct_count}")
    
    print("\nDifferences:")
    print("  - Weighted includes Asc (Gemini/Mutable) with 4 points")
    print("  - Weighted includes Ruler bonus (Mercury/Cardinal) with +2 points")
    print("  - Count method: Cardinal=3, Fixed=2, Mutable=2 (7 planets)")
    print("  - Weighted method: Cardinal has extra +2 from ruler bonus")


def run_all_tests():
    """Run all test cases"""
    print("\n" + "="*60)
    print("ELEMENT CALCULATOR TEST SUITE")
    print("="*60)
    
    test_get_element()
    test_get_quality()
    test_get_ruler_of_asc()
    test_calculate_qualities()
    test_calculate_elements()
    test_parse_planet_positions()
    test_comparison()
    
    print("\n" + "="*60)
    print("ALL TESTS COMPLETED")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_all_tests()
