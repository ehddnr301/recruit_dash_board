import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
import glob
from pandas.core.frame import DataFrame

class Similarity():
    def __init__(
        self,
        df : DataFrame,
        id : str,
        specialty : str,
        sim_method: str
    ) -> None:
        self.df = df
        self.id = id
        self.specialty = specialty.split('@')
        self.sim_method = sim_method
    
    def pivot(self, rating, index, columns):
        df = self.df.pivot_table(rating, index=index, columns=columns).fillna(0)
        return df
    
    def add_info(self, df:DataFrame):
        for sp in self.specialty:
            df.loc[self.id, sp] = 1
        df.fillna(0, inplace=True)
        return df
    
    def preprocess(self):
        df = self.pivot(rating='rating', index='recruit_id', columns='job_specialty')
        df = self.add_info(df)
        return df
    
    def calculate_similarity(self, df):
        if self.sim_method == 'cosine':
            return cosine_similarity(df, df)
        else:
            return euclidean_distances(df, df)
    
    def get_item(self) -> DataFrame:
        df = self.preprocess()
        sim = self.calculate_similarity(df)
        sim_df = pd.DataFrame(data=sim, index=df.index, columns= df.index)
        return sim_df[self.id].sort_values(ascending=False)[1:10].index

simirality_df = pd.read_csv("./recruit_specialty_matrix.csv", sep=';')


