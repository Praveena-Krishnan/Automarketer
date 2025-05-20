from src.ingest import load_customer_data

if __name__ == "__main__":
    data_path = "data/marketing_campaign.csv"  # Update if your file is named differently
    df = load_customer_data(data_path)
    print(df.head())
