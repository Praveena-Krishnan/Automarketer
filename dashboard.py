import streamlit as st
import pandas as pd

# Load cluster data
df = pd.read_csv("data/clustered_customers.csv")
email_df = pd.read_csv("data/cluster_emails.csv")

st.set_page_config(page_title="AutoMarketer Dashboard", layout="wide")

st.title("📊 AutoMarketer Dashboard")
st.markdown("View customer segments and preview marketing emails by cluster.")

# Sidebar for selecting cluster
clusters = sorted(df['ClusterLabel'].unique())
selected_cluster = st.sidebar.selectbox("🔍 Choose Cluster", clusters)

# Show cluster summary
st.subheader(f"🧠 Cluster {selected_cluster} Summary")
cluster_df = df[df['ClusterLabel'] == selected_cluster]

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
