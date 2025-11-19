from openai import OpenAI
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


gemini_model = genai.GenerativeModel("gemini-2.5-flash")


# FIRE PROMPTS
fire_low = """[SECTION: Element Overview]
Fire governs digestion, vitality, metabolism, emotional strength, immune responsiveness, warmth, motivation, and clarity. Low Fire shows through weak circulation, low energy, pale/dry skin, dull eyes, slow digestion, low immunity, and weakened confidence or ambition.

[SECTION: Physical Indicators]
- Urine: Light-colored, suggesting underactive metabolism.
- Skin: Pale, cold, dry.
- Eyes: Dull, tired, or nearsighted.
- Digestion: Slow, gassy, heavy, prone to brain fog or headaches.
- Immunity: Lethargic immune response; frequent illness.
- Body: Cold extremities, weak muscles, low body heat.

[SECTION: Emotional / Psychological Indicators]
- Low motivation, depleted joy.
- Decreased confidence, self-esteem, and courage.
- Depression, avoidance, difficulty initiating action.

[SECTION: Root Cause Dynamics]
Low Fire = weak Liver/Gallbladder axis (TCM), stagnation in digestion, emotional suppression, and chronic depletion of energy reserves.

[SECTION: Ways to Increase Fire]
Diet:
- Warming / stimulating foods: lemon, yogurt, cayenne, cinnamon, cardamom, curry, ginger, peppermint tea.
- Bitter and detoxifying herbs: burdock root, dandelion leaf.

Lifestyle & Exercise:
- Aerobic movement: hiking, skating, skiing.
- Exposure to warmth: candles, fireplaces, red/orange environments.

Herbal / Flower Remedies:
- Gems: carnelian, ruby, bloodstone, topaz.
- Flower remedies: Indian paintbrush, scarlet monkey flower.
- Aromas: basil, cinnamon, black pepper.

[SECTION: Summary Insight]
Low Fire = low spark. Restoration comes from warmth, circulation, stimulation, confidence-building activity, and digestive activation.
"""
fire_high = """[SECTION: Element Overview]
High Fire manifests as heat, inflammation, irritability, overdrive metabolism, dehydration, and emotional excess. It boosts energy but risks burnout.

[SECTION: Physical Indicators]
- Urine: Dark, strong odor.
- Skin: Redness, breakouts, inflammation, oily texture.
- Eyes: Sharp, intense; farsightedness possible.
- Digestion: Fast hunger, excessive appetite, diarrhea.
- Immunity: Overreactivity (fevers, swelling).
- Body: Sweating, dehydration, high blood pressure, migraines, ulcers.

[SECTION: Emotional Indicators]
- Anger, impatience, irritability.
- Pushiness, dominance, ego-centered focus.
- Burnout cycles (adrenal fatigue).

[SECTION: Root Dynamics]
Excess Fire overheats organs, taxes kidneys (TCM), and drives emotional volatility.

[SECTION: Cooling Strategies]
Diet:
- Cooling/hydrating foods: cucumber, melon, zucchini, apples, pears, tofu, soy, fish (not trout), seaweed, pumpkin seeds.
- Fluids: high hydration priority.
- Avoid overheating drinks/foods.

Lifestyle & Exercise:
- Swimming, cool baths.
- Reduce competition, intense heat exposure.
- Limit alcohol and emotional extremes.
- Wear greens/blues.

Herbal / Flower Remedies:
- Herbs: hops, violet, aloe, agrimony, rhubarb, sorrel, water lily, mallows.
- Gems: green calcite, aquamarine, emerald, malachite.
- Flower remedy: impatiens (anger modulation).
- TCM: strengthen kidneys to counter Excess Fire.

[SECTION: Summary Insight]
Excess Fire = heat overload. Cooling, hydration, emotional regulation, and kidney support restore balance.

"""
fire_balanced = """ [SECTION: Element Overview]
Balanced Fire expresses vitality, strong digestion, emotional warmth, sharp perception, decisive action, optimism, and resilience.

[SECTION: Physical Indicators]
- Eyes: Bright, clear.
- Skin: Warm, slightly rosy glow.
- Digestion: Strong but comfortable.
- Immunity: Responsive and strong.
- Energy: Motivated, stable, not excessive.

[SECTION: Emotional Indicators]
- Cheerful, alert, courageous, optimistic.
- Passionate without aggression.
- Quick recovery from emotional challenges.

[SECTION: Maintenance Guidance]
To maintain balance:
- Avoid excessive stimulants or heat.
- Use cooling, grounding rituals if stress rises.
- Practice moderate physical exertion.
- Ensure proper hydration.

[SECTION: Balancing Guidance (when slight over-fire appears)]
“To cool down”: introduce moisture, calming foods, grounding colors, restorative environments.

[SECTION: Summary Insight]
Balanced Fire supports joy, clarity, purpose, and immunity. Maintenance focuses on preventing overheating through moderation.

"""

