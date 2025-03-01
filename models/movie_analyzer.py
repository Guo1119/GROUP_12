import os
import pandas as pd
import requests
import tarfile
import matplotlib.pyplot as plt
import ast  # Import for parsing dictionary-like strings


class MovieAnalyzer:
    def __init__(self):
        """Initialize the class by checking for dataset and loading it."""
        self.data_dir = "data/MovieSummaries/"
        os.makedirs(self.data_dir, exist_ok=True)

        # Dataset file paths
        self.movie_data_file = os.path.join(self.data_dir, "movie.metadata.tsv")
        self.character_data_file = os.path.join(self.data_dir, "character.metadata.tsv")

        # Check if datasets exist; if not, download and extract them
        if not os.path.exists(self.movie_data_file) or not os.path.exists(
            self.character_data_file
        ):
            self.download_and_extract()

        # Load datasets
        self.movies_df = pd.read_csv(
            self.movie_data_file,
            sep="\t",
            header=None,
            names=[
                "wiki_movie_id",
                "freebase_movie_id",
                "movie_name",
                "release_date",
                "box_office",
                "runtime",
                "languages",
                "countries",
                "genres",
            ],
        )

        self.characters_df = pd.read_csv(
            self.character_data_file,
            sep="\t",
            header=None,
            names=[
                "wiki_movie_id",
                "freebase_movie_id",
                "release_date",
                "character_name",
                "actor_dob",
                "actor_gender",
                "actor_height",
                "actor_ethnicity",
                "actor_name",
                "actor_age",
                "char_actor_map_id",
                "char_id",
                "actor_id",
            ],
        )

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

    def movie_type(self, N: int = 10) -> pd.DataFrame:
        """Returns the N most common movie genres."""
        if not isinstance(N, int):
            raise ValueError("N must be an integer.")

        # Convert stringified dictionaries into real Python dicts (handle errors safely)
        def parse_genres(x):
            try:
                return ast.literal_eval(x) if isinstance(x, str) else {}
            except (SyntaxError, ValueError):
                return {}

        self.movies_df["genres"] = self.movies_df["genres"].apply(parse_genres)

        # Extract genre names
        all_genres = []
        for genre_dict in self.movies_df["genres"].dropna():
            if isinstance(genre_dict, dict):
                all_genres.extend(genre_dict.values())  # Extract genre names

        # Create a DataFrame counting occurrences of each genre
        genre_counts = (
            pd.DataFrame({"Movie_Type": all_genres}).value_counts().reset_index()
        )
        genre_counts.columns = ["Movie_Type", "Count"]

        return genre_counts.head(N)

    def actor_count(self) -> pd.DataFrame:
        """Returns histogram data of actors per movie."""
        actor_counts = (
            self.characters_df.groupby("wiki_movie_id")
            .size()
            .value_counts()
            .reset_index()
        )
        actor_counts.columns = ["Number_of_Actors", "Movie_Count"]
        return actor_counts

    def actor_distributions(
        self,
        gender: str = "All",
        max_height: float = 2.5,
        min_height: float = 1.0,
        plot: bool = False,
    ) -> pd.DataFrame:
        """
        Returns actor height distribution and optionally plots it.

        :param gender: "All" or specific gender ("Male", "Female", etc.).
        :param max_height: Maximum actor height.
        :param min_height: Minimum actor height.
        :param plot: If True, plots the height distribution.
        :return: Filtered DataFrame with actor names, gender, and height.
        :raises ValueError: If gender is not a string or height values are not numeric.
        """

        # Validate input types
        if not isinstance(gender, str):
            raise ValueError("Gender must be a string ('All', 'Male', 'Female', etc.).")

        if not isinstance(max_height, (int, float)) or not isinstance(
            min_height, (int, float)
        ):
            raise ValueError("Height values must be numeric.")

        if max_height < min_height:
            raise ValueError("max_height must be greater than min_height.")

        # Convert 'M' -> 'Male', 'F' -> 'Female' in the dataset
        self.characters_df["actor_gender"] = self.characters_df["actor_gender"].replace(
            {"M": "Male", "F": "Female"}
        )

        # Filter dataset based on height
        df = self.characters_df.dropna(
            subset=["actor_height"]
        )  # Remove missing heights
        df = df[(df["actor_height"] >= min_height) & (df["actor_height"] <= max_height)]

        # Get distinct non-missing gender values
        valid_genders = df["actor_gender"].dropna().unique().tolist()

        # Validate gender input
        if gender != "All" and gender not in valid_genders:
            raise ValueError(f"Invalid gender. Choose from {valid_genders} or 'All'.")

        # Filter by gender if not "All"
        if gender != "All":
            df = df[df["actor_gender"] == gender]

        # Plot if requested
        if plot:
            plt.figure(figsize=(8, 5))
            plt.hist(
                df["actor_height"].dropna(),
                bins=20,
                alpha=0.7,
                color="skyblue",
                edgecolor="black",
            )
            plt.xlabel("Height (m)")
            plt.ylabel("Frequency")
            plt.title(f"Actor Height Distribution - Gender: {gender}")
            plt.grid(axis="y", linestyle="--", alpha=0.7)

            # ✅ Ensure the plot is rendered in Streamlit
            import streamlit as st

            st.pyplot(plt)

        return df[["actor_name", "actor_gender", "actor_height"]]
