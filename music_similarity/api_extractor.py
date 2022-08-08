# Data Manipulation
import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

# API packages
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

class ApiExtractor:
    def __init__(self, se):
        '''
        Extractor class
        Input: preprocessor class dataset extracted from spotify API
        '''
        # credentials need to be exported via the command line
        self.auth_manager = SpotifyClientCredentials()
        self.sp_connection = spotipy.Spotify(auth_manager=self.auth_manager)
        self.search_limit = 10
        self.se = se

    def get_track_base_attrs(self, title, artist):
        '''
        Function that returns the basic features of a desired song
        if it's not present in the local dataset
        '''
        self.ta_response = self.sp_connection.search(
            q="artist:" + artist + " track:" + title,
            type="track",
            limit=1)

        # parse attributes from track
        self.track = self.ta_response['tracks']['items'][0]
        self.track_name = self.track['name']
        self.track_uri = self.track['uri']
        self.track_popularity = self.track['popularity']
        self.track_explicit = self.track['explicit']
        self.track_artists = [artist['name'] for artist in self.track['artists']]

        # get track features
        self.track_features = self.sp_connection.audio_features(tracks = self.track_uri)[0]

        return [self.track_name, self.track_artists, self.track_popularity,
                self.track_features['danceability'], self.track_features['valence'],
                self.track_features['energy'], self.track_explicit, self.track_features['key'],
                self.track_features['liveness'], self.track_features['loudness'],
                self.track_features['speechiness'], self.track_features['tempo']]

    def get_track_full_attrs(self, title, artist):
        '''
        Function that returns the advanced features of a desired song
        if it's not present in the local dataset
        '''
        # get search features

        # Perform API search request
        time.sleep(0.015)
        # Try the query
        # try:
        self.tfa_response = self.sp_connection.search(
                                    q="artist:" + artist + " track:" + title,
                                    type="track",
                                    limit=1)
        # If there is an exception:
        # print an error log
        # except:
        #     print(f"Oops! artist & song not found")

        # Saving the track informations
        self.tfa_track = self.tfa_response['tracks']['items'][0]
        # saving uri of the track
        self.tfa_song_uri = self.tfa_track['uri']
        # saving name of the track
        self.tfa_song_name = self.tfa_track['name']
        # saving artists of the track
        self.tfa_song_artists = [artist['name'] for artist in self.tfa_track['artists']]
        # saving popularity of the track
        self.tfa_song_popularity = self.tfa_track['popularity']
        # saving explicit of the track
        self.tfa_song_explicit = self.tfa_track['explicit']

        self.df_tfa = pd.DataFrame()
        self.df_tfa['uri'] = self.tfa_song_uri
        self.df_tfa['name'] = self.tfa_song_name
        self.df_tfa['artists'] = self.tfa_song_artists
        self.df_tfa['popularity'] = self.tfa_song_popularity
        self.df_tfa['explicit'] = self.tfa_song_explicit

        # Rewrite uri and name is needed
        self.df_tfa['uri'] = self.tfa_song_uri
        self.df_tfa['name'] = self.tfa_song_name

        # get audio_analysis features

        time.sleep(0.015)
        # Perform API audio_analysis request
        # try:
        self.tfa_track_analysis = self.sp_connection.audio_analysis(
                track_id = self.tfa_song_uri)
        # except:
        #    print(f"Oops! artist & song not found")
        # Reset segments arrays before new song analysis
        self.tfa_segment_pitch = []
        self.tfa_segment_timbre = []
        # Extract pitch and timbre for each segment of the song
        for segment in range(len(self.tfa_track_analysis['segments'])):
            self.tfa_segment_pitch.append(self.tfa_track_analysis['segments'][segment]['pitches'])
            self.tfa_segment_timbre.append(self.tfa_track_analysis['segments'][segment]['timbre'])
        # Reset df_song_segments dataframe
        self.tfa_df_song_segment = pd.DataFrame()
        # create pitch and timbre columns with np arrays
        self.tfa_df_song_segment['segment_pitch'] = self.tfa_segment_pitch
        self.tfa_df_song_segment['segment_timbre'] = self.tfa_segment_timbre
        # Split the array elements in different columns
        self.df_split_pitches = pd.DataFrame(self.tfa_df_song_segment['segment_pitch'].tolist(), columns=['sp1', 'sp2', 'sp3', 'sp4', 'sp5', 'sp6', 'sp7', 'sp8', 'sp9', 'sp10', 'sp11', 'sp12'])
        self.df_split_timbres = pd.DataFrame(self.tfa_df_song_segment['segment_timbre'].tolist(), columns=['tm1', 'tm2', 'tm3', 'tm4', 'tm5', 'tm6', 'tm7', 'tm8', 'tm9', 'tm10', 'tm11', 'tm12'])
        # Add new columns to df_segment
        self.tfa_df_song_segment = pd.concat([self.tfa_df_song_segment, self.df_split_pitches, self.df_split_timbres], axis=1)
        self.tfa_df_song_segment.drop(['segment_pitch', 'segment_timbre'], axis = 1, inplace = True)
        # Transpose mean serie into a dataframe row
        self.tfa_df_song_segment = self.tfa_df_song_segment.mean().to_frame().T

        # get audio_features features

        time.sleep(0.015)
        # Perform API audio_features request
        # try:
        self.tfa_track_features = self.sp_connection.audio_features(tracks = self.tfa_song_uri)[0]
        # except:
        #     print("Oops! artist & song with no features")
        self.tfa_df_track_features = pd.DataFrame()
        self.tfa_df_track_features = pd.DataFrame.from_dict([self.tfa_track_features])
        try:
            self.tfa_df_track_features.drop(columns=[
            'type',
            'track_href',
            'analysis_url',
            'duration_ms',
            'time_signature',
            'id',
            'uri'], inplace=True)
        except:
            print("Oops! artist & song with no features")

        # Merging all the features together
        self.df_tfa = pd.concat([self.df_tfa, self.tfa_df_track_features, self.tfa_df_song_segment], axis=1, join='inner')

    def create_df_songs(self):
        '''
        Function that create self.df_songs dataframe
        with the following features:

        - uri
        - name
        - artists
        - popylarity
        - explicit
        features
        '''
        # extract the list of artists in a np array
        # artists_array from the baseline dataset
        self.artists_array = np.array([])
        for artist in self.se.data.artists.unique():
            self.artists_array = np.append(self.artists_array, artist)

        # Test array for debugging purposes
        # self.test_artists_array = np.array(["['Robin Trower', 'Jack Bruce', 'Bill Lordan']",   TEST
        #                                     "['Michael Hedges']"])                             TEST

        # find 10 most popular songs for each artist
        # creating features np arrays to store first 5 informations
        self.songs_uri_array = np.array([])
        self.songs_name_array = np.array([])
        self.songs_artists_array = np.array([])
        self.songs_popularity_array = np.array([])
        self.songs_explicit_array = np.array([])

        # Test array to not overload API requests
        # for artist in self.test_artists_array:                                                 TEST
        for artist in self.artists_array:
            # Perform API search request
            time.sleep(0.015)
            print(f'{artist} ...')
            # Try the query
            try:
                self.asl_response = self.sp_connection.search(
                                    q="artist:" + artist,
                                    type="track",
                                    limit=self.search_limit)
            # If there is an exception:
            # jump to the next loop
            except:
                print(f"Oops! {artist} not valid.  Skipped...")
                continue

            # iteration over the self.search_limit songs
            for i in range(len(self.asl_response['tracks']['items'])):
                # append uri of the track
                self.songs_uri_array = np.append(
                    self.songs_uri_array, self.asl_response[
                        'tracks']['items'][i]['uri'])
                # append name of the track
                self.songs_name_array = np.append(
                    self.songs_name_array, self.asl_response[
                        'tracks']['items'][i]['name'])
                # append artists of the track
                self.songs_artists_array = np.append(
                    self.songs_artists_array, artist)
                # append popularity of the track
                self.songs_popularity_array = np.append(
                    self.songs_popularity_array, self.asl_response[
                        'tracks']['items'][i]['popularity'])
                # append explicit of the track
                self.songs_explicit_array = np.append(
                    self.songs_explicit_array, self.asl_response[
                        'tracks']['items'][i]['explicit'])

        self.df_songs = pd.DataFrame()
        self.df_songs['uri'] = self.songs_uri_array
        self.df_songs['name'] = self.songs_name_array
        self.df_songs['artists'] = self.songs_artists_array
        self.df_songs['popularity'] = self.songs_popularity_array
        self.df_songs['explicit'] = self.songs_explicit_array
        #self.df_songs.to_csv('../raw_data/songs.csv')

    def create_df_audio_analysis(self):
        '''
        Function that create a self.df_analysis dataframe
        with the following features:

        - 12 pitch features
        - 12 timbre features
        - uri
        '''
        # From uri array list, query pitch and timbre features
        self.df_analysis = pd.DataFrame()
        self.df_songs_csv = pd.read_csv('../raw_data/songs.csv')
        self.songs_uri_array_csv = self.df_songs_csv['uri']
        # For testing purposes only iterate over the first 3 uri
        #for uri in self.songs_uri_array[:3]:
        #for uri in self.songs_uri_array:
        for uri in self.songs_uri_array_csv:
            time.sleep(0.015)
            print(f'{uri} ...')
            # Perform API audio_analysis request
            try:
                self.track_analysis = self.sp_connection.audio_analysis(track_id = uri)
            except:
                print(f"Oops! {uri} not valid.  Skipped...")
                continue
            # Reset segments arrays before new song analysis
            self.segment_pitch = []
            self.segment_timbre = []
            # Extract pitch and timbre for each segment of the song
            for segment in range(len(self.track_analysis['segments'])):
                self.segment_pitch.append(self.track_analysis['segments'][segment]['pitches'])
                self.segment_timbre.append(self.track_analysis['segments'][segment]['timbre'])
            # Reset df_song_segments dataframe
            self.df_song_segments = pd.DataFrame()
            # create pitch and timbre columns with np arrays
            self.df_song_segments['segment_pitch'] = self.segment_pitch
            self.df_song_segments['segment_timbre'] = self.segment_timbre
            # Split the array elements in different columns
            self.df_split_pitches = pd.DataFrame(self.df_song_segments['segment_pitch'].tolist(), columns=['sp1', 'sp2', 'sp3', 'sp4', 'sp5', 'sp6', 'sp7', 'sp8', 'sp9', 'sp10', 'sp11', 'sp12'])
            self.df_split_timbres = pd.DataFrame(self.df_song_segments['segment_timbre'].tolist(), columns=['tm1', 'tm2', 'tm3', 'tm4', 'tm5', 'tm6', 'tm7', 'tm8', 'tm9', 'tm10', 'tm11', 'tm12'])
            # Add new columns to df_segment
            self.df_song_segments = pd.concat([self.df_song_segments, self.df_split_pitches, self.df_split_timbres], axis=1)
            self.df_song_segments.drop(['segment_pitch', 'segment_timbre'], axis = 1, inplace = True)
            # Transpose mean serie into a dataframe row
            self.df_song_segments = self.df_song_segments.mean().to_frame().T
            # Add uri column to perform the future merge
            self.df_song_segments['uri'] = uri
            self.df_analysis = pd.concat([self.df_analysis, self.df_song_segments])
        #self.df_analysis.to_csv('../raw_data/analysis.csv')

    def create_df_audio_features(self):
        '''
        Function that create a self.df_features dataframe
        with the following features:

        - danceability
        - energy
        - key
        - loudness
        - mode
        - speechiness
        - acousticness
        - instrumentalness
        - liveness
        - valence
        - tempo
        - uri
        '''
        self.df_features = pd.DataFrame()
        self.df_songs_csv = pd.read_csv('../raw_data/songs.csv')
        self.songs_uri_array_csv = self.df_songs_csv['uri']
        #for uri in self.songs_uri_array[:2]:
        for uri in self.songs_uri_array_csv:
            time.sleep(0.015)
            print(f'{uri} ...')
            # Perform API audio_features request
            try:
                self.track_features = self.sp_connection.audio_features(tracks = uri)[0]
            except:
                print(f"Oops! {uri} not valid.  Skipped...")
                continue
            self.df_track_features = pd.DataFrame()
            self.df_track_features = pd.DataFrame.from_dict([self.track_features])
            try:
                self.df_track_features.drop(columns=[
                'type',
                'track_href',
                'analysis_url',
                'duration_ms',
                'time_signature',
                'id'], inplace=True)
            except:
                print(f"Oops! {uri} has no features.  Skipped...")
            self.df_features = pd.concat([self.df_features, self.df_track_features])
        #self.df_features.to_csv('../raw_data/features.csv')

    def merge_dataframes(self):
        '''
        Function that merge all the dataframe toghether
        '''
        self.full_data = pd.merge(self.df_songs, self.df_analysis, how='outer', on='uri')
        self.full_data = pd.merge(self.full_data, self.df_features, how='outer', on='uri')
