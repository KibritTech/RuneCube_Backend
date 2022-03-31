from datetime import datetime
import random, socketio, json
from game_master import PlayerMaster, game_master, rune_master, current_rune_id
import game_master as gs #import it like this so can get rune_api


sio = socketio.Server(cors_allowed_origins='*')
main = socketio.WSGIApp(sio, static_files={
    '/':'./static/'
})


play_master = PlayerMaster()



#sid is session id, it is assigned to client when it connects, 
#environ is a dict that has all the details from client request like if they have any errors or cookies in environ
@sio.event
def connect(sid, environ):
    print(f"client with {sid} connected")




@sio.event
def disconnect(sid):
    print(f"client with {sid} disconnected")
    # for game in game_master.game:
    #     game.remove_player(player_username=player_username)



@sio.event
def choose_player(sid, data):
    incoming_role = data["role"] #data that user sends
    incoming_username = data["username"]
    print(incoming_role, "coming role")
    print(incoming_username, 'username')
    role = play_master.create_player(player_role=incoming_role, player_username=incoming_username)
    print(role,'printing choose player return') #if I create game here, I can't check for the first user bcz it still returns false even after adding
    return role


  
@sio.event
def check_rune(sid, data):
    incoming_rune = data['value']    
    incoming_color = data['color']
    rune = rune_master.get_rune(rune_id=current_rune_id[0])
    game = game_master.get_game()
    new_rune_object = []

    if incoming_rune == rune.value and incoming_color==rune.color:
        if game.count > 0: 
            game.count -= 1
            new_rune_object = get_new_rune()
            if game.count == 0:   #check game count again, because it decreases before this if and may be it is zero now
                # game.count = 5
                test = 5
                sio.emit('change_side', [test, new_rune_object])
            sio.emit('update_rune', [game.count, new_rune_object])
        else: 
            print('...........................correct rune finished...........................')
            game.count = 5
            new_rune_object = get_new_rune()
            sio.emit('change_side', [game.count, new_rune_object])
            game.each_side_count -= 1
            print('',game.each_side_count)
            if game.each_side_count == 0:
                print('...........................GAME COUNT .........', game.each_side_count)
                game.finish_time = datetime.now()
                players = play_master.players
                first_user = players[0]
                second_user = players[1]
                username1 = first_user.player_username
                username2 = second_user.player_username
                role1 = first_user.player_role
                role2 = second_user.player_role
                spent_time = game.finish_time - game.start_time
                spent_time_json = json.dumps(spent_time,default=str)
                username1_json = json.dumps(username1, default=str)
                username2_json = json.dumps(username2, default=str)
                role1_json = json.dumps(role1, default=str)
                role2_json = json.dumps(role2, default=str)
                sio.emit('finish_game', [username1_json, role1_json, username2_json, role2_json, spent_time_json])
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
    

   