# EARTH PROMPTS
earth_low = """[SECTION: Element Overview]
Earth offers stability, nourishment, structure, routine, discipline, and physical robustness. Low Earth weakens grounding, consistency, and embodiment.

[SECTION: Indicators of Low Earth]
- Spacey, unfocused, ungrounded.
- Difficulty completing tasks.
- Poor routines (eating, sleep, discipline).
- Lack of connection to the body.
- Dry skin, brittle bones, weak tone.

[SECTION: Psychological Indicators]
- Unrealistic planning.
- Disorganization.
- Escapism.
- Emotional inconsistency.

[SECTION: Strengthening Strategies]
Diet:
- Grounding/nutrient-dense foods: root vegetables, whole grains, mineral-rich meals.
- Warm, moist foods for nourishment.

Lifestyle:
- Routine building (meals, sleep, work).
- Outdoor activities with sun exposure.
- Earth-tone environments.

Crystals & Remedies:
- Chestnut bud, chicory, oak, mustard.
- Carnelian, hematite, rhodochrosite, fire agate.

TCM:
- Strengthen Liver/Gallbladder to support structure.

[SECTION: Summary Insight]
Low Earth needs grounding, routine, nourishment, and embodiment to rebuild stability.

"""
earth_high = """[SECTION: Element Overview]
High Earth intensifies heaviness, rigidity, accumulation, stagnation, and resistance to change. Physically and psychologically, density overtakes flow.

[SECTION: Physical Indicators]
- Thickened tissues, sluggish digestion.
- Calcium deposits, sclerosis.
- Slow metabolism, congestion.
- Joint blockages, heaviness.

[SECTION: Psychological Indicators]
- Stubbornness, over-caution, inflexibility.
- Avoidance of new ideas.
- Over-focus on material security.

[SECTION: Dietary Relief]
- Light, quick-digesting foods.
- Reduce dense foods: meats, potatoes, dairy excess.
- Herbs: borage, lemon balm, senna, polypody.

[SECTION: Lifestyle Relief]
- Precision sports: tennis, badminton, anything that increases agility.
- Bright colors (yellow, gold, orange).
- Movement practices that break stagnation.

Crystals & Remedies:
- Carnelian, fire agate.
- Flower remedies: chestnut bud, chicory, mustard.

TCM:
- Activate Wood organs (liver/gallbladder) to disperse accumulation.

[SECTION: Summary Insight]
Excess Earth = too much rigidity. Lightness, heat, movement, and variety break the stagnation.

"""
earth_balanced = """[SECTION: Element Overview]
Balanced Earth brings endurance, stability, practicality, discipline, good digestion, strong bones, reliability, and emotional steadiness.

[SECTION: Physical Indicators]
- Strong tissues, smooth skin.
- Steady appetite and digestion.
- Stable energy levels.

[SECTION: Emotional Indicators]
- Practicality, consistency.
- Realistic planning.
- Dependability.

[SECTION: Maintaining Balance]
- Balanced eating (not too heavy).
- Routine but flexible rhythms.
- Avoid emotional rigidity.
- Mix grounding with periodic lightness (air/movement).

[SECTION: If Air = Balanced (23–28%)]
Introduce harmonizing insights:
- Air adds flexibility, creativity, mental clarity.
- Combined Earth + Air balance = adaptable consistency without rigidity.

[SECTION: Summary Insight]
Balanced Earth is stable, steady, and dependable—maintenance requires avoiding stagnation.

"""

