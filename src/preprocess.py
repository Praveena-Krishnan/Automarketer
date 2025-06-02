import pandas as pd
from datetime import datetime
from sklearn.preprocessing import StandardScaler

def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    # Drop rows with missing values in key columns
    df = df.dropna(subset=['Income'])
    
    current_year = datetime.now().year
    df = df[(df['Year_Birth'] >= current_year - 100) & (df['Year_Birth'] <= current_year - 18)]

    # Convert date to datetime and engineer useful features
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], format='%d-%m-%Y')
    df['Customer_Tenure'] = (datetime.now() - df['Dt_Customer']).dt.days
    df['Age'] = datetime.now().year - df['Year_Birth']

    # Total spend across categories
    spend_cols = [
        'MntWines', 'MntFruits', 'MntMeatProducts',
        'MntFishProducts', 'MntSweetProducts', 'MntGoldProds'
    ]
    df['Total_Spend'] = df[spend_cols].sum(axis=1)

    # Drop unused or redundant columns
    # Columns you want to drop if present
    columns_to_drop = ['ID', 'Year_Birth', 'Dt_Customer', 'Z_CostContact', 'Z_Revenue']
    existing_cols_to_drop = [col for col in columns_to_drop if col in df.columns]

    df = df.drop(columns=existing_cols_to_drop)

    
    

    return df

def scale_features(df: pd.DataFrame, features: list) -> pd.DataFrame:
    """
    Standardize the selected numerical features.
    """
    scaler = StandardScaler()
    df_scaled = df.copy()
    df_scaled[features] = scaler.fit_transform(df[features])
    return df_scaled
