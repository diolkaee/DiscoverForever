import configparser
from spotipy import Spotify, util

# Initialize and Authorize Spotipy module
config = configparser.ConfigParser()
config.read('config.ini')

if "AUTH" not in config.sections():
    print("Config file could not be read successfully")
    exit()

token = util.prompt_for_user_token(
    username = config['INFO']['username'],
    scope = "user-library-read playlist-modify-private playlist-modify-public",
    client_id = config['AUTH']['user_id'],
    client_secret= config['AUTH']['user_secret'],
    redirect_uri= config['INFO']['redirect_uri']
)

if not token:
    print("Authorization failed")
    exit()

spotipy = Spotify(auth=token)
user = spotipy.current_user()
user_id = user['id']

# Add Weekly to Forever
weekly_playlist = spotipy.user_playlist_tracks(
    user='spotify', 
    playlist_id=config['INFO']['discover_weekly_uri']
    )

weekly_ids = []
for item in weekly_playlist['items']:
    weekly_ids.append(item['track']['id'])

forever_uri = config['INFO']['discover_forever_uri']
forever_playlist = spotipy.user_playlist_tracks(
    user=user_id, 
    playlist_id=forever_uri
    )

forever_size = forever_playlist['total']
forever_ids = []
tracks_to_add = []

# Spotify requires paginated queries
if forever_size > 100:
    for i in range(0, int(forever_size/100)+1):
        paged_forever_playlist = spotipy.user_playlist_tracks(user=user_id, playlist_id=forever_uri, offset=i*100)
        for item in paged_forever_playlist['items']:
            forever_ids.append(item['track']['id'])

# Filter for duplicates
for id in weekly_ids:
    if id not in forever_ids:
        tracks_to_add.append(id)

if len(tracks_to_add) == 0:
    print("You discovered all your weekly tracks already :(")
else:
    spotipy.user_playlist_add_tracks(user=user_id, playlist_id=forever_uri, tracks=tracks_to_add)
    print("Your weekly tracks have been saved :)")