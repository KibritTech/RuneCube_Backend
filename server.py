from datetime import datetime as dt
import random, socketio, requests
import time
from game_master import PlayerMaster, game_master, rune_master, current_rune_id
import game_master as gs #import it like this so can get rune_api
from threading import Timer
from reset_timer import TimerReset

sio = socketio.Server(cors_allowed_origins='*')
main = socketio.WSGIApp(sio, static_files={
    '/':'./static/'
})


play_master = PlayerMaster()
leaderboard_url = "https://runecube.herokuapp.com/api/leaderboards"


online_users = []
game_start_state = []

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
    print("online users in DISCONNECT ", online_users)
    print("GAME START STATE IN DISCONNECT", game_start_state)
    for user in online_users:
        if user["sid"] == sid:
            user["online"] = False
            print('Made this user offline', user )
            if True in game_start_state:
                global timer_object
                timer_object = func_thread()
                timer_object.start() #call func here to start countdown, if time is zero then delete the game
                print('STARTED TIMER OBJECT IN DISCONNECT')
                print("User ", user, ' is disconnected')
            else:
                online_users.clear()
                play_master.delete_players()
                sio.emit('disconnect_before_start')



@sio.event
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
                user["sid"] = new_sid
                print('After changing sid to new sid, users are', online_users)
                user["online"] = True
                if True in game_start_state:
                    print(timer_object, 'GLOBAL timer_object STARTED')
                    timer_object.cancel()


@sio.on('choose_player')
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



entered_users_count = 0
@sio.event
def read_story(sid):
    chosen_players = play_master.players
    global entered_users_count
    entered_users_count += 1
    if len(chosen_players) == 2 and entered_users_count == 2:
        print('BOTH USERS READ THE STORY')
        rune_object = game_master.create_game()
        sio.emit('read_story', rune_object)



start_game_count = 0
@sio.event
def game_started(sid):
    print('inside count function !')
    global start_game_count
    start_game_count += 1
    print(start_game_count, "start game count in game started event check")
    if start_game_count == 2:
        game_start_state.append(True)
        sio.emit('game_started', True)
        call_rune_time()
        call_side_time()
        print(game_start_state, 'Game start state in game start after appending start game count')
        start_game_count = 0
    else:
        sio.emit('game_started', False)



def call_rune_time():
    global rune_timer_object
    rune_timer_object = countdown_max_response_time()
    if rune_timer_object != None:
        rune_timer_object.start()
    else:
        print('rune timer object was none')


def call_side_time():
    global side_timer_object
    side_timer_object = countdown_side_time()
    if side_timer_object != None:
        side_timer_object.start()
    else:
        print('rune timer object was none')



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
            rune_timer_object.cancel()
            call_rune_time() #starts a new rune timer thread
            print(game.count, 'before minus')
            game.count -= 1
            print(game.count, 'after minus')
            new_rune_object = get_new_rune()
            if game.count == 0:   #check game count again, because it decreases before this if condition and may be it is zero now
                game.count = 3
                print('...........................correct rune count finished for one side...........................')
                new_rune_object = get_new_rune()
                side_timer_object.cancel()
                call_side_time()
                sio.emit('change_side', [game.count, new_rune_object])
                global found_side_object 
                found_side_object.append("new side")
                sio.emit('open_map', len(found_side_object))
                print("OPENED MAP COUNT  ", len(found_side_object))
                if game.each_side_count == len(found_side_object):
                    found_side_object = []
                    api_return = send_data_api(is_finished=True)
                    if api_return:
                        end_game()
                        sio.emit('finish_message', "finished")
                        time.sleep(2) #wait for user to see the map 
                        sio.emit('finish_game')

            else:
                sio.emit('update_rune', [game.count, new_rune_object, "right"]) #right so front makes tick sign
    else:
        rune_timer_object.cancel()
        call_rune_time()
        print("they are not same")
        new_rune_object = get_new_rune()
        sio.emit('change_side', [game.count, new_rune_object, "wrong"]) #right so front makes x sign



def get_new_rune():
    random_number =  random.randint(0,gs.length_rune_api-1)
    new_rune_object = gs.rune_api[random_number]
    current_rune_id[0] = new_rune_object["id"]
    rune = rune_master.create_rune(id=new_rune_object["id"], value=new_rune_object["value"], color=new_rune_object["color"])
    print('SENT RUNE ||||||||||||||||||||||||', new_rune_object)
    return new_rune_object



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
        show_disconnection_message = True
        sio.emit('finish_game', show_disconnection_message)   


threads = []
def func_thread():    
    timing = Timer(12.0, timeout)
    threads.append(timing)
    print(threads, "ALL THREADS AFTER DISCONNECT")
    return timing


def rune_time_finish():
    print('  Rune time finished I am executingggg')
    game = game_master.get_game()
    if game != None:
        new_rune_object = get_new_rune()
        sio.emit('rune_time_finished', [game.count, new_rune_object])


def side_time_finish():
    print('  SIDE time finished I am executingggg')
    game = game_master.get_game()
    if game != None:
        new_rune_object = get_new_rune()
        sio.emit('side_time_finished', [game.count, new_rune_object])


def countdown_max_response_time():    
    game = game_master.get_game()
    if game != None:
        timing = TimerReset(game.max_response_time, rune_time_finish)
        threads.append(timing)
        print(timing, 'timer in countdown response timer object')
        return timing


def countdown_side_time():    
    game = game_master.get_game()
    if game != None:
        timing = TimerReset(game.sides_time, side_time_finish)
        threads.append(timing)
        print(timing, 'timer in countdown side timer object')
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
        subtract_time = game.finish_time - game.start_time
        spent_time = str(subtract_time).split(".")[0]                    
        payload = {'username1': username1, 'role1': role1, 'username2': username2, 'spent_time': spent_time, 
        'is_finished': is_finished}
        posted_game_data = requests.post(leaderboard_url, json=payload)
        if posted_game_data:
            end_game()
            return True
        else:
            return False
    

def end_game():
    game = game_master.get_game()
    if game != None:
        global found_side_object
        found_side_object = []
        global online_users
        online_users = []
        global game_start_state
        game_start_state = []
        rune_timer_object.cancel()
        side_timer_object.cancel() 
        game.remove_players()
        game_master.delete_game()
        print(play_master.players, 'delete players object before clearing it')
        play_master.delete_players()
        print(play_master.players, 'delete players object after')
        print('GAME FINISHEDDDDD')

