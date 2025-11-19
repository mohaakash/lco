from openai import OpenAI
import google.generativeai as genai
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


gemini_model = genai.GenerativeModel("gemini-2.5-flash")

# ============================================================
# 1. SINGLE, CLEAN PROMPT PER MODALITY (ALREADY REFINED)
# ============================================================

MODALITY_PROMPTS = {
    "Cardinal": """[SECTION: Definition & Core Meaning]
Cardinal signs (Aries, Cancer, Libra, Capricorn) begin each season. Keyword: "Activity." They initiate, lead, push, act, and respond quickly.

[SECTION: Psychological Expression]
High Cardinal:
- Action-oriented, proactive, demanding, willful.
- Problem-solver through direct action.
- Type-A tendencies: rushing, overcommitting, pushing limits.
- May overwhelm others with force or intensity.

[SECTION: Physical Manifestations]
Areas affected:
- Chest, stomach, rib cage, head, kidneys, bones, gallbladder.
- Acute illnesses.
- Kidney or gallbladder weakness.
- Impatience for healing or results.

[SECTION: Remedies for Imbalance:]
- Practices of introspection: meditation, reflection.
- Inner-awareness physical arts: yoga, tai chi.
- Crystals: amethyst, fluorite, sugilite.
- Slowing down, pacing energy.

[SECTION: Summary Insight]
Cardinal energy leads and initiates. Too much = pressure, impatience, burnout. Too little = stagnation and avoidance. Balance comes through pacing, mindful action, and body-mind integration.
""",
    "Fixed": """[SECTION: Definition & Core Meaning]
Fixed signs (Taurus, Leo, Scorpio, Aquarius) hold the middle of each season. Keyword: "Stability." They express steadiness, persistence, loyalty, and long-term focus but can become rigid, resistant to change, or stubborn.

[SECTION: Psychological Expression]
High Fixed energy:
- Strong willpower, dependable, consistent.
- Difficulty adapting; resistance to new patterns.
- Emotional and physical “holding.”

[SECTION: Physical Manifestations]
Excess Fixed:
- Stiffness or rigidity in the body.
- Cumulative illnesses: cysts, blockages, growths, enlargements.
- Sluggish metabolism.
- Throat, reproductive organs, colon, thyroid, circulatory system stress.

Low Fixed:
- Poor grounding.
- Weak structural stability.
- Lack of embodied energy.

[SECTION: Remedies for Excess Fixed]
- Deep body therapies: Rolfing, bioenergetics, structural integration.
- Break old emotional/physical patterns.
- Flower essences: chicory, chestnut bud, fuchsia, black-eyed Susan, trillium.
- Crystals: smoky quartz, black obsidian.
- Reduce heavy foods.

[SECTION: Remedies for Low Fixed]
- Grounding disciplines: walking, running, weight-bearing rhythms.
- Build willpower and follow-through habits.
- Crystals: tiger’s eye, hawk’s eye.
- Foods: grains, root vegetables.

[SECTION: Summary Insight]
Fixed energy stabilizes life, but excess creates rigidity and deficiency reduces consistency. Balance requires grounding + flexibility work.
""",
    "Mutable": """[SECTION: Definition & Core Meaning]
Mutable signs (Gemini, Virgo, Sagittarius, Pisces) end each season. Keyword: "Flexibility." They adapt, shift, absorb, communicate, and integrate.

[SECTION: Psychological Expression]
High Mutable:
- Flexible, adaptable, social, mentally stimulated.
- Scattered, hyper, anxious, easily distracted.
- Difficulty relaxing; insomnia; overactivity.
- Hypochondria tendencies.

[SECTION: Physical Manifestations]
High Mutable:
- Lungs, intestines, nervous system, immune system sensitivity.
- Sudden but quick-recovering illnesses.
- Recurring conditions.
- Pancreas and lymphatic issues.
- Sugar sensitivity; metabolic disorders; ulcers; headaches.

[SECTION: Remedies for Excess Mutable]
- Build concentration: yoga, tai chi, meditation, biofeedback.
- Grounding practices: gardening, nature.
- Watch sugar intake.
- Immune-support foods: A, B, C vitamins, zinc.
- Flower remedies: white chestnut, madia elegans, Shasta daisy, vervain, wild oat.
- Crystals: green calcite, aventurine, chrysoprase, chrysocolla, malachite.

[SECTION: Summary Insight]
Mutable energy brings flexibility and integration. Excess scatters; deficiency hardens. Balance requires grounding, focus, rhythm, and emotional fluidity.
"""
}


def extract_json(text):
    """
    Safely extracts JSON from LLM output.
    Works even if extra text exists around the JSON.
    """
    if not text or not isinstance(text, str):
        raise ValueError("Model returned empty or non-string response.")

    # First attempt: direct parse
    try:
        return json.loads(text)
    except:
        pass

    # Second attempt: locate outermost braces
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1:
        candidate = text[start:end+1]
        try:
            return json.loads(candidate)
        except:
            pass

    raise ValueError("Valid JSON not found in model response.")


# ============================================
# 3. PROMPT BUILDER
# ============================================

def build_modality_prompt(cardinal_pct, fixed_pct, mutable_pct):

    modality_data = {
        "Cardinal": cardinal_pct,
        "Fixed": fixed_pct,
        "Mutable": mutable_pct
    }

    merged = [
        "You are a master-level psychological and medical astrologer.",
        "Output ONLY valid JSON. No markdown. No explanations.",
        "Use the following JSON structure:",
        """
{
  "Cardinal": {
    "Percentage": "...",
    "Description": "...",
    "Psychology": "...",
    "Physical_Indicators": "...",
    "Diet_and_Lifestyle": "...",
    "Healing_Modalities": "...",
    "Flower_Essences_and_Crystals": "...",
    "Summary": "..."
  },
  "Fixed": { ... },
  "Mutable": { ... }
}
""",
        "\nREFERENCE MATERIAL:\n"
    ]

    # Attach modality descriptions
    for modality, pct in modality_data.items():
        merged.append(f"### {modality} Energy ({pct}%)")
        merged.append(MODALITY_PROMPTS[modality])

    return "\n\n".join(merged)


# ============================================
# 4. MAIN ENGINE
# ============================================

def generate_modality_report(cardinal_pct, fixed_pct, mutable_pct):

    final_prompt = build_modality_prompt(cardinal_pct, fixed_pct, mutable_pct)

    system_instruction = (
        "You MUST output only valid JSON. "
        "No markdown, no commentary, no explanation — only pure JSON."
    )

    # Gemini does NOT use role messages — merge system + content manually
    full_prompt = system_instruction + "\n\n" + final_prompt

    # Use your existing Gemini model
    response = gemini_model.generate_content(full_prompt)

    raw_output = response.text.strip()

    return extract_json(raw_output)


# ============================================
# 5. TEST RUN
# ============================================

# result = generate_modality_report(
#     cardinal_pct=1,
#     fixed_pct=0,
#     mutable_pct=6
# )

# print(json.dumps(result, indent=4))
