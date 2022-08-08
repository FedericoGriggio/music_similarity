import streamlit as st
import pandas as pd
import numpy as np

# Package classes
from music_similarity.search_engine import SearchEngine
from music_similarity.preprocessor import Preprocessor
from music_similarity.playlist import Playlist
from music_similarity.query_spotify_api import get_track_attrs

st.set_page_config(
     page_title="Music Similarity",
     layout="wide",
     initial_sidebar_state="collapsed",
     menu_items={
         'About': "This app will help you find your next favourite songs!"
     }
 )

# Create a sidebar to add info
with st.sidebar:
    # with st.echo():
    st.markdown("## How does it work?")
    st.write("To find your new favourite songs, we use a model called KNN (k-nearest neighbors algorithm) which is a supervised learning classifier that uses proximity to make classifications or predictions about the grouping of an individual data point. In this case, it uses features such as danceability, liveness, loudness and tempo to try and find the most similar songs.  ")

# Use our css file for styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)

local_css("style.css")
remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')

'''
streamlit dummy app 05/08/2022
'''
# The title of our app
st.markdown('''
## Discover some new songs!
''')
st.text('Tell us a song that you like:')

# User input for song name and artist
col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Title", "Another One Bites The Dust")
with col2:
    artist = st.text_input("Artist", "Queen")

# Find the track from API
# spotify = get_track_attrs(artist, title)

if 'se' in globals():
    del se
spotify = pd.read_csv('raw_data/full_data.csv')
se = SearchEngine(spotify)
try:
    se.target_song(title, artist)
except:
    # Error if the song is not found
    st.error("We don't know this song, sorry! Try another one")

if 'preprocessor' in globals():
    del preprocessor
preprocessor = Preprocessor(se)
try:
    preprocessor.scale_data()
except:
    # Error if the song is not found
    st.error("We don't know this song, sorry! Try another one")
    st.stop()

if 'playlist' in globals():
    del playlist
playlist = Playlist(preprocessor, se)
playlist.build_model()

st.text(f'You have selected: {se.title} - {se.artist}')
st.text('We think you might like these songs:')
st.table(playlist.playlist)
