import pafy
import vlc
import time
import mysql_connector

def stream_the_song(song, Instance, player, playlist=[]):
    #fix this so it can work with the prompt mode
    name = song[1]
    url = song[2]
    #gets the song from youtube
    video = pafy.new(url)
    #whenever i get the video, get the best version
    best = video.getbestaudio()
    #gets the best version of the video
    music = best.url
    # starts vlc player?
    #Instance = vlc.Instance()

    # if i call this it makes a media player
    #player = Instance.media_player_new()
    # makes the media player
    Media = Instance.media_new(music)
    # gets the media resource locator
    Media.get_mrl()
    # puts the instance in motion?
    player.set_media(Media)

    # plays the song

    player.play()
    duration = player.get_length() / 1000
    print(duration)
    #time.sleep(50)  # Or however long you expect it to take to open vlc
    print(name)
    print("Player Controls\n"
          "s - stop\n"
          "p - pause (use to unpause as well)\n"
          "a - add to playlist\n"
          "e - play next"
          "")
    #puts the controls in another thread and kills it when the song is over

    #playlist_operations.controls(player, playlist, duration)
    print(player.get_state())

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
    c = mysql_connector.connection.cursor()
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

print("vdsavrfvav")