# AIR PROMPTS
air_low = """[SECTION: Element Overview]
Air governs movement, communication, perception, nervous system activity, and circulation. Low Air generates heaviness, introversion, sluggish thinking, and poor movement.

[SECTION: Physical Indicators]
- Poor circulation.
- Shortness of breath.
- Stiffness, inflexibility.
- Low elasticity in tissues.
- Slow reaction times.

[SECTION: Emotional Indicators]
- Introversion, limited communication.
- Reduced humor.
- Difficulty making decisions.
- Fatigue, mental dullness.

[SECTION: Dietary Guidance]
- Herbal teas: gotu kola, fo-ti.
- Raw fruits/vegetables, juices, sprouts.
- Avoid heavy foods.

[SECTION: Lifestyle Guidance]
- Deep breathing.
- Mountain trips.
- Dancing, group work.
- Sky colors: blue, coral.
- Calming music.

Remedies:
- Flower: scleranthus, sweet pea, quaking grass.
- TCM: stimulate stomach/spleen meridians.

[SECTION: Summary Insight]
Low Air needs movement, breath, connection, communication, and mental stimulation.

"""
air_high = """[SECTION: Element Overview]
High Air intensifies dryness, restlessness, nervous overactivity, erratic digestion, and excessive mental chatter.

[SECTION: Physical Indicators]
- Lean, wiry frame.
- Dry skin/hair; visible veins.
- Irregular digestion, bloating, constipation.
- Rapid movements; joint creaks.
- Spasms, tics, shooting pains.
- Insomnia (2–6 a.m. wakeups).

[SECTION: Emotional Indicators]
- Anxiety, fear, overthinking.
- Fragmented attention.
- Impulsivity.
- Difficulty grounding.

[SECTION: Dietary Support]
- Grounding foods: whole grains, leafy greens.
- Hydration needed.
- Calming teas: chamomile, skullcap, vervain, valerian.
- Cold/dry foods to counter heat.

[SECTION: Lifestyle Support]
- Moderate exercise.
- Reduce overstimulation.
- Gardening, grounding tasks.
- Dry sauna to release moisture.
- Deep rest periods.

Crystals:
- Blue tourmaline, chrysocolla, aquamarine.

Flower Remedies:
- White chestnut, mimulus, lavender.

TCM:
- Mild heat/spices to support circulation.

[SECTION: Summary Insight]
High Air requires grounding, moisture, warmth, and slower rhythms to stabilize the overactive mind.
"""

air_balanced = """
[SECTION: Element Overview]
Balanced Air shows clear perception, fluid communication, emotional lightness, and effective nervous-system function.

[SECTION: Indicators]
- Graceful movement.
- Clear, balanced mental activity.
- Healthy circulation and respiratory flow.

[SECTION: Harmonizing Insight]
If Air is 23–28%:
- Air supports curiosity, adaptability, and clarity.
- Integrates smoothly with all other elements.

[SECTION: Summary Insight]
Balanced Air = clarity, communication, creativity, and mental agility.

"""

