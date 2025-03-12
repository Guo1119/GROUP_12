import streamlit as st
import sys
import os

sys.path.append(os.path.abspath("models"))  # Ensure Python finds the models folder

from movie_analyzer import MovieAnalyzer  # Import from models/


st.title("CMU Movies Dataset")

analyzer = MovieAnalyzer()

st.header("Movie Type Distribution", divider="red")
N = st.number_input("Select N", min_value=1, max_value=50, value=10)
st.bar_chart(analyzer.movie_type(N).set_index("Movie_Type"))

st.header("Actor Count Histogram", divider="red")
st.bar_chart(analyzer.actor_count().set_index("Number_of_Actors"))

st.header("Actor Height Distribution",divider="red")
gender = st.selectbox("Select Gender", ["All", "Male", "Female"])
min_height = st.number_input("Min Height", min_value=0.5, max_value=2.5, value=1.0)
max_height = st.number_input("Max Height", min_value=0.5, max_value=2.5, value=2.5)
if st.button("Plot Distribution"):
    analyzer.actor_distributions(gender, max_height, min_height, plot=True)
