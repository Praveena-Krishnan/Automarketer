import requests

API_URL = "https://api.groq.ai/v1/generate"  # Example endpoint, verify actual from docs
API_KEY = "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"


def generate_email_with_groq(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.1",  # Use the exact model Groq provides
        "prompt": prompt,
        "max_tokens": 300,
        "temperature": 0.7,
        "stop": ["\n\n"]
    }

    response = requests.post(API_URL, json=data, headers=headers)
    response.raise_for_status()
    completion = response.json()

    # Adjust this depending on the exact Groq response structure
    return completion.get("text", "").strip()

def generate_email_for_cluster(cluster_summary: dict, tone: str = "friendly") -> str:
    prompt = (
        f"Write a {tone} marketing email targeting customers with the following profile:\n"
        f"Income: {cluster_summary.get('Income', 'N/A'):.2f}, "
        f"Customer Tenure: {cluster_summary.get('Customer_Tenure', 'N/A'):.2f}, "
        f"Age: {cluster_summary.get('Age', 'N/A'):.2f}, "
        f"Total Spend: {cluster_summary.get('Total_Spend', 'N/A'):.2f}.\n"
        "Focus on engaging the customer and encouraging purchases."
    )
    return generate_email_with_groq(prompt)

# Example usage
if __name__ == "__main__":
    sample_cluster = {
        "Income": 0.82,
        "Customer_Tenure": 0.14,
        "Age": 0.22,
        "Total_Spend": 1.02
    }
    email_text = generate_email_for_cluster(sample_cluster)
    print("Generated Email:\n", email_text)
