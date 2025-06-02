import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from src.email_generator import generate_email
from src.utils import extract_json
from src.profile import build_profile_for_cluster
from src.send_real_email import send_real_email

# ─────────────────────────────────────────────────────────────────────────────
# Page Setup & Style
st.set_page_config(page_title="AutoMarketer Dashboard", layout="wide")
st.markdown(
    """
    <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: 600;
            border-radius: 8px;
            padding: 0.5em 1em;
        }
        .stTextInput>div>input, .stTextArea>div>textarea {
            border-radius: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <style>
    /* Dark background for the whole app */
    .stApp {
        background-color: #121212;
        color: #f1f1f1;
    }

    /* Text inputs and text area */
    .stTextInput > div > input,
    .stTextArea > div > textarea {
        background-color: #1e1e1e;
        color: #ffffff;
        border: 1px solid #444;
        border-radius: 5px;
    }

    /* Headings */
    h1, h2, h3, h4, h5 {
        color: #f5f5f5;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #1f1f1f;
        color: #f1f1f1;
    }

    /* Buttons */
    .stButton>button {
        background-color: #1f6feb;
        color: white;
        border-radius: 6px;
        padding: 0.5em 1em;
        font-weight: bold;
    }

    /* Toast / popup */
    .stToast {
        background-color: #333 !important;
        color: #eee !important;
    }

    /* Dataframe text */
    .stDataFrame {
        background-color: #1e1e1e;
    }

    /* Code blocks */
    .stCodeBlock {
        background-color: #1e1e1e;
        color: #f8f8f2;
    }

    </style>
    """,
    unsafe_allow_html=True
)


st.title("🚀 AutoMarketer Dashboard")
st.caption("Powering personalized marketing with ML + LLMs.")

# ─────────────────────────────────────────────────────────────────────────────
# Load Data
df = pd.read_csv("data/clustered_customers.csv")
email_df = pd.read_csv("data/cluster_emails.csv")
clusters = sorted(df['ClusterLabel'].unique())

# ─────────────────────────────────────────────────────────────────────────────
# Tabs Layout
tab1, tab2, tab3 = st.tabs([" Cluster Insights", "Email Editor", "📤 Send Email"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1: Cluster Insights
with tab1:
    selected_cluster = st.selectbox("🔍 Select Cluster", clusters)
    cluster_df = df[df["ClusterLabel"] == selected_cluster]

    st.subheader(f" Cluster {selected_cluster} Summary")
    st.write(f"**🧮 Total Customers:** {len(cluster_df)}")

    st.markdown("### 📈 Average Metrics")
    avg_values = cluster_df[['Income', 'Customer_Tenure', 'Age', 'Total_Spend']].mean()
    st.bar_chart(avg_values)

    if 'Education' in cluster_df.columns:
        st.markdown("### 🎓 Education Breakdown")
        edu_counts = cluster_df['Education'].value_counts()
        fig, ax = plt.subplots()
        ax.pie(edu_counts, labels=edu_counts.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)

    st.markdown("### 🔎 Detailed Stats")
    st.dataframe(cluster_df.describe()[['Income', 'Customer_Tenure', 'Age', 'Total_Spend']])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2: Email Editor
with tab2:
    email_row = email_df[email_df["ClusterID"] == selected_cluster]

    st.subheader("📧 Current Email for this Cluster")

    if not email_row.empty:
        col1, col2 = st.columns([1, 3])
        edited_subject = col1.text_input("Subject", value=email_row['Subject'].values[0], key="subject_editor")
        edited_body = col2.text_area("Body", value=email_row['Body'].values[0], height=250, key="body_editor")
    else:
        edited_subject = st.text_input("Subject", "", key="subject_editor")
        edited_body = st.text_area("Body", "", height=250, key="body_editor")
        st.warning("No email found for this cluster.")

    col_save, col_regen = st.columns(2)

    with col_save:
        if st.button("💾 Save Changes"):
            email_df.loc[email_df["ClusterID"] == selected_cluster, "Subject"] = edited_subject
            email_df.loc[email_df["ClusterID"] == selected_cluster, "Body"] = edited_body
            email_df.to_csv("data/cluster_emails.csv", index=False)
            st.toast("✅ Email saved for this cluster")

    with col_regen:
        if st.button("🔄 Regenerate with LLM"):
            profile = build_profile_for_cluster(df, selected_cluster)
            new_email_json = generate_email(profile, cluster_label=selected_cluster)
            new_email = extract_json(new_email_json)

            if new_email:
                edited_subject = new_email["subject"]
                edited_body = new_email["body"]
                email_df.loc[email_df["ClusterID"] == selected_cluster, "Subject"] = edited_subject
                email_df.loc[email_df["ClusterID"] == selected_cluster, "Body"] = edited_body
                email_df.to_csv("data/cluster_emails.csv", index=False)
                st.toast("✅ New email generated and saved")
                st.experimental_rerun()
            else:
                st.error("❌ Failed to generate email using LLM")

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3: Send Email
with tab3:
    st.subheader("📤 Send Email to a Customer")
    recipient = st.text_input("Recipient Email", placeholder="e.g. your@gmail.com", key="recipient_email")

    st.markdown("#### ✏️ Preview (Editable)")
    email_row = email_df[email_df["ClusterID"] == selected_cluster]
    subject = email_row['Subject'].values[0] if not email_row.empty else ""
    body = email_row['Body'].values[0] if not email_row.empty else ""

    subject_input = st.text_input("Subject", value=subject, key="subject_sender")
    body_input = st.text_area("Body", value=body, height=250, key="body_sender")

    if st.button("📬 Send Email"):
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")

        if sender_email and sender_password:
            try:
                send_real_email(
                    recipient=recipient,
                    subject=subject_input,
                    body=body_input,
                    sender_email=sender_email,
                    sender_password=sender_password
                )
                st.toast(f"✅ Email sent to {recipient}")
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")
        else:
            st.error("Missing sender credentials in .env")
st.markdown(
    """
    <hr>
    <div style='text-align: center; font-size: 0.9rem; color: #999;'>
        Built with ❤️ by <strong>Praveena Krishnan</strong> · 
        <a href="https://github.com/Praveena-Krishnan/Automarketer" target="_blank">GitHub</a>
    </div>
    """,
    unsafe_allow_html=True
)