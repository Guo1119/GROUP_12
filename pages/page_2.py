import streamlit as st
import sys
import os
import altair as alt

sys.path.append(os.path.abspath("models"))  # Ensure Python finds the models folder

from movie_analyzer import MovieAnalyzer  # Import from models/


st.title("CMU Movies Dataset")

analyzer = MovieAnalyzer()

st.header("Release Years", divider="red")
genre_options = [None, 'Drama', 'Comedy', 'Romance Film', 'Black-and-white', 'Action', 'Thriller', 'Short Film', 
                 'World cinema', 'Crime Fiction', 'Indie']
selected_genre = st.selectbox(
    label="Select a genre",
    options=genre_options
)
st.bar_chart(analyzer.releases(selected_genre), x="Release Year", y="Number of Movies")

st.header("Actor Ages", divider="red")
selected_scale = st.selectbox(
    label="Select a scale",
    options={"Year", "Month"}
)

if selected_scale == "Year":
    st.bar_chart(analyzer.ages("Y"), x="Year", y="Number of Births")

if selected_scale == "Month":
    c = alt.Chart(analyzer.ages("M")).mark_bar().encode(x=alt.X("Month", sort=None), y="Number of Births")
    st.altair_chart(c)