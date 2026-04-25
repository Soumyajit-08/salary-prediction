import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "model")
LOGS_DIR = os.path.join(BASE_DIR, "logs")

# Files
DATA_PATH = os.path.join(DATA_DIR, "salary_data.csv")
MODEL_PATH = os.path.join(MODEL_DIR, "best_model.pkl")
COLUMNS_PATH = os.path.join(MODEL_DIR, "columns.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")

# ML Parameters
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Ensure directories exist
for d in [DATA_DIR, MODEL_DIR, LOGS_DIR]:
    if not os.path.exists(d):
        os.makedirs(d)
