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
        self.playlist_songs = 15

    def build_model(self):
        '''
        Model builder function
        '''
        # Define the model
        self.model=NearestNeighbors(
            n_neighbors=self.playlist_songs + 1).fit(
            self.preprocessor.X_mmscaled)
        # Extract index and distance of self.playlist_songs+1
        # number of colest songs
        self.distance, self.index=self.model.kneighbors(
            self.preprocessor.X_target_mmscaled,
            n_neighbors=self.playlist_songs + 1)
        # Copy found index rows from the original not scaled dataset
        self.playlist = self.se.data.iloc[self.index[0],:]
        self.playlist['distance'] = self.distance[0]
        # Remove the target song from the list
        self.playlist = self.playlist.tail(self.playlist_songs)
        # Ordering the playlist on distance, ascending order
        self.playlist = self.playlist.sort_values(
            by=['distance'], ascending=True, ignore_index=True)
        # Drop not necessary columns
        self.playlist = self.playlist[['name', 'artists', 'distance']]
        # Strip square brackets from the artists strings
        self.playlist['artists'] = self.playlist['artists'].apply(
            lambda x: x.strip("['").strip("']"))
        # Set starting index from 0 to 1
        self.playlist.index += 1
