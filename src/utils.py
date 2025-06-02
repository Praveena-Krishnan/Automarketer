def extract_json(text):
    import re, json

    # Try to extract JSON block using regex
    match = re.search(r'\{[\s\S]*\}', text)

    # Fallback: manually add closing brace if it's missing
    if not match and text.strip().startswith("{") and not text.strip().endswith("}"):
        print("⚠️ Detected missing closing brace. Attempting fix...")
        text += "}"
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            print("❌ Still invalid after adding brace:", e)
            return None

    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError as e:
            print("❌ JSON parse error:", e)
            return None

    print("⚠️ No JSON found in text.")
    return None