import streamlit as st
import pandas as pd
import numpy as np
import pickle
from PIL import Image

# Load the pickled models
model = pickle.load(open(r'saved_models\0\model\model.pkl', 'rb'))
encoder = pickle.load(open(r'saved_models\0\target_encoder\target_encoder.pkl', 'rb'))
transformer = pickle.load(open(r'saved_models\0\transform\transformed.pkl', 'rb'))

# Custom CSS styles
st.markdown(
    """
<style>
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7bcf,#2e7bcf);
        color: white;
    }
    .Widget>label {
        color: white;
        font-weight: 600;
    }
    [data-testid="stSelectbox"] {
        color: black;
    }
</style>
""",
    unsafe_allow_html=True,
)


st.title(" \n \n Insurance Premium Prediction")

# Sidebar inputs
st.sidebar.header("Input Parameters")
age = st.sidebar.number_input("Age", min_value=18, max_value=100, value=30, step=1)
sex = st.sidebar.selectbox("Gender", ("Male", "Female"))
bmi = st.sidebar.number_input("BMI", min_value=10.0, max_value=50.0, value=25.0, step=0.1)
children = st.sidebar.selectbox("Number of Children", (0, 1, 2, 3, 4, 5))
smoker = st.sidebar.selectbox("Smoker", ("Yes", "No"))
region = st.sidebar.selectbox("Region", ("southeast", "southwest", "northeast", "northwest"))

# Prepare the input data
l = {}
l["age"] = age
l["sex"] = sex
l["bmi"] = bmi
l["children"] = children
l["smoker"] = smoker
l["region"] = region

df = pd.DataFrame(l, index=[0])

df["region"] = encoder.transform(df["region"])
df["sex"] = df["sex"].map({"Male": 1, "Female": 0})
df["smoker"] = df["smoker"].map({"Yes": 1, "No": 0})

df = transformer.transform(df)
y_pred = model.predict(df)

# Display the result
if st.button("Predict"):
    st.success(f"The estimated premium is {round(y_pred[0])} INR")
