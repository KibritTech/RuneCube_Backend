import re
from game import Game, Player, Rune



class GameMaster:
    def __init__(self):
        # Init the list of games managed by this game master
        self.games = []

    def create_game(self, game_id, start_time, correct_rune):
        # Create the game
        game = Game(game_id, start_time, correct_rune)

        # Register it
        self.games.append(game)
        print(self.games, 'AFTER creating the game')
        return game

    def get_game(self, game_id):
        # Return the game matching the given game_id
        game = None

        for running_game in self.games:
            print(running_game)
            if running_game.game_id == game_id:
                game = running_game
                break
        return game


class PlayerMaster:
    def __init__(self):
        # Init the list of players managed by this player master
        self.players = []
        self.roles = []

    def create_player(self, player_username, player_role):
        # Create the player
        player = Player(player_username, player_role)

        start_game = False
        
        if player_role in self.roles:
            return f"{player_role} is already taken! Pick another one"
        else:
            self.roles.append(player_role)
            self.players.append(player)
            if len(self.roles) == 2: 
                start_game = True
            return start_game


    def get_player(self, player_username):
        # Return the player matching the given player_username
        player = None

        for active_player in self.players:
            if active_player.player_username == player_username:
                player = active_player
                break

        return player
    
    

class RuneMaster:
    def __init__(self):
        self.rune = []

    def create_rune(self, id, value, color, count, max_response_time, each_side_count, sides_count):
        rune = Rune(id, value, color, count, max_response_time, each_side_count, sides_count)
        self.rune.append(rune)
        return rune

    def get_rune(self):
        for rune in self.rune:
            return rune



        
