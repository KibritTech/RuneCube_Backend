import requests, random
from datetime import datetime as dt
from game import Game, Player, Rune




class GameMaster:
    def __init__(self):
        # Init the list of games managed by this game master
        self.games = []

    def create_game(self, game_id, start_time, count, max_response_time, each_side_count, sides_time):
        # Create the game
        game = Game(game_id, start_time, count, max_response_time, each_side_count, sides_time)

        # Register it
        self.games.append(game)
        print(self.games, 'AFTER CREATING THE GAME')
        return game

    def get_game(self):
        # Return the game matching the given game_id
        print('inside get game func')
        for game in self.games:
            return game
    

    def delete_game(self):
        print('inside delete game method func')
        self.games.clear()
        print(self.games, ' games list after clearing')
            
    


class RuneMaster:
    def __init__(self):
        self.runes = []

    def create_rune(self,id, value, color):
        rune = Rune(id, value, color)
        if rune not in self.runes:
            self.runes.append(rune)
        return rune

    def get_rune(self, rune_id):
        rune = None
        for active_rune in self.runes:
            if active_rune.id == rune_id :
                rune = active_rune
        return rune



game_master = GameMaster()
rune_master = RuneMaster()
random_number =  random.randint(0,23)
rune_api = []
current_rune_id = [0]
countdown_time = 0




class PlayerMaster:
    def __init__(self):
        # Init the list of players managed by this player master
        self.players = []
        self.roles = []

    def create_player(self, player_username, player_role):
        # Create the player
        start_game = False
        result = []
        
        if player_role != " ":
            player = Player(player_username, player_role)
            if player_role in self.roles:
                return [start_game, f"{player_role} is already taken! Pick another one"]
            else:
                self.roles.append(player_role)
                self.players.append(player)
                if len(self.roles) == 2: 
                    players = self.players
                    api = requests.get("https://runecube.herokuapp.com/api/Runes")
                    global rune_api
                    rune_api = api.json()
                    current_rune_object = rune_api[random_number]
                    current_rune_id[0] = current_rune_object["id"]
                    story_api = requests.get("https://runecube.herokuapp.com/api/Storys")
                    story = story_api.json()
                    settings_api = requests.get("https://runecube.herokuapp.com/api/settings")
                    settings = settings_api.json()
                    global countdown_time
                    countdown_time = settings["maxResponseTime"]
                    beginning_story = story["storyStartPrompt"]
                    ending_story = story["storyEndPrompt"]
                    game_id = 123  #random id to test get_game func
                    game = game_master.get_game()
                    rune = rune_master.create_rune(id=current_rune_object["id"], value=current_rune_object["value"],color=current_rune_object["color"])
                    if game == None: 
                        game = game_master.create_game(game_id=game_id, start_time=dt.now(), count=settings["count"], 
                    max_response_time=settings["maxResponseTime"], each_side_count=1, sides_time=settings["sidesTime"])
                    game.add_player(players=players)
                    start_game = True
                    result = [current_rune_object, {"start_story": beginning_story}, {"end_story": ending_story}, settings]
        return [start_game, result]


    def get_player(self, player_username):
        # Return the player matching the given player_username
        player = None

        for active_player in self.players:
            if active_player.player_username == player_username:
                player = active_player
                break
        return player
