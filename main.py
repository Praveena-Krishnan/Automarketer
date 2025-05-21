from src.ingest import load_customer_data
from src.preprocess import preprocess_data, scale_features

if __name__ == "__main__":
    df_raw = load_customer_data("data/marketing_campaign.csv")
    df_clean = preprocess_data(df_raw)

    numeric_features = ['Income', 'Customer_Tenure', 'Age', 'Total_Spend']
    df_scaled = scale_features(df_clean, numeric_features)

    print(df_scaled[numeric_features].head())

    #print(df_raw['Year_Birth'].describe())