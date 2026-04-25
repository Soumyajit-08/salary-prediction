import pandas as pd

def preprocess_data(df):
    df = df.dropna()
    df = pd.get_dummies(df, drop_first=True)
    return df