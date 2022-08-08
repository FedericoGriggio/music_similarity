# Data Manipulation
import numpy as np
import pandas as pd

class SearchEngine():
    def __init__(self, data):
        '''
        SearchEngine class
        Input: a songs dataset extracted from spotify API
        '''
        self.data = data

    def target_song(self, title='', artist=''):
        '''
        Search engine function for the target song
        Input: song title and/or artist
        Output: self.target dataset song
        '''
        # transform input strings in lowercase
        title = str(title).lower()
        artist = str(artist).lower()
        # filter self.data on the desired song
        if title != '' and artist != '':
            self.target = self.data[self.data[
                'artists'].str.lower().str.contains(artist)]
            self.target = self.target[self.target[
                'name'].str.lower().str.contains(title)]
        elif title != '':
            self.target = self.data[self.data[
                'name'].str.lower().str.contains(title)]
        elif artist != '':
            self.target = self.data[self.data[
                'artists'].str.lower().str.contains(artist)]
        else:
            print('Please select a song title and artist')
        # keep only the first song result
        self.target = self.target.head(1)
        self.artist = self.target["artists"].to_string(
            index=False).strip("['").strip("']")
        self.title = self.target["name"].to_string(index=False)
