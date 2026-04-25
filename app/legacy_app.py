
import streamlit as st
import pickle
import pandas as pd

# Load trained model
model = pickle.load(open('../model/model.pkl', 'rb'))

st.title("Smart Salary Predictor")

# User Inputs
experience = st.slider("Years of Experience", 0, 20, 2)

education = st.selectbox("Education", ["Graduate", "Postgraduate", "PhD"])

role = st.selectbox("Job Role", ["Software Engineer", "Data Analyst", "Data Scientist"])

location = st.selectbox("Location", ["Kolkata", "Delhi", "Bangalore", "Hyderabad", "Mumbai", "Pune"])

# Create DataFrame from input
input_df = pd.DataFrame({
    "Experience": [experience],
    "Education": [education],
    "Role": [role],
    "Location": [location]
})

# Convert categorical → numeric
input_df = pd.get_dummies(input_df)

# Load training columns (IMPORTANT FIX)
import pickle
cols = pickle.load(open('../model/columns.pkl', 'rb'))

input_df = input_df.reindex(columns=cols, fill_value=0)

# Prediction
if st.button("Predict Salary"):
    prediction = model.predict(input_df)
    st.success(f"Predicted Salary: ₹ {int(prediction[0])}")