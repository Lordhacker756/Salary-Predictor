import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Cleaning functions


def shorten_category(categories, cutoff):
    category_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            category_map[categories.index[i]] = categories.index[i]
        else:
            category_map[categories.index[i]] = "Other"
    return category_map


def clean_education(x):
    if "Bachelor's" in x:
        return "Bachelor's degree"
    if "Master's" in x:
        return "Master's degree"
    if "Professional" in x:
        return "Professional degree"
    return "Less than a Bachelor's"


def cleanExperience(x):
    if x == "Less than 1 year":
        return 0.5
    if x == "More than 50 years":
        return 50
    return float(x)


@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro",
             "Employment", "ConvertedCompYearly"]]
    df = df.rename({'ConvertedCompYearly': "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df['Employment'] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_category(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["Salary"] <= 500000]
    df = df[df["Salary"] >= 10000]
    df = df[df["Country"] != "Other"]

    df['YearsCodePro'] = df['YearsCodePro'].apply(cleanExperience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)

    return df


df = load_data()


def show_explore_page():
    st.title("Explore Software Developer Insights 📊")

    st.write("""
        ### Stats from Stack Overflow Developer Survey 2022
    """)

    data = df['Country'].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    st.write("### Where are the developers from?")
    st.pyplot(fig1)
