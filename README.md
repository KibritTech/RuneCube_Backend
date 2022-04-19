# The very first event "connect"

Once users enter the website provided by the link, an event "connect" occurs:

```
def connect(sid, environ):
    print(f"client with {sid} connected")
    game = game_master.get_game()
    print(game, ' GAME STATUS IN CONNECT')
    if game != None:
        print('there is ongoing game')
        sio.emit('ongoing_game', True)
    else:
        sio.emit('ongoing_game', False)
```

This event takes 2 parameters: sid is the socket id that is assigned for each device and optional environ is a dictionary that has all the details from client request like if they have any errors or cookies in environ. -
This event does the following:

1. it checks whether there is an ongoing game or not.
   1. If there is an existing game then it emits an event "ongoing_game" with the value true
   2. Otherwise it emits the same event with the false value.

# "choose_player" Event

Once one of the users chooses a role "choose_player" event is fired:

```
def choose_player(sid, data):
    incoming_role = data["role"] #data that user sends
    incoming_username = data["username"]
    print(data, 'choose player data')
    if incoming_username != " " and incoming_role != " ":
        user_data = {"username": incoming_username, "role": incoming_role, "sid": data["sid"], "online": True}
        online_users.append(user_data)
        game_ready_obj = play_master.create_player(player_role=incoming_role, player_username=incoming_username)
        print(game_ready_obj,'printing choose player return')
        sio.emit("choose_player", game_ready_obj)
    else:
        print(f"Either incoming_role: {incoming_role} or incoming_username: {incoming_username} is empty")
```

This event takes 2 parameters: sid and data contains information about the connected player (username, role,id)
This event does the following:

1.  First a simple validation happens which checks the incoming username and his role so that these values are not empty.

    1.  if the values are empty, then this event doesn't emit anything.
    2.  If values are not empty, game_ready_obj is created with the received values and then an event "choose_player" is emitted with the value being created game_ready_obj object.
        This game_ready_obj is created by create_player method of Play_master type's instance. This method returns game_ready_obj with the following fields: ready_to_start and story. - - ready_to_start as the name implies, it indicates whether a game can be started or not. - story is a dictionary that has the beginning and the end story.

            1) If all of the roles are chosen then create_player method returns the object with the following values: -
            ready_to_start:false,
            story:{}
            2) Otherwise if there is an available role then it checks whether it is the last role to be selected or not.
                1) If not, then it returns the game_ready_obj with the values: -
                ready_to_start:false,
                story:{}
                And this means that the game cannot be started yet.
                2) If it is the last role to be selected, then it returns the object with the following values:
                ready_to_start:true,
                story:{start_story,end_story}

Eventually this event emits "choose_player" event with value being the game_ready_obj.

# "start_game" Event -

When one of the users clicks ready button after choosing a role this event is fired:

```
def start_game(sid):
    chosen_players = play_master.players
    print(chosen_players, "GET PLAYERS IN START GAME")
    if len(chosen_players) == 2:
        print('length is 2 ')
        starting_game = game_master.create_game()
        sio.emit('start_game', starting_game)
```

This event takes 1 parameter: sid.
This event does the following:

1. It checks whether there are 2 chosen players or
   1. if the number of players is not 2 then it doesn't emit anything.
   2. If there is then it emits "start_game" event with value being starting_game object.
      starting_game object is created by create_game method of game_master type. This object has the following fields: current_rune_object, settings.
      current_rune_object is the rune object that has to be found within a specific amount of time. This specific time is kept in settings object as maxResponseTime. Besides this maxResponseTime field, this settings object contains the following fields: count, eachSideCount, sidesTime. - count is the number of runes that have to be found to complete the side. - eachSideCount is the total number of sides that have to be completed. - sidesTime is the total amount of time to complete one entire side

# " check_rune" Event

This event is fired when the explorer chooses a rune.

