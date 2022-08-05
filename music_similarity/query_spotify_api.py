import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# TO DO: I'LL TURN THIS INTO A CLASS LATER

def get_track_attrs(artist, title):

    # credentials need to be exported via the command line
    auth_manager = SpotifyClientCredentials()
    sp_connection = spotipy.Spotify(auth_manager=auth_manager)

    # get track attributes
    sp_response = sp_connection.search(
        q="artist:" + artist + " track:" + title,
        type="track",
        limit=1)

    # parse attributes from track
    track = sp_response['tracks']['items'][0]
    track_name = track['name']
    track_uri = track['uri']
    track_popularity = track['popularity']
    track_explicit = track['explicit']
    track_artists = [artist['name'] for artist in track['artists']]

    # get track features
    track_features = sp_connection.audio_features(tracks = track_uri)[0]

    return [track_name, track_artists, track_popularity,
            track_features['danceability'], track_features['valence'],
            track_features['energy'], track_explicit, track_features['key'],
            track_features['liveness'], track_features['loudness'],
            track_features['speechiness'], track_features['tempo']]
