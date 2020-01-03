"""
tools for editing the database
Run with db_file parameter
"""

import sqlite3
from sqlite3 import Error
import pafy
import sys
import os
import subprocess
from dataclasses import dataclass

@dataclass
class Song:
    id: int
    title: str
    game: str
    category: str
    url: str


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

def remove_table():
    c.execute("""DROP TABLE dmc_songs""")

def create_table(table_name):
    """
    makes a table
    """
    c.execute("""CREATE TABLE IF NOT EXISTS '%s' (
                  id integer PRIMARY KEY,
                  title text NOT NULL,
                  game text,
                  category text,
                  url text);""" % table_name)

def add_playlist_data(playlist_url):
    playlist = pafy.get_playlist2(playlist_url)
    return playlist

def add_song(song):
    """Inserts a song into a table"""
    try:
        c = connection.cursor()
        c.execute("""INSERT INTO DMC_SONG_LIST(id, title, game, category, url) values(?, ?, ?, ?, ?)""", (song.id, song.title, song.game, song.category, song.url))
        connection.commit()

    except Error as e:
        print(e)

def retrieve_values(playlist):
    """
    adds all the songs from a youtube playlist to the database
    :return:
    """
    # gets a pafy object (which is basically a song
    song_list = []
    yt_obj = add_playlist_data(playlist)
    #set the starting id number
    id_num = 2000
    #makes list of song objects
    #switch out the playlist url for different songs
    for num in range(len(yt_obj)):
        # get the title
        video_title = yt_obj[num].title[29:]
        # get the id and change it into url
        video_url = yt_obj[num].videoid
        video_url = 'https://www.youtube.com/watch?v=' + video_url
        song_list += [Song(id_num, video_title, 'Devil May Cry 2', None, video_url)]
        id_num += 1
    #add songs to database
    for song in song_list:
        add_song(song)


if len(sys.argv) == 3 and sys.argv[2] == "-new":
    #create and empty db file
    #get the current directory
    cwd = os.getcwd()
    #change the directory to the current one
    subprocess.run(["cd", "/d", cwd], shell=True)
    #make the new table
    subprocess.run(["sqlite3", sys.argv[1] + ".db", "\"\""], shell=True)
else:
    db_file = sys.argv[1]
    connection = create_connection(db_file)
    c = connection.cursor()
    #create_table("test table")
    #retrieve_values("https://www.youtube.com/watch?v=YiT619aLWTI&list=PL71DA485A8238C2E9")