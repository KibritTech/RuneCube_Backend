from game import Game, Player



class GameMaster:
    def __init__(self):
        # Init the list of games managed by this game master
        self.games = []

    def create_game(self, game_id, start_time):
        # Create the game
        game = Game(game_id, start_time)

        # Register it
        self.games.append(game)
        return game

    def get_game(self, game_id):
        # Return the game matching the given game_id
        game = None

        for running_game in self.games:
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

        # Register it
        self.players.append(player)
        return player

    def get_player(self, player_username):
        # Return the player matching the given player_username
        player = None

        for active_player in self.players:
            if active_player.player_username == player_username:
                player = active_player
                break

        return player
    
    def create_get_role(self, player_role):
        # # Create the role
        ready = False
        if player_role in self.roles:
            return f"{player_role} is already taken! Pick another one"
        else:
            self.roles.append(player_role)
            if len(self.roles) == 2: 
                ready = True
            return ready