```
def check_rune(sid, data):
    print(data, " CHECK RUNE MUSA DATA")
    incoming_rune = data['value']
    incoming_color = data['color']
    rune = rune_master.get_rune(rune_id=current_rune_id[0])
    game = game_master.get_game()
    new_rune_object = []
    print(rune.value, rune.color, "rune in me ...............")
    if incoming_rune == rune.value and incoming_color==rune.color:
        if game.count > 0:
            print(game.count, 'before minus')
            game.count -= 1
            print(game.count, 'after minus')
            new_rune_object = get_new_rune()
            if game.count == 0:   #check game count again, because it decreases before this if condition and may be it is zero now
                game.count = 3
                print('...........................correct rune count finished for one side...........................')
                new_rune_object = get_new_rune()
                sio.emit('change_side', [game.count, new_rune_object])
                global found_side_object
                found_side_object.append("new side")
                print(found_side_object, 'found side object after appending')
                sio.emit('open_map', len(found_side_object))
                print("OPENED MAP COUNT  ", len(found_side_object))
                if game.each_side_count == len(found_side_object):
                    found_side_object = []
                    api_return = send_data_api(is_finished=True)
                    if api_return:
                        global online_users
                        online_users = []
                        global game_start_state
                        game_start_state = []
                        sio.emit('finish_message', "finished")
                        time.sleep(2) #wait for user to see the map
                        sio.emit('finish_game')
            else:
                sio.emit('update_rune', [game.count, new_rune_object, "right"])
    else:
        print("they are not same")
        new_rune_object = get_new_rune()
        sio.emit('change_side', [game.count, new_rune_object, "wrong"])
```

This event takes 2 parameters: sid and data about the rune which explorer selected (value and color of the rune). This event does the following:

1. It checks whether the found rune is the correct one.

   1. If the explorer clicked the wrong the rune then this event emits "change_side" event with the following values:
      - new_rune_object
      - "wrong"
        new_rune_object is always a new random rune object and the string "wrong" is for the frontend. The frontend uses this string to display the right feedback for the explorer. In this case, the string is "wrong" which means that the explorer will see some X figure on his screen which indicates that the explorer found the wrong rune.
   2. If the explorer found the right rune, then it checks whether all the runes for the side are found or not.

      1. If there are runes to be found then this event emits "update_rune" event with the following values:

         - game.count (the number of runes that have to be found to complete the side)
         - new_rune_object (the new random rune object with the fields "value" and "color")
         - "right" (string indicates that the explorer has clicked the right rune and frontend can display the right feedback for the explorer which is a tick symbol in this case.)

      2. if all the runes are found, then the side is completed. It first emits "change_side" with values: game.count,new_rune_object. Then it emits "open_map" event with the value being the number of found sides.
         game.count field in the emitted "change_side" event is reset to its initial value (from the settings).
         After this it checks whether all sides are completed or not. 1) If not, it doesn't emit anything. 2) if all the sides are completed then first "finish_message" event is emitted with the value "finished" after which "finish_game" event is emitted with no value.

# "disconnect" Event

As the name implies, this event is fired when a user disconnects.

```
def disconnect(sid):
    print(f"client with {sid} disconnected")
    print("online users in DISCONNECT ", online_users)
    print("GAME START STATE IN DISCONNECT", game_start_state)
    for user in online_users:
        if user["sid"] == sid:
            user["online"] = False
            print('STARTING TIMER OBJECT IN DISCONNECT')
            if True in game_start_state:
                print("inside Trueeee")
                global timer_object
                timer_object = func_thread()
                timer_object.start() #call func here to start countdown, if time is zero then delete the game
                print("User ", user, ' is disconnected')
```

This event takes one parameter: sid. This socket id is used to find the user from the online_users list to make the user offline (by setting his online field to false).
This event first checks if the state of the game is true which means the game is ongoing.

1. If yes, then it sets a timer for the game to terminate if the user doesn't return back.
2. If no, then it doesn't do anything

# "user_reconnected" Event

As the name says, the event is fired when a user reconnects.

```
def user_reconnected(sid, data):
    print('PRINTING INCOMING DATA FROM CLIENT IN USER RECONNECT', data)
    print('PRINTING ONLINE USERS IN USER RECONNECT BEFORE CHANGING', online_users)
    username = data["username"]
    role = data["role"]
    if role != " ":
        for user in online_users:
            active_username = user["username"]
            active_role = user["role"]
            if (username == active_username and role == active_role)  and user["online"] == False:
                new_sid = data["sid"]
                print('After changing sid to new sid users', online_users)
                user["sid"] = new_sid
                user["online"] = True
                if True in game_start_state:
                    print(timer_object, 'GLOBAL timer_object STARTED')
                    timer_object.cancel()
```

This event takes 2 parameters: sid and data about the user(username,role).
This event does the following:

1. It checks whether the there is a user in the online_users who is offline (which means online field of the user is set to false) and whose username and role are equal to the username and role of the user who wants to reconnect.
   1. If the username indeed exists in the online_users list and he is offline, then an id is set for the user and his online boolean field is set to true.
      After this, it checks the game state whether it is ongoing or not
      1. If yes, then the timer is terminated.
      2. If not, then it doesn't do anything.
   2. If the username doesn't exist in the online_users list or if his is actually online then this event doesn't emit anything.
