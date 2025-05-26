from src.ingest import load_customer_data
from src.preprocess import preprocess_data, scale_features
from src.cluster import find_optimal_k, apply_kmeans
from src.email_generator import generate_email
from src.profile import build_profile_for_cluster
import json 
import re


def extract_json(text):
    match = re.search(r'\{[\s\S]*\}', text)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            print("⚠️ Extracted block is not valid JSON.")
            return None
    else:
        print("⚠️ No JSON found in response.")
        return None


if __name__ == "__main__":
    df_raw = load_customer_data("data/marketing_campaign.csv")
    df_clean = preprocess_data(df_raw)

    numeric_features = ['Income', 'Customer_Tenure', 'Age', 'Total_Spend']
    df_scaled = scale_features(df_clean, numeric_features)

    print(df_scaled[numeric_features].head())

    #print(df_raw['Year_Birth'].describe())
    
    # Step 1: Find optimal number of clusters
    best_k = find_optimal_k(df_scaled, numeric_features)
    #print(f"Best K: {best_k}")
    #print("\nAny NaNs in features?", df_scaled[numeric_features].isnull().any())
    print("Feature types:\n", df_scaled[numeric_features].dtypes)
    print(df_scaled[numeric_features].head())
    print(f"Best K: {best_k}")
    print(">> Now applying KMeans...")

    # try:
    #     df_clustered = apply_kmeans(df_scaled, numeric_features, n_clusters=best_k)
    #     print(">> KMeans successfully applied.")
    # except Exception as e:
    #     print("❌ Error during KMeans:", e)
    #Step 2: Apply KMeans clustering
    df_clustered = apply_kmeans(df_scaled, numeric_features, n_clusters=best_k)
    print("\nCluster distribution:")
    print(df_clustered['ClusterLabel'].value_counts())

    print("\nCluster summary (mean of features):")
    print(df_clustered[['ClusterLabel'] + numeric_features].groupby('ClusterLabel').mean())
    
    
    # Step 3: Save the clustered DataFrame
    df_clustered.to_csv("data/clustered_customers.csv", index=False)
    print("Clustered data saved to 'data/clustered_customers.csv'")
    
    print("\n🔗 Generating marketing emails for each cluster...\n")

    cluster_ids = df_clustered['ClusterLabel'].unique()
    for cluster_id in cluster_ids:
        print(f"\n📦 Cluster {cluster_id}")
        profile = build_profile_for_cluster(df_clustered, cluster_id)

        try:
            email_json_str = generate_email(profile, cluster_label=cluster_id)
            
            # print("📤 Raw LLM output:")
            # print(email_json_str)  # Debug print

            email_data = extract_json(email_json_str)

            if email_data:
                print("✅ Subject:", email_data["subject"])
                print("✅ Body:\n", email_data["body"])
                
            


        except Exception as e:
            print(f"❌ Failed to generate email for cluster {cluster_id}:", e)
