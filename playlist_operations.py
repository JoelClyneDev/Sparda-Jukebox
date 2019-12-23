
from func_timeout import func_timeout, FunctionTimedOut
import song_retrieval
import time
import vlc
import main_command
import threading


def operate_playlist(playlist, prev_songs = []):
    #fix this so it works with the prompt controls only
    """
    plays whatever song is next in the queue
    change so that it saves the old songs
    :param playlist:
    :return:
    """
    old_playlist = playlist
    for song in playlist:
        playlist_ctrl = song_retrieval.stream_the_song(song, playlist)
    if playlist != old_playlist:
        #when a song is added or removed from the playlist, removed the one that was just played and put it in prev
        prev_songs += [playlist[0]]
        playlist = playlist[1:]
        print("yeehaw")
        operate_playlist(playlist, prev_songs)


def command_playlist(playlist, prev_songs = []):
    """
    manages the playlists without inputs for the commnand mode
    :param player:
    :param playlist:
    :param duration:
    :return:
    """
    old_playlist = playlist
    for song in playlist:
        playlist_ctrl = threading.Thread(target=song_retrieval.stream_the_song, args=(song, main_command.Instance, main_command.player), name='Playlist_control')
        playlist_ctrl.start()
        time.sleep(10)
    if playlist != old_playlist:
        #when a song is added or removed from the playlist, removed the one that was just played and put it in prev
        prev_songs += [playlist[0]]
        playlist = playlist[1:]
        print("yeehaw")
        operate_playlist(playlist, prev_songs)

def controls(player, playlist, duration):
    #makes an infinte loop which keeps pycharm from closing the player while also allowing the user the play or pause
    old_time = time.time()
    end_time = time.time() + duration
    za_wardo = False
    while time.time() < end_time > 0:
        #the input will time out at the end of the song
        # disable the alarm after success
        try:
            nextcmd = func_timeout(duration, input, args="")
        except FunctionTimedOut:
            nextcmd = None
        except Exception as e:
            nextcmd = None
        #process user input
        """
        """
        #total time of song - how long the song has been playing since the last reset
        if nextcmd == "p":
            player.pause()
            #toggle pause and resume time
            za_wardo = not za_wardo
            if za_wardo == True:
                freeze_time = time.time()
            else:
                #time while paused
                freeze_time = time.time() - freeze_time
                print(freeze_time, "galactic fart")
                elapsed_time = time.time() - old_time
                old_time = time.time()
                duration = duration + freeze_time - elapsed_time
                end_time = end_time + freeze_time
                print(duration, "current")
        elif nextcmd == "s":
            player.stop()
            break
        elif nextcmd == "a":
            playlist += [song_retrieval.select_song()]
        elif nextcmd == "e":
            # if theres one playing before it, its time to stop
            player.stop()
            song_retrieval.stream_the_song(song_retrieval.select_song(), playlist)

print("dwsaf")