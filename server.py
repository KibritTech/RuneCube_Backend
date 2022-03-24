from datetime import datetime
import requests, json
import socketio
from game_master import GameMaster, PlayerMaster, RuneMaster
from game import Rune

sio = socketio.Server(cors_allowed_origins='*')
main = socketio.WSGIApp(sio, static_files={
    '/':'./static/'
})

game_master = GameMaster()
now = datetime.now()
play_master = PlayerMaster()
rune_master = RuneMaster()



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
    incoming_role = list(data.items())[1][1] # data that user sends
    incoming_username = list(data.items())[0][1]
    print(incoming_role, "coming role")
    print(incoming_username, 'username')
    role = play_master.create_player(player_role=incoming_role, player_username=incoming_username)
    print(role,'printing role')  #if I create game here, I can't check for the first user bcz it still returns false even after adding
    return role



@sio.event
def start_game(sid):
    players = play_master.players
    api = requests.get("https://runecube.herokuapp.com/api/Runes")
    rune_api = api.json()
    story_api = requests.get("https://runecube.herokuapp.com/api/Storys")
    story = story_api.json()
    beginning_story = story["storyStartPrompt"]
    ending_story = story["storyEndPrompt"]
    game_id = 123  #random id to test get_game func
    game = game_master.get_game(game_id=game_id)
    rune = rune_master.create_rune(id=rune_api["id"], value=rune_api["value"], 
        color=rune_api["color"], count=rune_api["count"], max_response_time=rune_api["maxResponseTime"], 
        each_side_count=rune_api["eachSideCount"], sides_time=rune_api["sidesCount"])

    if not game:
        game = game_master.create_game(game_id=game_id, start_time=now)

    game.add_player(players=players)
    json_rune = json.dumps(rune.__dict__, default=str)
    # json_game = json.dumps(game.__dict__, default=str)
    # print("",json_game)

    return [json_rune, {"start_story": beginning_story}, {"end_story": ending_story}]


    
@sio.event
def check_rune(sid, data):
    incoming_id = data["id"]
    incoming_rune = data['value']
    incoming_color = data['color']
    rune = rune_master.get_rune(rune_id=incoming_id)
    if incoming_rune == rune.value and incoming_color==rune.color:
        if rune.count > 0:
            rune.count -= 1
            sio.emit('rune_check', rune.count)
        else:
            api = requests.get("https://runecube.herokuapp.com/api/Runes")
            rune_api = api.json()
            rune = rune_master.create_rune(id=rune_api["id"], value=rune_api["value"], 
            color=rune_api["color"], count=rune_api["count"], max_response_time=rune_api["maxResponseTime"], 
            each_side_count=rune_api["eachSideCount"], sides_time=rune_api["sidesCount"])
            return rune
            # sio.emit('rune_check', {'data': "Rune's side has been completed"}) #create a new rune object here and send it
    else:
        return False

        

    

        


   


