import sqlite3
from sqlite3 import Error
import playlist_operations
import song_retrieval
import vlc
import threading
import time
import pafy
import sys
import youtube_dl
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import subprocess

def create_connection(db_file):
    """ Accesses the song database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    #the connection to the database
    return conn


def setup_prompt():
    """
    asks the user how they would like to initially set up the program
    :return:
    """
    playlist = []
    init_play = input("Welcome to Sparda's Jukebox!\n"
          "Would ya like a playlist? (y/n) ").lower()
    if init_play == "y" or init_play == "yes":
        pass
    else:
        first_song = song_retrieval.select_song()
        playlist = [first_song]
    return playlist

def prompt_mode():
    """
    Guides the user with prompts
    :return:
    """
    init_play = setup_prompt()
    playlist_operations.operate_playlist(init_play)

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
    result = add_to_playlist(song_title, player, arguments, playlist)
    player.next()
    #Media.get_mrl()
    player.play()
    if '--s' in arguments:
        #the url is result[2]
        save_song(result[2])

def fuzzy_search(search_name):
    c = connection.cursor()
    c.execute("SELECT title FROM DMC_SONG_LIST")
    names = c.fetchall()
    result = process.extractOne(search_name, names)
    result = result[0][0]
    return result

def song_by_id(num):
    c = connection.cursor()
    c.execute("SELECT id, title, url FROM DMC_SONG_LIST WHERE id = ?", (num,))
    result = c.fetchone()
    return result

def pause():
    player.pause()

def stop():
    player.stop()


def add_to_playlist(song_title, player, arguments, playlist):
    if "--id" in arguments:
        #get the song by its id
        result = song_by_id(song_title)
    else:
        #get the name
        name = fuzzy_search(song_title)
        print(name)
        #now the rest
        c = connection.cursor()
        c.execute("SELECT id, title, url FROM DMC_SONG_LIST WHERE title=?", (name,))
        result = c.fetchone()
        print(result)
    #add the songs name to playlist
    global new_song_name
    new_song_name = result[1]
    playlist += [new_song_name]
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
    #useful for other stuff
    return result



def add_playlist(song_title, arguments):
    add_to_playlist(song_title, player, arguments, playlist)

def close_program():
    sys.exit()

def skip():
    player.next()

def display_songs(tech_arguements= None, arguments=None):
    """
    shows all of the songs based on game, type, or both
    tech arguments is for cheating choice[1] into arguments
    :return:
    """
    arguments = [tech_arguements] + arguments
    print(arguments, "dfsadfg")
    c = connection.cursor()
    if arguments is None:
        #show everything
        c.execute("SELECT id, title FROM DMC_SONG_LIST")
    else:
        for i in range(len(arguments)):
            if arguments[i] == "--game":
                game_name = arguments[i + 1]
                c.execute("SELECT id, title FROM DMC_SONG_LIST WHERE game=?", (game_name,))
            elif arguments[i] == "--genre":
                genre_name = arguments[i + 1]
                c.execute("SELECT id, title FROM DMC_SONG_LIST WHERE category=?", (genre_name,))
    for value in c.fetchall():
        print(value)



def help_me():
    print("Commands\n"
          "play (name, id, playlist) - plays a song or playlist\n"
          "  name is default\n"
          "  use play playlist to play current playlist\n"
          "  --id enable search by id\n"
          "  --s to download song as mp3\n"
          "prompt - change program to prompt user for song type\n"
          "p - pause current song\n"
          "s - stop current song\n"
          "add - add song to playlist\n"
          "  name is default\n"
          "  --id enable search by id\n"
          "  --s to download song as mp3\n"
          "exit - close program\n"
          "skip - skip current song in playlist")

def view_playlist():
    print(playlist)

def save_song(url):
    print(url)
    subprocess.run(["youtube-dl", url, "-x", "--audio-format", "mp3"], shell=True)

def back():
    player.previous()

def view_song():
    temp = player.get_media_player().get_media()
    temp.parse_with_options(1, 0)
    while True:
        if str(temp.get_parsed_status()) == 'MediaParsedStatus.done':
            break  # Might be a good idea to add a failsafe in here.
    temp.set_meta(1, new_song_name)
    print(temp.get_meta(1))



command_dictionary = {
    "help": help_me,
    "prompt": prompt_mode,
    "play": play_song,
    "p": pause,
    "s": stop,
    "add": add_playlist,
    "exit": close_program,
    "skip": skip,
    "view_p": view_playlist,
    "back": back,
    "view_c": view_song,
    "list": display_songs

}

#these are sorta part of the main, but dont work with other files unless theyre outside

#create the connection to the database
connection = create_connection('dmc_songs.db')
#start VLC player and make it a new media player, create an instance with a media list
Instance = vlc.Instance()
#sets up the intial empty media list
Media = vlc.libvlc_media_list_new(Instance)
#makesthe player
player = vlc.libvlc_media_list_player_new(Instance)
#make a dynamic playlist with the names
playlist = []

def terminal_controls():
    while True:
        song_list = player.get_media_player()
        print(vlc.libvlc_media_player_is_seekable(song_list))
        choice = input(">> ")
        #separate the elements in the response and process the first one
        #breaks the program if choice is none
        if choice is not None:
            """
            if "\"" in choice:
                choice_list = []
                count = 0
                while count < len(choice):
                    if choice[len(choice)] == "\"":
                        choice_list += choice[0: len(choice) - 1]
            """
            choice = choice.split()
            #its looking for a name not an id
            print(choice, "fsdaff")
            if "--id" not in choice and len(choice) != 1:
                print("yes")
                search_query = ""
                count = 1
                #if theres no --, its a something to search for
                new_choice = [choice[0]]
                for i in choice[1:]:
                    if i[0:2] == "--":
                        if count > 1:
                            search_query = search_query[:-1]
                            new_choice += [search_query]
                            search_query = ""
                        new_choice += [i]
                    else:
                        search_query = search_query + i + " "
                        count += 1
                if search_query != "":
                    search_query = search_query[:-1]
                    new_choice += [search_query]
                #removes the last space in the search query
                """
                temp_choice = [choice[0], search_query]
                for arg in choice[count:]:
                    temp_choice += [arg]
                choice = temp_choice
                print(choice)
                """
                choice = new_choice
                if choice[1] == "":
                    choice = [choice[0]]
                print(choice)
            #print(choice)
            if choice[0] not in command_dictionary:
                print("Dismal - Invalid Command")
            elif len(choice) == 1:
                command_dictionary[choice[0]]()
            else:
                #add the extraneous parameters to a set and use those as the potential arguments
                arguments = []
                for arg in choice[2:]:
                    arguments += [arg]
                command_dictionary[choice[0]](choice[1], arguments)
                #they will be like id_num=True

def main():
    #tell user in beginning
    print("Welcome to Sparda's Jukebox, please enter a command below")
    print("Type -help for a list of commands")
    terminal_controls()




if __name__ == '__main__':
    main()