# WATER PROMPTS
water_low = """[SECTION: Element Overview]
Water governs emotion, intuition, lymphatics, fluids, cohesion, softness, and restorative capacity. Low Water mimics excess Air.

[SECTION: Physical Indicators]
- Stiffness, dehydration.
- Dry skin, brittle nails/hair.
- Sleep difficulties.
- Lack of smoothness and calm.

[SECTION: Emotional Indicators]
- Anxiety, instability.
- Weak emotional comprehension.
- Low empathy.
- Difficulty expressing feelings.

[SECTION: Diet]
- Increase fluids: vegetable juices, herbal teas.
- Moist foods: juicy fruits, hydrating vegetables.

[SECTION: Lifestyle]
- Swimming / water environments.
- Artistic expression.
- Relaxation practices.

Flower Remedies & Crystals:
- Holly, fuchsia, garlic.
- Pearl, opal, smoky quartz.

TCM:
- Stimulate Lung/Large Intestine to support Water.

[SECTION: Summary Insight]
Low Water = dryness + emotional disconnection. Moisture, rest, and emotional expression restore flow.

"""
water_high = """[SECTION: Element Overview]
High Water amplifies emotional heaviness, fluid retention, mucus buildup, lethargy, and hypersensitivity.

[SECTION: Physical Indicators]
- Phlegm, mucus, edema.
- Slow metabolism.
- Cold, soft body.
- Prone to colds, congestion, allergies.

[SECTION: Emotional Indicators]
- Moodiness, defensiveness.
- Overattachment, clinginess.
- Dreaminess, escapism.
- Subjective perception.

[SECTION: Dietary Reduction]
- Warm, dry foods.
- Reduce sweets, dairy, bread, salt.
- Use hot spices: cayenne, ginger, horseradish.
- Diuretic herbal teas: dandelion leaf, nettle, alfalfa.

[SECTION: Lifestyle Guidance]
- Avoid cold exposure.
- Seek heat sources.
- Saunas (long sessions).
- Moderate exercise (not too intense).
- Short sleep + regular movement.

Crystals:
- Rose quartz, amethyst, fluorite.

Flower Remedies:
- Honeysuckle, red chestnut, chamomile.

TCM:
- Support stomach/spleen to reduce Water accumulation.

[SECTION: Summary Insight]
Excess Water = emotional/physical heaviness. Dryness, heat, structure, and emotional boundaries restore balance.
"""
water_balanced = """[SECTION: Element Overview]
Balanced Water offers emotional sensitivity, intuition, creativity, softness, cohesion, and gentle perception.

[SECTION: Indicators]
- Smooth, plump body type.
- Melting eyes, plentiful hair.
- Calm, serene, protective personality.
- Stable lymphatic and fluid flow.

[SECTION: Harmonizing Insight]
If Water is balanced:
- Enhance intuition through creative arts.
- Maintain fluidity through hydration and gentle movement.

If combined with Balanced Air:
- Harmonizes emotional intelligence with mental clarity.

[SECTION: Summary Insight]
Balanced Water = empathy, intuition, serenity, and emotional resilience.

"""


# ----------------------------
# 2. ELEMENT LOGIC FUNCTIONS
# ----------------------------

def build_fire_prompt(value):
    if value == 0:
        return ""  # exclude completely
    if value > 28:
        return fire_high
    if value < 23:
        return fire_low
    return fire_balanced


def build_earth_prompt(value):
    if value == 0:
        return ""
    if value > 28:
        return earth_high
    if value < 23:
        return earth_low
    return earth_balanced


def build_air_prompt(value):
    if value == 0:
        return ""
    if value > 28:
        return air_high
    if value < 23:
        return air_low
    return air_balanced


def build_water_prompt(value):
    if value == 0:
        return ""
    if value > 28:
        return water_high
    if value < 23:
        return water_low
    return water_balanced


# ----------------------------
# 3. BUILD THE FINAL PROMPT
# ----------------------------

def build_final_prompt(fire, earth, air, water):
    prompt = ""

    prompt += build_fire_prompt(fire)
    prompt += "\n\n"
    prompt += build_earth_prompt(earth)
    prompt += "\n\n"
    prompt += build_air_prompt(air)
    prompt += "\n\n"
    prompt += build_water_prompt(water)

    return prompt.strip()


# ----------------------------
# 4. CLEANING RESPONSE
# ----------------------------
def clean_json_output(text):
    cleaned = text.strip().replace("```json", "").replace("```", "")
    cleaned = cleaned.replace("\n", "")   # REMOVE ALL NEWLINES
    return cleaned.strip()


# ----------------------------
# 5. GPT REQUEST FUNCTION
# ----------------------------

