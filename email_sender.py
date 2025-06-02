from src.send_real_email import send_real_email
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables (sender email + password)
load_dotenv()
recipient = os.getenv("SENDER_EMAIL")  # you're sending to yourself
sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")

# Load customer data (with clusters)
customers = pd.read_csv("data/clustered_customers.csv")
emails = pd.read_csv("data/cluster_emails.csv")

# 📍 Select a sample customer by row index (e.g., first customer)
test_customer = customers.iloc[0]
cluster_id = test_customer["ClusterLabel"]

# Fetch the email template for this cluster
email_row = emails[emails["ClusterID"] == cluster_id].iloc[0]
subject = email_row["Subject"]
body = email_row["Body"]

# Send real email
send_real_email(
    recipient=recipient,
    subject=subject,
    body=body
)
