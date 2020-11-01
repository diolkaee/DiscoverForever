# DiscoverForever
A small python script to save your Discover Weekly into a permanent DiscoverForever-Playlist with a single command!

# Installing
1. Install Spotipy via Pip
2. Register on https://developer.spotify.com/ for developer access
  * The scopes required are: 
    * user-library-read 
    * playlist-modify-private 
    * playlist-modify-public
3. Fill config.ini with user detail

# Usage
* When running the script for the first time (or after deleting the .cache file) you have to authenticate yourself to spotify.
This does not yet save your tracks, so run the script twice.
Afterwards, your credentials are stored in the .cache file and you won't have to reauthenticate.
