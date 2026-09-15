import streamlit as st
import numpy as np
import joblib
import os

st.title("Sales & Revenue Prediction")
st.write("Use the interactive form below to predict sales/revenue based on your trained Random Forest model.")

# Define paths to models folder relative to this page file
MODEL_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../models"))

@st.cache_resource
def load_artifacts():
    try:
        rf_model = joblib.load(os.path.join(MODEL_DIR, "random_forest.pkl"))
        scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
        le_country = joblib.load(os.path.join(MODEL_DIR, "le_country.pkl"))
        le_month = joblib.load(os.path.join(MODEL_DIR, "le_month.pkl"))
        le_day = joblib.load(os.path.join(MODEL_DIR, "le_day.pkl"))
        return rf_model, scaler, le_country, le_month, le_day
    except Exception as e:
        return None, None, None, None, None

rf_model, scaler, le_country, le_month, le_day = load_artifacts()

if rf_model is None:
    st.error("Model files not found! Please ensure you have run your Jupyter notebook and saved all `.pkl` files in the 'models/' directory.")
else:
    # Input Form Layout
    with st.form("prediction_form"):
        st.subheader("Transaction Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            quantity = st.number_input("Quantity", min_value=1, value=10, step=1)
            unit_price = st.number_input("Unit Price", min_value=0.0, value=2.50, step=0.1)

        with col2:
            country = st.selectbox("Country", options=le_country.classes_)
            month = st.selectbox("Month", options=le_month.classes_)
            day = st.selectbox("Day of Week", options=le_day.classes_)

        submit_button = st.form_submit_button(label="Predict")

    if submit_button:
        try:
            # Encode categorical inputs
            country_encoded = le_country.transform([country])[0]
            month_encoded = le_month.transform([month])[0]
            day_encoded = le_day.transform([day])[0]

            # Construct the 5-feature array:
            # ['Quantity', 'UnitPrice', 'Country', 'Month', 'Day']
            input_data = [[quantity, unit_price, country_encoded, month_encoded, day_encoded]]

            # Make prediction
            prediction = rf_model.predict(input_data)[0]

            st.success(f"### Predicted Output: {prediction:,.2f}")
            
        except Exception as e:
            st.error(f"An error occurred during prediction: {e}")