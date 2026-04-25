import pytest
import pandas as pd
from src.processor import get_data_pipeline

def test_pipeline_output_shape():
    """Test if the pipeline produces the correct output shape."""
    pipeline = get_data_pipeline()
    
    # Sample input
    data = pd.DataFrame({
        "Experience": [5.0],
        "Education": ["Postgraduate"],
        "Role": ["Data Scientist"],
        "Location": ["Bangalore"]
    })
    
    # Fit and transform
    pipeline.fit(data)
    transformed = pipeline.transform(data)
    
    # Basic assertion: Experience (1) + Categorical (depends on one-hot)
    assert transformed.shape[0] == 1
    assert transformed.shape[1] > 1

def test_config_paths():
    """Test if config paths are correctly resolved."""
    from src.config import BASE_DIR, DATA_PATH
    assert "Salary_Prediction" in BASE_DIR
    assert DATA_PATH.endswith("salary_data.csv")
