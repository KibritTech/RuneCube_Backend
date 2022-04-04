from datetime import datetime as dt
import random, socketio, json, requests
import time
from game_master import PlayerMaster, game_master, rune_master, current_rune_id
import game_master as gs #import it like this so can get rune_api
from threading import Timer

sio = socketio.Server(cors_allowed_origins='*')
main = socketio.WSGIApp(sio, static_files={
    '/':'./static/'
})


play_master = PlayerMaster()
leaderboard_url = "https://runecube.herokuapp.com/api/leaderboards"


online_users = []

#sid is session id, it is assigned to client when it connects, 
#environ is a dict that has all the details from client request like if they have any errors or cookies in environ
@sio.event
def connect(sid, environ):
    print(f"client with {sid} connected")
    game = game_master.get_game()
    print(game, ' GAME IN CONNECT')
    if game != None: 
        print('there is ongoing game')
        sio.emit('ongoing_game', True)
    else:
        sio.emit('ongoing_game', False)



@sio.event
def disconnect(sid):
    print(f"client with {sid} disconnected")
    for user in online_users:
        if user["sid"] == sid:
            user["online"] = False
            timing.start()
            #call func here to start countdown, if time is zero then delete the game
            print("User ", user, ' is disconnected')

            

@sio.event
def user_reconnected(sid, data):
    username = data["username"]
    role = data["role"]
    if role != " ":
        for user in online_users:
            active_username = user["username"]
            active_role = user["role"]
            if username == active_username and role == active_role :
                if user["online"] == False :
                    timing.cancel()
                    us_sid = data["sid"]
                    user["sid"] = us_sid
                    user["online"] = True
                    # sio.emit("user_reconnected", True)


@sio.event
def choose_player(sid, data):
    incoming_role = data["role"] #data that user sends
    incoming_username = data["username"]
    print(data, 'choose player data')
    if incoming_username != " " and incoming_role != " ": 
        user_data = {"username": incoming_username, "role": incoming_role, "sid": data["sid"], "online": True}
        online_users.append(user_data)
    print(incoming_role, "choose player coming role")
    print(incoming_username, 'choose player incoming username')
    role = play_master.create_player( player_role=incoming_role, player_username=incoming_username)
    print(role,'printing choose player return') #if I create game here, I can't check for the first user bcz it still returns false even after adding
    sio.emit("choose_player", role) 



open_map_side = 0
  
@sio.event
def check_rune(sid, data):
    incoming_rune = data['value']    
    incoming_color = data['color']
    rune = rune_master.get_rune(rune_id=current_rune_id[0])
    game = game_master.get_game()
    new_rune_object = []

    if incoming_rune == rune.value and incoming_color==rune.color:
        if game.count > 0: 
            print(game.count, 'before minus')
            game.count -= 1
            print(game.count, 'after minus')
            new_rune_object = get_new_rune()
            if game.count == 0:   #check game count again, because it decreases before this if condition and may be it is zero now
                game.count = 5
                print('...........................   correct rune finished...........................')
                game.count = 5
                new_rune_object = get_new_rune()
                sio.emit('change_side', [game.count, new_rune_object])
                game.each_side_count -= 1
                global open_map_side
                open_map_side += 1
                sio.emit('open_map', open_map_side)
                if game.each_side_count == 0:
                    print('...........................         GAME COUNT .........', game.each_side_count)
                    game.finish_time = dt.now()
                    players = play_master.players
                    first_user = players[0]
                    second_user = players[1]
                    username1 = first_user.player_username
                    username2 = second_user.player_username
                    role1 = first_user.player_role
                    role2 = second_user.player_role
                    subtract_time = game.finish_time - game.start_time
                    spent_time = str(subtract_time).split(".")[0]                    
                    spent_time_json = json.dumps(spent_time,default=str)
                    username1_json = json.dumps(username1, default=str)
                    username2_json = json.dumps(username2, default=str)
                    role1_json = json.dumps(role1, default=str)
                    role2_json = json.dumps(role2, default=str)
                    payload = {'username1': username1, 'role1': role1, 'username2': username2, 'spent_time': spent_time }
                    posted_game_data = requests.post(leaderboard_url, json=payload)
                    print(posted_game_data.json(), 'posted game data')
                    time.sleep(4)
                    sio.emit('finish_game', [username1_json, role1_json, username2_json, role2_json, spent_time_json])
            else:
                sio.emit('update_rune', [game.count, new_rune_object])
    else:
        print("they are not same")
        new_rune_object = get_new_rune()
        game.count = 5
        sio.emit('change_side', [game.count, new_rune_object]) 
        
    
def get_new_rune():
    random_number =  random.randint(0,23)
    new_rune_object = gs.rune_api[1]
    current_rune_id[0] = new_rune_object["id"]
    rune = rune_master.create_rune(id=new_rune_object["id"], value=new_rune_object["value"], color=new_rune_object["color"])
    print(new_rune_object, '||||||||||||||||||||||||')
    return new_rune_object


@sio.event
def side_time(sid):
    print('  SIDE time finished they are calling meeee')
    game = game_master.get_game()
    game.count = 5
    new_rune_object = get_new_rune()
    return  [game.count, new_rune_object]


@sio.event
def rune_time(sid):
    print(' RUNE time finished they are calling meeee')
    game = game_master.get_game()
    new_rune_object = get_new_rune()
    return  [game.count, new_rune_object]



# def countdown():
#     global my_timer
#     my_timer = 10
#     while my_timer > 0:
#         time.sleep(2)
#         print('hereeee')
#         my_timer -= 1


# countdown_thread = threading.Thread(target=countdown)
# countdown_thread.start()


def timeout():
    sio.emit('finish_game', True)
    print("Game Finished")


timing = Timer(30.0, timeout)

# # wait for time completion
# timing.join()
    

   


