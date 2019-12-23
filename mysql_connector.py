import sqlite3
from sqlite3 import Error
from dataclasses import dataclass
import pafy
import time
import vlc
from dataclasses import dataclass
from inputimeout import inputimeout, TimeoutOccurred
import threading
import sys, select
import signal
import os
from func_timeout import func_timeout, FunctionTimedOut

def timeout(func):
    def inner_func(*nums, **kwargs):
        t = threading.Thread(target=func, args=(*nums,))
        t.start()
        t.join(timeout=22)
    return inner_func


def timed_input():
    try:
            print('You have 5 seconds to type in your stuff...')
            foo = input()
            return foo
    except:
            # timeout
            return

# set alarm



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

def toolbar_input(duration):

    nextcmd = input("")
    return nextcmd

def make_table(connection, mySQL_table_statement):
    """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
    try:
        c = connection.cursor()
        c.execute(mySQL_table_statement)
    except Error as e:
        print(e)
    c.close()

@dataclass
class Song:
    id: int
    title: str
    game: str
    category: str
    url: str

def new_insert(name, title, game, category):
    """
    inserts new file into
    :param name:
    :param title:
    :param game:
    :param category:
    :return:
    """

"""
How i made the table
sql_create_projects_table = \""" CREATE TABLE IF NOT EXISTS DMC_SONG_LIST (
                                            id integer PRIMARY KEY,
                                            title text NOT NULL,
                                            game text,
                                            category text,
                                            url text
                                        ); \"""
make_table(database, sql_create_projects_table)
"""

"""
how to delete
c = database.cursor()
c.execute(\"""DROP TABLE dmc_songs\""")
"""

"""
this is how i add songs from a playlist
# gets a pafy object (which is basically a song
    dmc1_list = []
    yt_obj = add_playlist_data('https://www.youtube.com/watch?v=RqaNQeyvBWw&list=PLA225E25C69EE9BC5')


    id_num = 1000
    #makes list of song objects
    #switch out the playlist url for different songs
    for num in range(len(yt_obj)):
        # get the title
        video_title = yt_obj[num].title[29:]
        # get the id and change it into url
        video_url = yt_obj[num].videoid
        video_url = 'https://www.youtube.com/watch?v=' + video_url
        dmc1_list += [Song(id_num, video_title, 'Devil May Cry', None, video_url)]
        id_num += 1
    #add songs to database
    for song in dmc1_list:
        add_song(connection,song)"""

def add_song(song):
    """Inserts a song into a table"""
    try:
        c = connection.cursor()
        c.execute("""INSERT INTO DMC_SONG_LIST(id, title, game, category, url) values(?, ?, ?, ?, ?)""", (song.id, song.title, song.game, song.category, song.url))
        connection.commit()

    except Error as e:
        print(e)

def add_playlist_data(playlist_url):
    playlist = pafy.get_playlist2(playlist_url)
    return playlist

def get_song_info(id_num):
    #use the id to access the song
    try:
        c = connection.cursor()
        c.execute("SELECT title, game, category, url FROM DMC_SONG_LIST WHERE id = '%s'" % id_num)
        result = c.fetchone()
        return result
    except Error as e:
        print(e)

def stream_the_song(song, playlist):
    name = song[1]
    url = song[2]
    #gets the song from youtube
    video = pafy.new(url)
    #whenever i get the video, get the best version
    best = video.getbestaudio()
    #gets the best version of the video
    music = best.url
    # starts vlc player?
    Instance = vlc.Instance()

    # if i call this it makes a media player
    player = Instance.media_player_new()
    # makes the media player
    Media = Instance.media_new(music)
    # gets the media resource locator
    Media.get_mrl()
    # puts the instance in motion?
    player.set_media(Media)

    # plays the song

    player.play()
    time.sleep(1)  # Or however long you expect it to take to open vlc
    print(name)
    print("Player Controls\n"
          "s - stop\n"
          "p - pause (use to unpause as well)\n"
          "a - add to playlist\n"
          "e - play next"
          "")
    #puts the controls in another thread and kills it when the song is over
    duration = player.get_length() / 1000
    print(duration)
    controls(player, playlist, duration)
    print(player.get_state())

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
            playlist += [select_song()]
        elif nextcmd == "e":
            # if theres one playing before it, its time to stop
            player.stop()
            stream_the_song(select_song(), playlist)








    """
    while True:
        playlist += [select_song()]
        decision = input("add more? (y/n) ").lower()
        if decision != "y" or decision != "yes":
            break
    """


