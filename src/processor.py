import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from src.config import DATA_PATH, TEST_SIZE, RANDOM_STATE

def get_data_pipeline():
    """
    Creates a preprocessing pipeline for the salary dataset.
    """
    # Define categorical and numerical features
    categorical_features = ['Education', 'Role', 'Location']
    numerical_features = ['Experience']

    # Preprocessing for numerical data
    numerical_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    # Preprocessing for categorical data
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Bundle preprocessing for numerical and categorical data
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ])
    
    return preprocessor

def load_and_split_data():
    """
    Loads data and returns train/test splits.
    """
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip()
    
    X = df.drop('Salary', axis=1)
    y = df['Salary']
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    
    return X_train, X_test, y_train, y_test
