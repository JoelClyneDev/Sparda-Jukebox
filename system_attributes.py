def terminal_controls():
    while True:
        song_list = player.get_media_player()
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
            #breaks everything into a list
            choice = choice.split()
            #its looking for a name not an id
            print(choice, "fsdaff")
            if "--id" not in choice and len(choice) != 1:
                print("yes")
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
                        #add a space to the current search query string to separate the words and record the current
                        #amout of words
                        search_query = search_query + i + " "
                        count += 1
                # removes the last space in the search query if its not empty and adds it to the parsed commands
                if search_query != "":
                    search_query = search_query[:-1]
                    new_choice += [search_query]

                """
                temp_choice = [choice[0], search_query]
                for arg in choice[count:]:
                    temp_choice += [arg]
                choice = temp_choice
                print(choice)
                """
                choice = new_choice
                #ignores space from single words commands
                if choice[1] == "":
                    choice = [choice[0]]
                print(choice)
            #print(choice)
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