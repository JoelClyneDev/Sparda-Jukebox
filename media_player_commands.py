from dataclasses import dataclass
from database_attributes import true_database
from media_player_attributes import true_media_player
import pafy
import subprocess


song_by_id = true_database.list_songs
fuzzy_search = true_database.name_search
connection = true_database.connect
Instance = true_media_player.instance
Media = true_media_player.media
player = true_media_player.player
playlist = true_media_player.playlist
playlist_num = true_media_player.playlist_num

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
    result = add_to_playlist(song_title, player, arguments, playlist, playlist_num)
    player.play()
    player.next()
    # Media.get_mrl()

    if '--s' in arguments:
        # the url is result[2]
        save_song(result[2])

def save_song(url):
    print(url)
    subprocess.run(["youtube-dl", url, "-x", "--audio-format", "mp3"], shell=True)

def add_to_playlist(song_title, player, arguments, playlist, playlist_num):
    if "--id" in arguments:
        # get the song by its id
        result = song_by_id(song_title)
    else:
        # get the name
        name = fuzzy_search(song_title)
        print(name)
        # now the rest
        c = connection.cursor()
        c.execute("SELECT id, title, url FROM DMC_SONG_LIST WHERE title=?", (name,))
        result = c.fetchone()
        print(result)
    # add the songs name to playlist
    global new_song_name
    new_song_name = result[1]
    playlist += [new_song_name]
    playlist_num += 1
    url = result[2]
    # gets the song from youtube
    video = pafy.new(url)
    # whenever i get the video, get the best version
    best = video.getbestaudio()
    # gets the best version of the video
    music = best.url
    # add song to media list
    Media.add_media(music)
    # add media list to player
    player.set_media_list(Media)
    # useful for other stuff
    return result

def add_playlist(song_title, arguments):
    add_to_playlist(song_title, player, arguments, playlist, playlist_num)


def pause():
    player.pause()


def stop():
    player.stop()

def skip():
    global playlist_num
    if playlist_num + 1 <= len(playlist):
        playlist_num += 1
        player.next()




def back():
    global playlist_num
    if playlist_num + 1 <= 0:
        playlist_num += 1
        player.previous()


def view_song():
    # gets currently playing song
    new_song_name = playlist[playlist_num]
    temp = player.get_media_player().get_media()
    # parses the songs to enable metadata collection
    temp.parse_with_options(1, 0)
    # wait till its done
    while True:
        if str(temp.get_parsed_status()) == 'MediaParsedStatus.done':
            break  # Might be a good idea to add a failsafe in here because what if it never finishes?
    temp.set_meta(1, new_song_name)
    print(temp.get_meta(1))





def view_playlist():
    print(playlist)





@dataclass
class MediaCommands:
    # atr means atribute
    play_atr: play_song
    add_to_playlist_atr : add_to_playlist
    add_playlist_atr : add_playlist
    pause_atr: pause
    stop_atr: stop
    skip_atr : skip
    back_atr : back
    view_song_atr: view_song
    view_playlist_atr: view_playlist


# terminal : terminal_controls
true_media_commands = MediaCommands(play_song, add_to_playlist, add_playlist, pause, stop, skip, back, view_song, view_playlist)