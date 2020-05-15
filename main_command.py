#get the database class from true_database
from database_attributes import true_database
from media_player_commands import true_media_commands
from media_player_attributes import true_media_player
import vlc
import sys
from dataclasses import dataclass

#add all the commands
play_song = true_media_commands.play_atr
add_to_playlist = true_media_commands.add_to_playlist_atr
add_playlist = true_media_commands.add_playlist_atr
pause = true_media_commands.pause_atr
stop = true_media_commands.stop_atr
skip = true_media_commands.skip_atr
back = true_media_commands.back_atr
view_song = true_media_commands.view_song_atr
view_playlist = true_media_commands.view_playlist_atr
save_current = true_media_commands.save_atr


#add the media player
player = true_media_player.player

list_songs = true_database.list_songs

def close_program():
    sys.exit()

def help_me():
    print("Commands\n"
          "play (SONG_NAME, SONG_ID, playlist) - plays a song or playlist\n"
          "  name is default\n"
          "  use play playlist to play current playlist\n"
          "  --id enable search by id\n"
          "  --s to download song as mp3\n"
          "p - pause current song\n"
          "s - stop current song\n"
          "add - add song to playlist\n"
          "  name is default\n"
          "  --id enable search by id\n"
          "  --s to download song as mp3\n"
          "exit - close program\n"
          "list - display all song with id\n"
          "  --game GAME_NAME specify song game\n"
          "  --genre GENRE_NAME specify song genre \n"
          "skip - skip current song in playlist\n"
          "save - save currently playing song")






"""def save_current(url):
    true_media_commands.save_atr(url)
"""

#these are sorta part of the main, but dont work with other files unless theyre outside









command_dictionary = {
    "help": help_me,
    "play": play_song,
    "p": pause,
    "s": stop,
    "add": add_playlist,
    "exit": close_program,
    "skip": skip,
    "view_p": view_playlist,
    "back": back,
    "view_c": view_song,
    "list": list_songs,
    "save": save_current

}


def terminal_controls():
    """
    The loop for the command line which processes continually asks the user to input commands
    this is not blocked by the current song playing
    """
    while True:
        song_list = player.get_media_player()
        choice = input(">> ")
        #separate the elements in the response and process the first one
        #breaks the program if choice is none
        if choice is not None:
            #breaks everything into a list
            choice = choice.split()
            #its looking for a name not an id
            if "--id" not in choice and len(choice) != 1:
                search_query = ""
                count = 1
                #the first part of the list is the main command
                new_choice = [choice[0]]
                #search through everything that is not the main command

                for i in choice[1:]:
                    # if there is a --, its new term and you stop going for new stuff in the current search term
                    if i[0:2] == "--":
                        #for the first term, remove the last space in the previous search query and add it to the parsed searched parts
                        #clear the current search query
                        #then add the new -- command to the seach query
                        if count > 1:
                            search_query = search_query[:-1]
                            new_choice += [search_query]
                            search_query = ""
                            new_choice += [i]
                        else:
                            new_choice += [i]
                    else:
                        #add a space to the current search query string to separate the words and record the current
                        #amout of words
                        search_query = search_query + i + " "
                        count += 1
                # removes the last space in the search query if its not empty and adds it to the parsed commands
                if search_query != "":
                    search_query = search_query[:-1]
                    new_choice += [search_query]
                choice = new_choice
                #ignores space from single words commands
                if choice[1] == "":
                    choice = [choice[0]]
            if choice[0] not in command_dictionary:
                print("Dismal - Invalid Command")
            elif len(choice) == 1:
                #look in dictionary for correct string
                command_dictionary[choice[0]]()
            else:
                #add the extraneous parameters to a list and use those as the potential arguments
                arguments = []
                for arg in choice[2:]:
                    arguments += [arg]
                # look in dictionary for correct string
                command_dictionary[choice[0]](choice[1], arguments)

@dataclass
class SystemFunctions:
    command_dict: dict
    close: close_program
    assist: help_me

def main():

    #tell user in beginning
    print("Welcome to Sparda's Jukebox, please enter a command below")
    print("Type help for a list of commands")
    terminal_controls()

"""
The CLI would be the commands and tell stuff in the UI or the Media Player object to do things
Media Player Object
Segment the code into objects to make work and easier to read
"""

if __name__ == '__main__':
    main()