# Sparda's-Jukebox

A command-line audio player for songs from Devil May Cry. Parses user input to do media player commands (play, pause, add to playlist etc). Song information is stored in a database file which contains YouTube links to each song and they are accessed through SQLite. 

## Getting Started

These instructions will help you download, install, and run Sparda's Jukebox to your system.

### Prerequisites

Python 3.8XX

### Installing

1. Clone the repository

2. In the command line, run 
```
pip install -r PATH_TO_REPOSITORY/requirements.txt
```
3. Run main_command.py in a python shell

4. Start inputting commands

## Usage

These are all the valid commands and arguments that the user can type into the terminal

### Variable Arguments

SONG_TITLE - The title of a song found the database
(Inputting the the subtitle of a song is not necessary, the fuzzy search will find the correct song eg. Ultra Violet instead of Ultra Violet Nelo Angelo Battle]

SONG_ID - The four digit id number of a song, used with --id to find a song by its ID number eg. 1015

GAME_NAME - The name of the game the song is from. In the Devil May Cry song database, this can be Devil May Cry (() - 5)

GENRE_NAME - The genre of the song where its placed in the game
Can be: Battle, Boss, Menu, Cutscene

### Command Arguments

#### play

Plays the song of the specified name, ID, or beginning of the playlist. (The song is added to the end of the playlist)
Use --id to denote using a song id
Use --s to save the file to the current directory as an mp3

Usage 
play SONG_NAME
play SONG_ID --id
play playlist
play ... (-s)

#### add 

Adds a song of the specified name or ID to the end of the playlist
Use --id to denote using a song id
Use --s to save the file to the current directory as an mp3

Usage 
add SONG_NAME
add SONG_ID --id
add ... (-s)

#### list

Lists all of the available songs in the database with their game and ID number. Songs can be filtered by their game, genre, or both
Use --game to specify game filter
Use --genre to specify genre filter

Usage 
list --game GAME_NAME
list --genre GENRE_NAME
list --game GAME_NAME --genre GENRE_NAME (or vice versa)

#### playback commands

To use, just type the command's letter

p - pause the current song
s - stops the current song 
skip - skips the current song, and plays the next one in the playlist
save - saves the current song as an mp3 file
exit - closes the program

## Built with 

* Python - processes user input through the terminal and calls VLC functions 
* VLC - handles audio playback and the playlist
* SQLite - stores all songs in the database and queries based on user input
