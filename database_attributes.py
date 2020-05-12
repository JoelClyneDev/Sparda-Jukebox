import sqlite3
from sqlite3 import Error
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from dataclasses import  dataclass

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

def display_songs(arguments=None, tech_arguements= None):
    """
    shows all of the songs based on game, type, or both
    tech arguments is for cheating choice[1] into arguments
    :return:
    """
    print(tech_arguements)
    print(arguments)
    if tech_arguements is not None:
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
        print(value[0], "-", value[1])

@dataclass
class Database:
    connect: sqlite3.Connection
    name_search: fuzzy_search
    id_search: song_by_id
    list_songs: display_songs


#create the connection to the database

connection = create_connection('dmc_songs.db')
true_database = Database(connection, fuzzy_search, song_by_id, display_songs)