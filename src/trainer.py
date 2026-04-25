import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score
from src.processor import get_data_pipeline, load_and_split_data
from src.config import MODEL_PATH

def train_best_model():
    """
    Trains multiple models and saves the best performing one.
    """
    X_train, X_test, y_train, y_test = load_and_split_data()
    preprocessor = get_data_pipeline()

    models = {
        "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42),
        "GradientBoosting": GradientBoostingRegressor(n_estimators=200, random_state=42),
        "Ridge": Ridge(alpha=1.0)
    }

    best_score = -np.inf
    best_model = None
    best_name = ""

    print("--- Starting Model Training ---")
    for name, model in models.items():
        # Create a full pipeline with preprocessor and model
        clf = Pipeline(steps=[('preprocessor', preprocessor),
                              ('model', model)])
        
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        
        score = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        
        print(f"Model: {name} | R2: {score:.4f} | MAE: {mae:.2f}")
        
        if score > best_score:
            best_score = score
            best_model = clf
            best_name = name

    print(f"\nBest Model: {best_name} with R2 Score: {best_score:.4f}")
    
    # Save the best model (pipeline included)
    joblib.dump(best_model, MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    from sklearn.pipeline import Pipeline # Required inside the loop but imported here for safety
    train_best_model()
