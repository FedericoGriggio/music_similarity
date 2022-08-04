import streamlit as st
import pandas as pd
import numpy as np

# Package classes
from music_similarity.search_engine import SearchEngine
from music_similarity.preprocessor import Preprocessor
from music_similarity.playlist import Playlist
from music_similarity.query_spotify_api import get_track_attrs

'''
streamlit dummy app 04/08/2022
'''

st.markdown('''
## Insert title and artist to find similar songs
''')

title = st.text_input('Title', 'A Sort Of Homecoming')
artist = st.text_input('Artist', 'U2')

spotify = get_track_attrs(artist, title)

if 'se' in globals():
    del se
spotify = pd.read_csv('raw_data/ML_spotify_data.csv')
se = SearchEngine(spotify)
se.target_song(title, artist)

if 'preprocessor' in globals():
    del preprocessor
preprocessor = Preprocessor(se)
preprocessor.scale_data()

if 'playlist' in globals():
    del playlist
playlist = Playlist(preprocessor, se)
playlist.build_model()

st.write(playlist.playlist)