def select_song():
    """
    appears whenever the user asks for a song
    :param connection: the cursor
    :return: tuple of (id, name, url)
    """
    #prompts the user to pick a song
    valid_nums = ["2","3","4","5"]
    print("Song Select\n"
          "1 - Devil May Cry\n"
          "2 - Devil May Cry 2\n"
          "3 - Devil May Cry 3\n"
          "4 - Devil May Cry 4\n"
          "5 - Devil May Cry 5\n")
    while True:
        game_selection = input("")
        if game_selection == "1":
            game_selection = "Devil May Cry"
            break
        elif game_selection in valid_nums:
            game_selection = "Devil May Cry " + game_selection
            break
        else:
            print("Dismal - That one doesn't exist")
    print("Category Select\n"
          "1 - Boss\n"
          "2 - Battle\n"
          "3 - Stage\n"
          "4 - Cutscene\n"
          "5 - Menu")
    while True:
        category_selection = input("")
        if category_selection == "1":
            category_selection = "Boss"
            break
        elif category_selection == "2":
            category_selection = "Battle"
            break
        elif category_selection == "3":
            category_selection = "Stage"
            break
        elif category_selection == "4":
            category_selection = "Cutscene"
            break
        elif category_selection == "5":
            category_selection = "Menu"
            break
        else:
            print("Dull - That one doesn't exist")
        #now show all the songs who match the game and category
    c = connection.cursor()
    c.execute("SELECT id, title, url FROM DMC_SONG_LIST WHERE game = '%s'" % game_selection)
    c.execute("SELECT id, title, url FROM DMC_SONG_LIST WHERE category = '%s'" % category_selection)
    result = c.fetchall()
    # get song id
    valid_ids = {}
    for song in result:
        print(song[:2])
        valid_ids[song[0]] = song
    while True:
        id_selection = int(input("Type the ID of the song you want "))
        if id_selection in valid_ids:
            return valid_ids[id_selection]


def test_select_song():
    game_selection = 'Devil May Cry'
    category_selection = 'Boss'
    c = connection.cursor()
    c.execute("SELECT id, title, url FROM DMC_SONG_LIST WHERE game = '%s'" % game_selection)
    c.execute("SELECT id, title, url FROM DMC_SONG_LIST WHERE category = '%s'" % category_selection)
    result = c.fetchall()
    #get song id
    valid_ids = {}
    for song in result:
        print(song[:2])
        valid_ids[song[0]] = song
    while True:
        id_selection = int(input("Type the ID of the song you want "))
        if id_selection in valid_ids:
            print(valid_ids[id_selection][2])
            return valid_ids[id_selection][2]

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
        first_song = select_song()
        playlist = [first_song]
    return playlist


def operate_playlist(playlist):
    old_playlist = playlist
    for song in playlist:
        stream_the_song(song, playlist)
    if playlist != old_playlist:
        playlist = playlist[1:]
        print("yeehaw")
        operate_playlist(playlist)


def setup_playlist():
    #generates the initial playlist which will later be used as a queue
    playlist = [1001, 1002, 1003]
    return playlist

def play_next(new_song, playlist):
    pass

connection = create_connection("dmc_songs.db")

def main_loop():
    """
    the main loop of the file
    :return:
    """

    init_play = setup_prompt()
    print(init_play)
    operate_playlist(init_play)


if __name__ == '__main__':
    main_loop()
    """
    connection = create_connection('dmc_songs.db')
    test_select_song()
    song = get_song_info(1005)
    stream_the_song(song[3])
    connection.close()
    """