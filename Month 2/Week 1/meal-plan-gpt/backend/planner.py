import json
import re
from ollama_client import run_ollama

PROMPT_TEMPLATE = """
You are a meal planning assistant. Create a {days}-day meal plan (breakfast, lunch, dinner, and snack) for someone following a {diet} diet with {calories} kcal per day.

Return only the plan as JSON in the following format:
[
  {{
    "day": 1,
    "meals": {{
      "breakfast": "Example",
      "lunch": "Example",
      "dinner": "Example",
      "snack": "Example"
    }}
  }}
]
"""

def extract_json(text):
    # Cherche le premier bloc de texte entre [ et ]
    match = re.search(r"\[\s*{.*?}\s*\]", text, re.DOTALL)
    if not match:
        raise ValueError("❌ No JSON array found in LLM output.")
    return json.loads(match.group(0))

def generate_meal_plan(diet: str, calories: int, days: int = 7):
    prompt = PROMPT_TEMPLATE.format(diet=diet, calories=calories, days=days)
    result = run_ollama(prompt)
    print("\n🧠 Raw LLM output:\n", result)

    try:
        parsed = extract_json(result)
        return parsed
    except Exception as e:
        print("❌ Failed to parse LLM output:", e)
        return {"error": "Parsing error", "raw_output": result}
