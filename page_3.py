import streamlit as st
import sys
import os
import subprocess
import altair as alt
import ollama

sys.path.append(os.path.abspath("models"))
from movie_analyzer import MovieAnalyzer  # Import from models/

# Initialize analyzer
analyzer = MovieAnalyzer()

# Initialize LLM
subprocess.run(["ollama", "pull", "llama3.2"], check=True, text=False)

st.title("CMU Movies Dataset")

with st.container():
    shuffle_button = st.button(label="Shuffle", type="primary", icon=":material/casino:", use_container_width=True)

if shuffle_button:
    analyzer.randomize()
    movie_name = analyzer.random_movie["movie_name"]
    movie_release_year = analyzer.random_movie["release_date"].year
    movie_genres = f'{", ".join(analyzer.random_movie["genres"])}'

    storyline = ollama.generate(model='llama3.2', prompt=f"You are requested to fetch the storyline/plot of a given movie based on your knowledge. Please respond with only the storyline or plot. If you cannot find it, please simply respond with 'No information' \nThe movie is: {movie_name}, released in {movie_release_year}")
    
    genres = ollama.generate(model='llama3.2', prompt=f"In your response, you only need to suggest a series of genres based on a given movie (maximum 5) separeted by comma, text other than genre names is not requested. \nThe movie is: {movie_name}, released in {movie_release_year}")

    evaluation = ollama.generate(model='llama3.2', prompt=f"Compare a classification result of genres: {genres.response} to CMU Movie Dataset: {movie_genres}. Then present which genres in classification result is found in the credible CMU dataset. Response should follow this format: 'Found: \n - Genre Name 1 \n - Genre Name 2'. Other text is not requested.")
    st.header(f"{analyzer.random_movie["movie_name"]} ({analyzer.random_movie["release_date"].year})", divider="red")

    st.write("### Summary")

    st.write("**Release Date:**\n", analyzer.random_movie["release_date"])
    st.write("**Languages:**", f'{", ".join(analyzer.random_movie["languages"])}')
    st.write("**Countries:**", f'{", ".join(analyzer.random_movie["countries"])}')
    
    with st.chat_message(name="storyline", avatar=":material/movie:"):
        st.text_area("Storyline suggested by AI", storyline.response)

    with st.chat_message(name="genres", avatar=":material/category:"):
        st.text_area("Genres from dataset",f'{", ".join(analyzer.random_movie["genres"])}')
    
    with st.chat_message(name="genres", avatar=":material/robot:"):
        st.text_area("Genres suggested by AI", genres.response)
        st.text_area("Evaluation", evaluation.response)

    
    
    