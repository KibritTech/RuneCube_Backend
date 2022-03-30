import random
import socketio
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
        if game.count > 1: 
            game.count -= 1
            new_rune_object = get_new_rune()
            sio.emit('rune_check', [game.count, new_rune_object])
        else:
            game.count = 5
            new_rune_object = get_new_rune()
            sio.emit('rune_check', [game.count, new_rune_object]) 
    else:
        print("they are not same")
        new_rune_object = get_new_rune()
        game.count = 5
        sio.emit('rune_check', [game.count, new_rune_object, {'data': "Runes are not same"}]) 
        

    
def get_new_rune():
    random_number =  random.randint(0,23)
    new_rune_object = gs.rune_api[random_number]
    current_rune_id[0] = new_rune_object["id"]
    rune = rune_master.create_rune(id=new_rune_object["id"], value=new_rune_object["value"], color=new_rune_object["color"])
    return new_rune_object

        


   


