# src/email_generator.py

from groq import Groq
import json
# Directly pass the API key here (not recommended for production, fine for testing)
GROQ_API_KEY = "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"  # 🔐 Replace with your actual Groq API key

client = Groq(api_key=GROQ_API_KEY)

def generate_email(customer_profile: dict, cluster_label: int) -> str:
    """
    Generate a personalized marketing email using the Groq LLM.
    """
    prompt = f"""
        You are a professional marketing copywriter.

        Write a short promotional email for a customer with the following characteristics:

        {json.dumps(customer_profile, indent=2)}

        The email should:
        - Sound like it's for an individual person, not a "cluster"
        - Be friendly, persuasive, and natural
        - Be no more than 120–150 words
        - Include a catchy subject line and an engaging body

        Output must be in **JSON format only**:
        {{
        "subject": "Your catchy subject line here",
        "body": "The email body here"
        }}

        ❌ Do not mention clusters, segments, or technical terms
        ✅ Write as if you're emailing a single customer
        ✅ Only return the JSON. No explanations, labels, or extra text.
        """



    response = client.chat.completions.create(
        model="llama3-8b-8192",  # or "llama3-8b-8192"
        messages=[
            {"role": "system", "content": "You are a helpful marketing assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
