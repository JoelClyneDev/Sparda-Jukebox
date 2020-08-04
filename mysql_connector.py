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
make_table(database, sql_create_projects_table)
how to delete
c = database.cursor()
c.execute(\"""DROP TABLE dmc_songs\""")
"""



def add_song(song):
    """Inserts a song into a table"""
    try:
        c = connection.cursor()
        c.execute("""INSERT INTO DMC_SONG_LIST(id, title, game, category, url) values(?, ?, ?, ?, ?)""", (song.id, song.title, song.game, song.category, song.url))
        connection.commit()

    except Error as e:
        print(e)



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

