import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from src.email_generator import generate_email
from src.utils import extract_json
from src.profile import build_profile_for_cluster
from src.send_real_email import send_real_email

# Set up page
st.set_page_config(page_title="AutoMarketer Dashboard", layout="wide")
st.title("📊 AutoMarketer Dashboard")
st.markdown("View customer segments and preview marketing emails by cluster.")

# Load data
df = pd.read_csv("data/clustered_customers.csv")
email_df = pd.read_csv("data/cluster_emails.csv")

# Sidebar: Cluster selector
clusters = sorted(df['ClusterLabel'].unique())
selected_cluster = st.sidebar.selectbox("🔍 Choose Cluster", clusters)

# Cluster Summary
st.subheader(f"🧠 Cluster {selected_cluster} Summary")
cluster_df = df[df['ClusterLabel'] == selected_cluster]

st.markdown("### 📈 Cluster Visualizations")

# Bar chart
avg_values = cluster_df[['Income', 'Customer_Tenure', 'Age', 'Total_Spend']].mean()
st.bar_chart(avg_values)

# Pie chart for education
if 'Education' in cluster_df.columns:
    st.markdown("#### 🎓 Education Breakdown")
    edu_counts = cluster_df['Education'].value_counts()
    fig, ax = plt.subplots()
    ax.pie(edu_counts, labels=edu_counts.index, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

st.write("**Customer Count:**", len(cluster_df))
st.write(cluster_df.describe()[['Income', 'Customer_Tenure', 'Age', 'Total_Spend']])

# Show email
st.subheader("📧 Generated Marketing Email")
email_row = email_df[email_df['ClusterID'] == selected_cluster]

if not email_row.empty:
    st.write(f"**Subject:** {email_row['Subject'].values[0]}")
    st.markdown(email_row['Body'].values[0])
else:
    st.warning("No email found for this cluster.")

# Edit email
st.markdown("### ✍️ Edit Email")
edited_subject = st.text_input("Subject", value=email_row['Subject'].values[0])
edited_body = st.text_area("Body", value=email_row['Body'].values[0], height=200)

if st.button("💾 Save Changes"):
    email_df.loc[email_df['ClusterID'] == selected_cluster, 'Subject'] = edited_subject
    email_df.loc[email_df['ClusterID'] == selected_cluster, 'Body'] = edited_body
    email_df.to_csv("data/cluster_emails.csv", index=False)
    st.success("Email updated and saved successfully.")

# Regenerate email using LLM
if st.button("🔄 Regenerate Email"):
    profile = build_profile_for_cluster(df, selected_cluster)
    new_email_json = generate_email(profile, cluster_label=selected_cluster)
    new_email = extract_json(new_email_json)

    if new_email:
        edited_subject = new_email["subject"]
        edited_body = new_email["body"]
        st.success("New email generated!")
        st.experimental_rerun()
    else:
        st.error("Failed to generate new email.")

# Send real email
st.markdown("## ✉️ Send Real Email to a Customer")

recipient = st.text_input("Recipient Email (e.g. you@example.com)")
preview_subject = st.text_input("📌 Subject (editable)", value=edited_subject)
preview_body = st.text_area("📝 Body (editable)", value=edited_body, height=200)

if st.button("📤 Send Email to Customer"):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")

    if sender_email and sender_password:
        try:
            send_real_email(
                recipient=recipient,
                subject=preview_subject,
                body=preview_body,
                sender_email=sender_email,
                sender_password=sender_password
            )
            st.success(f"✅ Email sent to {recipient}")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")
    else:
        st.error("❌ Missing SENDER_EMAIL or SENDER_PASSWORD in your environment.")
