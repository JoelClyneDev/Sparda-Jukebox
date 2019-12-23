import sqlite3
from sqlite3 import Error
import playlist_operations
import song_retrieval
import vlc
import threading
import time

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
    if song_title == "playlist":
        playlist_operations.command_playlist(playlist)
    if "-id" in arguments:
        #get the song by its id
        result = song_by_id(song_title)
        song_retrieval.stream_the_song(result, Instance, player)
    else:
        print("the title")

def song_by_id(num):
    c = connection.cursor()
    c.execute("SELECT id, title, url FROM DMC_SONG_LIST WHERE id = '%s'" % num)
    result = c.fetchone()
    return result

def pause():
    player.pause()

def stop():
    player.stop()

def add_playlist(song_title, playlist, arguments):
    if "-id" in arguments:
        #get the song by its id
        result = song_by_id(song_title)
        playlist += [result]

command_dictionary = {
    "prompt": prompt_mode,
    "play": play_song,
    "p": pause,
    "s": stop,
    "add": add_playlist,
}

#these are sorta part of the main, but dont work with other files unless theyre outside

#create the connection to the database
connection = create_connection('dmc_songs.db')
#start VLC player and make it a new media player
Instance = vlc.Instance()
player = Instance.media_player_new()
#make a dynamic playlist
playlist = []

def terminal_controls():
    while True:
        print(playlist)
        choice = input(">> ")
        #separate the elements in the response and process the first one
        #breaks the program if choice is none
        if choice is not None:
            choice = choice.split()
            print(choice)
            if choice[0] not in command_dictionary:
                print("Dismal - Invalid Command")
            elif len(choice) == 1:
                command_dictionary[choice[0]]()
            elif choice[0] == "add":
                # add the extraneous parameters to a set and use those as the potential arguments
                arguments = set()
                for arg in choice[2:]:
                    arguments.add(arg)
                command_dictionary[choice[0]](choice[1], playlist, arguments)
            else:
                #add the extraneous parameters to a set and use those as the potential arguments
                arguments = set()
                for arg in choice[2:]:
                    arguments.add(arg)
                command_dictionary[choice[0]](choice[1], arguments)
                #they will be like id_num=True

def main():
    #tell user in beginning
    print("Welcome to Sparda's Jukebox, please enter a command below")
    print("Type -help for a list of commands")
    terminal_controls()




if __name__ == '__main__':
    main()