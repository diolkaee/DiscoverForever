from spotipy import Spotify, util
import json

#Initialize the spotipy module and authorization
client_id = #Your client_id comes here, client_id & client_secret are obtained from https://developer.spotify.com/
client_secret = #Your client_secret comes here
redirect_uri = "https://www.google.com"
scope = "user-library-read playlist-modify-public playlist-modify-private"
class DiscoverForever:
    
    def __init__(self, client_id, client_secret):
        self.discover_weekly_uri = #Your Discover Weekly URI comes here
        self.token = util.prompt_for_user_token(
            username= #Your Spotify Username comes here (keep the comma ->)  ,
            scope= "user-library-read playlist-modify-public playlist-modify-private", 
            client_id= client_id, 
            client_secret= client_secret, 
            redirect_uri= "https://www.google.com")
        if self.token:
            self.sp = Spotify(auth=self.token)
            self.user = self.sp.current_user()
            self.id = self.user['id']

    def get_own_playlists(self):
        return self.sp.user_playlists(self.id)
    
    def get_playlist_by_id(self, id):
        return self.sp.user_playlist(self.user, id)

    def get_discover_weekly_tracks(self):
        trackList = []
        print("Your discover weekly tracks:")
        for item in self.sp.user_playlist('spotify',self.discover_weekly_uri)['tracks']['items']:
            print(item['track']['name'] + ": " + item['track']['id'])
            trackList.append(item['track'])
        return trackList

    def get_tracks_from_playlist(self, playlists_list, name):
        returnList = []
        for playlist in playlists_list['items']:
            if 'name' in playlist:
                if playlist['name'] == name:
                    for track in playlist['tracks']:
                        returnList.append(track)

    def get_playlist_by_name(self, playlistName):
        playlists = self.get_own_playlists()['items']
        for playlist in playlists:
            if playlist['name'] == playlistName:
                print(playlist['name'] + " id: " + playlist['id'] + "\n")
                return playlist

    def add_weekly_to_forever(self, foreverId, weeklyIds):
        remote_playlist_ids = []
        tracks_to_add = []
        remote_playlist = self.sp.user_playlist_tracks(self.id, playlist_id=foreverId)
        remote_playlist_total_tracks = remote_playlist['total']

        #Check for duplicates
        for item in remote_playlist['items']:
            remote_playlist_ids.append(item['track']['id'])

        #Spotify requires pagination when length of playlist > 100
        if remote_playlist_total_tracks > 100:
            for i in range (1, int(remote_playlist_total_tracks/100)+1):
                remote_playlist = self.sp.user_playlist_tracks(self.id, playlist_id=foreverId, offset=i*100)
                for item in remote_playlist['items']:
                    remote_playlist_ids.append(item['track']['id'])
        
        for id in weeklyIds:
            if id not in remote_playlist_ids:
                tracks_to_add.append(id)

        if len(tracks_to_add) == 0:
            print("All tracks already added")
        else:
            self.sp.user_playlist_add_tracks(self.id, playlist_id=foreverId, tracks=tracks_to_add)
    
    def cleanup_duplicates_from_playlist(self, playlistId, weeklyIds):
        unique_ids = []
        remote_playlist = self.sp.user_playlist_tracks(self.id, playlist_id=playlistId)
        unique_ids += weeklyIds
        for item in remote_playlist['items']:
            if item['track']['id'] not in unique_ids:
                unique_ids.append(item['track']['id'])
        self.sp.user_playlist_replace_tracks(self.id, playlistId, unique_ids)
    
if __name__ == '__main__':
    disc = DiscoverForever(client_id, client_secret)
    foreverPlaylist = disc.get_playlist_by_name('Discover Forever')
    foreverId = foreverPlaylist['id']
    weeklyTracks = disc.get_discover_weekly_tracks()
    weeklyIds = []
    for track in weeklyTracks:
        weeklyIds.append(track['id'])
    disc.add_weekly_to_forever(foreverId, weeklyIds)
