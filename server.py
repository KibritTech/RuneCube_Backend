from datetime import datetime
from game import Player, Rune, Game
import socketio
from game_master import GameMaster, PlayerMaster

sio = socketio.Server(cors_allowed_origins='*')
main = socketio.WSGIApp(sio, static_files={
    '/':'./static/'
})

game_master = GameMaster()
now = datetime.now()
play_master = PlayerMaster()
@sio.event
def connect(sid, environ):
    print(f"client with {sid} connected")

# @sio.event
# def user_joined(sid, data):
#     print(data,'qwertyuiohytfrdes')
    # player1 = Player(player_sid=sid, player_username=data, player_role=)
    # print(player1)



@sio.event
def disconnect(sid):
    print(f"client with {sid} disconnected")


#sid is session id, it is assigned to client when it connects, 
#environ is a dict that has all the details from client request like if they have any errors or cookies in environ
@sio.event
def choose_player(sid, data):
    game_id = 123
    incoming_role = list(data.items())[1][1] # data user sends
    role = play_master.create_get_role(player_role=incoming_role)
    if role:
        incoming_username = list(data.items())[0][1]
        

    return role
    # game = game_master.get_game(game_id)

    # # If the game does not exist yet, create it
    # if not game:
    #     game = game_master.create_game(game_id, start_time=now)

    # # Add the player to the game
    # game.add_player(sid, player_name)
    # players = []
    # ready = False
    # print(players, 'players')
    # print(data,'data')
    # if data != "":
    #     if data not in players:
    #         players.append(data)
    #         print(players, 'list')
    #     else:
    #         sio.emit('choose_player', {'data': 'role is already taken'})
    #     print(players, 'listafter')
    # if len(data) == 2:
    #     ready = True
    #     return ready

    # if not data == '':
    #     if data == 'explorer':
    #         if explorer_count == 0:  
    #             explorer_count += 1
    #             print(explorer_count, 'explorer count +1 ')
    #         else:
    #             sio.emit('choose_player', {'data': 'explorer role is taken'})

    #     elif data == 'solver':
    #         if solver_count == 0:
    #             solver_count += 1
    #             print(solver_count, 'solver count +1 ')
    #         else: 
    #             sio.emit('choose_player', {'data': 'solver role is  taken'})
                
    # if explorer_count == 1 and solver_count == 1:
    #     ready = True
    #     print(ready, 'qwertyuiopoiutedsfiopfdsfgh')
    # return ready



@sio.event
def started_game(sid):
    return Rune


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
        

    

        


   


