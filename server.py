from datetime import datetime
import requests
import socketio
from game_master import GameMaster, PlayerMaster

sio = socketio.Server(cors_allowed_origins='*')
main = socketio.WSGIApp(sio, static_files={
    '/':'./static/'
})

game_master = GameMaster()
now = datetime.now()
play_master = PlayerMaster()



rune_api = requests.get("http://vahiddev-001-site1.htempurl.com/api/Runes")
print(rune_api.json())


#sid is session id, it is assigned to client when it connects, 
#environ is a dict that has all the details from client request like if they have any errors or cookies in environ
@sio.event
def connect(sid, environ):
    print(f"client with {sid} connected")




@sio.event
def disconnect(sid):
    print(f"client with {sid} disconnected")



@sio.event
def choose_player(sid, data):
    incoming_role = list(data.items())[1][1] # data that user sends
    incoming_username = list(data.items())[0][1]
    role = play_master.create_player(player_role=incoming_role, player_username=incoming_username)
    print(role,'printing role')  #if I create game here, I can't check for the first user bcz it still returns false even after adding
    return role


@sio.event
def start_game(sid, data):
    username = data[0]
    role = data[1]
    game_id = 123
    game = game_master.get_game(game_id)
    if not game:
        game = game_master.create_game(game_id= game_id, start_time=now, correct_rune=1)

    game.add_player(username, role)

    return True

    
# @sio.event
# def check_rune(sid, data):
#     incoming_rune = data['value']
#     incoming_color = data['color']
#     print(incoming_color, incoming_rune, 'musa check')
#     global rune_count
#     cc = Rune()
#     print(cc.rune_count)
#     rune_count = cc.rune_count
#     if rune_id == cc.rune_id:
#         if rune_count > 0:
#             rune_count -= 1
#             print(rune_count, 'rune count123')
#             sio.emit('rune_check', rune_count)
#         sio.emit('rune_check', {'data': 'Rune side finished'})
#     sio.emit('rune_check',  {'data': 'Ne tot Rune'})
        

    

        


   


