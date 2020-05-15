from dataclasses import dataclass
from database_attributes import true_database
from media_player_attributes import true_media_player
import pafy
import subprocess
import vlc


song_by_id = true_database.list_songs
fuzzy_search = true_database.name_search
connection = true_database.connect
Instance = true_media_player.instance
MediaList = true_media_player.media_list
player = true_media_player.player
playlist = true_media_player.playlist
playlist_num = true_media_player.playlist_num
playlist_gen = true_media_player.playlist_gen

def play_song(song_title, arguments):
    """
    if song_title == "playlist":
        playlist_operations.command_playlist(playlist)
    if "-id" in arguments:
        #get the song by its id
        result = song_by_id(song_title)
        song_retrieval.stream_the_song(result, Instance, player)
            else:
        print("the title")
    """
    player.stop()
    result = add_to_playlist(song_title, player, arguments, playlist, true_media_player.playlist_num)
    player.play_item_at_index(true_media_player.playlist_num), "hmm"
    if '--s' in arguments:
        # the url is result[2]
        save_song(result[2])

def find_song_by_title(song_title):
    c = connection.cursor()
    c.execute("SELECT id, title, url FROM DMC_SONG_LIST WHERE title = ?", (song_title,))
    song = c.fetchone()
    return song


def save_song(url=None):
    if url is not None:
        subprocess.run(["youtube-dl", url, "-x", "--audio-format", "mp3"], shell=True)
    else:
        temp = player.get_media_player().get_media()
        current_song_name = temp.get_meta(1)
        current_song_url = find_song_by_title(current_song_name)[2]
        subprocess.run(["youtube-dl", current_song_url, "-x", "--audio-format", "mp3"], shell=True)


def add_to_playlist(song_title, player, arguments, playlist, playlist_num):
    if "--id" in arguments:
        # get the song by its id
        result = true_database.id_search(song_title)
    else:
        # get the name
        name = fuzzy_search(song_title)
        # now the rest
        c = connection.cursor()
        c.execute("SELECT id, title, url FROM DMC_SONG_LIST WHERE title=?", (name,))
        result = c.fetchone()
        print(result[1], "-", result[0])
        print(result[2])
    # add the songs name to playlist
    global new_song_name
    new_song_name = result[1]
    #playlist += [new_song_name]
    url = result[2]
    # gets the song from youtube
    video = pafy.new(url)
    # whenever i get the video, get the best version
    best = video.getbestaudio()
    # gets the best version of the video
    music = best.url
    temp_media = Instance.media_new(music)
    temp_media.get_mrl()
    set_meta(temp_media, new_song_name)
    MediaList.add_media(temp_media)
    player.set_media_list(MediaList)
    true_media_player.playlist_num += 1
    #turn the music url into a media player object so i can give it metadata
    # set the title and get the specfic song now

    # add song to media list

    # add media list to player


    # useful for other stuff
    return result

def add_playlist(song_title, arguments):
    add_to_playlist(song_title, player, arguments, playlist, playlist_num)

def set_meta(Media, new_song_name):
    Media.parse_with_options(1, 0)
    # wait till its done
    while True:
        if str(Media.get_parsed_status()) == 'MediaParsedStatus.done':
            break  # Might be a good idea to add a failsafe in here because what if it never finishes?
    Media.set_meta(1, new_song_name)


def pause():
    player.pause()

def stop():
    player.stop()

def skip():
    player.next()
    #global playlist_num
    #if playlist_num + 1 <= len(playlist):
        #playlist_num += 1





def back():
    player.previous()
    #global playlist_num
    #if playlist_num + 1 >= 0:
        #playlist_num = 1



def view_song():
    # gets currently playing song
    temp = player.get_media_player().get_media()
    print(temp.get_meta(1))





def view_playlist():
    print(true_media_player.playlist_gen(true_media_player.media_list))





@dataclass
class MediaCommands:
    # atr means attribute
    play_atr: play_song
    add_to_playlist_atr : add_to_playlist
    add_playlist_atr : add_playlist
    pause_atr: pause
    stop_atr: stop
    skip_atr : skip
    back_atr : back
    view_song_atr: view_song
    view_playlist_atr: view_playlist
    set_meta_atr: set_meta
    save_atr: save_song


# terminal : terminal_controls
true_media_commands = MediaCommands(play_song, add_to_playlist, add_playlist, pause, stop, skip, back, view_song, view_playlist, set_meta, save_song)