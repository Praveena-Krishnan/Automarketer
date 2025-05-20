import pandas as pd

def load_customer_data(filepath: str) -> pd.DataFrame:
    """
    Loads customer personality analysis data from a CSV file.
    """
    try:
        df = pd.read_csv(filepath, sep='\t')  # The original file is often TSV
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()
