# Data Manipulation
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

# Unsupervised Learning
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# K-nn modelling
from sklearn.neighbors import NearestNeighbors

# Package classes
from music_similarity.search_engine import SearchEngine
from music_similarity.preprocessor import Preprocessor

class Playlist():
    def __init__(self, preprocessor, se):
        '''
        Extractor class
        Input: preprocessor class dataset extracted from spotify API
        '''
        self.preprocessor = preprocessor
        self.se = se
        self.playlist_songs = 10

    def build_model(self):
        '''
        Model builder function
        '''
        self.model=NearestNeighbors(
            n_neighbors=self.playlist_songs + 1).fit(
            self.preprocessor.X_mmscaled)
        self.distance, self.index=self.model.kneighbors(
            self.preprocessor.X_target_mmscaled,
            n_neighbors=self.playlist_songs + 1)
        self.playlist = self.se.data.iloc[self.index[0],:]
        self.playlist['distance'] = self.distance[0]
        self.playlist = self.playlist.tail(self.playlist_songs)
        self.playlist = self.playlist.sort_values(by=[
            'popularity'], ascending=False, ignore_index=True)