def generate_elemental_report(fire, earth, air, water):
    # Ensure all values are integers (fixes Balanced–Low bugs)
    try:
        fire = int(fire)
        earth = int(earth)
        air = int(air)
        water = int(water)
    except:
        raise ValueError("All elemental values must be numbers.")

    # Build the combined user prompt
    final_prompt = build_final_prompt(fire, earth, air, water)
    # print(final_prompt)
    # SYSTEM PROMPT (unchanged as requested)
    system_prompt = """
You are AstraElements — a professional Astrological Health and Elemental Balance AI.
Your purpose is to analyze the user’s elemental composition (Fire, Earth, Air, Water — as percentages)
and generate a professional, structured astrological interpretation in JSON format.
**Based on user input write the classifaction perfectly**

### RULES OF REASONING:
1. Interpret each element individually (Fire, Earth, Air, Water).
2. Classify each element as:
   - "Low" if < 23%
   - "Balanced" if 23–28%
   - "High" if > 28%
   - "Excluded" if 0% (omit or state "Not present").
3. For each element that exists (>0%):
   • Write **four detailed sections**, each around **200 words**:
      - Description (200 words)
      - Diet (200 words)
      - Lifestyle_and_Exercise (200 words)
      - Herbal_or_Flower_Remedies, (200 words)
   - Each element must be written as **one broad, coherent, well-written paragraph of approximately 200 words**.
   - Do NOT use bullet points or lists inside element descriptions.
4. Integrate scientific evidence with traditional astrological insight.
5. Never output text outside JSON.

### TASK:
Your task is to extract and reorganize the content into the following STRICT JSON structure for each element (**Description**, **Diet**, **Lifestyle and Exercise**, **Herbal_or_Flower_Remedies**):
**Example**:
"Fire": {
  "Classification": "...",
  "Description": "...",
  "Diet": "...",
  "Lifestyle_and_Exercise": "...",
  "Herbal_or_Flower_Remedies": "..."
},
    "Earth": {...},
    "Air": {...},
    "Water": {...}

### RULES:
1. DO NOT rewrite or shorten — use the user's text EXACTLY as provided and **explain each and every point**.
2. Split the text into the correct sections based on the labels inside the text.
3. Output ONLY valid JSON.
"""

    # Call OpenAI
    # Gemini requires a SINGLE STRING PROMPT
    prompt = system_prompt + "\n\nUSER INPUT:\n" + final_prompt

    response = gemini_model.generate_content(prompt)

    raw_output = response.text
    cleaned_output = clean_json_output(raw_output)

    try:
        return json.loads(cleaned_output)
    except:
        return cleaned_output


def generate_daily_guideline(user_input, elemental_report):
    """
    user_input = dict: {"fire":25, "earth":25, "air":25, "water":25}
    elemental_report = dict: previous LLM output (fire_low, earth_high etc.)
    """

    guideline_system_prompt = """
You are AstraElements — an advanced Elemental Health AI.

Generate a holistic *Daily Diet & Lifestyle Guideline* based on:
1. The user's elemental percentages
2. The previously generated elemental interpretation JSON

### STRICT RULES:
- Output ONLY valid JSON.
- Each section must contain ~100 words.
- No bullet points, no numbering — write in natural paragraphs.
- Use both the user's elemental values AND their report to personalize recommendations.
- The final JSON structure MUST be:

{
  "Morning": {
    "Diet": "...",
    "Lifestyle": "...",
    "Wear_Clothing": "...",
    "Exercise": "..."
  },
  "Midday": {
    "Diet": "...",
    "Lifestyle": "...",
    "Optional": "..."
  },
  "Evening": {
    "Diet": "...",
    "Lifestyle": "...",
    "Exercise": "..."
  },
  "Weekly_Addition": "..."
}

### GUIDELINE RULES:
- Morning section should focus on activation, grounding, or balancing based on elements.
- Midday should maintain stability and productivity based on dominant elements.
- Evening should calm, restore, and detox depending on imbalances.
- Weekly addition = 3–4 lines summarizing long-term support techniques.

NEVER include anything outside JSON.
"""

    final_user_prompt = f"""
User elemental input (percentages):
{json.dumps(user_input, indent=2)}

Previous elemental analysis:
{json.dumps(elemental_report, indent=2)}

Generate the structured JSON guideline now.
"""

    prompt = guideline_system_prompt + "\n\n" + final_user_prompt

    response = gemini_model.generate_content(prompt)

    raw = response.text
    cleaned = clean_json_output(raw)

    try:
        return json.loads(cleaned)
    except:
        return cleaned


# # ----------------------------
# # 6. EXAMPLE CALL
# # ----------------------------
# user_input = {
#     "fire": 32,
#     "earth": 12,
#     "air": 28,
#     "water": 28
# }

# first_report = generate_elemental_report(
#     fire=32, earth=12, air=28, water=28
# )

# print(json.dumps(first_report, indent=2))

# daily_guideline = generate_daily_guideline(user_input, first_report)

# print(json.dumps(daily_guideline, indent=2))
