from src.ingest import load_customer_data
from src.preprocess import preprocess_data, scale_features
from src.cluster import find_optimal_k, apply_kmeans

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