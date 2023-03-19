import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data


data = load_model()

regressor = data['model']
le_countries = data['le_countries']
le_education = data['le_education']


def show_predict_page():
    st.title('Software Developer Salary Prediction💹')

    st.write("""
        ### We neeed some information to predict the salary!
    """)

    countries = (
        'United States of America',
        'India',
        'United Kingdom of Great Britain and Northern Ireland',
        'Germany',
        'Canada',
        'France',
        'Brazil',
        'Poland',
        'Australia',
        'Netherlands',
        'Russian Federation',
        'Spain',
        'Italy',
        'Sweden',
    )

    education = (
        "Less than a Bachelor's",
        "Bachelor's degree",
        "Master's degree",
        "Professional degree",
    )

    countries = st.selectbox('Select Country', countries)
    education = st.selectbox('Select Education', education)

    experience = st.slider('Years of Experience', 0, 50, 3)

    ok = st.button("Predict Salary 🤖")
    if ok:
        X = np.array([[countries, education, experience]])
        X[:, 0] = le_countries.transform(X[:, 0])
        X[:, 1] = le_education.transform(X[:, 1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.write(f"""
            ### The expected salary is ${salary[0]:,.2f} per Annum
        """)
