import os
import pandas as pd 
import numpy as np
import seaborn as sns
import ast
import matplotlib.pyplot as plt
import datafetchtools

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


class analyzer:
    def __init__(self):
        self.movieMetaDataPath="..\\data\\MovieSummaries\\movie.metadata.tsv"
        self.movieMetaDataColumns=['wikiID', 'fbID', 'movieName', 'releaseDate', 'boxRevenue', 'runtime', 'language', 'country', 'genre']
        self.characterMetaDataPath="..\\data\\MovieSummaries\\character.metadata.tsv"
        self.characterMetaDataColumns=['wikiID', 'fbID', 'releaseDate', 'characterName', 'actorBirthday', 'actorGender', 'actorHeight', 
                                       'actorEthnicityID','actorName', 'ageAtRelease', 'fbMapID', 'fbCharacterID','fbActorID']
        
        try:
            print("Connceting to the datasets ...")
            self.movieData=pd.read_csv(self.movieMetaDataPath, sep="\t", names=self.movieMetaDataColumns, on_bad_lines='skip')
            self.characterData=pd.read_csv(self.characterMetaDataPath, sep="\t", names=self.characterMetaDataColumns, on_bad_lines='skip')
        except:
            datafetchtools.downloadData("https://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz", self.gzipPath)
            datafetchtools.extractData("..\\downloads\\MovieSummaries.tar.gz", "..\\data")
        finally:
            self.movieData=pd.read_csv(self.movieMetaDataPath, sep="\t", names=self.movieMetaDataColumns, on_bad_lines='skip')
            self.characterData=pd.read_csv(self.characterMetaDataPath, sep="\t", names=self.characterMetaDataColumns, on_bad_lines='skip')
            print("Successfully connected to the datasets")

    def movie_type(self, N=10):
        genres=self.movieData.genre.apply(lambda x: list(ast.literal_eval(x).values()))
        genresExploded=genres.explode(ignore_index=True)
        return genresExploded.value_counts()[1:N]
    
    def actor_count(self):
        countData=self.movieData[["wikiID", "movieName"]].join(self.characterData['wikiID'].value_counts().astype("Int64"), on="wikiID")
        countData.rename(columns={"count": "actorCounts"}, inplace=True)
        plt.figure(figsize=(12, 6))
        sns.histplot(data=countData,x="actorCounts",bins=40)
        plt.show()

