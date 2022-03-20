

class Player:
    def __init__(self, player_username, player_role):
        # self.player_sid = player_sid
        self.player_username = player_username
        self.player_role = player_role



class Game:
    def __init__(self, game_id, start_time, correct_rune, spend_time=None, finish_time=None,  game_finished=False):
        self.game_id = game_id
        self.start_time = start_time
        self.spend_time = spend_time
        self.game_finished = game_finished
        self.finish_time = finish_time 
        self.players = []
        self.correct_rune = correct_rune
    
    def add_player(self, player_username, player_role):
        self.players.append(Player(player_username, player_role))
        
    def remove_player(self, player_username):
        # Get the player corresponding to the given sid and remove it if it is found
        player = self.get_player(player_username)
        
        if player:
            self.players.remove(player)


class Rune:
    def __init__(self,rune_id=1, value="cube", rune_count=5, max_response_time=12, each_side_count=60, sides_count = 6):
        """
        :param rune_count: how many runes will be in each side
        :param max_response_time: The time given to a player to answer a question
        :param each_side_count: The time between each cube side  ( seconds )
        :param sides_count: How many sides will have a rune (it is fixed )
        :return:
        """
        self.rune_id = rune_id
        self.value = value
        self.rune_count = rune_count
        self.max_response_time = max_response_time
        self.each_side_count = each_side_count
        self.sides_count = sides_count