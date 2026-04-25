import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.config import MODEL_PATH

app = FastAPI(
    title="Salary Prediction API",
    description="API for predicting annual salaries based on experience, education, role, and location.",
    version="1.0.0"
)

# Load the model once on startup
if not os.path.exists(MODEL_PATH):
    raise RuntimeError(f"Model file not found at {MODEL_PATH}. Please run training first.")

model = joblib.load(MODEL_PATH)

class PredictionInput(BaseModel):
    Experience: float
    Education: str
    Role: str
    Location: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "Experience": 5.0,
                "Education": "Postgraduate",
                "Role": "Data Scientist",
                "Location": "Bangalore"
            }
        }
    }

class PredictionOutput(BaseModel):
    predicted_salary: float
    currency: str = "INR"

@app.get("/")
def home():
    return {"message": "Salary Prediction API is running. Visit /docs for documentation."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    try:
        # Convert input to DataFrame
        input_df = pd.DataFrame([data.model_dump()])
        
        # Predict using the loaded pipeline
        prediction = model.predict(input_df)[0]
        
        return PredictionOutput(predicted_salary=round(float(prediction), 2))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
