import streamlit as st
import joblib
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load model and dataset
model = joblib.load("model.joblib")
df = pd.read_csv("bbc_news_dataset.csv")

vectorizer = model.named_steps["tfidfvectorizer"]

st.title("📰 News Classifier & Recommendation")

news = st.text_area("Enter a News Article")

if st.button("Predict"):

    if news.strip() == "":
        st.warning("Please enter a news article.")
    else:
        # Predict category
        category = model.predict([news])[0]

        st.success(f"Predicted Category: {category}")

        # Recommend similar articles
        same_category = df[df["Category"] == category]

        user_vector = vectorizer.transform([news])
        article_vectors = vectorizer.transform(same_category["Text"])

        similarity = cosine_similarity(user_vector, article_vectors)

        top = np.argsort(similarity[0])[-3:][::-1]

        st.subheader("Top 3 Similar Articles")

        for i, index in enumerate(top, start=1):
            st.write(f"### Article {i}")
            st.write(same_category.iloc[index]["Text"][:500] + "...")
            st.write("---")