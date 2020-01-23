from dataclasses import dataclass
import vlc

def generate_playlist(media_list):
    playlist = []
    for i in range(true_media_player.playlist_num + 1):
        playlist += [media_list.item_at_index(i).get_meta(1)]
    return playlist

@dataclass
class MediaPlayer:
    instance: vlc.Instance
    media_list: vlc.MediaList
    player: vlc.MediaListPlayer
    playlist: list
    playlist_gen: generate_playlist
    playlist_num: int




#start VLC player and make it a new media player, create an instance with a media list
Instance = vlc.Instance()
#sets up the intial empty media list
MediaList = vlc.libvlc_media_list_new(Instance)
#makesthe player
player = vlc.libvlc_media_list_player_new(Instance)
#make a dynamic playlist with the names and keeps track of the current one
playlist = []
#-1 bcs its empty, and 0 will be the first index
playlist_num = -1

true_media_player = MediaPlayer(Instance, MediaList, player, playlist, generate_playlist, playlist_num)
