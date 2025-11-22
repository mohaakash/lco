"""Element calculator utilities.

This module provides functions to parse extracted text or directly extract
page 3 from a Kepler-style PDF (using PyMuPDF when available). Importing
the module does not require PyMuPDF; the package is imported lazily only
when `extract_page3_text` is invoked.
"""

# ----------------------------------------------------------
# 1. Read Text from PDF (Only Page 3)
# ----------------------------------------------------------


def extract_page3_text(pdf_path):
    try:
        import pymupdf  # PyMuPDF
    except Exception as e:
        raise RuntimeError(
            "PyMuPDF (fitz) is required for PDF extraction: " + str(e))

    doc = pymupdf.open(pdf_path)

    # Page index starts at 0 → page 3 = index 2
    try:
        text = doc[2].get_text()
    except IndexError:
        raise ValueError("PDF does not contain page 3.")

    doc.close()
    return text


def parse_planet_positions(text):
    """Simple parser: preserve for backward compatibility.

    The file often contains columnar output where planet names and the
    zodiac sign may appear on separate lines. Use the more robust
    `parse_planet_positions_robust` for general use.
    """
    return parse_planet_positions_robust(text)


def parse_planet_positions_robust(text):
    """Robustly parse planet positions from messy PDF-extracted text.

    Strategy:
    - Split text into lines and trim whitespace.
    - Find indexes where planet names appear (case-insensitive).
    - For each planet, scan the next few lines for a known zodiac name.
    - If not found in nearby lines, assign from a global sequence match
      by scanning all zodiac occurrences and mapping by nearest planet index.
    """
    planets = {
        "Sun": None,
        "Moon": None,
        "Asc": None,
        "Mercury": None,
        "Venus": None,
        "Mars": None,
        "Jupiter": None,
        "Saturn": None
    }

    zodiac_names = [
        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    # Build map of line index -> text lower
    lower_lines = [ln.lower() for ln in lines]

    # Find planet header positions
    planet_positions = {}
    for i, ln in enumerate(lower_lines):
        for planet in list(planets.keys()):
            if ln.startswith(planet.lower()):
                planet_positions.setdefault(planet, []).append(i)

    # Find all zodiac occurrences with indices
    zodiac_positions = []
    for i, ln in enumerate(lines):
        for z in zodiac_names:
            if z.lower() in ln.lower():
                zodiac_positions.append((i, z))

    # For each planet, try to find zodiac in subsequent lines (within window)
    for planet in planets.keys():
        found = None
        pos_list = planet_positions.get(planet, [])
        if pos_list:
            # use the first occurrence
            p_idx = pos_list[0]
            for offset in range(0, 6):
                idx = p_idx + offset
                if idx < len(lines):
                    for z in zodiac_names:
                        if z.lower() in lines[idx].lower():
                            found = z
                            break
                if found:
                    break
        # fallback: find nearest zodiac by index distance
        if not found and zodiac_positions and pos_list:
            p_idx = pos_list[0]
            closest = min(zodiac_positions, key=lambda t: abs(t[0] - p_idx))
            found = closest[1]

        # final fallback: if still not found, try a global sequential assignment
        planets[planet] = found

    # If no explicit Asc entry but there is a line 'Asc.' or 'Asc', try to detect
    if not planets.get('Asc'):
        for i, ln in enumerate(lines):
            if ln.lower().startswith('asc') or ln.lower().startswith('asc.'):
                # try to pick zodiac from following lines
                for offset in range(1, 5):
                    idx = i + offset
                    if idx < len(lines):
                        for z in zodiac_names:
                            if z.lower() in lines[idx].lower():
                                planets['Asc'] = z
                                break
                    if planets['Asc']:
                        break
                if planets['Asc']:
                    break

    return planets


# ----------------------------------------------------------
# 3. Determine Ruler of Ascendant
# ----------------------------------------------------------
def get_ruler_of_asc(sign):
    rulers = {
        "Aries": "Mars",
        "Taurus": "Venus",
        "Gemini": "Mercury",
        "Cancer": "Moon",
        "Leo": "Sun",
        "Virgo": "Mercury",
        "Libra": "Venus",
        "Scorpio": "Mars",
        "Sagittarius": "Jupiter",
        "Capricorn": "Saturn",
        "Aquarius": "Saturn",
        "Pisces": "Jupiter",
    }
    return rulers.get(sign, None)


# ----------------------------------------------------------
# 4. Determine the element of a zodiac sign
# ----------------------------------------------------------
def get_element(sign):
    fire = ["Aries", "Leo", "Sagittarius"]
    water = ["Cancer", "Scorpio", "Pisces"]
    earth = ["Taurus", "Virgo", "Capricorn"]
    air = ["Gemini", "Libra", "Aquarius"]

    if sign in fire:
        return "Fire"
    if sign in water:
        return "Water"
    if sign in earth:
        return "Earth"
    if sign in air:
        return "Air"
    return None


# ----------------------------------------------------------
# 5. Calculate elemental distribution
# ----------------------------------------------------------
def calculate_elements(planets):
    element_scores = {"Fire": 0, "Water": 0, "Earth": 0, "Air": 0}

    planet_points = {
        "Sun": 4,
        "Moon": 4,
        "Asc": 4,
        "Mercury": 3,
        "Venus": 3,
        "Mars": 3,
        "Jupiter": 2,
        "Saturn": 2
    }

    # Add points for planets, ascendant
    for planet, sign in planets.items():
        if sign:
            element = get_element(sign)
            if element:
                element_scores[element] += planet_points.get(planet, 0)

    # Handle Ruler of Ascendant (extra 2 points)
    asc_sign = planets.get("Asc")
    if asc_sign:
        ruler = get_ruler_of_asc(asc_sign)
        ruler_sign = planets.get(ruler)
        if ruler_sign:
            ruler_element = get_element(ruler_sign)
            if ruler_element:
                element_scores[ruler_element] += 2   # +2 points

    # Convert to percentages
    total_points = sum(element_scores.values())
    element_percentages = {
        el: round((score / total_points) * 100, 2) if total_points > 0 else 0
        for el, score in element_scores.items()
    }

    return element_scores, element_percentages


# ----------------------------------------------------------
# 6. Combine everything
# ----------------------------------------------------------
def process_kepler_pdf(pdf_path):
    text = extract_page3_text(pdf_path)
    return process_text(text)


def process_text(text):
    """Process raw text (extracted from page 3) and compute element scores.

    Returns (planets_dict, element_scores, element_percentages)
    """
    planets = parse_planet_positions_robust(text)
    scores, percentages = calculate_elements(planets)
    return planets, scores, percentages


# ----------------------------------------------------------
# 7. Example Usage
# ----------------------------------------------------------
if __name__ == "__main__":
    pdf_path = "docs/kepler.pdf"   # <-- replace with your file path
    planets, scores, percentages = process_kepler_pdf(pdf_path)

    print("\nExtracted Planet Positions:")
    print(planets)

    print("\nElement Points:")
    print(scores)

    print("\nElement Percentages:")
    print(percentages)
