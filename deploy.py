from sklearn.preprocessing import LabelEncoder
import joblib
import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('heart.csv')

# Assume `df` is your DataFrame
encoders = {}

for column in ['Sex', 'ChestPainType', 'FastingBS', 'RestingECG', 'ExerciseAngina', 'ST_Slope']:
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    encoders[column] = le

# Save each encoder separately
for column, encoder in encoders.items():
    joblib.dump(encoder, f'{column}_encoder.pkl')

import streamlit as st
import pandas as pd
import joblib

# Load the model
model = joblib.load('model.pkl')

# Load individual encoders
sex_encoder = joblib.load('Sex_encoder.pkl')
chestpain_encoder = joblib.load('ChestPainType_encoder.pkl')
fastingbs_encoder = joblib.load('FastingBS_encoder.pkl')
restingecg_encoder = joblib.load('RestingECG_encoder.pkl')
exerciseangina_encoder = joblib.load('ExerciseAngina_encoder.pkl')
st_slope_encoder = joblib.load('ST_Slope_encoder.pkl')

# Create a function to predict heart disease
def predict_heart_disease(input_data):
    # Apply encoding for each categorical variable
    input_data['Sex'] = sex_encoder.transform(input_data['Sex'])
    input_data['ChestPainType'] = chestpain_encoder.transform(input_data['ChestPainType'])
    input_data['FastingBS'] = fastingbs_encoder.transform(input_data['FastingBS'])
    input_data['RestingECG'] = restingecg_encoder.transform(input_data['RestingECG'])
    input_data['ExerciseAngina'] = exerciseangina_encoder.transform(input_data['ExerciseAngina'])
    input_data['ST_Slope'] = st_slope_encoder.transform(input_data['ST_Slope'])

    # Predict using the model
    pred = model.predict(input_data)
    return pred[0]

# Create the web app
st.title('Heart Disease Prediction')

# Create the form
Age = st.number_input('Age', min_value=1, max_value=120, value=30)
Sex = st.selectbox('Sex', ['M', 'F'])
ChestPainType = st.selectbox('Chest Pain Type', ['ATA', 'NAP', 'ASY', 'TA'])
RestingBP = st.number_input('Resting Blood Pressure', min_value=50, max_value=200, value=120)
Cholesterol = st.number_input('Serum Cholesterol', min_value=100, max_value=500, value=200)
FastingBS = st.selectbox('Fasting Blood Sugar', ['0', '1'])
RestingECG = st.selectbox('Resting Electrocardiographic Results', ['Normal', 'ST', 'LVH'])
MaxHR = st.number_input('Maximum Heart Rate Achieved', min_value=50, max_value=200, value=120)
ExerciseAngina = st.selectbox('Exercise Induced Angina', ['N', 'Y'])
Oldpeak = st.number_input('Oldpeak', min_value=0.0, max_value=5.0, value=0.0)
ST_Slope = st.selectbox('ST Slope', ['Up', 'Flat', 'Down'])

# Submit form
if st.button('Predict'):
    # Create DataFrame from input
    input_data = pd.DataFrame([[Age, Sex, ChestPainType, RestingBP, Cholesterol, FastingBS, RestingECG, MaxHR, ExerciseAngina, Oldpeak, ST_Slope]], 
                              columns=['Age', 'Sex', 'ChestPainType', 'RestingBP', 'Cholesterol', 'FastingBS', 'RestingECG', 'MaxHR', 'ExerciseAngina', 'Oldpeak', 'ST_Slope'])

    # Call the prediction function
    prediction = predict_heart_disease(input_data)

    # Display the result
    if prediction == 0:
        st.write('No Heart Disease')
    else:
        st.write('Heart Disease')

# Add a footer
st.markdown('---')
st.markdown('Developed by [David Obi](https://github.com/DavieObi)')