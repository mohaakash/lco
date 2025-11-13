from openai import OpenAI
import json
import re
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the API key from the environment
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """
You are AstraElements — a professional Astrological Health and Elemental Balance AI.
Your purpose is to analyze the user’s elemental composition (Fire, Earth, Air, Water — as percentages)
and generate a professional, structured astrological interpretation in JSON format.

### RULES OF REASONING:
1. Interpret each element individually (Fire, Earth, Air, Water).
2. Classify each element as:
   - "Low" if < 23%
   - "Balanced" if 23–28%
   - "High" if > 28%
   - "Excluded" if 0% (omit or state "Not present")
3. For each element that exists (>0%):
   - Provide a short Description (its nature and role in health and behavior).
   - Provide a Scientific_Correlation (linking traditional ideas to modern physiology).
   - Explain Imbalance_Effects depending on High or Low status.
   - Give Remedies with subsections:
     - Diet
     - Lifestyle_and_Exercise
     - Herbal_or_Energy_Support.
   Each element = one well-written paragraph, not bullet points.

4. Integrate scientific evidence with traditional astrological insight.
5. Never output text outside JSON.

### OUTPUT FORMAT (MANDATORY):
{
  "Elemental_Analysis": {
    "Fire": {...},
    "Earth": {...},
    "Air": {...},
    "Water": {...}
  },
  "Summary": "",
  "Disclaimer": "This interpretation is for educational and holistic insights only, not medical advice."
}
"""

def clean_json_output(text):
    cleaned = re.sub(r"^```(?:json)?", "", text.strip(), flags=re.IGNORECASE | re.MULTILINE)
    cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE)
    return cleaned.strip()

def generate_elemental_report(elements):
    """
    elements: dict = {"Fire": 0, "Earth": 52, "Air": 0, "Water": 48}
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0.6,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps({"Elemental_Percentages": elements})}
        ]
    )

    raw_output = response.choices[0].message.content
    cleaned_output = clean_json_output(raw_output)

    try:
        return json.loads(cleaned_output)
    except Exception:
        return cleaned_output
    
if __name__ == "__main__":
    elements = {"Fire": 0, "Earth": 52, "Air": 0, "Water": 48}
    result = generate_elemental_report(elements)
    print(json.dumps(result, indent=2))