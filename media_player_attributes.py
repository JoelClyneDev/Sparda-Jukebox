from dataclasses import dataclass
import vlc

@dataclass
class MediaPlayer:
    instance: vlc.Instance
    media: vlc.MediaList
    player: vlc.MediaListPlayer
    playlist: list
    playlist_num: int

#start VLC player and make it a new media player, create an instance with a media list
Instance = vlc.Instance()
#sets up the intial empty media list
Media = vlc.libvlc_media_list_new(Instance)
#makesthe player
player = vlc.libvlc_media_list_player_new(Instance)
#make a dynamic playlist with the names and keeps track of the current one
playlist = []
#-1 bcs its empty
playlist_num = -1

true_media_player = MediaPlayer(Instance, Media, player, playlist, playlist_num)
