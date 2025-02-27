import os
import pandas as pd
import requests
import tarfile
from typing import Union
import matplotlib.pyplot as plt
import ast  


class MovieAnalyzer:
    def __init__(self):
        """Initialize the class by checking for dataset and loading it."""
        self.data_dir = "data/MovieSummaries/"  # ✅ Adjusted path
        os.makedirs(self.data_dir, exist_ok=True)

        # ✅ Update dataset file paths
        self.movie_data_file = os.path.join(self.data_dir, "movie.metadata.tsv")
        self.character_data_file = os.path.join(self.data_dir, "character.metadata.tsv")

        # Check if datasets exist; if not, download and extract them
        if not os.path.exists(self.movie_data_file) or not os.path.exists(self.character_data_file):
            self.download_and_extract()

        # Load datasets
        self.movies_df = pd.read_csv(self.movie_data_file, sep='\t', header=None, names=[
            "wiki_movie_id", "freebase_movie_id", "movie_name", "release_date", "box_office", "runtime",
            "languages", "countries", "genres"
        ])

        self.characters_df = pd.read_csv(self.character_data_file, sep='\t', header=None, names=[
            "wiki_movie_id", "freebase_movie_id", "release_date", "character_name", "actor_dob",
            "actor_gender", "actor_height", "actor_ethnicity", "actor_name", "actor_age",
            "char_actor_map_id", "char_id", "actor_id"
        ])

    def download_and_extract(self):
        """Download dataset if not present and extract it."""
        url = "http://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz"
        tar_path = os.path.join("data", "MovieSummaries.tar.gz")

        if not os.path.exists(tar_path):
            print("Downloading dataset...")
            response = requests.get(url, stream=True)
            with open(tar_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

        print("Extracting dataset...")
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall("data/")  # ✅ Extract correctly into 'data/MovieSummaries/'

    import ast  # Import to parse dictionary-like strings

    def movie_type(self, N: int = 10) -> pd.DataFrame:
        """Returns the N most common movie genres."""
        if not isinstance(N, int):
            raise ValueError("N must be an integer.")
    
        # Convert stringified dictionaries into real Python dicts
        self.movies_df["genres"] = self.movies_df["genres"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
        # Extract genre names
        all_genres = []
        for genre_dict in self.movies_df["genres"].dropna():
            if isinstance(genre_dict, dict):
                all_genres.extend(genre_dict.values())  # Extract only genre names
    
        # Create a DataFrame counting occurrences of each genre
        genre_counts = pd.DataFrame({"Movie_Type": all_genres}).value_counts().reset_index()
        genre_counts.columns = ["Movie_Type", "Count"]
    
        return genre_counts.head(N)


    def actor_count(self) -> pd.DataFrame:
        """Returns histogram data of actors per movie."""
        actor_counts = self.characters_df.groupby("wiki_movie_id").size().value_counts().reset_index()
        actor_counts.columns = ["Number_of_Actors", "Movie_Count"]
        return actor_counts

    def actor_distributions(self, gender: str = "All", max_height: float = 2.5, min_height: float = 1.0, plot: bool = False) -> pd.DataFrame:
        """Returns actor height distribution and optionally plots it."""
        if not isinstance(gender, str) or not isinstance(max_height, (float, int)) or not isinstance(min_height, (float, int)):
            raise ValueError("Invalid input types.")

        filtered_df = self.characters_df[(self.characters_df["actor_height"] >= min_height) & (self.characters_df["actor_height"] <= max_height)]
        if gender != "All":
            filtered_df = filtered_df[filtered_df["actor_gender"] == gender]

        if plot:
            plt.hist(filtered_df["actor_height"].dropna(), bins=20)
            plt.xlabel("Height (m)")
            plt.ylabel("Frequency")
            plt.title(f"Actor Height Distribution - Gender: {gender}")
            plt.show()

        return filtered_df[["actor_name", "actor_height", "actor_gender"]]

