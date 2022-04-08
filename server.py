from datetime import datetime as dt
import random, socketio, requests
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
start_game_count = 0

#sid is session id, it is assigned to client when it connects, 
#environ is a dict that has all the details from client request like if they have any errors or cookies in environ
@sio.event
def connect(sid, environ):
    print(f"client with {sid} connected")
    game = game_master.get_game()
    print(game, ' GAME STATUS IN CONNECT')
    if game != None: 
        print('there is ongoing game')
        sio.emit('ongoing_game', True)
    else:
        sio.emit('ongoing_game', False)



@sio.event
def disconnect(sid):
    print(f"client with {sid} disconnected")
    print(start_game_count, 'start game count in disconnect event')
    if start_game_count == 2:
        for user in online_users:
            if user["sid"] == sid:
                user["online"] = False
                print('timing is not alive')
                global timer_object
                timer_object = func_thread()
                timer_object.start() #call func here to start countdown, if time is zero then delete the game
                print("User ", user, ' is disconnected')


@sio.event
def user_reconnected(sid, data):
    print('PRINTING INCOMING DATA FROM CLIENT IN USER RECONNECT', data)
    username = data["username"]
    role = data["role"]
    if role != " ":
        for user in online_users:
            active_username = user["username"]
            active_role = user["role"]
            if (username == active_username and role == active_role)  and user["online"] == False:
                print(timer_object, 'GLOBAL timer_object VARIABLE')
                timer_object.cancel()
                us_sid = data["sid"]
                user["sid"] = us_sid
                user["online"] = True


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

found_side_object = []

@sio.event
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
                        sio.emit('finish_message', "finished")
                        time.sleep(3) #wait for user to see the map 
                        sio.emit('finish_game')
            else:
                sio.emit('update_rune', [game.count, new_rune_object, "right"])
    else:
        print("they are not same")
        new_rune_object = get_new_rune()
        sio.emit('change_side', [game.count, new_rune_object, "wrong"]) 
        

    
def get_new_rune():
    random_number =  random.randint(0,15)
    new_rune_object = gs.rune_api[random_number]
    current_rune_id[0] = new_rune_object["id"]
    rune = rune_master.create_rune(id=new_rune_object["id"], value=new_rune_object["value"], color=new_rune_object["color"])
    print(new_rune_object, '||||||||||||||||||||||||')
    return new_rune_object


@sio.event
def side_time(sid):
    print('  SIDE time finished they are calling meeee')
    game = game_master.get_game()
    if game != None:
        new_rune_object = get_new_rune()
        return  [game.count, new_rune_object]


@sio.event
def rune_time(sid):
    print('RUNE time finished they are calling meeee')
    game = game_master.get_game()
    if game != None:
        new_rune_object = get_new_rune()
        return  [game.count, new_rune_object]



def timeout():
    api_return = send_data_api(is_finished=False)
    if api_return:
        global found_side_object
        found_side_object = []
        # global start_game_count
        # start_game_count = 0
        sio.emit('finish_game', True)
        print("Game Finished")




threads = []

def func_thread():    
    timing = Timer(13.0, timeout)
    threads.append(timing)
    print(threads, "ALL THREADS")
    return timing



def send_data_api(is_finished):
    print(is_finished, "is finished value")
    game = game_master.get_game()
    if game != None:
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
        payload = {'username1': username1, 'role1': role1, 'username2': username2, 'spent_time': spent_time, 
        'is_finished': is_finished}
        posted_game_data = requests.post(leaderboard_url, json=payload)
        if posted_game_data:
            game.remove_players()
            game_master.delete_game()
            print(play_master.players, 'delete players object ')
            play_master.delete_players()
            print(play_master.players, 'delete players object after')
            return True
        else:
            return False
    


@sio.event
def game_started(sid):
    print('inside count function has started')
    global start_game_count
    start_game_count += 1
    print('start_game_count after incresing', start_game_count)
    if start_game_count == 2:
        sio.emit('game_started', True)
    else:
        sio.emit('game_started', False)