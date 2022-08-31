import streamlit as st
import pandas as pd
import numpy as np

# Package classes
from music_similarity.search_engine import SearchEngine
from music_similarity.preprocessor import Preprocessor
from music_similarity.playlist import Playlist
from music_similarity.query_spotify_api import get_track_attrs
from music_similarity.api_extractor import ApiExtractor

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

# The title of our app
st.markdown('''
## Discover some new songs!
Tell us a song that you like:
''')

# User input for song name and artist
col1, col2 = st.columns(2)
with col1:
    title = st.text_input("Title:", "Another One Bites The Dust")
with col2:
    artist = st.text_input("Artist:", "Queen")

# Create search button
button_clicked = st.button("Search")

# Find the track from API
# spotify = get_track_attrs(artist, title)

# Clean objects memory
if 'se' in globals():
    del se
if 'preprocessor' in globals():
    del preprocessor
if 'ae' in globals():
    del ae
if 'playlist' in globals():
    del playlist

# After user searches their song, run model
if button_clicked:
    spotify = pd.read_csv('raw_data/full_data.csv', index_col=0)
    se = SearchEngine(spotify)
    ae = ApiExtractor(se)
    se.target_song(title, artist) # Check if the song is in the local database
    ae.get_track_full_attrs(title, artist) # Perform the get request
    preprocessor = Preprocessor(se, ae)
    try:
        preprocessor.scale_se()
        # If is not, request the song to Spotify
    except:
        try:
            preprocessor.scale_ae()
        except:
            # If is not present in the Spotify database show an error
            st.error("Sorry, this song is not available, try another one")
        else:
            song_title = ae.tfa_song_name
            song_artist = ae.tfa_song_artists
    else:
        song_title = se.title
        song_artist = se.artist
    song_artist = str(song_artist).strip("['").strip("']")
    playlist = Playlist(preprocessor, se)
    playlist.build_model()
    st.text(f'You have selected: {song_title} - {song_artist}')
    st.text('We think you might like these songs:')
    st.table(playlist.playlist)
