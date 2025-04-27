import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Consumer Behavior Survey Analysis", layout="wide")

st.title("Consumer Behavior Survey Analysis Dashboard")
st.markdown("By Harsh Rana")

# Upload data
st.sidebar.header("Upload Your CSV Data")
cities_file = st.sidebar.file_uploader("Upload dim_cities.csv", type=["csv"])
respondents_file = st.sidebar.file_uploader("Upload dim_respondents.csv", type=["csv"])
responses_file = st.sidebar.file_uploader("Upload fact_survey_responses.csv", type=["csv"])

if cities_file and respondents_file and responses_file:
    cities = pd.read_csv(cities_file)
    respondents = pd.read_csv(respondents_file)
    survey_responses = pd.read_csv(responses_file)

    # Merge the datasets
    data = survey_responses.merge(respondents, on="Respondent_ID", how="left").merge(cities, on="City_ID", how="left")
    
    st.header("Sample Merged Data")
    st.dataframe(data.head())

    st.header("Survey Analysis")

    # Gender preference bar chart
    st.subheader("Survey Responses by Gender")
    gender_counts = data["Gender"].value_counts()
    fig, ax = plt.subplots()
    gender_counts.plot(kind="bar", color=["skyblue", "pink", "purple"], ax=ax)
    plt.title("Survey Responses by Gender")
    st.pyplot(fig)

    # Age vs Gender heatmap
    st.subheader("Survey Responses by Gender and Age")
    gender_age = data.groupby(["Gender", "Age"])["Response_ID"].count().unstack()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(gender_age, annot=True, cmap="YlGnBu", fmt="g", ax=ax)
    st.pyplot(fig)

    # Consumption frequency heatmap
    st.subheader("Consumption Frequency by Gender and Age")
    gender_age_consume = data.groupby(["Gender", "Age"])["Consume_frequency"].value_counts().unstack().fillna(0)
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.heatmap(gender_age_consume, annot=True, cmap="YlGnBu", fmt="g", ax=ax)
    st.pyplot(fig)

    # Preferred ingredients
    st.subheader("Preferred Ingredients")
    ingredients = data["Ingredients_expected"].value_counts(normalize=True)
    fig, ax = plt.subplots()
    sns.barplot(x=ingredients.index, y=ingredients.values, palette="Blues_d", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Packaging preferences
    st.subheader("Packaging Preferences")
    packaging = data["Packaging_preference"].value_counts(normalize=True)
    fig, ax = plt.subplots()
    sns.barplot(x=packaging.index, y=packaging.values, palette="Blues_d", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.success("Analysis Completed! Scroll and explore different sections!")

else:
    st.info("Please upload all three required CSV files to start analysis.")