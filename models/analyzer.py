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
        # Indicate paths and creates lists for column names
        self.gzipPath="..\\downloads\\MovieSummaries.tar.gz"
        self.movieMetaDataPath="..\\data\\MovieSummaries\\movie.metadata.tsv"
        self.movieMetaDataColumns=['wikiID', 'fbID', 'movieName', 'releaseDate', 'boxRevenue', 'runtime', 'language', 'country', 'genre']
        self.characterMetaDataPath="..\\data\\MovieSummaries\\character.metadata.tsv"
        self.characterMetaDataColumns=['wikiID', 'fbID', 'releaseDate', 'characterName', 'actorBirthday', 'actorGender', 'actorHeight', 
                                       'actorEthnicityID','actorName', 'ageAtRelease', 'fbMapID', 'fbCharacterID','fbActorID']
        
        try:
            # try to load datasets
            print("Connceting to the datasets ...")
            self.movieData=pd.read_csv(self.movieMetaDataPath, sep="\t", names=self.movieMetaDataColumns, on_bad_lines='skip')
            self.characterData=pd.read_csv(self.characterMetaDataPath, sep="\t", names=self.characterMetaDataColumns, on_bad_lines='skip')  

        except:
            # if the datasets don't exist in the local directory
            datafetchtools.downloadData("https://www.cs.cmu.edu/~ark/personas/data/MovieSummaries.tar.gz", self.gzipPath)
            datafetchtools.extractData("..\\downloads\\MovieSummaries.tar.gz", "..\\data")

        finally:
            # load again
            self.movieData=pd.read_csv(self.movieMetaDataPath, sep="\t", names=self.movieMetaDataColumns, on_bad_lines='skip')
            self.characterData=pd.read_csv(self.characterMetaDataPath, sep="\t", names=self.characterMetaDataColumns, on_bad_lines='skip')
            print("Successfully connected to the datasets")

    def movie_type(self, N=10):
        # Take the column "genres" out and form lists using the values of dictionary 
        genres=self.movieData.genre.apply(lambda x: list(ast.literal_eval(x).values()))
        # A native feature of pandas that breaks down columns made of list into new entries
        genresExploded=genres.explode(ignore_index=True)
        return genresExploded.value_counts()[1:N]
    
    def actor_count(self):
        # 1. Use value_counts() to count how many times a wikiID occurs in the Character dataset
        # 2. Create a new dataframe using .join(), having columns: wikiID, movieName, actorCounts
        countData=self.movieData[["wikiID", "movieName"]].join(self.characterData['wikiID'].value_counts().astype("Int64"), on="wikiID")
        countData.rename(columns={"count": "actorCounts"}, inplace=True)
        # Make sure can be executed in terminal and return a figue
        plt.figure(figsize=(12, 6))
        sns.histplot(data=countData,x="actorCounts",bins=40)
        plt.show()
    
    def actor_distributions(self, max_height, min_height, gender="All", plot=False):
        actorData=self.characterData[["actorName", "actorGender", "actorHeight"]].drop_duplicates()
        if gender == "All":
            actorDataConstraint=actorData
        else:
            actorDataConstraint=actorData[actorData.actorGender == gender]
 
        if plot == True:
            actorDataConstraint=actorDataConstraint[(actorDataConstraint.actorHeight > min_height) 
                                                    & (actorDataConstraint.actorHeight < max_height)]
            sns.histplot(actorDataConstraint, x="actorHeight")
        else:
            actorDataConstraint=actorDataConstraint[(actorDataConstraint.actorHeight > min_height) 
                                                    & (actorDataConstraint.actorHeight < max_height)]
            return actorDataConstraint


analyzer()
