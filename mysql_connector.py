import sqlite3
from sqlite3 import Error
from dataclasses import dataclass
import pafy
import time
import vlc
from dataclasses import dataclass
from inputimeout import inputimeout, TimeoutOccurred
import threading
import youtube_dl
import sys, select
import signal
import os
from func_timeout import func_timeout, FunctionTimedOut
import playlist_operations
import song_retrieval


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











    """
    while True:
        playlist += [select_song()]
        decision = input("add more? (y/n) ").lower()
        if decision != "y" or decision != "yes":
            break
    """




"""
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
"""


def main_loop():
    """
    the main loop of the file
    :return:
    """

    init_play = setup_prompt()
    print(init_play)
    playlist_operations.operate_playlist(init_play)

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

connection = create_connection("dmc_songs.db")

