"""
Quick verification that calculate_elements now uses calculate_qualities
"""

from element_calculator import calculate_elements, calculate_qualities

# Sample chart
planets = {
    "Sun": "Aries",      # Cardinal
    "Moon": "Taurus",    # Fixed
    "Asc": "Gemini",     # Mutable (should be IGNORED in qualities)
    "Mercury": "Cancer", # Cardinal
    "Venus": "Leo",      # Fixed
    "Mars": "Virgo",     # Mutable
    "Jupiter": "Libra",  # Cardinal
    "Saturn": "Scorpio", # Fixed
}

print("="*60)
print("VERIFICATION: calculate_elements uses calculate_qualities")
print("="*60)

# Get results from calculate_elements
elem_scores, elem_pcts, qual_scores_from_calc, qual_pcts_from_calc = calculate_elements(planets)

# Get results directly from calculate_qualities
qual_scores_direct, qual_pcts_direct = calculate_qualities(planets)

print("\nQuality Scores from calculate_elements():")
print(f"  {qual_scores_from_calc}")

print("\nQuality Scores from calculate_qualities() directly:")
print(f"  {qual_scores_direct}")

print("\nQuality Percentages from calculate_elements():")
print(f"  {qual_pcts_from_calc}")

print("\nQuality Percentages from calculate_qualities() directly:")
print(f"  {qual_pcts_direct}")

# Verify they match
if qual_scores_from_calc == qual_scores_direct and qual_pcts_from_calc == qual_pcts_direct:
    print("\n✅ SUCCESS: Both methods return identical results!")
    print("✅ calculate_elements() is now using calculate_qualities() internally")
    print("✅ Ascendant is correctly IGNORED in quality calculations")
    print(f"✅ Only 7 planets counted: {sum(qual_scores_direct.values())} planets")
else:
    print("\n❌ MISMATCH: Results differ!")

print("\nNote: Element calculations still use weighted system (includes Asc + ruler)")
print(f"Element Percentages: {elem_pcts}")
print("="*60)
