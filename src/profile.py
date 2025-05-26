# src/profile.py

import pandas as pd

def build_profile_for_cluster(df: pd.DataFrame, cluster_id: int) -> dict:
    cluster_df = df[df['ClusterLabel'] == cluster_id]
    avg_age = cluster_df['Age'].mean()
    avg_income = cluster_df['Income'].mean()
    avg_spend = cluster_df['Total_Spend'].mean()

    return {
        "age_group": "20-30" if avg_age < 30 else "30-45" if avg_age < 45 else "45+",
        "income_level": "low" if avg_income < 30000 else "medium" if avg_income < 60000 else "high",
        "spending_behavior": "budget-conscious" if avg_spend < 300 else "value-focused" if avg_spend < 700 else "premium and brand-loyal",
        "preferred_products": ["wine", "gold"] if avg_spend > 600 else ["food", "discounted offers"],
        "family_status": "married with kids",  # Can later use real data
        "marketing_goal": "upsell premium subscription" if avg_income > 60000 else "increase cart size with offers"
    }
