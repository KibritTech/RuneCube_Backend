import requests, random
from datetime import datetime as dt
from game import Game, Player, Rune


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



class PlayerMaster:
    def __init__(self):
        # Init the list of players managed by this player master
        self.players = []
        self.roles = []

    def create_player(self, player_username, player_role):
        # Create the player
        ready_to_start = False
        story = {}
        if not len(self.roles) == 2:
            if player_role in self.roles:
                return [ready_to_start, f"{player_role} is already taken! Pick another one"]
            else:
                player = Player(player_username, player_role)
                self.roles.append(player_role)
                self.players.append(player)
                if len(self.roles) == 2: 
                    players = self.players
                    story_api = requests.get("https://runecube.herokuapp.com/api/Storys")
                    story = story_api.json()
                    beginning_story = story["storyStartPrompt"]
                    ending_story = story["storyEndPrompt"]
                    ready_to_start = True
                    story = {"start_story": beginning_story, "end_story": ending_story}
            return [ready_to_start, story]
    
    def delete_players(self):
        self.players.clear()
        self.roles.clear()


    def get_player(self, player_username):
        # Return the player matching the given player_username
        player = None

        for active_player in self.players:
            if active_player.player_username == player_username:
                player = active_player
                break
        return player



player_master = PlayerMaster()
rune_master = RuneMaster()
random_number =  random.randint(0,15)
rune_api = []
current_rune_id = [0]
# countdown_time = 0



class GameMaster:
    def __init__(self):
        # Init the list of games managed by this game master
        self.games = []

    def create_game(self):
        # Create the game
        api = requests.get("https://runecube.herokuapp.com/api/Runes")
        global rune_api
        rune_api = api.json()
        current_rune_object = rune_api[random_number]
        current_rune_id[0] = current_rune_object["id"]
        settings_api = requests.get("https://runecube.herokuapp.com/api/settings")
        settings = settings_api.json()
        # global countdown_time
        # countdown_time = settings["maxResponseTime"]
        game_id = 123  #random id to test get_game func
        if self.games == []:
            rune = rune_master.create_rune(id=current_rune_object["id"], value=current_rune_object["value"],color=current_rune_object["color"])
            game = Game(game_id=game_id, start_time=dt.now(), count=settings["count"], 
            max_response_time=settings["maxResponseTime"], each_side_count=settings["eachSideCount"], sides_time=settings["sidesTime"])
            players = player_master.players
            game.add_player(players=players)
            self.games.append(game)
            rune_object = [current_rune_object, settings]
        print(self.games, 'AFTER CREATING THE GAME')
        return rune_object

    def get_game(self):
        print('inside get game func')
        for game in self.games:
            return game
    

    def delete_game(self):
        print('inside delete game method func')
        self.games.clear()
        print(self.games, ' games list after clearing')
            
game_master = GameMaster()
